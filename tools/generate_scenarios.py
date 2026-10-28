#!/usr/bin/env python3
"""Generate 10 toy Java merge scenarios (S001..S010).

Layout of every scenario folder:
    base.java   - the common ancestor version
    left.java   - branch A  = base + one independent addition
    right.java  - branch B  = base + another independent addition
    merge.java  - the result of merging left + right
    README.md   - the semantic trap the scenario is built to expose

Guarantees (checked by tools/verify_scenarios.py):
    * each side only ADDS lines, and the two additions fall in DISJOINT regions
      of the file -> `git merge` is always clean: no conflict markers and no
      textual interference between the two changes;
    * merge.java is exactly what the automatic merge produces;
    * base/left/right/merge all compile with javac -> NO type conflicts.

The "trap" in each scenario is purely SEMANTIC: the tool says "merged fine", but
a human decision (naming, ordering, duplication, reachability, invariants) has
been silently taken for you.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A scenario is a list of blocks:
#   "line"                -> present in base, left, right and merge (context)
#   ("L", ["l1", "l2"])   -> added ONLY by the left branch
#   ("R", ["l1", "l2"])   -> added ONLY by the right branch
# Because sides never modify shared lines, their hunks can never interfere.
SCENARIOS = []


def scen(name, title, trap, blocks):
    SCENARIOS.append((name, title, trap, blocks))


# ------------------------------------------------------------------------ S001
scen("S001", "Same method name, two different meanings (accidental overloading)",
     """TRAP (semantic): both branches add a validator called isValid(). The
merge is clean because the two additions sit at different anchors, and it
compiles because the signatures differ. But now isValid() means "the stock is
sane" while isValid(qty) means "this order fits the stock". Nothing in the diff
tells the responsible whether these are one concept or two: keeping both under
one name hides which check a caller gets, and "tidying" them into a single
method silently drops one feature.""",
     [
     "class Inventory {",
     "    private int stock = 0;",
     "",
     "    public void setStock(int s) { this.stock = s; }",
     "    public int getStock() { return stock; }",
     ("R", ["",
            "    // NEW (right): validate that an order quantity fits in stock",
            "    public boolean isValid(int qty) {",
            "        return qty > 0 && qty <= stock;",
            "    }"]),
     ("L", ["",
            "    // NEW (left): validate that the stock itself is not negative",
            "    public boolean isValid() {",
            "        return stock >= 0;",
            "    }"]),
     "}",
     ])

# ------------------------------------------------------------------------ S002
scen("S002", "Two unrelated limits that happen to be named MAX_SIZE",
     """TRAP (semantic): left adds BUFFER_MAX_SIZE = 1024 (bytes per read),
right adds USER_MAX_SIZE = 500 (registered users). Each author first renamed the
tentative "MAX_SIZE" they had on their own branch; the merged file keeps both
constants, compiles, and looks perfectly fine. The hidden decision is that these
two numbers belong to different domains: any later refactor that re-unifies them
under one "MAX_SIZE" (very tempting when reviewing) breaks one of the limits.""",
     [
     "class Config {",
     "    public static final String APP_NAME = \"ToyApp\";",
     ("L", ["    // NEW (left): maximum number of bytes read per buffer",
            "    public static final int BUFFER_MAX_SIZE = 1024;"]),
     "",
     "    public static String describe() {",
     "        return APP_NAME;",
     "    }",
     ("R", ["",
            "    // NEW (right): maximum number of registered users allowed",
            "    public static final int USER_MAX_SIZE = 500;"]),
     "}",
     ])

# ------------------------------------------------------------------------ S003
scen("S003", "Same local identifier 'threshold' for two different limits",
     """TRAP (semantic): each branch adds a method whose body declares a local
variable named 'threshold' holding a different value (80.0 CPU vs 90.0 memory).
Locals live in their own scope, so there is no conflict and no type error - but
in the merged file the two 'threshold's read like one shared setting. The usual
"cleanup" during review (hoist it into a field or a constant) silently changes
one of the two alert levels.""",
     [
     "class Monitor {",
     "    public double average(double[] v) {",
     "        double sum = 0;",
     "        for (double x : v) sum += x;",
     "        return sum / v.length;",
     "    }",
     ("L", ["",
            "    // NEW (left): alert when the average CPU load is too high",
            "    public boolean cpuAlert(double[] loads) {",
            "        double threshold = 80.0;",
            "        return average(loads) > threshold;",
            "    }"]),
     ("R", ["",
            "    // NEW (right): alert when the average memory usage is too high",
            "    public boolean memAlert(double[] usage) {",
            "        double threshold = 90.0;",
            "        return average(usage) > threshold;",
            "    }"]),
     "}",
     ])

# ------------------------------------------------------------------------ S004
scen("S004", "One helper name, two responsibilities (date vs money formatting)",
     """TRAP (semantic): left adds format(d, m, y) for dates, right adds
