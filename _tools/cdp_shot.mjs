// cdp_shot.mjs — dependency-free Edge/Chromium CDP driver for still capture.
// Spawns headless Edge detached (stdio ignored, allowed in confined sandboxes),
// talks Chrome DevTools Protocol over the global WebSocket (Node >= 22).
//
// usage: node cdp_shot.mjs plan.json
// plan.json: {
//   html, out, width, height, quality, port, keepOpen,
//   shots: [{ name, time, url?, eval?, wait, events:[["move",x,y],["click",x,y],["wheel",x,y,dy]] }]
// }
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import http from "node:http";

const PLAN = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const W = PLAN.width || 1920;
const H = PLAN.height || 1080;
const OUT = PLAN.out;
const QUALITY = PLAN.quality || 90;
const PORT = PLAN.port || 9451;

const CANDIDATES = [
  process.env.EDGE_PATH,
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
].filter(Boolean);
const BROWSER = CANDIDATES.find((p) => fs.existsSync(p));
if (!BROWSER) throw new Error("no browser found");

fs.mkdirSync(OUT, { recursive: true });
const PROFILE = path.join(OUT, "..", "edge_profile");
fs.mkdirSync(PROFILE, { recursive: true });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const httpJSON = (p) =>
  new Promise((resolve, reject) => {
    const req = http.get({ host: "127.0.0.1", port: PORT, path: p, timeout: 3000 }, (res) => {
      let buf = "";
      res.on("data", (d) => (buf += d));
      res.on("end", () => {
        try { resolve(JSON.parse(buf)); } catch (e) { reject(e); }
      });
    });
    req.on("error", reject);
    req.on("timeout", () => { req.destroy(); reject(new Error("timeout")); });
  });

const waitCDP = async () => {
  for (let i = 0; i < 120; i++) {
    try {
      const v = await httpJSON("/json/version");
      if (v && v.webSocketDebuggerUrl) return v;
    } catch { /* retry */ }
    await sleep(300);
  }
  throw new Error("CDP never came up");
};

class CDP {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.id = 0;
    this.pending = new Map();
    this.events = [];
    this.waiters = [];
    this.ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message || JSON.stringify(msg.error)));
        else resolve(msg.result);
      } else if (msg.method) {
        this.events.push(msg);
        this.waiters = this.waiters.filter((w) => !w(msg));
      }
    });
  }
  ready() {
    return new Promise((resolve, reject) => {
      if (this.ws.readyState === 1) return resolve();
      this.ws.addEventListener("open", () => resolve(), { once: true });
      this.ws.addEventListener("error", () => reject(new Error("ws error")), { once: true });
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    this.ws.send(JSON.stringify(payload));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      setTimeout(() => {
        if (this.pending.delete(id)) reject(new Error("timeout " + method));
      }, 60000);
    });
  }
  once(pred, timeout = 30000) {
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error("event timeout")), timeout);
      const check = (msg) => {
        if (pred(msg)) { clearTimeout(t); resolve(msg); return true; }
        return false;
      };
      for (const e of this.events) if (check(e)) return;
      this.waiters.push(check);
    });
  }
  close() { try { this.ws.close(); } catch { /* noop */ } }
}

async function evaluate(cdp, sid, expression, awaitPromise = true) {
  const r = await cdp.send("Runtime.evaluate", {
    expression, awaitPromise, returnByValue: true, allowUnsafeEvalBlockedByCSP: false,
  }, sid);
  if (r && r.exceptionDetails) {
    const d = r.exceptionDetails;
    throw new Error("evaluate failed: " + (d.exception && d.exception.description || d.text));
  }
  return r.result && r.result.value;
}

