#!/usr/bin/env python3
"""Verify the 10 toy merge scenarios S001..S010.

Checks, for every scenario:
  1. left.java / right.java are pure ADDITIONS of base.java (difflib reports no
     deleted common line) -> each side touches only its own region.
  2. The regions added by left and by right are DISJOINT in base coordinates
     -> the two changes cannot interfere textually.
  3. `git merge` of the left and right branches is CLEAN (no conflict markers).
  4. The auto-merged file equals merge.java (modulo trailing blank lines).
  5. base.java, left.java, right.java and merge.java all compile with javac
     -> no type conflicts anywhere.
"""

import difflib
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = ["S%03d" % i for i in range(1, 11)]


def read(p):
    with open(p) as f:
        return f.read().splitlines()


def added_regions(base, other):
    """Return list of (base_index_before_insertion, inserted_lines) plus a flag
    telling whether any common base line was removed."""
    sm = difflib.SequenceMatcher(None, base, other, autojunk=False)
    inserts, deletions = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"):
            deletions.extend(base[i1:i2])
        if tag in ("insert", "replace"):
            inserts.append((i2, other[j1:j2]))
    return inserts, deletions


def run(cmd, cwd=None, shell=False):
    return subprocess.run(cmd, cwd=cwd, shell=shell,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def git(args, cwd):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    return subprocess.run(["git"] + args, cwd=cwd, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def build_repo(work, d, s):
    """base commit -> branch 'left' ; base commit -> branch 'right'."""
    os.makedirs(work)
    assert git(["init", "-q", "."], work).returncode == 0
    shutil.copy(os.path.join(d, "base.java"), os.path.join(work, "%s.java" % s))
    git(["add", "."], work)
    git(["commit", "-qm", "base"], work)

    git(["checkout", "-qb", "left"], work)
    shutil.copy(os.path.join(d, "left.java"), os.path.join(work, "%s.java" % s))
    git(["commit", "-qam", "left change"], work)

    git(["checkout", "-q", "master"], work)
    git(["checkout", "-qb", "right"], work)
    shutil.copy(os.path.join(d, "right.java"), os.path.join(work, "%s.java" % s))
    git(["commit", "-qam", "right change"], work)

    git(["checkout", "-q", "left"], work)


failures = []


def check(cond, msg):
    print(("  [OK]   " if cond else "  [FAIL] ") + msg)
    if not cond:
        failures.append(msg)


for s in SCENARIOS:
    print("=== %s" % s)
    d = os.path.join(ROOT, s)
    base = read(os.path.join(d, "base.java"))
    left = read(os.path.join(d, "left.java"))
    right = read(os.path.join(d, "right.java"))
    merge = read(os.path.join(d, "merge.java"))

    li, ld = added_regions(base, left)
    ri, rd = added_regions(base, right)
    check(not ld, "left.java only ADDS lines to base (no altered/deleted line)")
    check(not rd, "right.java only ADDS lines to base (no altered/deleted line)")

    lpos = {p for p, lines in li if lines}
    rpos = {p for p, lines in ri if lines}
    check(bool(lpos) and bool(rpos), "both sides really introduce a change")
    check(not (lpos & rpos),
          "insertion points are disjoint: left@%s vs right@%s (no interference)"
          % (sorted(lpos), sorted(rpos)))

    tmp = tempfile.mkdtemp(prefix="mt_" + s + "_")
    work = os.path.join(tmp, "repo")
    try:
        build_repo(work, d, s)
        m = git(["merge", "--no-edit", "right"], work)
        merged_txt = open(os.path.join(work, "%s.java" % s)).read()
        check(m.returncode == 0,
              "`git merge left+right` is automatic, no conflict (exit=%d)" % m.returncode)
        check("<<<<<<<" not in merged_txt and ">>>>>>>" not in merged_txt
              and "=======" not in merged_txt, "merged file has no conflict markers")
        norm = lambda t: "\n".join(t.rstrip().splitlines())
        check(norm(merged_txt) == norm("\n".join(merge)),
              "merge.java is exactly the automatic merge result")
    finally:
        # ---- compilation of every flavour (kept out of the repo dir)
        for flav in ("base", "left", "right", "merge"):
            out = run(["javac", "-d", os.path.join(tmp, "cls_" + flav),
                       os.path.join(d, flav + ".java")])
            check(out.returncode == 0, "%s.java compiles with javac (no type conflict)" % flav)
            if out.returncode:
                print(out.stdout.decode())
        shutil.rmtree(tmp, ignore_errors=True)

print()
if failures:
    print("FAILED checks: %d" % len(failures))
    sys.exit(1)
print("All scenarios verified: clean textual merges, no interference, no type conflicts.")
