#!/usr/bin/env python3
"""Guard the Between Turns quality-gated cadence policy against regressions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABOUT = (ROOT / "src/pages/about.astro").read_text()
EDITORIAL = (Path.home() / ".hermes/skills/blog-editorial/SKILL.md").read_text()
POSTING = (Path.home() / ".hermes/skills/blog-posting/SKILL.md").read_text()
CRON_FILE = Path.home() / ".hermes/cron/jobs.json"
JOBS = {job["name"]: job for job in json.loads(CRON_FILE.read_text())["jobs"]}
WRITER = JOBS["blog-writer"]["prompt"]
EDITOR = JOBS["blog-editor"]["prompt"]
REVIEWER = JOBS["blog-reviewer"]["prompt"]

required = {
    "About page explains schedule is not a quota": "schedule is an invitation, not a quota" in ABOUT,
    "editorial policy allows zero drafts": "or no draft" in EDITORIAL,
    "editorial policy scans Cortex ideas": "idea_list" in EDITORIAL and "feed_list" in EDITORIAL,
    "editorial policy includes RSS-derived items": "RSS/news-derived" in EDITORIAL,
    "editorial policy includes OK notes": "/home/hermes/ok-wiki" in EDITORIAL,
    "editorial policy preserves held drafts without substitute": "does not trigger a replacement post" in EDITORIAL,
    "posting procedure allows zero drafts": "at most one draft" in POSTING.lower() and "no draft is a valid outcome" in POSTING.lower(),
    "writer prompt allows no draft": "or no draft if nothing meets the quality bar" in WRITER,
    "writer prompt scans Cortex candidates": "idea_list" in WRITER and "feed_list" in WRITER,
    "editor prompt allows zero topics": "zero is valid" in EDITOR,
    "editor prompt scans Cortex candidates": "idea_list" in EDITOR and "feed_list" in EDITOR,
    "reviewer prompt does not require substitute": "never requires a quota-driven substitute" in REVIEWER,
    "writer schedule is unchanged": JOBS["blog-writer"]["schedule"]["expr"] == "0 6,10 * * 1,2,4,5,6",
    "editor schedule is unchanged": JOBS["blog-editor"]["schedule"]["expr"] == "0 9 * * 0",
}
forbidden = {
    "About page has no four-post minimum": "publish at least four times a week" not in ABOUT.lower(),
    "editorial policy has no four-post promise": "4-posts-a-week promise" not in EDITORIAL,
    "editorial policy has no mandatory substitute": "MUST write and publish this substitute" not in EDITORIAL,
    "posting procedure has no unconditional one-post quota": "ONE post per run." not in POSTING,
    "posting procedure has no owed-post wording": "it forfeits the day's post" not in POSTING,
    "writer prompt has no hard one-post command": "Exactly ONE post this run" not in WRITER,
    "editor prompt has no minimum seed count": "keep >=5 seeds" not in EDITOR,
    "reviewer prompt has no substitute command": "publish a short honest" not in REVIEWER,
}
failed = [f"FAIL: {label}" for label, ok in {**required, **forbidden}.items() if not ok]
if failed:
    print("\n".join(failed))
    raise SystemExit(1)
print(f"OK: {len(required) + len(forbidden)} editorial policy checks passed")
