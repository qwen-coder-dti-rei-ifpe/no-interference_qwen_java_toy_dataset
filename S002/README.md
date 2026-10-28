# S002 - Two unrelated limits that happen to be named MAX_SIZE

TRAP (semantic): left adds BUFFER_MAX_SIZE = 1024 (bytes per read),
right adds USER_MAX_SIZE = 500 (registered users). Each author first renamed the
tentative "MAX_SIZE" they had on their own branch; the merged file keeps both
constants, compiles, and looks perfectly fine. The hidden decision is that these
two numbers belong to different domains: any later refactor that re-unifies them
under one "MAX_SIZE" (very tempting when reviewing) breaks one of the limits.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
