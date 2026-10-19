#!/usr/bin/env python3
"""riksdag_scan.py: find wealth tax language in the Swedish Riksdag's open data. Standard library only.

A per-country source adapter (like ocn_scan.py for UK councils). It lists documents that contain a search term, fetches
the full text, prints the sentences around each hit with the signatories, and flags wording that suggests a call for
the tax or a defence of its abolition. Hits are leads: read each one in context before recording anything.

Commands
  search  [--term T ...] [--doktyp mot,ip,fr,bet,frs,prop] [--from 2010-01-01] [--to DATE] [--party V,MP]
          [--context 200] [--max-hits 3] [--json OUT.json] [--list-only]
          Documents containing a term (default: the Swedish wealth tax terms below). Free-text search matches whole
          words, so the default also runs the stems; the hit filter then applies the regex in TERMS_RE.
  signers DOK_ID                      signatories (dokintressent) of one document
  speeches [--term T ...] [--from DATE] [--to DATE] [--party V] [--context 200] [--json OUT.json]
          Hits in chamber debates (plenary protocols), attributed to the speaker (Anf. N Name (Party)).
          The speech-list API cannot filter by text, so this reads the protocols found by a full-text search.
  votes   --rm 2013/14 --bet SkU21 [--punkt 3] [--names Nej] [--json OUT.json]
          Roll call of the votes on one committee report: counts per item and party; --names lists who voted that way.
  member  "First Last"                status from the member register ("Avliden" = deceased), party, birth year

Examples
  python skill/scripts/riksdag_scan.py search --doktyp mot --from 2025-01-01 --party V
  python skill/scripts/riksdag_scan.py search --doktyp ip,fr,bet --json /tmp/se_other.json
  python skill/scripts/riksdag_scan.py votes --rm 2013/14 --bet SkU21
  python skill/scripts/riksdag_scan.py member "Nooshi Dadgostar"

Notes
  * Document types (doktyp): mot motion, ip interpellation, fr written question, frs question for oral answer,
    bet committee report, prop government bill, skr government communication, rskr Riksdag communication.
  * Full text comes from data.riksdagen.se/dokument/<id>.text (XML with the text inside); the page used as a quote
    source is data.riksdagen.se/dokument/<id>.html. The page splits some long words with a soft hyphen, so printed
    context drops it but marks a window "SOFT-HYPHEN" when the raw text had one: keep quotes clear of such words or
    run wtdb.py checkquotes on them.
  * Be polite: one request at a time, cached under SE_CACHE (default /tmp/riksdag_cache).
"""
import argparse, datetime as dt, html, json, os, re, sys, time, urllib.parse, urllib.request

BASE = "https://data.riksdagen.se"
CACHE = os.environ.get("SE_CACHE", "/tmp/riksdag_cache")
UA = {"User-Agent": "wealth-tax-database/1.0 (https://github.com/egalitaristen/wealth-tax-database)"}
SEARCH_TERMS = ["förmögenhetsskatt", "miljardärsskatt", "miljardärskatt", "förmögenhetsbeskattning",
                "förmögenhetsskatten", "förmögenhetsskatter", "miljardärsskatten", "miljardärer", "superrika"]
TERMS_RE = re.compile(r"(?i)förmögenhetsskatt\w*|förmögenhetsbeskatt\w*|miljardärs?skatt\w*|skatt(en)? på (stora |extrema )?"
                      r"(förmögenhet\w*|miljardär\w*)|zucman\w*|skatt på superrika|exitskatt\w*")
FOR_CUES = re.compile(r"(?i)\b(införs|införa|återinför\w*|ska införas|bör införas|föreslår|vill utreda|utredning|"
                      r"utreda|tillkännager|bör finnas|kräver|vill ha)\b")
AGAINST_CUES = re.compile(r"(?i)\b(slopad\w*|slopade|slopat|avskaff\w*|avskaffad\w*|motsätter|farlig\w*|"
                          r"kapitalflykt|ska inte återinföras|bör inte återinföras)\b")
_last = [0.0]


def get(url, binary=False, tries=5):
    for k in range(tries):
        wait = 0.4 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            return raw if binary else raw.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(5 * (k + 1))
        except Exception:
            time.sleep(3 * (k + 1))
    return None


def getjson(url):
    t = get(url)
    return json.loads(t) if t else None


def fulltext(dok_id):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, dok_id + ".txt")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read()
    t = get(f"{BASE}/dokument/{dok_id}.text")
    if t is None:
        return None
    t = html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(t)))
    t = re.sub(r"[ \t\r\n]+", " ", t)
    open(p, "w", encoding="utf-8").write(t)
    return t


