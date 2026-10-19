#!/usr/bin/env python3
"""meetingplus_scan.py: full-text search of Swedish municipal and regional meeting portals built on MeetingPlus
(Formpipe/Tietoevry "Meetings Plus"). Standard library plus `pdftotext` (poppler) for the optional PDF read.

Sites known to use it: meetingspublic.stockholm.se (Stockholm), sammantraden.huddinge.se (Huddinge),
meetingsplus.danderyd.se (Danderyd), sammantraden.gotland.se (Region Gotland). Other municipalities use Sitevision
pages with PDF links, Visma Insyn, Ciceron or other portals: those need their own adapter.

The search matches whole words: förmögenhetsskatt finds 20 documents in Stockholm, förmögenhetsskatten 8 more, förmögenhetsskatt* all forms, so use the trailing * (the default does).
The portal's search page is  <base>/search?text=<term>&psize=<n>&pindex=<page>  and returns server-rendered rows
(document title, committee, meeting date, type, link). It searches the text of agenda items and attached documents.

Usage
  python skill/scripts/adapters/se_meetingplus_scan.py BASE_URL [--term T ...] [--read] [--context 250] [--json OUT.json]
  e.g. python skill/scripts/adapters/se_meetingplus_scan.py https://meetingspublic.stockholm.se --read

Without --read it lists the hits (title, committee, date, type, URL). With --read it downloads each hit that is a
protocol, motion, interpellation or agenda text, extracts the text and prints the sentences around the terms, so
you can see whether a councillor or party called for a wealth tax. A hit in an attachment (an SOU, a PM) is a
mention, not support: read in context.
"""
import argparse, html, json, os, re, subprocess, sys, tempfile, time, urllib.parse, urllib.request

UA = {"User-Agent": "wealth-tax-database/1.0 (https://github.com/egalitaristen/wealth-tax-database)"}
TERMS = ["förmögenhetsskatt*", "miljardärsskatt*", "miljardärskatt*", "förmögenhetsbeskattning*"]  # the search is whole-word; * matches endings
TERMS_RE = re.compile(r"(?i)förmögenhetsskatt\w*|förmögenhetsbeskatt\w*|miljardärs?skatt\w*|skatt på (?:stora )?förmögenhet\w*")
_last = [0.0]


def get(url, binary=False):
    for k in range(4):
        wait = 0.6 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            return raw if binary else raw.decode("utf-8", "replace")
        except Exception:
            time.sleep(3 * (k + 1))
    return None


def search(base, term, psize=100):
    rows, page = [], 1
    while True:
        u = f"{base}/search?{urllib.parse.urlencode({'text': term, 'psize': psize, 'pindex': page})}"
        t = get(u)
        if not t:
            break
        items = re.findall(r'<li class="search-result-item-row">(.*?)</li>', t, re.S)
        for it in items:
            m = re.search(r'<div class="name">\s*<a href="([^"]+)">\s*(.*?)\s*</a>', it, re.S)
            c = re.search(r'<div class="committee">.*?<a [^>]*>(.*?)</a>', it, re.S)
            d = re.search(r'<div class="meeting-date">.*?<a [^>]*>(.*?)</a>', it, re.S)
            ty = re.search(r'<div class="type[^"]*">\s*<div>(.*?)</div>', it, re.S)
            if m:
                rows.append({"title": html.unescape(m.group(1 + 1)).strip(), "url": urllib.parse.urljoin(base + "/", m.group(1)),
                             "committee": html.unescape(c.group(1)).strip() if c else "",
                             "date": d.group(1).strip() if d else "", "type": html.unescape(ty.group(1)).strip() if ty else ""})
        total = re.search(r'<div>(\d+)\s*</div>\s*<div>resultat funna', t)
        if not items or (total and page * psize >= int(total.group(1))):
            break
        page += 1
    return rows


def read_doc(url):
    data = get(url + ("&" if "?" in url else "?") + "downloadMode=open", binary=True)
    if not data:
        return ""
    if data[:4] == b"%PDF":
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(data)
            p = f.name
        try:
            return subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
        finally:
            os.unlink(p)
    return html.unescape(re.sub(r"<[^>]+>", " ", data.decode("utf-8", "replace")))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base")
    ap.add_argument("--term", action="append")
    ap.add_argument("--read", action="store_true")
    ap.add_argument("--attachments", action="store_true", help="with --read, also read attachments (type Bilaga): slow, mostly SOUs and reports")
    ap.add_argument("--context", type=int, default=250)
    ap.add_argument("--json")
    a = ap.parse_args()
    base = a.base.rstrip("/")
    seen = {}
    for term in a.term or TERMS:
        for r in search(base, term):
            seen[r["url"]] = r
    rows = sorted(seen.values(), key=lambda r: (r["date"], r["title"]))
    print(f"{len(rows)} hits at {base}", file=sys.stderr)
    for r in rows:
        print(f"{r['date']}  {r['committee'][:28]:28}  {r['type'][:16]:16}  {r['title'][:90]}\n    {r['url']}")
        if a.read and r["title"].lower().endswith(".pdf") and (a.attachments or r["type"].lower() != "bilaga"):
            txt = re.sub(r"\s+", " ", read_doc(r["url"]).replace("\xad", ""))
            r["contexts"] = []
            for m in list(TERMS_RE.finditer(txt))[:4]:
                c = txt[max(0, m.start() - a.context): m.end() + a.context]
                r["contexts"].append(c)
                print("      …" + c + "…")
    if a.json:
        json.dump(rows, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
