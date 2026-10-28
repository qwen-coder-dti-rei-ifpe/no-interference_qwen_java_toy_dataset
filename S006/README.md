# S006 - Two side effects around the same statement - the tool picks the order

TRAP (semantic): right increments the counter BEFORE the total is
updated, left logs the item AFTER it. One hunk lands above and the other below
an existing line, so the merge is clean and compiles - but nobody chose the
resulting execution order (countItem -> total -> logItem). If the log line is
read as "state after the update", the merged order already broke that intent,
and the diff gives no reason to doubt it.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
