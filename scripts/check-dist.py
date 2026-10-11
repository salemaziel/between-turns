#!/usr/bin/env python3
"""Check the BUILT site (dist/) before it is deployed. Exit 1 on any problem.
Catches what the frontmatter validator cannot: empty <title>, wrong canonical,
og:image that points at a missing file, posts missing from the build or feeds."""
import pathlib, re, sys
# stdlib ElementTree is safe here: we only parse feeds our own build just wrote to dist/ (no untrusted XML).
import xml.etree.ElementTree as ET  # noqa: S405

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SITE = "https://between-turns.netlify.app"
errs = []

def read(p): return p.read_text(encoding="utf-8", errors="replace")

def check_page(path, expect_canonical):
    h = read(path); rel = path.relative_to(DIST)
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    if not m or not m.group(1).strip(): errs.append(f"{rel}: empty <title>")
    if "undefined" in h.lower().replace("typeof undefined", ""): errs.append(f"{rel}: contains 'undefined'")
    c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    if not c or c.group(1) != expect_canonical: errs.append(f"{rel}: canonical {c.group(1) if c else None!r} != {expect_canonical!r}")
    img = re.search(r'<meta property="og:image" content="([^"]+)"', h)
    if not img: errs.append(f"{rel}: no og:image")
    elif img.group(1).startswith(SITE) and not (DIST / img.group(1)[len(SITE):].lstrip("/")).exists():
        errs.append(f"{rel}: og:image file missing in dist: {img.group(1)}")
    for src in re.findall(r'<img[^>]+src="(/[^"]+)"', h):
        if not (DIST / src.lstrip("/")).exists(): errs.append(f"{rel}: <img> missing in dist: {src}")

if not DIST.exists():
    print("FAIL dist/ missing - run the build first"); sys.exit(1)

check_page(DIST / "index.html", SITE + "/")
live = 0
for coll in ("essays", "journal"):
    for d in sorted((DIST / coll).glob("*/")):
        page = d / "index.html"
        if page.exists():
            live += 1; check_page(page, f"{SITE}/{coll}/{d.name}/")

if live == 0: errs.append("no post pages were built")

for feed in ("all", "essays", "journal"):
    f = DIST / "rss" / f"{feed}.xml"
    if not f.exists(): errs.append(f"rss/{feed}.xml missing"); continue
    try: n = len(ET.parse(f).getroot().findall("./channel/item"))
    except ET.ParseError as e: errs.append(f"rss/{feed}.xml unparsable: {e}"); continue
    want = live if feed == "all" else len(list((DIST / feed).glob("*/index.html")))
    if n != want: errs.append(f"rss/{feed}.xml has {n} items, expected {want}")

for e in errs: print("FAIL", e)
print(f"OK: dist checked ({live} post pages, 3 feeds)" if not errs else f"FAILED: {len(errs)} problem(s)")
sys.exit(1 if errs else 0)
