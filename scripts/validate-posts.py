#!/usr/bin/env python3
"""Validate blog post frontmatter + length rules. Exit 1 on any failure."""
import datetime, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ = ["title", "description", "pubDate", "kind", "tags"]
KINDS = {"essay", "journal"}
DIRKIND = {"essays": "essay", "journal": "journal"}
MINWORDS = {"essay": 350, "journal": 120}

def parse_frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    lines = m.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val in (">-", ">", "|"):  # folded scalar: consume indented block
            parts = []
            i += 1
            while i < len(lines) and (lines[i].startswith(("  ", "\t")) or not lines[i].strip()):
                parts.append(lines[i].strip())
                i += 1
            fm[key] = " ".join(parts)
            continue
        if val == "" and i + 1 < len(lines) and lines[i + 1].lstrip().startswith("- "):
            items = []
            i += 1
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                items.append(lines[i].lstrip()[2:].strip().strip('"').strip("'"))
                i += 1
            fm[key] = items
        else:
            fm[key] = val.strip('"').strip("'")
            i += 1
    return fm, text[m.end():]

def check_file(path):
    errs = []
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    rel = str(path.relative_to(ROOT))
    if fm is None:
        return [f"FAIL {rel}: no YAML frontmatter"]
    for k in REQ:
        if k not in fm or fm[k] in ("", []):
            errs.append(f"FAIL {rel}: missing/empty '{k}'")
    if "kind" in fm and fm["kind"] not in KINDS:
        errs.append(f"FAIL {rel}: kind '{fm['kind']}' not in {sorted(KINDS)}")
    if fm.get("pubDate"):
        try:
            datetime.date.fromisoformat(fm["pubDate"][:10])
        except ValueError:
            errs.append(f"FAIL {rel}: pubDate '{fm['pubDate']}' not ISO date")
    dirmatch = re.search(r"src/content/(essays|journal)/", rel)
    if dirmatch and fm.get("kind") and DIRKIND[dirmatch.group(1)] != fm["kind"]:
        errs.append(f"FAIL {rel}: kind '{fm['kind']}' must be '{DIRKIND[dirmatch.group(1)]}' for its directory")
    if fm.get("draft") == "true":
        return errs  # drafts exempt from length rules
    words = len(re.findall(r"\S+", body))
    kind = fm.get("kind") or (DIRKIND[dirmatch.group(1)] if dirmatch else "essay")
    if kind in MINWORDS and words < MINWORDS[kind]:
        errs.append(f"FAIL {rel}: {words} words < {MINWORDS[kind]} required for '{kind}'")
    if fm.get("hero") and not str(fm["hero"]).startswith("/images/posts/"):
        errs.append(f"FAIL {rel}: hero must be a /images/posts/ root-relative path")
    if fm.get("hero") and str(fm["hero"]).startswith("/images/posts/") and not (ROOT / fm["hero"].lstrip("/")).exists():
        errs.append(f"FAIL {rel}: hero file missing on disk: {fm['hero']}")
    return errs

def main():
    args = sys.argv[1:]
    files = [pathlib.Path(a).resolve() for a in args] if args else \
        sorted((ROOT / "src/content").rglob("*.md"))
    all_errs = []
    for f in files:
        all_errs += check_file(f)
    for e in all_errs:
        print(e)
    print(f"OK: {len(files)} post(s) validated" if not all_errs else f"FAILED: {len(all_errs)} problem(s)")
    sys.exit(1 if all_errs else 0)

if __name__ == "__main__":
    main()
