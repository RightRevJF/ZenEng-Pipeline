"""The final report with Part 30 added (the hook; 17 Nov): Start here re-rendered, Parts 1 to 29 taken unchanged from the final report,
Part 30 appended from its Doc's PDF export. Run in /home/claude/handoff with r3/hooks.pdf."""
import subprocess, shutil
from pypdf import PdfReader, PdfWriter
R = "/home/claude/zeneng-pipeline/reports"
SRC = "Luthier - final report for v8 (14-17 November 2026).pdf"
OLD = PdfReader(f"{R}/{SRC}")
marks = [(OLD.get_destination_page_number(o), o.title) for o in OLD.outline if not isinstance(o, list)]
starts = {t: p for p, t in marks}; order = [t for _, t in marks]
def span(title):
    i = order.index(title); a = starts[title]; b = starts[order[i + 1]] if i + 1 < len(order) else len(OLD.pages); return a, b
n = lambda f: len(PdfReader(f).pages)
olds = [t for t in order if t.startswith("Part ") and not t.startswith("Part 30.")]
NEW = [("30", "Part 30. The hook for Luthier v8: what makes a chorus stick", "r3/hooks.pdf")]
def pages(S):
    P = {}; a = S + 1
    for t in olds:
        k = t.split(".")[0].split()[1]; P[f"P{k}"] = a; s0, s1 = span(t); a += s1 - s0
    for k, _, f in NEW: P[f"P{k}"] = a; a += n(f)
    return P
def render(S):
    P = pages(S); md = open(f"{R}/start_here.md").read()
    for k in sorted(P, key=lambda x: -len(x)): md = md.replace("{" + k + "}", str(P[k]))
    assert "{P" not in md
    open("start_filled.md", "w").write(md)
    subprocess.run(["pandoc", "start_filled.md", "-o", "start.docx", "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "start.docx"], capture_output=True)
    return n("start.pdf"), P
S = 5
for _ in range(4):
    m, P = render(S)
    if m == S: break
    S = m
w = PdfWriter()
s0 = len(w.pages); w.append("start.pdf", import_outline=False); w.add_outline_item("Start here", s0)
for t in olds:
    a, b = span(t); s0 = len(w.pages); w.append(OLD, pages=(a, b), import_outline=False); w.add_outline_item(t, s0)
for _, t, f in NEW:
    s0 = len(w.pages); w.append(f, import_outline=False); w.add_outline_item(t, s0)
w.add_metadata({"/Title": "Luthier: the final report for v8 (14 to 17 November 2026)", "/Author": "Jason Bryant"})
out = SRC; w.write(out); shutil.copy(out, f"{R}/{out}"); print(out, len(w.pages), P)
