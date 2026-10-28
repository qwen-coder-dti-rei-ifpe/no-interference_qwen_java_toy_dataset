# S005 - Guard clause added at the top, new behaviour added at the bottom

TRAP (semantic): left inserts an early return for price <= 0, right adds
the big-basket bonus after the discount. The hunks are far apart, so git merges
them happily and the code still compiles. In the merged method the bonus can no
longer be reached for any input the guard intercepts, and neither author ever
tested the combination (apply(-1) = 0, apply(1100) = 995). No line of the diff
reveals that the two blocks interact through the same return path.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
