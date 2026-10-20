#!/usr/bin/env python3
"""Serve the built site locally the way Cloudflare Pages does: unknown paths fall back to index.html.

Usage: python scripts/build_site.py && python scripts/serve.py [--port 8000]
"""
import argparse, functools, http.server
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "_site"


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = Path(self.translate_path(self.path))
        if not path.is_file() and not (path / "index.html").is_file():
            if path.with_name(path.name + ".html").is_file():  # a page with its own share tags: /gb -> gb.html
                self.path = self.path.split("?")[0].rstrip("/") + ".html"
            else:  # any other client-side route
                self.path = "/index.html"
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")  # always show the latest build while developing
        super().end_headers()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    port = ap.parse_args().port
    handler = functools.partial(Handler, directory=str(ROOT))
    print(f"Serving {ROOT} at http://localhost:{port}")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    main()
