"""One shareable PDF, rebuilt after song 54 (16 Nov): a new Start here, the fix list exported fresh from its Doc (Part 1), Parts 2 to 14
taken unchanged from the 15 November file, and song 54's test report as Part 15. Run in /home/claude/handoff with fixlist.pdf (Doc export)
and song54.pdf (the test report's Word copy through soffice) beside it."""
import subprocess, shutil
from pypdf import PdfReader, PdfWriter
R = "/home/claude/zeneng-pipeline/reports"
OLD = PdfReader(f"{R}/Luthier - everything learned while offline (14-15 November 2026).pdf")
marks = [(OLD.get_destination_page_number(o), o.title) for o in OLD.outline if not isinstance(o, list)]
starts = {t: p for p, t in marks}; order = [t for _, t in marks]
def span(title):
    i = order.index(title); a = starts[title]; b = starts[order[i + 1]] if i + 1 < len(order) else len(OLD.pages); return a, b
n = lambda f: len(PdfReader(f).pages)
olds = [t for t in order if t.startswith("Part ") and not t.startswith("Part 1.")]
def pages(S):
    P = {"P1": S + 1}; a = S + 1 + n("fixlist.pdf")
    for t in olds:
        k = t.split(".")[0].split()[1]; P[f"P{k}"] = a; s0, s1 = span(t); a += s1 - s0
    P["P15"] = a; return P
def render(S):
    P = pages(S); md = open(f"{R}/start_here.md").read()
    for k in sorted(P, key=lambda x: -len(x)): md = md.replace("{" + k + "}", str(P[k]))
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
s0 = len(w.pages); w.append("fixlist.pdf", import_outline=False); w.add_outline_item("Part 1. Luthier fix list for v8 (since v7)", s0)
for t in olds:
    a, b = span(t); s0 = len(w.pages); w.append(OLD, pages=(a, b), import_outline=False); w.add_outline_item(t, s0)
s0 = len(w.pages); w.append("song54.pdf", import_outline=False); w.add_outline_item("Part 15. The Man Mama Prayed I'd Be (song 54): test report", s0)
w.add_metadata({"/Title": "Luthier: everything learned while the engine was offline, and since (14 to 16 November 2026)", "/Author": "Jason Bryant"})
out = "Luthier - everything learned while offline and since (14-16 November 2026).pdf"; w.write(out); shutil.copy(out, f"{R}/{out}"); print(out, len(w.pages), P)
