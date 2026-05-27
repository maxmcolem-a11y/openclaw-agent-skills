#!/usr/bin/env python3
import argparse
import json
import time
import urllib.request
import urllib.error

parser = argparse.ArgumentParser(description="Read the ngrok inspector API and print the public URL for a local port.")
parser.add_argument("port", type=int)
parser.add_argument("--timeout", type=float, default=20.0)
args = parser.parse_args()

deadline = time.time() + args.timeout
needle = f"http://localhost:{args.port}"
needle_alt = f"http://127.0.0.1:{args.port}"

while time.time() < deadline:
    try:
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2) as resp:
            payload = json.load(resp)
        for tunnel in payload.get("tunnels", []):
            addr = (((tunnel or {}).get("config") or {}).get("addr"))
            public = tunnel.get("public_url")
            if addr in {needle, needle_alt} and public:
                print(public)
                raise SystemExit(0)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        pass
    time.sleep(0.5)

raise SystemExit("Timed out waiting for ngrok tunnel URL")