async function main() {
  const args = [
    "--headless=new",
    "--remote-debugging-port=" + PORT,
    "--user-data-dir=" + PROFILE,
    "--no-first-run", "--no-default-browser-check",
    "--disable-extensions", "--disable-background-networking", "--disable-sync",
    "--disable-features=Translate,MediaRouter",
    "--disable-gpu", "--disable-dev-shm-usage", "--hide-scrollbars",
    "--force-device-scale-factor=1", "--force-color-profile=srgb",
    "--allow-file-access-from-files", "--mute-audio",
    "--window-size=" + W + "," + (H + 120),
    "about:blank",
  ];
  const proc = spawn(BROWSER, args, { stdio: "ignore", windowsHide: true, detached: false });
  let cdp;
  try {
    const ver = await waitCDP();
    cdp = new CDP(ver.webSocketDebuggerUrl);
    await cdp.ready();
    const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank", width: W, height: H });
    const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
    const sid = sessionId;
    await cdp.send("Page.enable", {}, sid);
    await cdp.send("Runtime.enable", {}, sid);
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: W, height: H, deviceScaleFactor: 1, mobile: false,
    }, sid);

    const url = PLAN.html.startsWith("file://") ? PLAN.html : "file:///" + PLAN.html.replace(/\\/g, "/");
    const loaded = cdp.once((m) => m.method === "Page.loadEventFired", 60000);
    await cdp.send("Page.navigate", { url }, sid);
    await loaded.catch(() => null);
    await sleep(250);
    // wait for the composition to be ready
    const t0 = Date.now();
    while (Date.now() - t0 < 120000) {
      const ok = await evaluate(cdp, sid, "window.__rendered === true").catch(() => false);
      if (ok) break;
      await sleep(200);
    }
    await evaluate(cdp, sid, "document.fonts ? document.fonts.ready.then(() => true) : true").catch(() => null);
    await sleep(150);

    const results = [];
    for (const shot of PLAN.shots || []) {
      if (shot.url) {
        await cdp.send("Page.navigate", { url: shot.url }, sid);
        await sleep(400);
        const t1 = Date.now();
        while (Date.now() - t1 < 60000) {
          const ok = await evaluate(cdp, sid, "window.__rendered === true").catch(() => false);
          if (ok) break;
          await sleep(120);
        }
        await sleep(200);
      }
      if (shot.time !== undefined && shot.time !== null) {
        await evaluate(cdp, sid, "window.__renderAt(" + Number(shot.time) + ")");
      }
      for (const ev of shot.events || []) {
        const [kind, ...a] = ev;
        if (kind === "move") {
          await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: a[0], y: a[1], button: "none", clickCount: 0 }, sid);
        } else if (kind === "click") {
          await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: a[0], y: a[1], button: "none" }, sid);
          await sleep(60);
          await cdp.send("Input.dispatchMouseEvent", { type: "mousePressed", x: a[0], y: a[1], button: "left", clickCount: 1 }, sid);
          await sleep(40);
          await cdp.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: a[0], y: a[1], button: "left", clickCount: 1 }, sid);
        } else if (kind === "wheel") {
          await cdp.send("Input.dispatchMouseEvent", { type: "mouseWheel", x: a[0], y: a[1], deltaX: 0, deltaY: a[2] || 300 }, sid);
        } else if (kind === "down") {
          await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: a[0], y: a[1], button: "none" }, sid);
          await cdp.send("Input.dispatchMouseEvent", { type: "mousePressed", x: a[0], y: a[1], button: "left", clickCount: 1 }, sid);
        } else if (kind === "up") {
          await cdp.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: a[0], y: a[1], button: "left", clickCount: 1 }, sid);
        } else if (kind === "key") {
          await cdp.send("Input.dispatchKeyEvent", { type: "keyDown", key: a[0], code: a[1] || a[0] }, sid);
          await cdp.send("Input.dispatchKeyEvent", { type: "keyUp", key: a[0], code: a[1] || a[0] }, sid);
        } else if (kind === "eval") {
          await evaluate(cdp, sid, a[0]);
        }
        await sleep(60);
      }
      if (shot.eval) await evaluate(cdp, sid, shot.eval);
      await sleep(shot.wait === undefined ? 160 : shot.wait);
      const { data } = await cdp.send("Page.captureScreenshot", {
        format: "jpeg", quality: QUALITY, captureBeyondViewport: false, fromSurface: true,
      }, sid);
      const file = path.join(OUT, shot.name + ".jpg");
      fs.writeFileSync(file, Buffer.from(data, "base64"));
      if (shot.eval2) await evaluate(cdp, sid, shot.eval2);
      results.push({ name: shot.name, file, bytes: fs.statSync(file).size });
      console.log("shot", shot.name, fs.statSync(file).size);
    }
    if (!PLAN.keepOpen) {
      await cdp.send("Browser.close").catch(() => null);
    }
    cdp.close();
    console.log(JSON.stringify({ ok: true, shots: results.length }));
  } finally {
    if (!PLAN.keepOpen) {
      await sleep(300);
      try { proc.kill(); } catch { /* noop */ }
    }
  }
}

main().catch((e) => { console.error("FAIL", e.message); process.exit(1); });
