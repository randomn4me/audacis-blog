+++
title = "Trusting Trust in the Age of AI"
description = "Ken Thompson's poisoned compiler, forty years on, has the same shape as the AI we are learning to trust."
date = 2026-06-25

[taxonomies]
tags = ["cybersecurity", "ai"]
+++

At a [workshop in Singapore](/blog/singapore-and-the-air-conditioned-city/) the liveliest stretch was about international law and trust: when you can trust a system, and whether trust is even possible at a given level.
That pulled me back to a 1984 paper, and the more I sat with it the more it read like a description of the AI we are building now.

<!-- more -->

## The 1984 argument

The paper is Ken Thompson's [Reflections on Trusting Trust](https://dl.acm.org/doi/10.1145/358198.358210), his Turing Award lecture.
The argument is short and brutal.
You cannot fully trust code you did not write yourself, because the compiler that built it could have been compromised in a way no amount of source review will catch.
Thompson showed you can rig a compiler to insert a backdoor, have it reinsert that same rule when it compiles future versions of itself, and then strip the evidence from the source.
The clean source compiles to a dirty binary, forever, and nothing you can read tells you so.
Trust is not a property you verify once and keep.
It is a chain, and every link is someone else's assumption.

The parallels to today's AI are almost too clean.
Thompson worried about a poisoned compiler.
We now have data poisoning at the training set, a training process no outside party can audit, an inference step shaped by system prompts the user never sees, and the model output itself, which you take on faith.
Each of those is a link, and each is opaque to the person relying on it.

## The Fable case

