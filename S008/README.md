# S008 - Both branches extend the same switch, one of them past the default label

TRAP (semantic): left appends 'case 3' before the default branch, right
appends 'case 6/7' AFTER it. The additions land on different lines, so the merge
is clean and javac accepts it without a warning. The weekend cases now live
below 'default', which most readers assume closes the switch: the behaviour is
correct but the intent is buried, and the classic post-merge "cleanup" that
moves 'default' to the bottom is exactly where the real bug gets introduced.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