format(value) for money. Overloading makes the merge compile cleanly, yet the
merged class now exposes two unrelated jobs behind one verb. A future call site
written as format(x) reads ambiguously - format(2024.5) prints "$2024.50" while
format(2) does not even compile - and nothing in the merge records that the two
helpers were meant to stay separate.""",
     [
     "class Report {",
     "    public String title() {",
     "        return \"Quarterly report\";",
     "    }",
     ("R", ["",
            "    // NEW (right): format an amount with a currency symbol",
            "    public String format(double value) {",
            "        return \"$\" + String.format(\"%.2f\", value);",
            "    }"]),
     ("L", ["",
            "    // NEW (left): format a day/month/year date",
            "    public String format(int d, int m, int y) {",
            "        return d + \"/\" + m + \"/\" + y;",
            "    }"]),
     "}",
     ])

# ------------------------------------------------------------------------ S005
scen("S005", "Guard clause added at the top, new behaviour added at the bottom",
     """TRAP (semantic): left inserts an early return for price <= 0, right adds
the big-basket bonus after the discount. The hunks are far apart, so git merges
them happily and the code still compiles. In the merged method the bonus can no
longer be reached for any input the guard intercepts, and neither author ever
tested the combination (apply(-1) = 0, apply(1100) = 995). No line of the diff
reveals that the two blocks interact through the same return path.""",
     [
     "class Discount {",
     "    public double apply(double price) {",
     "        double result = price;",
     ("L", ["        // NEW (left): free samples never get a discount",
            "        if (price <= 0) {",
            "            return 0;",
            "        }"]),
     "        result = result * 0.95;",
     ("R", ["        // NEW (right): extra bonus for big baskets",
            "        if (result > 1000) {",
            "            result = result - 50;",
            "        }"]),
     "        return result;",
     "    }",
     "}",
     ])

# ------------------------------------------------------------------------ S006
scen("S006", "Two side effects around the same statement - the tool picks the order",
     """TRAP (semantic): right increments the counter BEFORE the total is
updated, left logs the item AFTER it. One hunk lands above and the other below
an existing line, so the merge is clean and compiles - but nobody chose the
resulting execution order (countItem -> total -> logItem). If the log line is
read as "state after the update", the merged order already broke that intent,
and the diff gives no reason to doubt it.""",
     [
     "class Order {",
     "    private double total = 0;",
     "",
     "    public void addItem(double price) {",
     ("R", ["        // NEW (right): count the item before touching the total",
            "        countItem();"]),
     "        total = total + price;",
     ("L", ["        // NEW (left): log the item once the total is updated",
            "        logItem(price);"]),
     "    }",
     "",
     ("L", ["    private void logItem(double price) {",
            "        System.out.println(\"item added, total now \" + price);",
            "    }"]),
     ("R", ["",
            "    private void countItem() {",
            "        System.out.println(\"counter updated\");",
            "    }"]),
     "",
     "    public double getTotal() { return total; }",
     "}",
     ])

# ------------------------------------------------------------------------ S007
scen("S007", "Identical field/getter pair duplicated in two classes with different meanings",
     """TRAP (semantic): left gives Feature a flag 'enabled' (default true),
right gives Device a power state 'enabled' (default false). Two disjoint regions,
identical types, zero conflicts. The merged code looks like obvious duplication,
so the reviewer is tempted to factor isEnabled() into a shared parent/interface
or to copy one default into the other - merging a feature toggle with a hardware
switch and flipping the device's initial state.""",
     [
     "class Feature {",
     ("L", ["    // NEW (left): feature flag, on by default",
            "    private boolean enabled = true;",
            "",
            "    public boolean isEnabled() { return enabled; }",
            ""]),
     "    public String name() { return \"search\"; }",
     "}",
     "",
     "class Device {",
     ("R", ["    // NEW (right): device power state, off by default",
            "    private boolean enabled = false;",
            "",
            "    public boolean isEnabled() { return enabled; }",
            ""]),
     "    public String model() { return \"X100\"; }",
     "}",
     ])

