"""One shareable PDF: Start here, fix list, avenues and rules, metre atlas, the reports and studies (Parts 4 to 13), chromatic study (Part 14)."""
import subprocess
from pypdf import PdfReader, PdfWriter
n = lambda f: len(PdfReader(f).pages)
RP = {4: 1, 5: 11, 6: 24, 7: 41, 8: 45, 9: 48, 10: 50, 11: 53, 12: 73, 13: 75}      # part starts inside reports.pdf
def pages(S):
    a = S + 1; P = {"P1": a}; a += n("fixlist.pdf"); P["P2"] = a; a += n("avenues.pdf"); P["P3"] = a; a += n("atlas.pdf")
    for k, v in RP.items(): P[f"P{k}"] = a + v - 1
    P["P14"] = a + n("reports.pdf"); return P
def render(S):
    P = pages(S); md = open("start_here.md").read()
    for k in sorted(P, key=lambda x: -len(x)): md = md.replace("{" + k + "}", str(P[k]))
    open("start_filled.md", "w").write(md)
    subprocess.run(["pandoc", "start_filled.md", "-o", "start.docx", "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "start.docx"], capture_output=True)
    return n("start.pdf"), P
S = 2
for _ in range(4):
    m, P = render(S)
    if m == S: break
    S = m
w = PdfWriter()
for title, f in [("Start here", "start.pdf"), ("Part 1. Luthier fix list for v8 (since v7)", "fixlist.pdf"), ("Part 2. Avenues and new rules", "avenues.pdf"), ("Part 3. Metre atlas", "atlas.pdf")]:
    s0 = len(w.pages); w.append(f, import_outline=False); w.add_outline_item(title, s0)
w.append("reports.pdf", import_outline=False)
names = {4: "Time signature research and song data", 5: "Accompaniment corpora and music theory", 6: "Shapes of music like story arcs", 7: "Shapes of songs: the first study",
         8: "Surprise against expectation and YouTube views", 9: "Moments people love", 10: "The rhythm layer", 11: "Psychoacoustics for the songwriting engine",
         12: "What musicians re-record (covers study)", 13: "Sung to Sleep (song 53): test report"}
for k in range(4, 14): w.add_outline_item(f"Part {k}. {names[k]}", P[f"P{k}"] - 1)
s0 = len(w.pages); w.append("part14.pdf", import_outline=False); w.add_outline_item("Part 14. Chromatic harmony: views, covers and our songs", s0)
w.add_metadata({"/Title": "Luthier: everything learned while the engine was offline (14 to 15 November 2026)", "/Author": "Jason Bryant"})
out = "Luthier - everything learned while offline (14-15 November 2026).pdf"; w.write(out); print(out, len(w.pages), P)
