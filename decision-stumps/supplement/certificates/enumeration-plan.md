# Finite targets selected after pilot

Pilot (one Python process): m=6,d=2, all internal cuts, 3,421
compressed instances, 0.118 s; m=6,d=3, 192,181 instances,
1.395 s; m=6,d=4, 7,380,076 instances, 61.995 s.
Small overhead and exact integers make extending d=2 to m=8 feasible.
The main finite target is m=2..6,d=1..3 in all three distinct-set
conventions (all/no constants, transition/no constants, shared constants),
plus m=7,8,d=1,2. m=7,d=3 is attempted only after the next pilot.
The m=6,d=4 all/no-constants pilot is also a completed exhaustive result.

Independent checking will enumerate raw permutations rather than
deduplicated local antichains. No SAT claim or DRAT certificate is used.
The mathematical bounds and explicit marker construction are the
principal general results; larger tables are secondary.
