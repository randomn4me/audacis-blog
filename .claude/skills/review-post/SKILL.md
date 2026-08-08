---
name: review-post
description: Review a drafted blog post for audacis.net before publishing. Checks the through-line, voice against the existing corpus, whether every claim is referenced and the references actually support it, whether links resolve, cross-links to other posts, bloat, and house style. Use when the user asks to review, critique, fact-check, or sanity-check a post before publishing.
argument-hint: <post slug or file path>
---

# Review Blog Post

Adversarial pre-publication review of a post for Philipp's blog at audacis.net.

Source: `$ARGUMENTS` — a slug, filename, or path, resolving to `content/blog/SLUG.md`. If empty, review the most recently modified post with `draft = true`.

## Stance

Read-only until the report is delivered. Find what a hostile reader would find.

- Don't praise. A clean category gets one line.
- Don't rewrite the voice into neutral prose. It's supposed to sound like a person.
- Never remove `draft = true`. Author's call.
- Verify, don't recall. Open the source; your memory of a paper is not a citation.
- When unsure whether something is a problem, say so and let the author decide. A confident wrong finding costs more than an admitted uncertainty.

## Phase 1 — Calibrate on the corpus

List posts by age (`grep -m1 '^date = '` across `content/blog/*.md`, sort). Read in full the three oldest, the two most recent, and any post on a related topic.

Weight the oldest most heavily — they're the baseline voice, before any drift or drafting help. If the draft matches last month's post but not the 2024 posts, that's a finding. Record concrete markers (sentence length, openings, closings, density of "I", where humor lands, hedge vs commit, heading style, how links sit in sentences), then name the specific off line and the older post it should sound like.

## Phase 2 — The thread

Before rereading the intro, state the argument in one sentence. If you can't, that's the top finding.

For each section, ask what it contributes to that sentence. A section deletable without weakening the argument gets cut or folded in.

**Orthogonal frames.** The subtler failure is not a section contributing nothing, but several sections each contributing a *different* argument that all pass the "does it contribute" test yet pull toward different conclusions — leaving the reader with a bag of observations instead of one argument. Count the conceptual lenses; more than two or three each carrying a section is a flag. The tell is a closing sentence that *lists* ("just a documented case, a paper that described it, and the observation that...") instead of concluding. Name the load-bearing chain, mark the rest severable to a sentence. Weigh against house style — sitting with unresolved tension and circling a subject are allowed; the finding is competing equally-weighted ideas, not merely more than one idea.

Check shape against `CLAUDE.md`: opens mid-scene or on the core observation, no preamble; sections end on implication or concrete detail, not summary; unresolved tension may stay unresolved, but an unearned tidy conclusion may not; insights come from concrete experience.

## Phase 3 — Claims and references

The heaviest phase. Enumerate every checkable statement: numbers, dates, names, titles, attributions, quotes, capability claims, anything with "first/only/never/always". Sort into personal experience (no cite), checkable fact (needs a reference), opinion (must read as opinion).

For every checkable fact: (1) is there a reference? Unreferenced fact = blocker. (2) does the reference support *this specific* claim? Open it and find the carrying sentence — a right-sounding title is not support.

Extra scrutiny: **superlatives** (actively search for a counterexample before accepting "first"; narrow and name prior art if found); **quotes** (verbatim, character for character, including ellipses and caps); **secondary sourcing** (name the primary where one exists); **numbers** (recompute anything derived).

On 403: try `curl` with a browser UA, then the Wayback Machine, then the gstack `/browse` headless browser. Don't fall back to a news summary and call it verified. Note unreachable sources in the report.

## Phase 4 — Links resolve

Extract every URL and check the status code:

```sh
grep -oE 'https?://[^)"[:space:]]+' content/blog/SLUG.md | sed 's/[.,)]*$//' | sort -u |
while read -r u; do printf '%-72s ' "$u"; curl -sL -o /dev/null -m 20 -A 'Mozilla/5.0' -w '%{http_code}\n' "$u"; done
```

Check non-2xx by hand — some hosts 403 scripts but serve browsers, some 200 a soft 404; confirm the page still contains what's cited. Internal `/blog/...` links must point at a real, non-draft slug in `content/blog/`:

```sh
grep -oE '\]\(/blog/[^)]+\)' content/blog/SLUG.md
ls content/blog/
```

Existing infra, don't rebuild: `.forgejo/workflows/link-check*.yml` (lychee, built + live), `scripts/linkwatch.py` + `.linkwatch/` (content drift behind live links). Mention linkwatch if the post leans on a page likely to change. `zola` is in `nix develop`; lychee is CI-only, so use `curl` locally.

## Phase 5 — Cross-references

Search the whole corpus by topic (`rg -il`), one search per theme; age is irrelevant. Link only where a reader is genuinely better off following it — a callback that pays off beats a bare topical link. Also check the reverse: does an older post now deserve a forward link to this one? Report as a suggestion; don't edit other posts without asking.

## Phase 6 — House style and mechanics

Voice per `CLAUDE.md`: personal and reflective, self-deprecating where it lands, concrete over abstract, no enthusiasm inflation, no filler openers, Elements of Style, no em dashes.

```sh
F=content/blog/SLUG.md
grep -n '—' "$F"                 # em dashes: none
grep -n '<!-- more -->' "$F"     # excerpt break present
sed -n '1,12p' "$F"              # frontmatter
grep -rh 'tags = ' content/blog/ | sort | uniq -c | sort -rn   # reuse existing tags
```

Confirm: one sentence per line; slug matches title; `description` is a teaser not a dry summary; date is intended; code blocks carry a language hint; images use `img`/`gallery` shortcodes with real alt text.

Footnotes work here (`[^1]` inline, `[^1]: text` at the bottom; the theme adds backlinks). If used, verify every reference has a definition and vice versa:

```sh
python3 - <<'PY'
import re
t = open('content/blog/SLUG.md').read()
refs = set(re.findall(r'\[\^(\w+)\](?!:)', t))
defs = set(re.findall(r'^\[\^(\w+)\]:', t, re.M))
print('undefined:', refs - defs or 'none')
print('unused:   ', defs - refs or 'none')
PY
```

## Phase 7 — Bloat

Report word count, then ask what the post loses at 80% of it. Flag: a sentence restating the previous one; a point already made; adjectives doing no work; a section that exists because the research was interesting; throat-clearing before the real sentence. If a paragraph survives only because it was hard to write, cut it.

## Output

Three buckets, most severe first. Each finding gets `file:line`, what's wrong, why it matters, a concrete replacement.

- **BLOCKER** — factually wrong, unsupported claim, misquote, dead link, a superlative prior art disproves.
- **SHOULD FIX** — voice drift, weak or broken thread, competing frames, bloat, a missing cross-link that would help, style rule violated.
- **CONSIDER** — taste. Say it once.

Close with: the thread in one sentence as you read it, word count, sources you couldn't verify directly and why, and a verdict (ship, or fix blockers first). Then ask whether to apply fixes. Apply only what's agreed; leave `draft = true` alone.
