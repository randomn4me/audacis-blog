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

## After Writing

1. Use the **Read** tool to display the final post file (so Philipp sees it with line numbers)
2. Mention the file path where it was saved
3. Remind that it's saved as `draft = true`
4. Ask if anything should be adjusted before Philipp removes the draft flag
