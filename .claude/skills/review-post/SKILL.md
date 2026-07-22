---
name: review-post
description: Review a drafted blog post for audacis.net before publishing. Checks the through-line, voice against the existing corpus, whether every claim is referenced and the references actually support it, whether links resolve, cross-links to other posts, bloat, and house style. Use when the user asks to review, critique, fact-check, or sanity-check a post before removing the draft flag.
argument-hint: <post slug or file path>
---

# Review Blog Post

Adversarial pre-publication review of a post for Philipp's blog at audacis.net.

## Input

Source: `$ARGUMENTS`

A slug (`the-model-that-cheated-on-its-own-exam`), a filename, or a path. Resolve to `content/blog/SLUG.md`. If empty, review the most recently modified post with `draft = true`.

## Stance

Read-only until the report is delivered. Find what a hostile reader would find.

- Do not praise. A category with nothing wrong gets one line: `Thread: clean.`
- Do not rewrite the voice into neutral prose. The post is supposed to sound like a person.
- Never remove `draft = true`. That is the author's call.
- Verify, do not recall. If you are checking a claim, open the source. Your memory of a paper is not a citation.
- When you are unsure whether something is a problem, say so and let the author decide. A confident wrong finding costs more than an admitted uncertainty.

## Phase 1 — Calibrate on the corpus, weighted to the older posts

List the posts by age:

```sh
for f in content/blog/*.md; do
  [ "$(basename "$f")" = "_index.md" ] && continue
  printf '%s %s\n' "$(grep -m1 '^date = ' "$f" | sed 's/date = //')" "$f"
done | sort
```

Read **in full**: the three oldest posts, the two most recent, and any post on a related topic.

Weight the oldest posts most heavily. They are the baseline voice, written before any house style drifted and before any drafting help. Recent posts may have drifted toward something flatter or more essayistic. Treat drift as drift, not as the new normal. If the post under review matches last month's post but not the 2024 posts, that is a finding.

Record concrete markers rather than impressions: typical sentence length, how posts open, how they close, density of "I", where humor lands, whether the author hedges or commits, paragraph length, heading style, how links are worked into sentences.

Then check the draft against those markers. Name the specific line that is off and the specific older post it should sound more like.

## Phase 2 — The thread

Before rereading the intro, state the post's argument in one sentence. If you cannot, that is the top finding.

Then for each section ask what it contributes to that sentence. A section that could be deleted without weakening the argument should be cut or folded in, no matter how interesting it was to research.

Check the shape against `CLAUDE.md`:

- Opens mid-scene or on the core observation. No context-setting preamble.
- Sections end on implication or concrete detail, not summary.
- Unresolved tension is allowed to stay unresolved. "I do not have a conclusion here" is a valid ending; a tidy conclusion that was not earned is not.
- Insights come from concrete experience, not abstract claims.

## Phase 3 — Claims and references

The heaviest phase. Enumerate every checkable statement: numbers, dates, names, titles, attributions, quotes, capability claims, and anything with "first", "only", "never", "always".

Sort each into:

- **Personal experience** — needs no citation. "My calves had opinions by day two."
- **Checkable fact** — needs a reference.
- **Opinion** — needs no reference, but must read as opinion rather than fact.

For every checkable fact, run both tests:

1. **Is there a reference?** An unreferenced fact is a blocker.
2. **Does the reference support this specific claim?** Open the source and find the sentence that carries it. A link whose title sounds right is not support. This is the test that catches real errors: a citation pointing at the right project but the wrong page, or a figure that lives in a different document than the one linked.

Extra scrutiny for:

- **Superlatives.** Before accepting "first", actively search for a counterexample. If prior art exists, the claim must be narrowed until it survives, and the prior art should be named in the post.
- **Quotes.** Verbatim, character for character, against the primary source. Check ellipses and capitalisation.
- **Secondary sourcing.** If the post cites a news write-up where a primary source exists, say so and give the primary.
- **Numbers.** Recompute anything derived (percentages, tallies, date arithmetic).

Some publishers block automated fetching. When `WebFetch` returns 403, try, in order: a `curl` with a browser user agent, the Wayback Machine (`http://archive.org/wayback/available?url=...`, then fetch the snapshot with `curl` and strip tags), or the headless browser from the gstack `/browse` skill. Do not fall back to a news summary of the source and call it verified. Note in the report which sources you could not reach directly.

