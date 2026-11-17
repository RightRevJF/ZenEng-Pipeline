"""One shareable PDF, rebuilt after the harmony and arrangement work (16 Nov): a new Start here, Parts 1 to 16 taken unchanged from the
14-16 November file, and Parts 17 to 19 (audit, harmony study, arrangement study) as their Docs' own PDF exports. Run in /home/claude/handoff
with r3/audit.pdf, r3/harmony.pdf and r3/arrangement.pdf beside it."""
import subprocess, shutil
from pypdf import PdfReader, PdfWriter
R = "/home/claude/zeneng-pipeline/reports"
SRC = "Luthier - everything learned while offline and since (14-16 November 2026).pdf"
OLD = PdfReader(f"{R}/{SRC}")
marks = [(OLD.get_destination_page_number(o), o.title) for o in OLD.outline if not isinstance(o, list)]
starts = {t: p for p, t in marks}; order = [t for _, t in marks]
def span(title):
    i = order.index(title); a = starts[title]; b = starts[order[i + 1]] if i + 1 < len(order) else len(OLD.pages); return a, b
n = lambda f: len(PdfReader(f).pages)
olds = [t for t in order if t.startswith("Part ")]
NEW = [("17", "Part 17. Luthier audit: harmony and arrangement", "r3/audit.pdf"),
       ("18", "Part 18. Harmony research for Luthier v8: what follows what", "r3/harmony.pdf"),
       ("19", "Part 19. Arrangement research for Luthier v8: what the band does", "r3/arrangement.pdf")]
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
S = 3
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
w.add_metadata({"/Title": "Luthier: everything learned while the engine was offline, and since (14 to 16 November 2026)", "/Author": "Jason Bryant"})
out = SRC; w.write(out); shutil.copy(out, f"{R}/{out}"); print(out, len(w.pages), P)