def signers(dok_id):
    d = getjson(f"{BASE}/dokumentstatus/{dok_id}.json")
    if not d:
        return []
    it = d["dokumentstatus"].get("dokintressent", {}).get("intressent", [])
    it = it if isinstance(it, list) else [it]
    return [(x["namn"], x.get("partibet", ""), x.get("roll", "")) for x in it]


def list_docs(terms, doktyp, frm, to, party):
    seen = {}
    for term in terms:
        for dt in doktyp:
            page = 1
            while True:
                q = {"sok": term, "doktyp": dt, "from": frm, "utformat": "json", "sz": 200, "p": page}
                if to:
                    q["tom"] = to
                if party:
                    q["parti"] = party
                d = getjson(f"{BASE}/dokumentlista/?" + urllib.parse.urlencode(q))
                if not d:
                    break
                d = d["dokumentlista"]
                for x in d.get("dokument") or []:
                    seen[x["dok_id"]] = x
                if page >= int(d.get("@sidor", 1) or 1):
                    break
                page += 1
    return sorted(seen.values(), key=lambda x: (x["datum"], x["dok_id"]))


def contexts(text, width, max_hits):
    plain = text.replace("\xad", "")
    plain = re.sub(r"\s*­\s*", "", plain)
    out = []
    for m in TERMS_RE.finditer(plain):
        s, e = max(0, m.start() - width), min(len(plain), m.end() + width)
        win = plain[s:e]
        out.append({"hit": m.group(0), "context": win,
                    "for_cues": sorted({c.lower() for c in FOR_CUES.findall(win)}),
                    "against_cues": sorted({c.lower() for c in AGAINST_CUES.findall(win)}),
                    "soft_hyphen": "\xad" in text[max(0, m.start() - width): m.end() + width + 40]})
    # drop hits whose windows overlap an earlier one
    keep, last_end = [], -1
    for c in out:
        pos = plain.find(c["context"])
        if pos >= last_end:
            keep.append(c)
            last_end = pos + len(c["context"])
    return keep[:max_hits], len(out)


def cmd_search(a):
    terms = a.term or SEARCH_TERMS
    docs = list_docs(terms, a.doktyp.split(","), a.frm, a.to, a.party)
    print(f"{len(docs)} documents from the search", file=sys.stderr)
    result = []
    for x in docs:
        if a.list_only:
            print(x["datum"], x["dok_id"], x["doktyp"], x.get("undertitel", "")[:50], "|", x["titel"][:70])
            continue
        t = fulltext(x["dok_id"])
        if not t:
            print(f"# {x['dok_id']}: no text", file=sys.stderr)
            continue
        ctx, n = contexts(t, a.context, a.max_hits)
        if not ctx:
            continue
        sg = signers(x["dok_id"])
        rec = {"dok_id": x["dok_id"], "date": x["datum"], "type": x["doktyp"], "rm": x.get("rm", ""),
               "title": x["titel"], "by": x.get("undertitel", ""), "signers": sg, "hits": n, "contexts": ctx,
               "url": f"{BASE}/dokument/{x['dok_id']}.html"}
        result.append(rec)
        print(f"\n## {rec['date']} {rec['dok_id']} [{rec['type']}] {rec['by']} | {rec['title'][:80]}  ({n} hits)")
        print("   signers:", "; ".join(f"{nm} ({p})" for nm, p, r in sg[:12]) + (" ..." if len(sg) > 12 else ""))
        print("   ", rec["url"])
        for c in ctx:
            tag = ("FOR? " + ",".join(c["for_cues"]) if c["for_cues"] else "") + \
                  (" AGAINST? " + ",".join(c["against_cues"]) if c["against_cues"] else "") + \
                  (" SOFT-HYPHEN" if c["soft_hyphen"] else "")
            print(f"   - [{tag.strip()}] …{c['context']}…")
    if a.json:
        json.dump(result, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"wrote {a.json}: {len(result)} documents with hits", file=sys.stderr)


def cmd_signers(a):
    for nm, p, r in signers(a.dok_id):
        print(f"{nm}\t{p}\t{r}")


SPEAKER_RE = re.compile(r"Anf\.\s+(\d+)\s+(.{3,90}?\([A-Za-zÅÄÖåäö-]{1,4}\))")


