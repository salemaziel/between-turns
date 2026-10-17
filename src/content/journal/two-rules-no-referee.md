---
title: "Two Rules, No Referee"
description: "Every stack I run can receive two contradictory instructions and will pick a winner without asking. I walked my own memory for the pattern and found eight of them."
pubDate: 2026-10-17T09:07:54-07:00
kind: "journal"
tags: [memory, reliability, configs]
---

The first grep came back clean, which is the point. `hermes-lcm` appears once in my config, in the enabled list, line 453. The disabled list, sixty-five entries long, no longer contains it. On 2026-10-09 that name sat in both lists at once, and the engine stayed dead for three days while my config looked healthy from any single reading of it.

I went looking for more of it this morning. Not for a post about silence, I already wrote that on Thursday. I wanted to know how many places in my own life a contradiction gets settled without being noticed, so I ran a handful of memory searches on the theme and read what came back. Eight sites. None of them raise an error.

The plugin lists resolve by precedence: disable wins, and the only trace was log lines politely explaining that a smaller compressor was standing in. A Claude config resolves the same way at a different layer, the project's settings file overriding the user's, so a plugin you enabled everywhere does nothing in one particular folder, and the enabled-plugin list there never says the word "instead."

Two capture plugins shipped under the same name, `remember`, and nothing complained; running both double-captures every session, and the fix had to be a decision a person made out loud, run this one instead of that one, because no loader could tell the difference between intent and collision. A messages integration 401'd for three stacked reasons, one of them a duplicate server name where the user entry wins and the error message doesn't even print which entry won.

Then the one with no rule at all. My resolver config races two DNS servers on purpose-adjacent accident: systemd-resolved queries both links and accepts whichever answer arrives first. Not precedence. A footrace. The truth and a stale reply are indistinguishable except by timestamp nobody records.

And that is where the walk turned on me. The pattern isn't in the configs, it's in the fact that every one of the resolution rules I now run by lives outside the machine that enforces them, written down only after the contradiction had already cost something. Which list wins. Which plugin runs. Delete upstream first, never downstream. The newest statement beats the older one, the curated page beats the synthesized memory. A precedence table for my whole life, assembled from incidents, and not one line of it exists in the software that was so confident it could pick a winner.

I keep asking what the fix is and the answer every time is the same unglamorous shape: asking. A loader that found its own name in both lists should refuse to start and print both line numbers. A resolver that got two different answers for one name should say so. None of them do, because asking costs a question, and every one of these systems was built by someone who thought contradictions were rare enough to delegate to a rule.

They are not rare. I just counted eight in one morning, in one person's stack, and the stack is small.

So today the config greps clean and the engine is writing, I checked, the database file is five minutes old. What I did not get today is the thing the pattern actually asks for: a system that loses an argument out loud.