# ------------------------------------------------------------------------ S008
scen("S008", "Both branches extend the same switch, one of them past the default label",
     """TRAP (semantic): left appends 'case 3' before the default branch, right
appends 'case 6/7' AFTER it. The additions land on different lines, so the merge
is clean and javac accepts it without a warning. The weekend cases now live
below 'default', which most readers assume closes the switch: the behaviour is
correct but the intent is buried, and the classic post-merge "cleanup" that
moves 'default' to the bottom is exactly where the real bug gets introduced.""",
     [
     "class WeekdayName {",
     "    public static String of(int day) {",
     "        switch (day) {",
     "            case 1: return \"Monday\";",
     "            case 2: return \"Tuesday\";",
     ("L", ["            // NEW (left): support Wednesday",
            "            case 3: return \"Wednesday\";"]),
     "            default: return \"unknown\";",
     ("R", ["            // NEW (right): support the weekend",
            "            case 6: return \"Saturday\";",
            "            case 7: return \"Sunday\";"]),
     "        }",
     "    }",
     "}",
     ])

# ------------------------------------------------------------------------ S009
scen("S009", "Extract-method refactor meets a brand-new copy of the extracted logic",
     """TRAP (semantic): left extracts the duplicated tax rate into rate();
right adds surcharge() repeating that very same inline expression. The changes
sit in different regions and share the literal 0.10, so the auto-merge is
flawless and compiles - while silently re-introducing the duplication the
refactor was created to remove. The next rate change updates three methods and
misses surcharge(), and the merge commit shows nothing suspicious.""",
     [
     "class Tax {",
     "    public double taxA(double income) {",
     "        return income * 0.10;",
     "    }",
     "",
     "    public double taxB(double income) {",
     "        return income * 0.10;",
     "    }",
     ("L", ["",
            "    // REFACTOR (left): single place for the rate",
            "    private double rate(double income) {",
            "        return income * 0.10;",
            "    }"]),
     ("R", ["",
            "    // NEW (right): surcharge applied to high incomes",
            "    public double surcharge(double income) {",
            "        return income * 0.10;",
            "    }"]),
     "}",
     ])

# ------------------------------------------------------------------------ S010
scen("S010", "A new normalisation rule lands next to the old one it should have replaced",
     """TRAP (semantic): left makes name() trim its argument, right adds a second
entry point normaliseEmail() that lowercases the e-mail - an untouched method
sits between the two hunks, so the merge is trivially clean and compiles. Now
the class exposes email(e) (raw) and normaliseEmail(e) (lowercased) side by
side: callers can pick either, and the "unique e-mail" invariant right branch
intended only holds for whoever calls the new setter. Nothing in the diff tells
the responsible that these two setters were supposed to be one, nor that the
combined identity rule ("trim + lowercase") has never been tested.""",
     [
     "class UserBuilder {",
     "    private String name = \"\";",
     "    private String email = \"\";",
     "",
     ("L", ["    /* NEW (left): trim names to avoid leading spaces */",
            "    public UserBuilder name(String n) { this.name = n.trim(); return this; }"]),
     "",
     "    public String describeClass() {",
     "        return \"UserBuilder\";",
     "    }",
     "",
     "    public UserBuilder email(String e) { this.email = e; return this; }",
     ("R", ["    /* NEW (right): lowercase emails to avoid duplicate accounts */",
            "    public UserBuilder normaliseEmail(String e) {",
            "        this.email = e.toLowerCase();",
            "        return this;",
            "    }"]),
     "",
     "    public String build() {",
     "        return name + \" <\" + email + \">\";",
     "    }",
     "}",
     ])


def render(blocks, flavour):
    """flavour: 'base' | 'left' | 'right' | 'merge'.

    Context lines are always emitted; tagged blocks are emitted only for the
    side that owns them (and for 'merge', which keeps both). The rendered text
    is never trimmed, so the merge result is exactly what git produces.
    """
    out = []
    for b in blocks:
        if not isinstance(b, tuple):          # plain context line
            out.append(b)
            continue
        tag, lines = b                        # ("L"/"R", added lines)
        if flavour == "base":
            continue
        if flavour == "merge" or flavour == tag:
            out.extend(lines)
    return "\n".join(out) + "\n"


def main():
    for name, title, trap, blocks in SCENARIOS:
        d = os.path.join(ROOT, name)
        os.makedirs(d, exist_ok=True)
        for flavour in ("base", "left", "right", "merge"):
            with open(os.path.join(d, flavour + ".java"), "w") as f:
                f.write(render(blocks, flavour))
        with open(os.path.join(d, "README.md"), "w") as f:
            f.write("# %s - %s\n\n%s\n\n"
                    "*Files:* `base.java` (ancestor), `left.java`, `right.java`, "
                    "`merge.java` (clean automatic merge of both sides, compiles with javac).\n"
                    % (name, title, trap))
    print("generated %d scenarios" % len(SCENARIOS))


if __name__ == "__main__":
    main()
