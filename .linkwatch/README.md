# linkwatch

Content-drift monitor for external links cited in blog posts. Where the lychee
workflows catch *broken* links, this catches links that still resolve but whose
*content* changed.

`scripts/linkwatch.py` collects every external URL in `content/**/*.md`, fetches
each over HTTP (kreuzberg extracts text from HTML or PDF), and compares it to the
snapshot stored here. On any difference it files one Forgejo issue with per-URL
diffs, then the workflow commits the refreshed snapshots so it only fires again
on further change. No JS rendering — it would hang/overrun the runner's job cap;
plain HTTP is bounded and fast.

To keep runs inside that cap it processes least-recently-checked URLs first
(tracked in `checked.json`) under a wall-clock budget, committing progress and
resuming next run, so coverage converges.

## Files

- `snapshots/<sha1>.txt` — last-seen normalised text per URL. Committed, so
  drift shows up as a git diff too.
- `checked.json` — per-URL last-checked time; drives the rotation.
- `urls.json` — the current watch list (regenerated each run).
- `ignore.txt` — substring patterns for URLs to skip (placeholders, churny
  pages whose diffs are noise). `#` comments allowed, inline too.

## Setup

Add a repo secret `LINKWATCH_TOKEN`: a Forgejo access token with **issue write**
and **repository content write** scope. Then trigger the workflow manually once
(`workflow_dispatch`) to lay down the baseline snapshots — the first run files no
issue. After that it runs Mondays 09:00.

## Triage

When an issue arrives, read the diff. Real change → update the citation or note
it. Noise (timestamp, vote count, ad) → add the URL to `ignore.txt`.

## Run locally

```sh
uv venv && . .venv/bin/activate
uv pip install kreuzberg==4.9.9
LINKWATCH_DRY=1 python scripts/linkwatch.py   # prints, never files
```