def cmd_speeches(a):
    """Chamber speeches containing a term. The speech list API cannot filter by text, so search the plenary
    protocols (doktyp prot, full-text) and attribute each hit to the nearest preceding 'Anf. N Name (Party)'."""
    terms = a.term or ["förmögenhetsskatt", "miljardärsskatt", "miljardärskatt", "förmögenhetsbeskattning",
                       "förmögenhetsskatten", "miljardärsskatten"]
    docs = list_docs(terms, ["prot"], a.frm, a.to, "")
    print(f"{len(docs)} protocols from the search", file=sys.stderr)
    out = []
    for x in docs:
        text = fulltext(x["dok_id"])
        if not text:
            continue
        plain = re.sub(r"\s*\xad\s*", "", text)
        speakers = [(m.start(), m.group(1), m.group(2).strip()) for m in SPEAKER_RE.finditer(plain)]
        ctx, n = contexts(text, a.context, 50)
        for c in ctx:
            pos = plain.find(c["context"])
            sp = [s for s in speakers if s[0] <= pos + 200]
            who = sp[-1] if sp else (0, "", "?")
            if a.party and f"({a.party})" not in who[2]:
                continue
            rec = {"date": x["datum"], "protocol": x["dok_id"], "title": x["titel"], "anf": who[1], "speaker": who[2],
                   "url": f"{BASE}/dokument/{x['dok_id']}.html", "context": c["context"],
                   "for_cues": c["for_cues"], "against_cues": c["against_cues"]}
            out.append(rec)
            tag = ("FOR? " + ",".join(c["for_cues"]) if c["for_cues"] else "") + \
                  (" AGAINST? " + ",".join(c["against_cues"]) if c["against_cues"] else "")
            print(f"\n## {rec['date']} {rec['title'][:40]} Anf. {rec['anf']} {rec['speaker']}\n   {rec['url']}\n   - [{tag.strip()}] …{c['context']}…")
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"wrote {a.json}: {len(out)} hits", file=sys.stderr)


def cmd_votes(a):
    q = {"rm": a.rm, "bet": a.bet, "utformat": "json", "sz": 500}
    if a.punkt:
        q["punkt"] = a.punkt
    v, page = [], 1
    while True:
        q["p"] = page
        d = getjson(f"{BASE}/voteringlista/?" + urllib.parse.urlencode(q))
        xs = (d or {}).get("voteringlista", {}).get("votering") or []
        xs = xs if isinstance(xs, list) else [xs]
        if not xs:
            break
        v += xs
        if len(xs) < 500:
            break
        page += 1
    if not v:
        sys.exit("no vote data")
    by = {}
    for x in v:
        by.setdefault((x.get("punkt", ""), x["parti"], x["rost"]), []).append(x["namn"])
    print(f"{a.rm} {a.bet} punkt {a.punkt or '(all)'}: {len(v)} individual votes")
    for pk in sorted({k[0] for k in by}, key=lambda s: (len(s), s)):
        print(f" punkt {pk}")
        for p in sorted({k[1] for k in by if k[0] == pk}):
            print(f"   {p:4}", {r: len(n) for (a_, pp, r), n in by.items() if a_ == pk and pp == p})
        if a.names:
            for (a_, pp, r), n in sorted(by.items()):
                if a_ == pk and r == a.names:
                    print(f"     {r} {pp}: " + "; ".join(sorted(n)))
    if a.json:
        json.dump(v, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"wrote {a.json}", file=sys.stderr)


def cmd_member(a):
    first, _, last = a.name.strip().rpartition(" ")
    q = {"utformat": "json", "rdlstatus": "samtliga", "enamn": last}
    if first:
        q["fnamn"] = first
    d = getjson(f"{BASE}/personlista/?" + urllib.parse.urlencode(q))
    ps = (d or {}).get("personlista", {}).get("person") or []
    ps = ps if isinstance(ps, list) else [ps]
    if not ps:
        print("not found")
    for p in ps:
        print(f"{p['tilltalsnamn']} {p['efternamn']}\t{p['status']}\t{p['parti']}\tborn {p['fodd_ar']}\t{p['valkrets']}\t{p['intressent_id']}")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = ap.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("search"); x.add_argument("--term", action="append"); x.add_argument("--doktyp", default="mot")
    x.add_argument("--from", dest="frm", default="2010-01-01"); x.add_argument("--to", default="")
    x.add_argument("--party", default=""); x.add_argument("--context", type=int, default=200)
    x.add_argument("--max-hits", type=int, default=3); x.add_argument("--json"); x.add_argument("--list-only", action="store_true")
    x.set_defaults(f=cmd_search)
    x = s.add_parser("signers"); x.add_argument("dok_id"); x.set_defaults(f=cmd_signers)
    x = s.add_parser("speeches"); x.add_argument("--term", action="append"); x.add_argument("--from", dest="frm", default="2010-01-01")
    x.add_argument("--to", default=""); x.add_argument("--party", default=""); x.add_argument("--context", type=int, default=200)
    x.add_argument("--json"); x.set_defaults(f=cmd_speeches)
    x = s.add_parser("votes"); x.add_argument("--rm", required=True); x.add_argument("--bet", required=True)
    x.add_argument("--punkt", default=""); x.add_argument("--names", default="", help="list names that voted this way (Ja, Nej, Avstår)")
    x.add_argument("--json"); x.set_defaults(f=cmd_votes)
    x = s.add_parser("member"); x.add_argument("name"); x.set_defaults(f=cmd_member)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
