+++
date = 2025-03-29
title = "Academia wrapped up"
description = "My journey through academia and some lessons learned"
draft = true

[taxonomies]
tags = [ "research", "academia", "writing", "life-lessons", ]
+++

On Wednesday, on 26th March 2025, I successfully defended my dissertation *Proactive Cyber Threat Intelligence: Automating the Intelligence Cycle based on Open Sources*.
With this blog post I wrap up my journey in academia up until now, as my driving force seeks for a different doing right now.
While I still enjoy doing research and exploring new avenues, my current direction seems to shift. But more on that later.
I want to shed some light on this journey up until now, my wins, my regrets, and my learnings for the time to come.
In the end, I will share some thoughts on what I would do differently, when I would start this journey all over again.
So let's get started.

{{ toc() }}

## Academia -- A Journey unfolds

After school, I knew I wanted to do something with computers, as I always had an interest in how these things actually worked, but my parents focused more on *get them working* in form of IT support.
In this kind of field, I never had any interest.
I saw, that you might do some bucks there as well, but my sole interest lay deeper in these devices than just piece them together and get them running.

So I applied for Computer Science course of nearest, best-rated University to my hometown, the Technical University of Darmstadt.
Up until then, I didn't even know the difference between a University and a University for Applied Sciences.
Shortly after, I received the positive response and entered my first term as freshman in October 2012.

While I was fascinated about scientists in my teenage years, I never dreamt of becoming one myself.
But as the time went on, and the terms passed, I got more and more involved with the process of learning new stuff and reading scientific literature, that my curiosity grew and grew.
Meanwhile, I was hooked by using my Linux powered Thinkpad L430 as my daily driver and tinkered with it nearly every day[^1].

## My first Contacts with Research

In my 7th term, I attended a seminar course, which had the goal to write a short paper about the concept of [Homomorphic Encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption) (HE) and how it works.
It introduced, very broadly, into the concepts of finding related papers and the writing process.
And during my research of related papers, I noticed some strange papers, e.g., a spam detection paper which leverages Homomorphic Encryption to detect spam[^2].
On the surface, not surprising, but getting into the gist of the paper revealed, that the paper included just that information.
The authors introduced into HE, stepped over related work in their area, defined the methodology, which contained a sentence like 'Let $spam(m)$ be a predicate, which states, whether message $m$ is a spam message within a HE system', and went on with discussion, and conclusion.
Never in the paper did they explain this specific function, which implementation of HE they used, stated any evaluation of their system, none.
In my novice eyes, it seemed like to total disaster, that a paper like this got published as it contained no novel information.
'Wow, you used HE to apply a function to your encrypted piece of data and called it a paper'.
I was simply shocked.

In the same term I wrote my Bachelor's thesis at the same chair, where I was guided by my Supervisor [Robert Künnemann](https://www.kunnemann.de/) through the process of working scientifically in more detail and with more Tips and Best Practices.
He also introduced me to different areas like the writing process of scientific writing with the *[The Elements of Style](https://en.wikipedia.org/wiki/The_Elements_of_Style)* by Strunk & White, [LaTeX](https://en.wikipedia.org/wiki/LaTeX), and task management tools, something I dismissed that time, but proves to be valuable long after, [Getting Things Done](https://en.wikipedia.org/wiki/Getting_Things_Done) and [taskwarrior](https://taskwarrior.org/) as underlying application.
This led to some deep dives into data obfuscation and exploitation of CalDAV to hide data within, and was one of the first real moments where I realized, that I actually liked working this way.
Combining different concepts, coming up with creative ideas[^3], and solving problems not thought of up until now.
And first and foremost, doing what currently drives your interest, diving deep into the topic, turning every breadcrumb for more information, and getting paid for that (first in credits and later in cash).

Afterward, I started my Master's in Information Security (same university) in 2016 to dive deeper into this topic and deeper into the science rabbit hole.
This fostered my understanding of various novel topics, more Crypto, and the theoretical side of information security.
In the second last term I got in touch with my going-to-be employer [PEASEC] in their lecture presenting practical appliances between the fields information security, arms control, and peace building.
This led to my Master's thesis, which I started mid 2019 and got published later during my job under the title [*ExTRUST: Reducing Exploit Stockpiles With a Privacy-Preserving Depletion System for Inter-State Relationships*](https://ieeexplore.ieee.org/document/10138062).

The contact with [PEASEC] showed me more of what is available in the intersecting fields with computer science.
Up until then I knew of foundational research topics like algorithms, databases, machine learning, security, theoretical computer science, and the like.
But I never thought about topics like human-computer interaction, crisis informatics, misinformation detection, or dual-use.



[^1]: I used Arch btw.
[^2]: I am unable to access the records of my Bachelor terms and the seminars work as well, so I sadly cannot reference the mentioned paper.
[^3]: At that time I used hashes to detect changes in the underlying data structure. As my data was sent in chunks, I came up with the idea to store all data within a tree, and hash the whole tree starting at the parents of the leaves and going up the tree this way. To that, my supervisor said: 'Well done, you reinvented a *Merckel Tree*'. In addition, as I stored transaction, which store a time series of events, I combined the hash information of the current tree, with the previous one, to easily detect, whether a malicious source changed previous information. To that idea my supervisor replied: 'And now you have something like a blockchain.' So sometimes the ideas your come up with aren't new, but you use them in creative ways.

[PEASEC]: https://peasec.de
