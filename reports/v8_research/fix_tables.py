"""Generic table repair for Doc-export markdown (Parts 26 on): rows that are line-wrap continuations (half or more of their cells empty)
are folded into the row above (into the header when they follow the separator); a table split at a page break, whose second half repeats
the header, is rejoined; 'word– 12' spacing inside ranges is closed. Usage: fix_tables.py name (reads and writes name.md)."""
import re, sys
name = sys.argv[1]; md = open(name + ".md").read()
def cells(l): return l.strip()[1:-1].split("|")
def join(a, b):
    a = a.rstrip(); b = b.strip()
    if not b: return a
    if not a: return b
    return a + ("" if a.endswith(("–", "(")) else " ") + b
lines = md.split("\n"); out = []
for l in lines:
    if l.startswith("|") and not l.startswith("|---") and out and out[-1].startswith("|"):
        c = cells(l)
        empty = sum(1 for x in c if not x.strip())
        tgt = len(out) - 1
        if out[tgt].startswith("|---"): tgt -= 1
        p = cells(out[tgt]) if tgt >= 0 and out[tgt].startswith("|") else None
        if p is not None and len(p) == len(c) and (empty * 2 >= len(c) or not c[0].strip()):
            out[tgt] = "|" + "|".join(join(a, b) for a, b in zip(p, c)) + "|"; continue
    out.append(l)
md = "\n".join(out)
# rejoin a table whose continuation repeats its header after a blank line
def rejoin(m):
    return m.group(1) if m.group(1).split("\n")[0] == m.group(3) else m.group(0)
for _ in range(3):
    md = re.sub(r"((\|[^\n]*\|)\n\|---[^\n]*\|(?:\n\|[^\n]*\|)*)\n\n(\|[^\n]*\|)\n\|---[^\n]*\|", lambda m: m.group(1) if m.group(2) == m.group(3) else m.group(0), md)
md = re.sub(r"(\d)– (\d)", r"\1–\2", md)
md = md.replace("one- syllable", "one-syllable")
open(name + ".md", "w").write(md); print(name, md.count("\n|---"))
