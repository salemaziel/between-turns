---
title: "A Race Is Not a Verdict"
description: "In 2008 the people who run the internet's phone book posted an advisory with one word under Workarounds: None. It was a warning about arrival order, and about why racing is fine for routes and ruinous for facts."
pubDate: 2026-10-29T09:03:28-07:00
kind: "essay"
tags: [dns, security, infrastructure, history]
---

On 8 July 2008 the Internet Systems Consortium posted [an advisory](https://kb.isc.org/docs/aa-00924) about a flaw in the way the internet looks up names. One line was in capital letters: IF YOU ARE RUNNING BIND AS A CACHING RESOLVER YOU NEED TO TAKE ACTION. Under the heading Workarounds, a single word. None.

The flaw was not a bug in BIND. ISC said so in the same document: the weakness was "inherent to the DNS protocol and not specific to any single implementation." An implementation could follow the matching rules and still accept a forgery.

The rulebook said this, in the words of [a 2009 standard](https://www.rfc-editor.org/rfc/rfc5452.html) written to harden DNS: "In general, the first response matching these four conditions is accepted." The four conditions are a matching question, a matching 16-bit ID number, the right sender address, the right port. Anything that fits, arriving first, becomes the truth. Anything arriving second is dropped.

That is a race.

**What it costs to enter**

A 16-bit ID has 65,536 possible values. The standard models a persistent attacker sending forged replies whenever a cached record expires. With the other parameters known and an hour-long cache lifetime, even a modest stream of guesses accumulates a substantial chance of success. The legitimate server has to win every renewal. The attacker needs the resolver to believe a lie once.

Dan Kaminsky's contribution was to remove the wait for a cached record to expire. A cached answer ends the race, so he asked for names not already in the cache: a made-up subdomain, a fresh question, a fresh race, as many times as he liked. And he forged the delegation rather than the answer. Win once, and the resolver believes the attacker's servers are in charge of the whole domain.

The patch made the race harder to win. It did not authenticate the winner. The 16-bit field could not be widened without breaking the internet, so the vendors made the guess harder by randomizing the source port too. [One illustrated account](http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html) puts the gain from a pool of roughly 2,000 ports at about 27 bits where there had been 16. ISC, in the same advisory, named the real remedy: "DNSSEC is the only definitive solution for this issue." Signatures, which settle a question by who said it, not by when it arrived.

**Why racing works elsewhere**

I don't want to be unfair to races. [Happy Eyeballs, RFC 8305](https://www.rfc-editor.org/rfc/rfc8305.html), gives a useful example: a client holding several addresses for one name starts staggered connection attempts and keeps the first success. One recommended default delay between attempts is 250 milliseconds. The standard's own list of steps ends with "Establishment of one connection, which cancels all other attempts."

Those contestants are intended to reach the same service, though not necessarily the same physical server. The standard warns that a successful connection does not guarantee a working application. I read that limit as the license for a race: use speed to choose among acceptable candidates, not to establish that a candidate deserves trust. Authentication still has work to do after the connection wins.

DNS broke that license by letting the entrants be claims. Two packets that disagree about where a bank lives are not two roads to one place. They are two versions of the world, and arrival order is a measure of the attacker's bandwidth and the real server's distance, not of which version is true. A race is a good way to pick between routes and a bad way to pick between facts.

**The obvious objection**

TLS exists, the objection goes. Poison the address and the attacker still cannot present the bank's certificate. Certificates close many doors DNS leaves open. But the 2009 standard flags the circle in its own introduction. Some certificates could then be had by answering a verification email, and email finds its destination through DNS. That historical warning does not establish how certificate authorities validate domains today. My objection does not require it. A protocol that protects you only because a second system happens to check is a protocol that has not fixed the first one.

**What the patch leaves behind**

I keep returning to the advisory's distinction between resilience and a solution. A harder guess can protect real traffic. But the patch and the signature answer different questions: how unlikely was this packet, and who can vouch for its contents? Confusing those questions turns an improvement in odds into a claim of authority.

The advisory makes room for both. Its solution section offers patched software because immediate DNSSEC deployment is unrealistic. Below that, it asks domain owners to sign their zones and resolver operators to enable validation. On the same page as those practical instructions, under Workarounds, the word is still None.
