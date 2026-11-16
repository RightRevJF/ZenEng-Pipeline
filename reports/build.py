import subprocess, re
from pypdf import PdfReader, PdfWriter
def render(S):
    rp={1:0,4:1,5:11,6:24,7:41,8:45,9:48,10:50,11:53,12:73,13:75}
    P={"P1":S+1,"P2":S+33,"P3":S+42}
    for k,v in rp.items():
        if k>=4: P[f"P{k}"]=S+54+v-1
    md=open("start_here.md").read()
    for k,v in P.items(): md=md.replace("{"+k+"}",str(v))
    open("start_filled.md","w").write(md)
    subprocess.run(["pandoc","start_filled.md","-o","start.docx","--reference-doc=/home/claude/carol/songbook/ref.docx"],check=True)
    subprocess.run(["soffice","--headless","--convert-to","pdf","start.docx"],capture_output=True)
    return len(PdfReader("start.pdf").pages), P
S=3
for _ in range(3):
    n,P=render(S)
    if n==S: break
    S=n
print("start pages",S)
w=PdfWriter()
parts=[("Start here","start.pdf"),("Part 1. Luthier fix list for v8 (since v7)","fixlist.pdf"),("Part 2. Avenues and new rules","avenues.pdf"),("Part 3. Metre atlas","atlas.pdf")]
for title,f in parts:
    start=len(w.pages); w.append(f); w.add_outline_item(title,start)
start=len(w.pages); w.append("reports.pdf")
names={4:"Time signature research and song data",5:"Accompaniment corpora and music theory",6:"Shapes of music like story arcs",7:"Shapes of songs: the first study",8:"Surprise against expectation and YouTube views",9:"Moments people love",10:"The rhythm layer",11:"Psychoacoustics for the songwriting engine",12:"What musicians re-record (covers study)",13:"Sung to Sleep (song 53): test report"}
for k in range(4,14): w.add_outline_item(f"Part {k}. {names[k]}",P[f"P{k}"]-1)
w.add_metadata({"/Title":"Luthier: everything learned while the engine was offline (14 to 15 November 2026)","/Author":"Jason Bryant"})
out="Luthier - everything learned while offline (14-15 November 2026).pdf"
w.write(out); print(out,len(w.pages))
