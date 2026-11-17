"""Post-clean fixes for voices.md (Part 24): stray heading levels from the PDF, a list item merged at a page break, paragraphs split at page breaks."""
import re
md = open("voices.md").read()
md = md.replace("#### **Motion and placement** (%, except the per-100 columns)", "**Motion and placement** (%, except the per-100 columns)")
md = md.replace("\nV1. Six kinds of second voice, each with its own writer\n", "\n### V1. Six kinds of second voice, each with its own writer\n")
md = md.replace("arrangements). The Church Collective,", "arrangements).\n\n- The Church Collective,")
md = md.replace("#### Wikipedia, Vocal harmony;", "- Wikipedia, Vocal harmony;")
lines = md.split("\n"); out = []
for l in lines:
    if l and l[0].islower() and len(out) >= 2 and out[-1] == "" and out[-2] and not out[-2].startswith(("#", "|")) and not out[-2].rstrip().endswith((".", ":", ")")):
        out.pop(); out[-1] = out[-1].rstrip() + " " + l
    else: out.append(l)
md = "\n".join(out)
assert "####" not in md
open("voices.md", "w").write(md); print("ok", len(md))
