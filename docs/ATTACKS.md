# Attack Scenarios

The attacks in this package consist of *path manipulations* and *route leaks*.
Importantly, every attack scenario here uses announcements that pass Route
Origin Validation (ROV) and therefore require additional defenses to detect and
prevent.

A general description of each attack type is provided below.

###Origin Hijack

An Origin Hijack is the simplest kind of attack which is ROV-valid. The
attacker fabricates an AS path that shows its rogue AS as a neighbor of the
legitimate origin and announces this to all providers.

###Accidental Leak

This scenario simulates more of a misconfiguration than an attack. The attacker
controls a single rogue AS which "accidentally" changes its export policy for
an announcement received from its provider. The announcement is sent without
malicious modification to the other providers of the rogue AS.

###Shortest-Path Export-All

This attack strategy is defined in [this paper](https://www.cs.princeton.edu/~jrex/papers/secure-bgp10.pdf) as 

> Announce to every neighbor, the shortest possible path that is
> not flagged as bogus by the secure routing protocol.

To construct this path, the attacker is given access to a single rogue AS that
they control. The attacker searches through the RIBs_In of this AS to find the
announcement with the shortest possible path it can export to all of its
neighbors. For each path it has received, it will attempt to truncate it as
much as possible while still avoiding detection by the secure routing protocol. 

###Global Eavesdropper

Unlike the scenarios above, a global eavesdropper can access the RIBs_In of
*all* ASes on the internet which are not adopting a defense mechanism. Using
the Shortest-Path Export-All strategy, this generally means the attacker is
able to advertise a shorter path from its rogue AS  which attracts more
traffic.
