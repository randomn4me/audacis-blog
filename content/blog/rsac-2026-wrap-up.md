+++
title = "RSAC 2026: What a Researcher Sees When 45,000 Practitioners Gather"
date = 2026-03-27
description = "My first RSA Conference, the agentic AI reality check, and why every PhD student in applied security should attend at least once."

[taxonomies]
tags = ["cybersecurity", "rsac", "cti"]
+++

I study cyber threat intelligence for a living.
I build language models that parse advisories, design knowledge graphs that map vulnerability ecosystems, and write papers about automating what analysts do manually today.
Until this week, I had never been to RSA Conference.

That gap matters more than I realized.

## The Research Bubble Is Real

Academic cybersecurity lives in a world of controlled experiments, benchmark datasets, and double-blind reviews.
RSAC is the opposite.
It is loud, commercial, and driven by problems that do not wait for publication cycles.
And that contrast is exactly why every PhD student working in applied security should find a way to attend a major industry conference at least once during their doctoral journey.

The conversations I had this week did not just validate research directions.
They recalibrated them.
Talking to CSIRT leads, CTI analysts, and platform engineers surfaces constraints and priorities that no literature review can fully capture.
Networking is not a side activity of the PhD.
It is a core method for understanding whether the problems you are solving actually matter to the people who would use your solutions.

## The Agentic AI Gap, Seen From the Research Side

Every second booth at RSAC 2026 carried the *agentic AI* label.
As someone who works on agentic architectures professionally, I found the floor both encouraging and sobering.
Encouraging because the industry clearly sees where things are heading.
Sobering because most of what I saw was closer to orchestration than agency.

Many products wrap a sequence of tool calls in a chat interface and call it agentic.
From a research standpoint, that is roughly equivalent to a fixed pipeline with a natural language frontend.
True agentic behavior, where a system reasons about goals, plans multi-step actions, recovers from failures, and adapts its strategy, remains rare in production.
The gap is not surprising.
Reliable autonomy in adversarial domains is genuinely hard, and security is one of the most unforgiving environments to get it wrong.

But the direction is right.
The demand signal from practitioners is unmistakable: they want systems that think, not just systems that chain.
That is a research opportunity as much as a product opportunity, and it is the kind of gap that [our work at Serify](https://serify.eu) is trying to close.

## Intelligence Is Converging

The other signal that came through clearly: CTI is shifting from proprietary silos toward collaborative, telemetry-driven models.
Vendors are sharing enrichment data, building on each other's scoring, and contributing detection telemetry back into shared pools.
One conversation stuck with me: a threat intel lead at a mid-size MSSP described how their team spends more time deduplicating and reconciling indicators across three vendor feeds than actually analyzing them.
They have the data.
What they lack is a way to correlate it structurally, to see that two advisories describe the same campaign even when the IOCs do not overlap.
That is exactly the kind of problem that knowledge graphs and domain-adapted NLP are built to solve, and hearing it described as a daily operational pain rather than a research hypothesis made it feel a lot more urgent.
I wrote a more detailed take on this trend [from the Serify side](https://serify.eu/news/rsac-2026-intelligence-is-getting-collaborative/).

## What I Am Taking Home

I came to San Francisco to learn, to connect, and to pressure-test whether the thing we are building at Serify solves a problem the market actually feels.
All three happened.
The European CTI community showed up with substance and ambition, and some of the most promising collaboration opportunities came from conversations with fellow European teams.

But the deeper takeaway is personal.
Doing a PhD in applied security without engaging the practitioner community is like training a model without evaluation data.
You might produce something technically sound, but you will not know if it generalizes.
RSAC made that lesson unavoidable, and I am glad it did.

<!-- TODO: add me -->
