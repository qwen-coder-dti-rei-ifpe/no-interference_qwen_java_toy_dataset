# S004 - One helper name, two responsibilities (date vs money formatting)

TRAP (semantic): left adds format(d, m, y) for dates, right adds
format(value) for money. Overloading makes the merge compile cleanly, yet the
merged class now exposes two unrelated jobs behind one verb. A future call site
written as format(x) reads ambiguously - format(2024.5) prints "$2024.50" while
format(2) does not even compile - and nothing in the merge records that the two
helpers were meant to stay separate.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