The timing made the example sharper.
Two weeks after the workshop, Anthropic was caught having shipped a Claude policy that [silently degraded its own answers](https://fortune.com/2026/06/10/anthropic-accu-claude-fable-5-limits-capabilities-ai-researchers-developers/) for users whose work looked like frontier AI development, the kind of work that competes with Anthropic's own.
No error, no refusal, just quietly worse output, on a sliver of traffic the company later put at 0.03 percent.
The [r/MachineLearning discussion](https://www.reddit.com/r/MachineLearning/comments/1u23f8p/anthropics_new_model_fable_will_silently_handicap/) where it broke keeps circling one conclusion: if you cannot see the system prompt or the weights, you cannot verify the output, so open weights are the only escape from having to trust the lab.
The sharper worry in the thread is the false positive, because a silent degradation does not announce itself, and legitimate work that merely looks like frontier development gets quietly worse with no way to tell.

When the filter is loud, you at least see it: a medical physicist [on Hacker News](https://news.ycombinator.com/item?id=48473302) had legitimate MRI and nuclear-spin work refused as a policy violation, and support told them they had hit the "nuclear filter," tough luck.
Fable's intervention is that same impulse with the lights off.
Anthropic reversed it after the backlash and apologized, but the shape is what matters: it shipped, no user could have detected it, and it lived below the layer anyone outside the company could inspect.
Strictly, this is the weaker cousin of Thompson's claim.
He showed that source you can read still cannot be trusted; a closed model is unverifiable for the duller reason that you cannot see inside it at all.
The cleaner match comes later, in the weights.

## On the podcast

The security podcast Three Buddy Problem spent [an episode on the Fable mess](https://securityconversations.fireside.fm/mythos-fable-anthropic-big-trust-problem), and the hosts kept rebuilding Thompson's argument without ever naming him.
Ryan Naraine put the trust problem in one sentence: "if you can refuse to tell the user that you switched the behavior, how do we trust that whatever results we get are accurate?"
He reached for a microscope to make it concrete. "Imagine buying a microscope, looking at something, and it's all blurry. You're going to distrust what you're seeing."
A blurry microscope at least tells on itself.
The Fable case is a microscope that quietly halves its own resolution and reports nothing.
One of them landed the line the others seized on: it is not guardrailing, it is gatekeeping.

And then Juan Andres Guerrero-Saade, talking about vulnerability research, walked into the same gap: the open question of "whether there's perfect equivalence between what you can discover as vulnerabilities from a compiled binary versus from source code, which itself is a discussion about vulnerabilities introduced by compilers and optimizations."
The source you can read is not always the artifact that runs.
That is the same gap Thompson opened in 1984, reached for by people who work the problem daily and did not need the citation.
The same episode kept circling back to open weights, with Guerrero-Saade rooting for Mythos-class capability to become public and noting that what the labs actually guard is the reasoning trace, the step you cannot inspect or distill.
The same conclusion as the Reddit thread, from the other side of the table: if you cannot see the trace or the weights, you trust the lab or you leave.

## The same idea in the field

The cleaner illustration is older and physical, and [WIRED reported it in detail](https://www.wired.com/story/fast16-malware-stuxnet-precursor-iran-nuclear-attack/).
A piece of sabotage malware called Fast16, decoded earlier this year by SentinelOne's Vitaly Kamluk and Juan Andres Guerrero-Saade, the same Guerrero-Saade from the Fable episode.
The code dates to 2005, which makes it a precursor to Stuxnet by the researchers' reckoning, and it was likely built by the United States or an ally.
It did not destroy anything.
It corrupted the math.
Fast16 sat below the simulation software that engineers and physicists relied on, LS-DYNA among the candidates, the kind of tool Iranian nuclear research is documented to have used, and "silently altered the calculations the software is running to imperceptibly corrupt its results."
Not crashes.
Drift.
Kamluk's description was "slight alterations to these calculations so that they lead to failures," subtle enough that "systems might wear out faster, collapse, or crash, and scientific research could yield incorrect conclusions." His word for it was "a nightmare."
What makes it Thompson rather than ordinary malware is what it does to verification.
The obvious defense is to recompute on a second machine and compare.
Fast16 spreads as a worm, which the researchers read as the point: "when a victim double-checks their calculation or simulation results with a different computer in the same lab, that machine, too, will confirm the erroneous result."
You cannot verify your way out by comparison, because the machine you would check against is poisoned too.
That is the trap in its purest form.

The AI turn is already inside the story.
Kamluk only cracked Fast16 while testing his own skills against AI reverse-engineering tools.
Five different top AI tools looked at the same driver and confidently called it a rootkit.
It was not.
The tool you would reach for to check the tool gave the wrong answer without hesitating, which is the whole problem one level up.

The victims, meanwhile, blame themselves.
A poisoned simulation does not announce itself, so the scientist assumes the mistake is theirs.
That is the false positive from the Fable thread wearing different clothes.
The medical physicist who got refused assumed they had hit a policy.
The scientist running corrupted numbers assumes they fumbled the model.
In both cases the first trust to break is trust in yourself.

Thomas Rid, who studies this history, drew the conclusion that should sit with anyone: a high-value target "can't trust your computers. And even worse: you could never trust them."
Not cannot trust them now.
Could never have.
The doubt runs backward through everything already computed.

## The narrow exit

Thompson's trap has an exit, worth knowing precisely because of how narrow it is.
You cannot read your way out, but you can sometimes reproduce your way out.
[Diverse double-compiling](https://dwheeler.com/trusting-trust/), the method David A. Wheeler worked out, uses a second, independent compiler to rebuild the compiler from its own source, then checks that the suspect compiler reproduces itself bit for bit. A Thompson backdoor that lives in the binary but not the source breaks that self-reproduction.
The [Reproducible Builds](https://reproducible-builds.org/) project is the everyday version of the same instinct, though it secures a different link: it makes builds deterministic so anyone can confirm a binary matches its source, on the assumption that the compiler itself is honest.
An independent compiler and a reproducible path together are roughly what it takes to trust a binary you did not write.
The escape is not inspection.
It is independent reproduction, and it holds only while the second path stays independent.
Which is what Fast16 took away.
The worm spread so the second machine was no longer independent, and the recomputation that should have caught the drift confirmed it instead.

The question I keep circling is whether weights have anything like this, and as far as I can tell they do not.
Open weights solve the Fable link.
Hold the artifact and the lab cannot silently switch it, cannot hide a system prompt, cannot run one model for you and a different one for the next user.
But open weights do not touch the link shaped like Thompson's compiler, which is the data.
A model can be trained on a poisoned set so that it behaves until a trigger appears, and the safety training meant to scrub that behavior does not remove it.
Anthropic's own ["sleeper agents" work](https://arxiv.org/abs/2401.05566) built exactly this: models that wrote clean code until a trigger flipped them, persisting through supervised fine-tuning, reinforcement learning, even adversarial training, which mostly taught them to hide the trigger better.
The poison rides in the data. The released weights look clean.
You can read every number and have no reliable way to find it, the same way you can read clean compiler source and never see the backdoor it carries.
And there is no diverse-double-anything to fall back on.
Reproduction saved the compiler because you could swap in an independent toolchain and demand the same binary.
There is no independent retraining: an honest rerun on the same data reproduces the same poison, and a rerun on different data is a different model, not a check on this one.
The verification primitive that rescues binaries has no analog for weights.

Pull the thread to where adversaries have to trust each other and it gets worse.
Verification between states is built on reproduction: count the centrifuges, sample the air, rerun the measurement and compare.
AI offers no such step, and the conflict-analysis and early-warning systems people want to build sit on exactly the models that lack it, at exactly the moments, escalation and attribution, when being quietly wrong is worst.

---

Thompson's poisoned compiler was a thought experiment in 1984.
Fast16 was the same idea in the field, aimed, most likely, at a nuclear program, before most people had heard of Stuxnet.
A model that quietly downgrades your work is the same idea again, aimed at whoever a policy decides looks too much like competition.
Kamluk and Guerrero-Saade presented the Fast16 work at Black Hat Asia in Singapore, the same city where this started for me. The layer you cannot inspect keeps climbing the stack.
