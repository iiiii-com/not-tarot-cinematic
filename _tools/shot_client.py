# -*- coding: utf-8 -*-
"""shot_client.py -- POST a capture plan to the local shot service.

    python _tools/shot_client.py plan.json [--port 9600]
"""
import argparse
import json
import sys
import time
import urllib.request


def post(port, path, obj, timeout=300):
    data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:%d%s" % (port, path), data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def health(port):
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/health" % port, timeout=4) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--port", type=int, default=9600)
    ap.add_argument("--wait-server", type=float, default=0)
    args = ap.parse_args()
    t0 = time.time()
    while True:
        h = health(args.port)
        if h.get("ok") or time.time() - t0 > args.wait_server:
            break
        time.sleep(0.5)
    if not h.get("ok"):
        print(json.dumps({"ok": False, "error": "shot service down: %s" % h}))
        return 1
    with open(args.plan, "r", encoding="utf-8") as f:
        plan = json.load(f)
    res = post(args.port, "/capture", plan)
    print(json.dumps({k: v for k, v in res.items() if k != "shots"}, ensure_ascii=False))
    for s in res.get("shots", []):
        print("  %-16s %8d B  %s" % (s["name"], s["bytes"], s["file"]))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
