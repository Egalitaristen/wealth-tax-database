#!/usr/bin/env python3
"""fetch_page.py: read pages and files that plain HTTP clients cannot (JavaScript pages, bot walls that answer 403,
PDF links behind them) with a real headless browser. Optional tooling: nothing else in the repository needs it.

Setup (once)
  pip install playwright trafilatura          # Python side
  (cd skill/scripts && npm install defuddle jsdom)   # optional: cleaner article text, author and date
  A Chromium build is needed. In the cloud sessions one is preinstalled under /opt/pw-browsers (set CHROMIUM_PATH to
  override); elsewhere run `playwright install chromium`. PDFs are read with `pdftotext` (poppler-utils).

Usage
  python skill/scripts/fetch_page.py URL                  page as JSON: status, title, author, published, text
  python skill/scripts/fetch_page.py URL --text           just the text (for quotes, grep, wtdb checkquotes)
  python skill/scripts/fetch_page.py URL --html OUT.html  also save the rendered HTML
  python skill/scripts/fetch_page.py URL.pdf --text       PDF: downloaded through the page's own session, then pdftotext
  python skill/scripts/fetch_page.py URL.pdf --save OUT.pdf
  --wait-for SELECTOR   wait for an element (JS search results); --wait MS extra wait; --no-extract skips defuddle
  --links               print the page's links as "text<TAB>URL" lines (to turn a site-search result page into article URLs)
  --consent             click a cookie-consent button (Godkänn/Acceptera/Jag förstår ...) before reading; many Swedish
                        news sites show only the consent wall to a fresh browser

How it gets past a wall: it opens the site's home page first (cookies, challenge scripts) and fetches files with
fetch() from inside that page, which a bare request from outside cannot do. It obeys no robots rules and is slow:
use it for the few pages that matter, not for sweeps. Quote only text you can see on the page.
"""
import argparse, base64, glob, json, os, re, shutil, subprocess, sys, tempfile

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
FETCH_JS = """async (u) => { const r = await fetch(u, {credentials: 'include'}); const b = new Uint8Array(await r.arrayBuffer());
  let s = ''; for (let i = 0; i < b.length; i += 32768) s += String.fromCharCode.apply(null, b.subarray(i, i + 32768));
  return {status: r.status, type: r.headers.get('content-type') || '', b64: btoa(s)}; }"""


def chromium_path():
    p = os.environ.get("CHROMIUM_PATH")
    if p:
        return p
    for pat in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome", "/opt/pw-browsers/chromium"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None  # let playwright use its own download


def pdf_text(data):
    if not shutil.which("pdftotext"):
        sys.exit("pdftotext not found (install poppler-utils)")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(data)
        p = f.name
    try:
        return subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
    finally:
        os.unlink(p)


def extract(html, url, use_defuddle=True):
    """Main text plus title, author, date: defuddle if installed, else trafilatura, else None."""
    helper = os.path.join(HERE, "defuddle_extract.mjs")
    if use_defuddle and shutil.which("node") and os.path.isdir(os.path.join(HERE, "node_modules", "defuddle")):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            p = f.name
        try:
            r = subprocess.run(["node", helper, p, url], capture_output=True, text=True, cwd=HERE)
            if r.returncode == 0 and r.stdout.strip():
                return json.loads(r.stdout)
        finally:
            os.unlink(p)
    try:
        import trafilatura
        d = trafilatura.bare_extraction(html, url=url, with_metadata=True)
        if d:
            g = (lambda k: getattr(d, k, None)) if not isinstance(d, dict) else d.get
            return {"title": g("title"), "author": g("author"), "published": g("date"), "content": g("text")}
    except ImportError:
        pass
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--html")
    ap.add_argument("--save")
    ap.add_argument("--wait-for")
    ap.add_argument("--wait", type=int, default=0)
    ap.add_argument("--no-extract", action="store_true")
    ap.add_argument("--consent", action="store_true")
    ap.add_argument("--links", action="store_true")
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright is not installed: pip install playwright")
    from urllib.parse import urlparse
    origin = "{0.scheme}://{0.netloc}/".format(urlparse(a.url))
    is_file = bool(re.search(r"\.(pdf|docx?|xlsx?)(\?|$)", a.url, re.I))
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if chromium_path():
            kw["executable_path"] = chromium_path()
        b = p.chromium.launch(**kw)
        ctx = b.new_context(locale="sv-SE", user_agent=UA)
        pg = ctx.new_page()
        try:
            if is_file:
                pg.goto(origin, wait_until="domcontentloaded", timeout=60000)
                try:
                    pg.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
                r = pg.evaluate(FETCH_JS, a.url)
                data = base64.b64decode(r["b64"])
                if r["status"] != 200 or not data:
                    sys.exit(f"HTTP {r['status']} for {a.url}")
                if a.save:
                    open(a.save, "wb").write(data)
                if data[:4] == b"%PDF":
                    text = pdf_text(data)
                    print(text if a.text or not a.save else f"saved {a.save} ({len(data)} bytes)")
                else:
                    print(f"saved {len(data)} bytes ({r['type']})" if a.save else data[:2000].decode("utf-8", "replace"))
                return
            resp = pg.goto(a.url, wait_until="domcontentloaded", timeout=60000)
            try:
                pg.wait_for_load_state("networkidle", timeout=20000)
            except Exception:
                pass
            if a.consent:
                for label in (r"Godkänn alla", r"Acceptera alla", r"Godkänn", r"Acceptera", r"Jag förstår", r"Tillåt alla", r"Accept all", r"OK"):
                    try:
                        pg.get_by_role("button", name=re.compile(label, re.I)).first.click(timeout=2500)
                        pg.wait_for_timeout(1500)
                        break
                    except Exception:
                        continue
                try:
                    pg.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
            if a.wait_for:
                pg.wait_for_selector(a.wait_for, timeout=20000)
            if a.wait:
                pg.wait_for_timeout(a.wait)
            if a.links:
                for text, href in pg.eval_on_selector_all("a[href]", "els => els.map(e => [e.innerText.trim().replace(/\\s+/g, ' '), e.href])"):
                    if text and href.startswith("http"):
                        print(f"{text[:140]}\t{href}")
                return
            html = pg.content()
            if a.html:
                open(a.html, "w", encoding="utf-8").write(html)
            body = pg.inner_text("body")
            ex = None if a.no_extract else extract(html, a.url)
            text = (ex or {}).get("content") or body
            if a.text:
                print(text)
            else:
                print(json.dumps({"url": a.url, "status": resp.status if resp else None, "title": (ex or {}).get("title") or pg.title(),
                                  "author": (ex or {}).get("author"), "published": (ex or {}).get("published"), "text": text},
                                 ensure_ascii=False, indent=1))
        finally:
            b.close()


if __name__ == "__main__":
    main()
