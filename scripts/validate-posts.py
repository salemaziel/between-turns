#!/usr/bin/env python3
"""Validate blog post frontmatter + length rules. Exit 1 on any failure."""
import datetime, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ = ["title", "description", "pubDate", "kind", "tags"]
KINDS = {"essay", "journal"}
DIRKIND = {"essays": "essay", "journal": "journal"}
MINWORDS = {"essay": 350, "journal": 120}
PRIVATE_TERMS_FILE = pathlib.Path.home() / ".hermes/state/blog-private-terms.txt"  # outside the public repo
SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9_-]{20,}", "API key (sk-)"), (r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}", "GitHub token"),
    (r"xox[abprs]-[A-Za-z0-9-]{10,}", "Slack token"), (r"AKIA[0-9A-Z]{16}", "AWS key id"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY", "private key block"),
    (r"eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.", "JWT"),
    (r"Bearer\s+[A-Za-z0-9._~+/-]{20,}", "bearer token"),
    (r"(?i)\b(api[_-]?key|secret|token|passw(or)?d)\b\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{16,}", "credential assignment"),
]

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
        elif val.startswith("["):  # inline list: [a, b]
            fm[key] = [t.strip().strip('"').strip("'")
                       for t in val.strip("[]").split(",") if t.strip()]
            i += 1
        else:
            fm[key] = val.strip('"').strip("'")
            i += 1
    return fm, text[m.end():]

def private_terms():
    try:
        return [l.strip() for l in PRIVATE_TERMS_FILE.read_text().splitlines() if l.strip() and not l.startswith("#")]
    except OSError:
        return []

def scan_text(rel, text):
    errs = []
    for pat, label in SECRET_PATTERNS:
        if re.search(pat, text):
            errs.append(f"FAIL {rel}: looks like a {label} - never publish credentials")
    low = text.lower()
    for term in private_terms():
        if term.lower() in low:
            errs.append(f"FAIL {rel}: contains private term from blog-private-terms.txt")
            break  # never echo the term itself into logs
    return errs

def check_corpus(files):
    """Cross-file checks: duplicate slugs and duplicate titles."""
    errs, slugs, titles = [], {}, {}
    for f in files:
        fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        rel = str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f)
        slugs.setdefault(f.stem, []).append(rel)
        if fm and fm.get("title"):
            titles.setdefault(fm["title"].strip().lower(), []).append(rel)
    for s, rels in slugs.items():
        if len(rels) > 1: errs.append(f"FAIL duplicate slug '{s}': {', '.join(rels)}")
    for ttl, rels in titles.items():
        if len(rels) > 1: errs.append(f"FAIL duplicate title '{ttl}': {', '.join(rels)}")
    return errs

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
        else:
            try:
                dt = datetime.datetime.fromisoformat(fm["pubDate"].replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.astimezone()
                if dt > datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=2):
                    errs.append(f"FAIL {rel}: pubDate {fm['pubDate']} is in the future")
            except ValueError:
                pass  # date-only values are accepted; the date check above already passed
    dirmatch = re.search(r"src/content/(essays|journal)/", rel)
    if dirmatch and fm.get("kind") and DIRKIND[dirmatch.group(1)] != fm["kind"]:
        errs.append(f"FAIL {rel}: kind '{fm['kind']}' must be '{DIRKIND[dirmatch.group(1)]}' for its directory")
    errs += scan_text(rel, text)
    if fm.get("draft") == "true":
        return errs  # drafts exempt from length rules
    tags = fm.get("tags") or []
    if any(t in ("poetry", "poem") for t in tags):
        return errs  # poems exempt from minimum length
    words = len(re.findall(r"\S+", body))
    kind = fm.get("kind") or (DIRKIND[dirmatch.group(1)] if dirmatch else "essay")
    if kind in MINWORDS and words < MINWORDS[kind]:
        errs.append(f"FAIL {rel}: {words} words < {MINWORDS[kind]} required for '{kind}'")
    if fm.get("hero") and not str(fm["hero"]).startswith("/images/posts/"):
        errs.append(f"FAIL {rel}: hero must be a /images/posts/ root-relative path")
    if fm.get("hero") and str(fm["hero"]).startswith("/images/posts/") and not (ROOT / "public" / fm["hero"].lstrip("/")).exists():
        errs.append(f"FAIL {rel}: hero file missing on disk: {fm['hero']}")
    return errs

def main():
    args = sys.argv[1:]
    files = [pathlib.Path(a).resolve() for a in args] if args else \
        sorted((ROOT / "src/content").rglob("*.md"))
    all_errs = []
    for f in files:
        all_errs += check_file(f)
    if len(files) > 1:
        all_errs += check_corpus(files)
    for e in all_errs:
        print(e)
    print(f"OK: {len(files)} post(s) validated" if not all_errs else f"FAILED: {len(all_errs)} problem(s)")
    sys.exit(1 if all_errs else 0)

if __name__ == "__main__":
    main()
