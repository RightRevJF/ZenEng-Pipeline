"""Doc-export PDFs -> clean markdown for the web page: drop running heads and page footers, rejoin tables split across pages,
flatten cell line breaks, and restore the links from the PDF's own link annotations, in document order."""
import re, sys, fitz, pymupdf4llm
def links(pdf):
    out = []
    for p in fitz.open(pdf):
        for l in p.get_links():
            if l.get("uri"):
                t = " ".join(p.get_textbox(l["from"]).split())
                if t: out.append((t, l["uri"]))
    # merge consecutive pieces of one link split over lines
    m = []
    for t, u in out:
        if m and m[-1][1] == u: m[-1] = (m[-1][0] + " " + t, u)
        else: m.append((t, u))
    return m
def clean(name):
    md = open(name + "_raw.md").read()
    title = md.split("\n", 1)[0].strip()
    md = md.replace("<u>", "").replace("</u>", "")
    md = re.sub(r"(?m)^Page \d+ of \d+\s*$", "", md)
    md = re.sub(r"(?m)^" + re.escape(title) + r"\s*$", "", md)
    md = md.replace("<br>", " ")
    lines = [l.rstrip() for l in md.split("\n")]
    # rejoin split tables: a table, blank lines, then the same header row again
    out = []; i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|") and out:
            j = len(out) - 1
            while j >= 0 and out[j] == "": j -= 1
            if j >= 0 and out[j].startswith("|"):
                # find this table's header in out
                k = j
                while k > 0 and out[k - 1].startswith("|"): k -= 1
                if out[k] == l and i + 1 < len(lines) and lines[i + 1].startswith("|---"):
                    del out[j + 1:]; i += 2; continue
        out.append(l); i += 1
    md = "\n".join(out)
    md = re.sub(r"\A\s*# .*\n", "", md.lstrip())          # the title (the part heading carries it)
    md = re.sub(r"\A\s*Nov 16, 2026 · @Jason Bryant[^\n]*\n", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    # restore links in order
    pos = 0
    for t, u in links(name + ".pdf"):
        k = md.find(t, pos)
        if k < 0: k = md.find(t)
        while k > 0 and md[k - 1] == "[": k = md.find(t, k + 1)
        if k < 0: print("  link text not found:", t[:50], file=sys.stderr); continue
        rep = f"[{t}]({u})"; md = md[:k] + rep + md[k + len(t):]; pos = k + len(rep)
    open(name + ".md", "w").write(md.strip() + "\n"); print(name, len(md))
import sys
for n in (sys.argv[1:] or ["audit", "harmony", "arrangement"]): clean(n)
