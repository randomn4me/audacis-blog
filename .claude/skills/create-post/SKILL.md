---
name: create-post
description: Draft a blog post for audacis.net from a topic, idea, or file. Use when the user asks to write a post, draft an article, or create blog content.
argument-hint: <topic, idea, or file path>
---

# Create Blog Post

Draft a blog post for Philipp's personal blog at audacis.net.

Source: `$ARGUMENTS` — if a file path, read it first; if a topic or loose thoughts, use it as the starting point.

## Voice

**Read 2-3 existing posts in `content/blog/` before writing to calibrate.** That is the real spec; the notes below are guardrails, not a substitute.

First person, casual, honest. Self-deprecating, opinionated, and tangential are all fine. Show genuine curiosity — the reader should feel they're hearing from someone who cares. No corporate polish, marketing speak, or thought-leadership framing. Don't over-explain; trust a technical reader. Swearing is fine when it fits ("fuck-up" appears in existing posts). Light humor, never forced. Short paragraphs, conversational flow. Emphasis with *italics*, not quotation marks. See `CLAUDE.md` for the house style (Elements of Style, no em dashes).

## File and frontmatter

Write to `content/blog/SLUG.md`, SLUG in kebab-case from the title.

```toml
+++
title = "Post Title"
description = "Punchy teaser for listings and SEO, not a dry summary"
date = YYYY-MM-DD   # today
draft = true        # always; Philipp publishes when ready

[taxonomies]
tags = ["tag1", "tag2"]   # 1-3, reuse existing tags where possible
+++
```

## Content

- Open on a situation, problem, question, or confession. No "In this post I will discuss...".
- `<!-- more -->` break after the first paragraph or two (controls the listing excerpt).
- `#`/`##` headings when the post is long enough to need them.
- One sentence per line — cleaner diffs.
- **Cite with inline links, not footnotes.** The corpus is consistent: `trusting-trust-in-the-age-of-ai.md` carries nine sources and zero footnotes. Footnotes in older posts are asides and jokes, never bibliography. A stack of numbered references reads as an academic habit.
- Code blocks carry language hints (` ```nix `, ` ```rust `). Images via `{{ img(src="/img/filename.jpg", alt="description") }}`.
- Link to related posts in `content/blog/` where it fits — a follow-up, a callback, shared context.
- Length follows the topic (rant 300-500, walkthrough 600-1200, deep dive as long as needed). Don't pad; if it's said in 400 words, stop.

## Timeline sections

For a genuine sequence of three or four dated events where order is the point, use the `timeline` shortcode instead of a run of "On 16 July, ..." paragraphs:

```
{% timeline() %}
## 16 July

The disclosure goes up. One sentence per line, as everywhere else.
{% end %}
```

Each `## ` heading is the date stamp, so the prose must not repeat it: write *Hugging Face publishes the disclosure*, not *On 16 July, Hugging Face publishes...*. A single dated fact is a sentence, not a timeline.

**No footnotes inside the timeline.** Zola renders shortcode bodies through the `markdown` filter, separate from the page's footnote pass, so a `[^1]` inside is invisible to numbering — its definition is treated as unreferenced, sorted to the end, and silently shifts the printed number of *every* footnote in the post while anchors keep working. Cite inline instead, or put the footnote in the prose around the timeline. (Zola numbers footnotes by order of first reference; keep the definition block in that order. See `templates/shortcodes/timeline.html` and `sass/style.scss`.)

## Present the draft as an artifact

Publish a rendered reading copy so Philipp reads a page, not markdown — problems that hide in a diff (a section that drags, a wall of citations, a flat ending) show up in a rendered column.

1. Load the `artifact-design` skill first (required before writing artifact HTML).
2. Write the HTML to the session scratchpad, **never** into the repo — it's a preview, not site content.
3. Publish with the **Artifact** tool; redeploy the *same file path* every revision so the URL and open tabs stay stable. Keep the same favicon.

The reading copy needs, beyond plain HTML:

- **Absolute URLs** for internal links (`https://audacis.net/blog/other-post/`) — relative paths don't resolve off-site.
- **Footnotes rendered by hand** — Zola's `[^1]` is not HTML. Use superscript anchors to a numbered notes list; check every reference has a note and vice versa.
- The **draft state shown honestly** (a `DRAFT` chip, a footer naming the source file), updated the moment the flag changes.

Keep the artifact in sync with the markdown — every edit is an edit to both, or the reading copy starts lying.

### The share block

End the artifact with a LinkedIn version and a **Copy text** button.

- ~150 words (LinkedIn truncates past the fold), leading with the single most surprising concrete fact, not context.
- Plain text only — LinkedIn strips markdown; use straight quotes for titles.
- End with the canonical URL `https://audacis.net/blog/SLUG/`.
- Assemble the copied string from individual paragraphs in JS so blank lines survive.
- **Name the people the post actually leans on** (paper authors, whoever is quoted or did the work) in the body text, so Philipp can turn them into tags — only those the short version genuinely uses. Below the copyable block, outside it, list the candidates with affiliations and any orgs worth tagging; say plainly you haven't verified their profiles and each handle needs confirming.

## After writing

1. **Read** the final file so Philipp sees it with line numbers.
2. Give the file path and the artifact URL, and remind it's `draft = true`.
3. Offer `/review-post` before publishing (checks claims, references, links, voice, bloat).
4. Ask what to adjust before Philipp removes the draft flag.
