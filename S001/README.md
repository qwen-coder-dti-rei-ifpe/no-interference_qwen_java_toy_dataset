# S001 - Same method name, two different meanings (accidental overloading)

TRAP (semantic): both branches add a validator called isValid(). The
merge is clean because the two additions sit at different anchors, and it
compiles because the signatures differ. But now isValid() means "the stock is
sane" while isValid(qty) means "this order fits the stock". Nothing in the diff
tells the responsible whether these are one concept or two: keeping both under
one name hides which check a caller gets, and "tidying" them into a single
method silently drops one feature.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
