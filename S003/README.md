# S003 - Same local identifier 'threshold' for two different limits

TRAP (semantic): each branch adds a method whose body declares a local
variable named 'threshold' holding a different value (80.0 CPU vs 90.0 memory).
Locals live in their own scope, so there is no conflict and no type error - but
in the merged file the two 'threshold's read like one shared setting. The usual
"cleanup" during review (hoist it into a field or a constant) silently changes
one of the two alert levels.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
