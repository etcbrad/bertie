#!/usr/bin/env python3
from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_INDEX = "canvas.html"


class NoCacheHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def end_headers(self):
        # Disable caching to make iteration fast.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        # Allow asset fetches if you later add module scripts or JSON requests.
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        if self.path in ("/", ""):
            self.path = f"/{DEFAULT_INDEX}"
        return super().do_GET()


def main() -> int:
    parser = argparse.ArgumentParser(description="Local dev server for Bertie.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), NoCacheHandler)
    url = f"http://{args.host}:{args.port}/{DEFAULT_INDEX}"
    print(f"Serving Bertie on {url}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
