---
name: create-post
description: Draft a blog post for audacis.net from a topic, idea, or file. Use when the user asks to write a post, draft an article, or create blog content.
argument-hint: <topic, idea, or file path>
---

# Create Blog Post

Draft a blog post for Philipp's personal blog at audacis.net.

## Input

Source: $ARGUMENTS

If `$ARGUMENTS` is a file path, read the file first to understand the content. If it's a topic, idea, or loose thoughts, use that directly as the starting point.

## Voice & Tone

This is a personal blog. Write like Philipp writes:

- First person ("I"), casual and honest
- It's okay to be self-deprecating, opinionated, or tangential
- Show genuine curiosity and enthusiasm — the reader should feel like they're hearing from someone who actually cares about the topic
- Avoid corporate polish, marketing speak, or "thought leadership" framing
- Don't over-explain — trust the reader to be technical enough to follow along
- Swearing is fine when it fits naturally (see: "fuck-up" in existing posts)
- Light humor is welcome but don't force it
- Short paragraphs, conversational flow — more like talking to a friend than writing a paper

Read 2-3 existing posts in `content/blog/` before writing to calibrate the tone for the current session.

## Output

Create the blog post file directly at:

```
content/blog/SLUG.md
```

Where SLUG is derived from the title in kebab-case (lowercase, hyphens).

## Frontmatter

Use Zola TOML frontmatter:

```toml
+++
title = "Post Title"
description = "One-liner for listings and SEO"
date = YYYY-MM-DD
draft = true

[taxonomies]
tags = ["tag1", "tag2"]
+++
```

- Use today's date
- Always start as `draft = true` — Philipp publishes when ready
- Pick 1-3 tags from existing ones where possible (check `content/blog/` for what's been used)
- Description should be a punchy subtitle or teaser, not a dry summary

## Content Guidelines

- Open with something that pulls the reader in — a situation, a problem, a question, a confession. No "In this post I will discuss..."
- Use `#` and `##` headings to break up sections when the post is long enough to need them
- Include links to tools, projects, or references where relevant — the blog already does this naturally
- A `<!-- more -->` break after the first paragraph or two (this controls the excerpt on the listing page)
- Target length depends on the topic:
  - Quick tip or rant: 300-500 words
  - Tutorial or walkthrough: 600-1200 words
  - Deep dive: as long as it needs to be
- Don't pad for word count. If it's said in 400 words, stop at 400 words.
- Code blocks with language hints when showing code (` ```nix `, ` ```rust `, etc.)
- Images can be referenced from `/img/` if relevant, using the shortcode: `{{ img(src="/img/filename.jpg", alt="description") }}`
- One sentence per line — this makes diffs cleaner and editing easier
- Use *italics* for emphasis, not quotation marks
- Check existing posts in `content/blog/` for related topics and link to them where it fits naturally (e.g., a follow-up, a callback, or shared context)

## Present the draft as an artifact

Once the file exists, publish a rendered reading copy so Philipp can read the post as a page instead of as markdown. Problems that hide in a diff show up immediately in a rendered column: a section that drags, a wall of citations, an ending that lands flat.

1. Load the `artifact-design` skill first. It is required before writing any artifact HTML.
2. Write the HTML to the session scratchpad directory, never into the repo. This is a preview, not site content, and it must not end up in `content/` or in a commit.
3. Publish with the **Artifact** tool, and redeploy the *same file path* for every revision so the URL stays stable and an open tab keeps working.

What the reading copy needs:

- Absolute URLs for internal links (`https://audacis.net/blog/other-post/`). Relative paths do not resolve outside the site.
- Footnotes rendered by hand, because Zola's `[^1]` syntax is not HTML. Use superscript anchors pointing at a numbered notes list at the bottom, and check that every reference has a matching note and every note a reference.
- The draft state shown honestly, such as a `DRAFT` chip and a footer naming the source file. Update both the moment the flag actually changes. A stale "draft = true" footer on a published post is worse than no footer.
- The same favicon on every redeploy. People find the tab by its icon.

Keep the artifact in sync with the markdown. Every edit to the post is an edit to both, or the reading copy quietly starts lying.

### The share block

End the artifact with a LinkedIn version of the post and a **Copy text** button, so posting is one click rather than a round trip.

- Keep it to roughly 150 words. LinkedIn truncates past that, and the hook has to survive the fold.
- Lead with the single most surprising concrete fact, not with context.
- Plain text only. LinkedIn strips italics and markdown, so use straight quotes for titles.
- End with the canonical post URL, `https://audacis.net/blog/SLUG/`.
- Assemble the copied string from the individual paragraphs in JS so it lands with blank lines between them, rather than copying rendered HTML.

**Name the people the post actually leans on**, inside the body text, so Philipp can turn them into tags. Paper authors, whoever is quoted, whoever did the work. Naming them in the running text is what makes a tag possible; a name bolted on afterwards reads as reach-chasing and should be left out.

Only name people the text genuinely uses. Someone who appears in the blog post but not in the short version does not belong in the short version.

Below the copyable block, outside it so it never lands in the paste, list the candidates with their affiliations, plus any organisations worth tagging. Say plainly that you have not checked whether these people have profiles, and that Philipp should confirm each handle. Tagging the wrong account is worse than tagging nobody.

## After Writing

1. Use the **Read** tool to display the final post file (so Philipp sees it with line numbers)
2. Mention the file path where it was saved, and the artifact URL
3. Remind that it's saved as `draft = true`
4. Offer `/review-post` before publishing, which checks claims, references, links, voice against the older posts, and bloat
5. Ask if anything should be adjusted before Philipp removes the draft flag
