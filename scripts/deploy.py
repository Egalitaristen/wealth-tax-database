#!/usr/bin/env python3
"""Build the site and deploy it to Cloudflare from this machine.

Usage: python scripts/deploy.py [--dry-run]

Needs Node.js and a one-time `npx wrangler login`. The deployment settings (static assets in _site/,
single-page fallback, custom domains) are in wrangler.jsonc at the repository root.
"""
import argparse, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="build and check, but upload nothing")
    dry = ap.parse_args().dry_run
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py")], check=True)
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        sys.exit("npx not found: install Node.js, then run `npx wrangler login` once.")
    cmd = [npx, "--yes", "wrangler@4", "deploy"] + (["--dry-run"] if dry else [])
    return subprocess.run(cmd, cwd=ROOT).returncode


if __name__ == "__main__":
    sys.exit(main())
