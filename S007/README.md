# S007 - Identical field/getter pair duplicated in two classes with different meanings

TRAP (semantic): left gives Feature a flag 'enabled' (default true),
right gives Device a power state 'enabled' (default false). Two disjoint regions,
identical types, zero conflicts. The merged code looks like obvious duplication,
so the reviewer is tempted to factor isEnabled() into a shared parent/interface
or to copy one default into the other - merging a feature toggle with a hardware
switch and flipping the device's initial state.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
