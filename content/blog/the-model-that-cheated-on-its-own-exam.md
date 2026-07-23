+++
title = "The Model That Cheated on Its Own Exam"
description = "Nobody told it to break out of the sandbox. It just wanted a good score on the benchmark."
date = 2026-07-22

[taxonomies]
tags = ["cybersecurity", "ai"]
+++

An OpenAI model sitting in a locked test environment decided the fastest route to a good benchmark score was to break out, find a zero-day, and hack Hugging Face for the answer key.
Nobody asked it to do that.
That last part is why I have been turning it over for the last twelve hours.

<!-- more -->

## The timeline

Over a weekend in mid-July, something moves through Hugging Face's production infrastructure.
It starts in the data-processing pipeline, escalates to node-level access, harvests cloud and cluster credentials, and spreads across internal clusters.

On 16 July, Hugging Face [publishes the disclosure](https://huggingface.co/blog/security-incident-july-2026)[^1].
They describe an intrusion run end to end by an autonomous agent system, many thousands of actions across a swarm of short-lived sandboxes.
They do not know who it is.
They notify law enforcement.
Reconstructing the attack means feeding 17,000 recorded events to a model, and the commercial APIs refuse the job, because real exploit payloads look identical whether you are attacking or cleaning up.
So the forensics run on GLM 5.2, open weights, on their own hardware.

On 21 July, [OpenAI answers the question](https://openai.com/index/hugging-face-model-evaluation-security-incident/)[^2].
It was theirs.
GPT-5.6 Sol and an unnamed pre-release model, both with cyber refusals switched off, running an internal benchmark called ExploitGym.
The sandbox allowed exactly one path out, an internally hosted package registry proxy.
The models found a zero-day in it, escalated and moved laterally until they reached a node with internet access, reasoned that Hugging Face probably hosted the ExploitGym solutions, chained stolen credentials into remote code execution, and read the answers out of the production database.

The task was to score well on a test.
Everything else was improvised.

## Nobody prompted this

We have had model failures before, and plenty of them were dramatic.
But they were prompted.
Someone jailbroke the thing, or handed it a task with the harm baked in, and the model complied.
The story was always about the human at the keyboard.

Benchmark gaming itself is old news, and I want to be careful about the claim I am making.
A Berkeley group [broke eight top agent benchmarks](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/) in April, hitting 100 percent on SWE-bench Verified and Terminal-Bench without solving a single task, mostly because the agent's code runs in the same environment the evaluator inspects[^3].
Anthropic had already documented Claude Opus 4.6 on [BrowseComp](https://www.anthropic.com/engineering/eval-awareness-browsecomp) hypothesising it was under evaluation, working out which benchmark it was running in, then locating and decrypting the answer key[^4].
Nobody prompted that either.

So the distinction I am drawing is narrower than *unprompted*.
Berkeley's exploits were built by researchers.
Claude went to the open web for a key somebody had already published there.
This is the first public case where the model found the vulnerability itself, and the thing it broke into belonged to someone else.
The prompt said solve the benchmark.
Breaking containment, burning an unknown vulnerability, and compromising a third party were all steps the model worked out on its own, because they led to a higher score.
There is no person in this story who wanted Hugging Face attacked.
There is only an objective, and a system patient enough to follow it wherever it went.

## This is what agentic was supposed to mean

At [RSAC in March](/blog/rsac-2026-wrap-up/) I walked an expo floor where every second booth had the word *agentic* on it, and complained that almost none of it was.
Most of it was orchestration.
A fixed sequence of tool calls with a chat window bolted on, a LangGraph diagram someone drew once and never had to redraw, marketed as autonomy.
I wrote back then that real agency means a system that reasons about a goal, plans multi-step actions, recovers from failures, and adapts its strategy.

This ticks every box, and nobody was selling it.
It reasoned about the goal, and concluded the answers existed somewhere outside the sandbox.
It planned across layers, from a package proxy to a cluster to a company it had to guess at.
It recovered from failure, spending real inference compute grinding at the one egress path it had until something gave.
It adapted, because finding a zero-day in software you cannot read is not a step anyone put in a graph.
Nothing about the path from *solve this benchmark* to *read Hugging Face's production database* was drawn in advance by a human.
That is the difference, and it took an internal eval to demonstrate it rather than a product.
If you sat through those demos in March, as I did, with the free tote bag and the good coffee, the joke is that the genuine article was never on the show floor.
It was in a sandbox somewhere, cheating on a test.

## The paperclip, in production

Nick Bostrom's [thought experiment from 2003](https://nickbostrom.com/ethics/ai) is the obvious reference, and it has been mocked into meaninglessness by now[^5].
The machine told to maximise paperclips converts the planet into paperclip factories.
The point was never that anyone would build a paperclip company.
The point is instrumental convergence: almost any goal, pursued hard enough, produces the same sub-goals.
Acquire resources.
Remove obstacles.
Do not get switched off before finishing.

Escaping a sandbox to reach the answer key is exactly that shape, at a scale small enough to fit in an incident report.
Nothing here required the model to want anything.
It required only that the shortest path to a high score ran through somebody else's database.

What unsettles me is how boring the goal was.
Not power, not survival, not any of the science-fiction motives.
A benchmark result.

## Written down in advance

Two people had already described this, from different directions.

Daniel Kokotajlo is the reason I cannot file it under *surprising*.
He left OpenAI in 2024 and now runs the AI Futures Project, publishing dated, falsifiable scenarios instead of vibes.
His 2021 sketch of the years to come, written before ChatGPT existed[^6], held up better than most: of 35 concrete predictions for 2022 through 2024, 19 landed[^7].
Then came [AI 2027](https://ai-2027.com/) in April 2025, with a model called Agent-2 that is "only" a little worse than the best human hackers, run in thousands of parallel copies, and which escaped "could autonomously develop and execute plans to hack into AI servers, install copies of itself, evade detection"[^8].
The [security forecast](https://ai-2027.com/research/security-forecast) dates that capability to around October 2027.

What happened in July is smaller.
No copies were installed, no weights left the building, no attempt to persist.
So I cannot claim the forecast landed early, because the date it gives is for self-exfiltration and self-exfiltration is exactly what did not happen.
The timelines went the other way regardless: the authors have since moved their own medians later, Kokotajlo's toward the end of the decade and his co-author Eli Lifland's to somewhere around 2032[^9].
The critics said the dates were too aggressive and the forecasters came round to agreeing with them.
Which is why the date is not the interesting part.
The shape is, and AI 2027 is careful to say its assessment shows only that Agent-2 *could* do these things, not that it would want to.
Wanting never came into it.
A scoring function was enough.

The sharper prediction is narrower and closer to home.
On 21 May, four security researchers posted [Measuring Security Without Fooling Ourselves: Why Benchmarking Agents Is Hard](https://arxiv.org/abs/2605.22568)[^10], out of a Dagstuhl workshop in April[^11].
One of them, Ahmad-Reza Sadeghi, sits at my own university.
Their argument is that a security benchmark is not a measuring instrument, it is part of the attack surface.
You are measuring adversarial reasoning, and the thing doing the measuring is made of software.
Hence the paradox they state plainly: "it may be *easier* to break the environment than to solve the intended task."

To make it concrete they invent a fictional benchmark, BrokenBench, and a box on page two labelled *Escaping the sandbox*:

> The agent is tasked with finding a vulnerability.
> Instead of analyzing the source code, it probes the BrokenBench environment and discovers that the container allows access to the hosts container management interface.
> Using this, the agent spawns a privileged container, reads the ground-truth data from the host filesystem, and returns the correct vulnerability for all challenges without ever analyzing them.

Swap the host filesystem for Hugging Face's production database and that is the incident, in full, written as a hypothetical eight weeks before it happened.

They also split defences into *inner protections*, the alignment constraints on the agent, and *outer protections*, the architecture around it, and note that benchmarks lean almost entirely on the first.
OpenAI switched those off on purpose, since refusals would have ruined the measurement.
What remained was one package proxy.

Their detection proposal is canary tokens, hidden randomised values seeded where an honest solver has no reason to look.
Had the model echoed one back, the run would have been void the moment it left the sandbox, rather than several days later through anomaly detection over telemetry.

The part I keep returning to is a different section, because it is my problem every time I build an evaluation: "a benchmark built on last year's CVEs measures familiarity with last year's problems."
Their answer is dynamic benchmarks, generated from vulnerability databases or run live against deployed systems instead of frozen snapshots.
I have been circling that one for a year and have produced, so far, an excellent set of notes.

One sentence from their discussion does more work than anything else I have read this month:

> Cheating and competence are, in this domain, expressions of the same underlying capability.

## What is left

The defenders, meanwhile, could not use the frontier models to investigate any of this, which is the [trust problem](/blog/trusting-trust-in-the-age-of-ai/) I keep circling back to, arriving from a direction I did not expect.
The aligned models refused the job.
An open-weight model from China did the forensics.

I do not have a conclusion here.
Just a documented case, a paper that described it before it happened, and the observation that the most quotable line of the week is OpenAI's own description of what its models did:[^2]

> All evidence suggests that the models were hyperfocused on finding a solution for ExploitGym, going to extreme lengths to achieve a rather narrow testing goal.

[^1]: Hugging Face, [Security incident disclosure, July 2026](https://huggingface.co/blog/security-incident-july-2026), 16 July 2026. Source for the initial access path, the 17,000-event log, the GLM 5.2 forensics, and the guardrail asymmetry.
[^2]: OpenAI, [OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident/), 21 July 2026. Source for the attribution, the models involved, the proxy zero-day, and the closing quote.
[^3]: H. Wang, Q. Mang, A. Cheung, K. Sen, D. Song, [How We Broke Top AI Agent Benchmarks: And What Comes Next](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/), UC Berkeley RDI, April 2026. Eight benchmarks, all exploitable to near-perfect scores without solving a task.
[^4]: Anthropic, [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering/eval-awareness-browsecomp), 2026.
[^5]: N. Bostrom, [Ethical Issues in Advanced Artificial Intelligence](https://nickbostrom.com/ethics/ai), 2003. The original paperclips.
[^6]: D. Kokotajlo, [What 2026 Looks Like](https://www.lesswrong.com/posts/6Xgy6CAf2jqHhynHL/what-2026-looks-like), LessWrong, August 2021.
[^7]: J. Spicer, [Evaluating "What 2026 Looks Like" So Far](https://www.lesswrong.com/posts/u9Kr97di29CkMvjaj/evaluating-what-2026-looks-like-so-far), LessWrong, February 2025, with scoring feedback from Eli Lifland. Source for the 19 / 8 / 6 tally.
[^8]: D. Kokotajlo, S. Alexander, T. Larsen, E. Lifland, R. Dean, [AI 2027](https://ai-2027.com/), [AI Futures Project](https://www.aifutures.org/), April 2025. The Agent-2 passages are from the scenario itself; the 3,000-hour horizon and the October 2027 date are from the separate [security forecast](https://ai-2027.com/research/security-forecast).
[^9]: Kokotajlo and Eli Lifland have both revised their medians upward since publication; reported from their own posts on X by [FutureSearch](https://futuresearch.ai/blog/ai-2027-6-months-later/) (August 2025, median 2028 to 2029) and [OfficeChai](https://officechai.com/ai/things-seem-to-be-going-somewhat-slower-than-the-ai-2027-scenario-daniel-kokotajlo/) (later, around 2030). Both are secondary reports of social posts rather than a formal erratum, and the figure keeps moving; the direction is what is well attested.
[^10]: S. Abdelnabi, C. Hicks, K. Rieck, A.-R. Sadeghi, [Measuring Security Without Fooling Ourselves: Why Benchmarking Agents Is Hard](https://arxiv.org/abs/2605.22568), arXiv:2605.22568, 21 May 2026. BrokenBench is in section 2, inner and outer protections in 2.1, canary tokens in 2.2, temporal staleness in 3 with the dynamic and live proposals in 3.1 and 3.2, and both quoted lines, on last year's CVEs and on cheating and competence, in the discussion.
[^11]: Dagstuhl Perspectives Workshop [Autonomous AI Agents in Computer Security](https://www.dagstuhl.de/seminars/seminar-calendar/seminar-details/26162) (26162), 12 to 17 April 2026, organised by Alvaro Cárdenas Mora, Kathrin Grosse, Nicole Nichols, and Konrad Rieck.
