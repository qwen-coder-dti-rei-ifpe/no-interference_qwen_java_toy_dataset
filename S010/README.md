# S010 - A new normalisation rule lands next to the old one it should have replaced

TRAP (semantic): left makes name() trim its argument, right adds a second
entry point normaliseEmail() that lowercases the e-mail - an untouched method
sits between the two hunks, so the merge is trivially clean and compiles. Now
the class exposes email(e) (raw) and normaliseEmail(e) (lowercased) side by
side: callers can pick either, and the "unique e-mail" invariant right branch
intended only holds for whoever calls the new setter. Nothing in the diff tells
the responsible that these two setters were supposed to be one, nor that the
combined identity rule ("trim + lowercase") has never been tested.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
