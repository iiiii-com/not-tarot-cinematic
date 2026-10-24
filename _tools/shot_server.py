# -*- coding: utf-8 -*-
"""shot_server.py -- local still-capture service (runs OUTSIDE the DSH file sandbox).

Keeps one headless Chromium (Edge channel) alive and captures deterministic frames of
the cinematic HTML on demand, so confined build/review loops can iterate quickly.

    python _tools/shot_server.py --port 9600

HTTP API (all JSON):
    GET  /health                      -> {"ok": true, "version": ...}
    POST /capture  <plan>             -> {"ok": true, "shots": [...]}
    POST /shutdown                    -> {"ok": true}

plan = {
  "html": "E:/.../x.html?capture=1",       # required (file path or file:// URL)
  "out":  "E:/deepseek/review_out/shots",  # required, jpgs land here as <name>.jpg
  "width": 1920, "height": 1080, "quality": 88,
  "shots": [ {"name": "t03.6", "time": 3.6, "eval": "js", "events": [["move",x,y],
             ["click",x,y], ["wheel",x,y,dy], ["down",x,y], ["up",x,y], ["key","Space"],
             ["eval","js"]], "wait": 160} ]
}
"""
import argparse
import json
import os
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

from playwright.sync_api import sync_playwright

STATE = {"browser": None, "playwright": None, "version": None, "lock": threading.Lock()}
ARGS = None


def ensure_browser():
    if STATE["browser"] is not None:
        return STATE["browser"]
    pw = sync_playwright().start()
    args = ["--force-device-scale-factor=1", "--force-color-profile=srgb",
            "--hide-scrollbars", "--disable-lcd-text", "--mute-audio",
            "--disable-background-networking", "--allow-file-access-from-files"]
    browser = None
    for channel in ("msedge", "chrome", None):
        try:
            browser = pw.chromium.launch(headless=True, channel=channel, args=args)
            STATE["version"] = "chromium" + (":" + channel if channel else "")
            break
        except Exception as exc:  # try next channel
            sys.stderr.write("launch %s failed: %s\n" % (channel, exc))
    if browser is None:
        raise RuntimeError("no chromium available")
    STATE["playwright"] = pw
    STATE["browser"] = browser
    return browser


def file_url(p):
    if p.startswith("file://"):
        return p
    return "file:///" + p.replace("\\", "/")


def run_plan(plan):
    browser = ensure_browser()
    width = int(plan.get("width", 1920))
    height = int(plan.get("height", 1080))
    quality = int(plan.get("quality", 88))
    out = plan["out"]
    os.makedirs(out, exist_ok=True)
    results = []
    ctx = browser.new_context(viewport={"width": width, "height": height},
                              device_scale_factor=1, reduced_motion="no-preference")
    page = ctx.new_page()
    page.set_default_timeout(90000)
    logs = []
    page.on("console", lambda m: logs.append("CONSOLE " + m.type + ": " + m.text))
    page.on("pageerror", lambda e: logs.append("PAGEERROR: " + str(e)))
    try:
        page.goto(file_url(plan["html"]), wait_until="load")
        if plan.get("require_rendered", True):
            try:
                page.wait_for_function("window.__rendered === true", timeout=120000)
            except Exception:
                raise RuntimeError("render never armed.\nLOGS:\n" + "\n".join(logs[-30:]))
        else:
            page.wait_for_timeout(int(plan.get("settle", 400)))
        page.evaluate("document.fonts ? document.fonts.ready.then(()=>true) : true")
        page.wait_for_timeout(250)
        for shot in plan.get("shots", []):
            if shot.get("url"):
                page.goto(file_url(shot["url"]), wait_until="load")
                page.wait_for_function("window.__rendered === true", timeout=120000)
                page.wait_for_timeout(250)
            if shot.get("time") is not None:
                page.evaluate("t => window.__renderAt(t)", float(shot["time"]))
            for ev in shot.get("events", []):
                kind = ev[0]
                a = ev[1:]
                if kind == "move":
                    page.mouse.move(float(a[0]), float(a[1]))
                elif kind == "click":
                    page.mouse.move(float(a[0]), float(a[1]))
                    page.wait_for_timeout(50)
                    page.mouse.click(float(a[0]), float(a[1]))
                elif kind == "down":
                    page.mouse.move(float(a[0]), float(a[1]))
                    page.mouse.down()
                elif kind == "up":
                    page.mouse.up()
                elif kind == "wheel":
                    page.mouse.move(float(a[0]), float(a[1]))
                    page.mouse.wheel(0, float(a[2]) if len(a) > 2 else 300)
                elif kind == "key":
                    page.keyboard.press(str(a[0]))
                elif kind == "eval":
                    page.evaluate(str(a[0]))
                page.wait_for_timeout(60)
            if shot.get("eval"):
                page.evaluate(shot["eval"])
            page.wait_for_timeout(int(shot.get("wait", 160)))
            probes = {}
            for j, expr in enumerate(shot.get("probe") or []):
                try:
                    probes[str(j)] = page.evaluate(str(expr))
                except Exception as exc:
                    probes[str(j)] = "ERR " + str(exc)[-200:]
            path = os.path.join(out, shot["name"] + ".jpg")
            page.screenshot(path=path, type="jpeg", quality=quality, animations="allow")
            results.append({"name": shot["name"], "file": path, "bytes": os.path.getsize(path),
                            "probe": probes})
        probe_out = {}
        for i, expr in enumerate(plan.get("probe") or []):
            try:
                probe_out[str(i)] = page.evaluate(str(expr))
            except Exception as exc:
                probe_out[str(i)] = "ERR " + str(exc)[-300:]
    finally:
        ctx.close()
    return {"shots": results, "probe": probe_out}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *a):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % a))

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/health"):
            return self._send(200, {"ok": True, "version": STATE["version"],
                                    "browser": STATE["browser"] is not None})
        return self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            plan = json.loads(raw.decode("utf-8"))
        except Exception:
            return self._send(400, {"ok": False, "error": "bad json"})
        if self.path.startswith("/shutdown"):
            self._send(200, {"ok": True})
            threading.Thread(target=ARGS.shutdown_hook, daemon=True).start()
            return
        if self.path.startswith("/capture"):
            try:
                t0 = time.time()
                res = run_plan(plan)
                return self._send(200, {"ok": True, "shots": res["shots"], "probe": res["probe"],
                                        "ms": int((time.time() - t0) * 1000)})
            except Exception:
                traceback.print_exc()
                return self._send(500, {"ok": False, "error": traceback.format_exc()[-4000:]})
        return self._send(404, {"ok": False, "error": "not found"})


def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9600)
    ap.add_argument("--warm", action="store_true", help="launch browser at boot")
    ARGS = ap.parse_args()
    # NOTE: Playwright's sync API is thread-bound -- the browser must be created
    # and used on the same thread that runs serve_forever (the main thread).
    if ARGS.warm:
        ensure_browser()
    srv = HTTPServer(("127.0.0.1", ARGS.port), Handler)
    srv.daemon_threads = False

    def shutdown():
        time.sleep(0.2)
        srv.shutdown()
        try:
            STATE["browser"].close()
            STATE["playwright"].stop()
        except Exception:
            pass
        os._exit(0)

    ARGS.shutdown_hook = shutdown
    sys.stdout.write("READY http://127.0.0.1:%d\n" % ARGS.port)
    sys.stdout.flush()
    srv.serve_forever()


if __name__ == "__main__":
    main()