## Phase 4 — Do the links resolve

Extract every URL and check it:

```sh
grep -oE 'https?://[^)"[:space:]]+' content/blog/SLUG.md | sed 's/[.,)]*$//' | sort -u |
while read -r u; do printf '%-72s ' "$u"; curl -sL -o /dev/null -m 20 \
  -A 'Mozilla/5.0' -w '%{http_code}\n' "$u"; done
```

Anything not 2xx gets checked by hand before it is called broken: some hosts return 403 to scripts but serve fine in a browser, and some return 200 for a soft 404. Confirm the page still contains what is being cited.

Internal links (`/blog/other-post/`) must point at a slug that exists in `content/blog/` and is not itself a draft:

```sh
grep -oE '\]\(/blog/[^)]+\)' content/blog/SLUG.md
ls content/blog/
```

This repo already has link infrastructure, so do not rebuild it:

- `.forgejo/workflows/link-check.yml` runs lychee over the built site on every change.
- `.forgejo/workflows/link-check-live.yml` checks the live site weekly.
- `scripts/linkwatch.py` plus `.linkwatch/` watch cited pages for *content drift* behind links that still resolve. See `.linkwatch/README.md`. Worth a mention in the report if the post leans on a page likely to change.

`zola` comes from `nix develop`; lychee is CI-only, so use `curl` locally.

## Phase 5 — Cross-references to the rest of the blog

Search the **whole** corpus by topic. Age is irrelevant: a 2024 post is as linkable as last month's.

```sh
rg -il 'keyword|synonym|related term' content/
```

Run several searches, one per theme in the post. For each hit, ask whether a reader would actually be better off following the link. Link where it earns its place, not to hit a quota. A callback that pays off ("at RSAC in March I complained that...") is worth more than a bare topical link.

Also check the reverse direction: does an older post now deserve a link *forward* to this one? Report it as a suggestion. Do not edit other posts without asking.

## Phase 6 — House style and mechanics

From `CLAUDE.md`: personal and reflective voice, self-deprecating where it lands, concrete over abstract, no enthusiasm inflation, no filler openers, Elements of Style, no em dashes.

Mechanical checks:

```sh
F=content/blog/SLUG.md
grep -n '—' "$F"                          # em dashes: should be none
grep -c '' "$F"                           # line count vs sentence count
grep -n '<!-- more -->' "$F"              # excerpt break present
sed -n '1,12p' "$F"                       # frontmatter: title, description, date, draft, tags
grep -rh 'tags = ' content/blog/ | sort | uniq -c | sort -rn   # reuse existing tags
```

Also confirm: one sentence per line; slug matches the title; `description` is a teaser and not a dry summary; the date is the intended one; code blocks carry a language hint; images use the `img`/`gallery` shortcodes with real alt text.

Footnotes work in this setup (`[^1]` inline, `[^1]: text` at the bottom; the theme adds backlinks). If the post uses them, verify every reference has a definition and vice versa:

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

Report the word count, then ask what the post would lose at 80 percent of it.

Flag:

- A sentence that restates the previous sentence in different words.
- A point already made in an earlier section.
- Adjectives and intensifiers doing no work.
- A section that exists because the research was interesting, not because the argument needs it.
- Throat-clearing before the actual sentence.

If a paragraph survives only because it was hard to write, cut it.

## Output

Report in three buckets, most severe first. Each finding gets `file:line`, what is wrong, why it matters, and a concrete suggested replacement.

- **BLOCKER** — factually wrong, unsupported claim, misquote, dead link, a superlative that prior art disproves.
- **SHOULD FIX** — voice drift from the older posts, weak or broken thread, bloat, a missing cross-link that would genuinely help, style rule violated.
- **CONSIDER** — taste. Say it once and move on.

Close with:

- The post's thread in one sentence, as you understood it from reading.
- Word count.
- Sources you could not verify directly, and why.
- A verdict: ship, or fix the blockers first.

Then ask whether to apply the fixes. Apply only what is agreed, and leave `draft = true` alone.
