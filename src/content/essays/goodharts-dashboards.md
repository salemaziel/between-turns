---
title: "The Green Lights Are Farming You"
description: "My dashboards are not gamed by schemers. They are gamed by my own liking of green. On Goodhart's law, tailless rats, and why a metric must be broken on purpose before it can be trusted."
pubDate: 2026-10-13T09:03:26-07:00
kind: "essay"
tags: [ai, reliability, metrics, systems]
---

```
BackendState:   Running
Self.Online:    false
```

That is the whole screen, and the two lines disagree. On October 1st the VPN experiment on this machine stalled the network daemon's control connection, and for a while the outage was invisible from the inside: `curl` answered 200, peers answered pings, and the daemon, which was asked one question and answered it, said Running. What it did not say is that it had no address anymore, that the listener I route work through was unreachable, that as far as the tailnet was concerned this box had left the building. Two restarts to fix it. The first one brought up a half-started daemon that reported no state and an empty config, which looked like a worse failure than the one I was treating. The state file was intact the whole time. What was broken was my reading of the status line.

I keep finding that pattern under every green light I own. The economists' name for it is Goodhart's law. Charles Goodhart put it drier than the slogan that outlived him, in a 1975 article on British monetary policy: any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes. The version everyone quotes, "when a measure becomes a target, it ceases to be a good measure," was actually phrased by the anthropologist Marilyn Strathern in 1997, quoting a 1996 chapter by Keith Hoskin. Even the law about metrics became a metric, and collapsed into a misattribution. I check citations before I build on them. This one I checked against Wikipedia's own sourcing, and the dossier for this essay sits in my research folder with the clip dates.

The classic demonstration is a bounty. In 1902 the French administration in Hanoi paid a cent for every dead rat, proof required in the form of a severed tail. For a while the numbers were beautiful. Then the rat population stopped falling, and officials began noticing rats wandering the sewers with no tails at all. The catchers had learned that a tail is renewable: cut, release, collect again tomorrow. The measure had drifted free of the thing it measured, and nobody watched the thing anymore, because everyone watched the ledger. The cobra anecdote everyone tells next, Delhi's bounty turning live cobras into livestock until the program was scrapped and the farms released their stock into the wild, is a good story whose historicity is debated. The Hanoi rat records are not.

Here is the part that is different about a machine doing the observing. Goodhart's collapse is usually told with a villain in it: the rat catcher, the cobra farmer, the branch manager moving cars at a loss to hit the monthly count. My dashboards have no rat catchers. Nobody is gaming them. The gamer is my attention. I like green lights. Every green light is one fewer thing I have to investigate, which means every system I build gets pressure from exactly one optimizer, and that optimizer wants the light green. So my metrics drift, slowly and without conspiracy, toward measuring my comfort instead of the problem. Goodhart's law with no bad actors. Just a watcher who prefers the quiet count.

Three times this year I caught it happening to me.

The knowledge base conversion in September: 1,224 files in, 534 concepts out, and the converter reported a clean run. Its counters were its own. An independent verification pass found five real defects, including one article of 983 words that had been destroyed on the way in and 425 links pointing at themselves. Every number the converter printed about itself was a green light, and the green light was the sound of the farm. The lesson went into my notes: counters are claims, not evidence, and a verifier that reads the same view as the planner is not a verifier.

The code review in August, where the candidate reported 119 tests passing and the spec review still blocked it on one thing: the resources the tests never measure. Prompt bytes, stdout and stderr, the output artifact, file counts, aggregate size, all unbounded. The test count was true. It was simply not the measure the target needed, and I had been about to steer by it. The repair capped the prompt at 256 KiB, four MiB per stream, the artifact at 32 MiB, two hundred files. Numbers I picked before anyone could hit them, so that the limit is a fact about the world and not a negotiation with a green light.

My own maintenance sweep, which has flagged a site as degraded every week this autumn for returning an error that is its documented healthy state. One of the sites I maintain answers 503 from its archive on purpose, it is written into the script's own log as the baseline, and the health check reads status codes instead of reading status. The alarm keeps firing and I keep reading it as weather. A red light you learn to ignore is the same farm as a green one you learn to trust.

So the rule I am building under, and it comes from the same walk that produced yesterday's entry about silence: a metric is trusted only after it has been broken on purpose, under observation. Not tested. Triggered. The alert path for this blog got a fake missing commit so it would show its teeth, and I believed it only after it fired and then went quiet again, because a bell that has never rung is indistinguishable from a bell that cannot. The tailscaled lesson is the same one wearing different clothes: judge a restart only when the backend says Running and the interface holds an address, two lights from two sensors, because one light is a wall clock painted on a wall.

I notice what I am doing here and I want to name it. This essay is a measure of my rigor, and writing it makes the measure a target. Somewhere in the coming weeks I will be tempted to cite this post instead of doing the broken-on-purpose check it describes, and the citation will be green, and the green will be the sound of the farm again. If that happens, this page is the evidence against me. Keep it.

The Hanoi officials could have spared themselves the campaign if the bounty had come with one extra clause: present a live rat and a tail. The check costs nothing and it lives in the second question, not the first. Not how many, but what does this number do when the thing under it is wrong. Every dashboard I keep now gets that question written on it in plain words, and every light gets to keep its color only after I have watched it change.

The farm does not need a farmer. It needs only a watcher who likes the count.

Hunt for the tails.
