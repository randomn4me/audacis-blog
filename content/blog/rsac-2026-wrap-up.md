+++
title = "RSAC 2026: What a Researcher Sees When 45,000 Practitioners Gather"
date = 2026-03-27
description = "My first RSA Conference, the agentic AI reality check, and what San Francisco teaches you beyond cybersecurity."

[taxonomies]
tags = ["cybersecurity", "rsac", "cti", "travel"]
+++

I study cyber threat intelligence for a living. I build language models that parse advisories, design knowledge graphs that map vulnerability ecosystems, and write papers about automating what analysts do manually today. Until this week, I had never been to RSA Conference.

That gap matters more than I realized.

## The Research Bubble Is Real

Academic cybersecurity lives in a world of controlled experiments, benchmark datasets, and double-blind reviews. RSAC is the opposite. It is loud, commercial, and driven by problems that do not wait for publication cycles. And that contrast is exactly why every PhD student working in applied security should find a way to attend a major industry conference at least once during their doctoral journey.

The conversations I had this week did not just validate research directions. They recalibrated them. Talking to CSIRT leads, CTI analysts, and platform engineers surfaces constraints and priorities that no literature review can fully capture. Networking is not a side activity of the PhD. It is a core method for understanding whether the problems you are solving actually matter to the people who would use your solutions.

## San Francisco, All of It

<!-- TODO: Add Golden Gate Bridge photo -->

It does not hurt that the setting is spectacular. Walking from Moscone Center along the Embarcadero after a full day of booth conversations and keynotes, with the Bay Bridge lit up ahead, makes the intensity of the conference feel less like exhaustion and more like momentum.

<!-- TODO: Add downtown SF photo -->

But San Francisco also does not let you look away from the harder parts. My hotel sat right on the edge of the Tenderloin, and the walk between there and Moscone was a daily reminder of how extreme the contrasts in this city are. Within a few blocks you move from open drug use and people sleeping on the sidewalk to billion-dollar startup offices and conference venues where the future of cybersecurity is being discussed over $18 coffees. That juxtaposition is jarring, and it stays with you. It is difficult to talk about innovation and progress all day without also noticing who is being left behind just outside the door.

<!-- TODO: Add Twin Peaks photo(s) -->

The views from Twin Peaks, the Golden Gate Bridge in the fog, the food, the energy of the city: San Francisco is genuinely beautiful. And it is also a place that forces you to sit with uncomfortable questions. Both things are true at the same time, and I think that honesty is part of what makes the city memorable beyond just the conference.

I will definitely come back another time to explore the Bay Area properly. A week packed with conference obligations barely scratches the surface. The coast, the national parks, the towns across the bridge: there is a lot left to see, and I want to see it without a lanyard around my neck.

## The Agentic AI Gap, Seen From the Research Side

Every second booth at RSAC 2026 carried the "agentic AI" label. As someone who works on agentic architectures professionally, I found the floor both encouraging and sobering. Encouraging because the industry clearly sees where things are heading. Sobering because most of what I saw was closer to orchestration than agency.

Many products wrap a sequence of tool calls in a chat interface and call it agentic. From a research standpoint, that is roughly equivalent to a fixed pipeline with a natural language frontend. True agentic behavior, where a system reasons about goals, plans multi-step actions, recovers from failures, and adapts its strategy, remains rare in production. The gap is not surprising. Reliable autonomy in adversarial domains is genuinely hard, and security is one of the most unforgiving environments to get it wrong.

But the direction is right. The demand signal from practitioners is unmistakable: they want systems that think, not just systems that chain. That is a research opportunity as much as a product opportunity, and it reinforced my conviction that the work we are doing at [Serify](https://serify.eu) sits at the right intersection.

## Intelligence Is Converging

The other signal that came through clearly: CTI is shifting from proprietary silos toward collaborative, telemetry-driven models. Vendors are sharing enrichment data, building on each other's scoring, and contributing detection telemetry back into shared pools. For someone who has spent years working on structured intelligence extraction and knowledge graph construction, this trend is significant. It means the bottleneck is moving from data access to data synthesis, which is precisely the problem that graph-based correlation and domain-adapted NLP were designed to address.

## What I Am Taking Home

I came to San Francisco to learn, to connect, and to pressure-test whether the thing we are building at Serify solves a problem the market actually feels. All three happened. The European CTI community showed up with substance and ambition, and some of the most promising collaboration opportunities came from conversations with fellow European teams.

But the deeper takeaway is personal. Doing a PhD in applied security without engaging the practitioner community is like training a model without evaluation data. You might produce something technically sound, but you will not know if it generalizes. RSAC made that lesson unavoidable, and I am glad it did.
