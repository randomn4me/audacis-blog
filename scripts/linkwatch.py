#!/usr/bin/env python3
"""Detect content drift behind external links cited in blog posts.

Complements the lychee link-check workflows: lychee tells you a link is *broken*
(404), linkwatch tells you the page behind a still-working link *changed*.

Flow: collect every external URL from content/**/*.md, fetch each (PDFs by
download, everything else rendered headless via Playwright/Chromium so JS
resolves), extract readable text with kreuzberg, normalise it, and compare
against the committed snapshot in .linkwatch/snapshots/. On any text difference
it opens one Forgejo issue listing the changed URLs with diffs. The workflow
then commits the rewritten snapshots, so the next run only fires on *further*
drift.

Exact text comparison is the trigger (a one-word edit fires); the reported
SequenceMatcher ratio only labels how big the change is. URLs matching a line in
.linkwatch/ignore.txt are skipped.

Env:
  FORGEJO_API    instance base URL, e.g. https://git.audacis.net
  FORGEJO_REPO   owner/name, e.g. philippkuehn/blog
  FORGEJO_TOKEN  access token with issue write scope (omit to skip filing)
  LINKWATCH_DRY  set to anything to print the issue instead of filing it
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from kreuzberg import extract_bytes_sync
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
STATE = ROOT / ".linkwatch"
SNAPSHOTS = STATE / "snapshots"
IGNORE_FILE = STATE / "ignore.txt"
URLS_FILE = STATE / "urls.json"
CHECKED_FILE = STATE / "checked.json"  # sha -> last-checked epoch, drives rotation

OWN_DOMAIN = "audacis.net"
NAV_TIMEOUT_MS = 20_000
SETTLE_MS = 800
# We only extract text, so skip heavy assets: far faster page loads (the run
# must finish inside the runner's ~6m job cap) and no signed image-URL noise.
SKIP_RESOURCES = {"image", "media", "font"}
# The runner kills the job at ~6m. Stop rendering before then and let the
# workflow commit the progress made; pages not reached this run are picked up
# next run (we process least-recently-checked first), so coverage converges.
RENDER_BUDGET_S = 180
USER_AGENT = "linkwatch/1 (+https://audacis.net; content-drift monitor)"
MAX_DIFF_LINES = 80  # truncate per-URL diffs so issues stay readable
MAX_CONTENT_CHARS = 16_000  # cap embedded full-text so issues stay manageable

# Inline-link target `](url)`, autolink `<url>`, and bare url. Trailing
# punctuation that markdown/prose tends to glue on is stripped afterwards.
URL_RE = re.compile(r"https?://[^\s)\]<>\"'`]+")


def extract_links() -> list[str]:
    """Every distinct external http(s) URL appearing in content/**/*.md."""
    found: set[str] = set()
    for md in CONTENT.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for raw in URL_RE.findall(text):
            url = raw.rstrip(".,;:!?")
            # Drop one trailing ) only if it has no opener (markdown `](url).`)
            if url.endswith(")") and url.count("(") < url.count(")"):
                url = url[:-1]
            if OWN_DOMAIN in url:
                continue
            found.add(url)
    return sorted(found)


def load_ignore() -> list[str]:
    if not IGNORE_FILE.exists():
        return []
    out = []
    for raw in IGNORE_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()  # drop full-line and inline comments
        if line:
            out.append(line)
    return out


def is_ignored(url: str, patterns: list[str]) -> bool:
    return any(p in url for p in patterns)


def snapshot_path(url: str) -> Path:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    return SNAPSHOTS / f"{digest}.txt"


def normalise(text: str) -> str:
    """Stabilise extracted text: strip per-request noise, collapse blank runs.

    Pages vary between fetches without their content changing. Three classes
    dominate and would otherwise fire false drift:
    - base64 `data:` URIs (e.g. arXiv SVGs) reorder attributes per request;
    - image targets are often signed/CDN URLs (GitHub's githubusercontent
      links carry an expiring `?jwt=...&X-Amz-Signature=...`) that regenerate
      every fetch, while the alt text is stable;
    - URL query strings hold signatures, cache-busters and session tokens.
    Collapse all three; keep alt text and the URL path (the meaningful parts).
    """
    text = re.sub(r"data:[^\s)]+", "data:…", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"![\1]", text)
    text = re.sub(r"(https?://[^\s)\]]+?)\?[^\s)\]]*", r"\1", text)
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    blank = 0
    for line in lines:
        line = line.rstrip()
        if line == "":
            blank += 1
            if blank <= 1:
                out.append("")
        else:
            blank = 0
            out.append(line)
    return "\n".join(out).strip() + "\n"


def fetch_pdf(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    return normalise(extract_bytes_sync(data, "application/pdf").content)


def fetch_html(page, url: str) -> str:
    page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
    page.wait_for_timeout(SETTLE_MS)  # let hydration / late JS settle
    html = page.content().encode("utf-8")
    return normalise(extract_bytes_sync(html, "text/html").content)


def fetch_text(page, url: str) -> str | None:
    """Rendered, extracted, normalised text, or None if the fetch failed."""
    try:
        if url.lower().split("?")[0].endswith(".pdf") or "/pdf/" in url.lower():
            return fetch_pdf(url)
        return fetch_html(page, url)
    except Exception as exc:  # noqa: BLE001 - report and move on, lychee owns 404s
        print(f"  ! fetch failed: {url}\n    {type(exc).__name__}: {exc}")
        return None


def make_diff(old: str, new: str, url: str) -> tuple[float, str]:
    ratio = difflib.SequenceMatcher(None, old, new).ratio()
    diff = list(
        difflib.unified_diff(
            old.splitlines(), new.splitlines(), "before", "after", lineterm=""
        )
    )
    if len(diff) > MAX_DIFF_LINES:
        diff = diff[:MAX_DIFF_LINES] + [f"... ({len(diff) - MAX_DIFF_LINES} more lines)"]
    return ratio, "\n".join(diff)


def render_issue(changes: list[dict]) -> tuple[str, str]:
    title = f"Link content drift: {len(changes)} page(s) changed"
    parts = [
        "Content behind one or more cited links changed since the last "
        "snapshot. Review each diff; if it is noise (timestamp, counter, ad), "
        "add the URL to `.linkwatch/ignore.txt`.\n",
    ]
    for c in changes:
        pct = round(c["ratio"] * 100)
        content = c["content"]
        if len(content) > MAX_CONTENT_CHARS:
            snap = snapshot_path(c["url"]).name
            content = (
                content[:MAX_CONTENT_CHARS]
                + f"\n\n... (truncated; full text in .linkwatch/snapshots/{snap})"
            )
        parts.append(
            f"\n### {c['url']}\n"
            f"similarity to previous: {pct}%\n\n"
            f"<details><summary>diff</summary>\n\n"
            f"```diff\n{c['diff']}\n```\n\n</details>\n\n"
            f"<details><summary>full extracted text (current)</summary>\n\n"
            f"```\n{content}\n```\n\n</details>\n"
        )
    return title, "".join(parts)


def file_issue(title: str, body: str) -> None:
    api = os.environ.get("FORGEJO_API", "").rstrip("/")
    repo = os.environ.get("FORGEJO_REPO", "")
    token = os.environ.get("FORGEJO_TOKEN", "")
    if os.environ.get("LINKWATCH_DRY") or not (api and repo and token):
        print(f"\n[dry-run] would file issue: {title}\n\n{body}")
        return
    url = f"{api}/api/v1/repos/{repo}/issues"
    payload = json.dumps({"title": title, "body": body}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"token {token}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            number = json.load(resp).get("number")
        print(f"\nFiled issue #{number}: {title}")
    except urllib.error.HTTPError as exc:
        print(f"\n! issue API {exc.code}: {exc.read().decode('utf-8', 'ignore')}")
        sys.exit(1)


def main() -> None:
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    ignore = load_ignore()
    links = [u for u in extract_links() if not is_ignored(u, ignore)]
    checked = json.loads(CHECKED_FILE.read_text()) if CHECKED_FILE.exists() else {}
    # Least-recently-checked first (never-checked = 0 = first). A budget-truncated
    # run advances the frontier instead of redoing the head, so coverage converges.
    links.sort(key=lambda u: checked.get(snapshot_path(u).stem, 0))
    print(f"Watching {len(links)} external link(s).")

    current_shas = {snapshot_path(u).stem for u in links}
    changes: list[dict] = []
    new_baselines = 0
    processed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page(user_agent=USER_AGENT)
        page.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in SKIP_RESOURCES
            else route.continue_(),
        )
        start = time.time()
        for url in links:
            if time.time() - start > RENDER_BUDGET_S:
                print(f"  … budget reached; {len(links) - processed} link(s) "
                      f"deferred to next run")
                break
            processed += 1
            text = fetch_text(page, url)
            if text is None:
                continue
            snap = snapshot_path(url)
            checked[snap.stem] = int(time.time())
            if not snap.exists():
                snap.write_text(text, encoding="utf-8")
                new_baselines += 1
                print(f"  + baseline: {url}")
                continue
            old = snap.read_text(encoding="utf-8")
            if old == text:
                continue
            ratio, diff = make_diff(old, text, url)
            changes.append(
                {"url": url, "ratio": ratio, "diff": diff, "content": text}
            )
            snap.write_text(text, encoding="utf-8")
            print(f"  ~ changed ({round(ratio * 100)}% similar): {url}")
        browser.close()

    # Prune snapshots for links no longer cited anywhere.
    for snap in SNAPSHOTS.glob("*.txt"):
        if snap.stem not in current_shas:
            snap.unlink()
            print(f"  - pruned stale snapshot: {snap.name}")

    URLS_FILE.write_text(json.dumps(sorted(links), indent=2) + "\n", encoding="utf-8")
    checked = {s: t for s, t in checked.items() if s in current_shas}
    CHECKED_FILE.write_text(json.dumps(checked, indent=0) + "\n", encoding="utf-8")

    print(
        f"\nDone. checked {processed}/{len(links)}, "
        f"{new_baselines} new baseline(s), {len(changes)} change(s)."
    )
    if changes:
        file_issue(*render_issue(changes))


if __name__ == "__main__":
    main()
