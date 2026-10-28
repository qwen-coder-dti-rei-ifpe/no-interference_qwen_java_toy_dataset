# S009 - Extract-method refactor meets a brand-new copy of the extracted logic

TRAP (semantic): left extracts the duplicated tax rate into rate();
right adds surcharge() repeating that very same inline expression. The changes
sit in different regions and share the literal 0.10, so the auto-merge is
flawless and compiles - while silently re-introducing the duplication the
refactor was created to remove. The next rate change updates three methods and
misses surcharge(), and the merge commit shows nothing suspicious.

*Files:* `base.java` (ancestor), `left.java`, `right.java`, `merge.java` (clean automatic merge of both sides, compiles with javac).
