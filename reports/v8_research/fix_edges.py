"""Post-clean fixes for edges.md (Part 25): table rows split at line wraps or page breaks rejoined, the endings table's repeated header
removed, words broken at hyphens rejoined."""
import re
md = open("edges.md").read()
# the endings table: drop the second header block repeated after the page break
md = re.sub(r"\n\n\|Period\|Fade-\|Cold endings:\|[^\n]*\n\|---[^\n]*\n\|\|out\|[^\n]*\n", "\n", md)
lines = md.split("\n"); out = []
def cells(l): return l.strip()[1:-1].split("|")
for l in lines:
    if l.startswith("|") and out and out[-1].startswith("|") and not l.startswith("|---") and not out[-1].startswith("|---"):
        c = cells(l); p = cells(out[-1])
        cont = len(c) == len(p) and (c[0].strip() == "" or all(x.strip() == "" for x in c[1:]))
        if cont:
            out[-1] = "|" + "|".join((a.rstrip() + ("" if a.rstrip().endswith("–") else " ") + b.strip()).strip() if b.strip() else a for a, b in zip(p, c)) + "|"; continue
    out.append(l)
md = "\n".join(out)
md = re.sub(r"(\d{4})– ?(\d\d)\b", r"\1–\2", md)
md = md.replace("Fade- out", "Fade-out").replace("non- musicians", "non-musicians").replace("Resolved:♭VII–I", "Resolved: ♭VII–I")
md = re.sub(r"(\w)- (\w)", lambda m: m.group(0) if m.group(2).isupper() else m.group(1) + "-" + m.group(2), md)
md = md.replace("|Resolved:|V–I, last chord held|The default before 1965 (half of|\n|authentic||cold endings)|", "|Resolved: authentic|V–I, last chord held|The default before 1965 (half of cold endings)|")
assert "|authentic||" not in md
open("edges.md", "w").write(md); print(md.count("\n|---"))
