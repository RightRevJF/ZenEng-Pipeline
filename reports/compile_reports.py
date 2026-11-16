"""One file: every document written for the engine's maintainer since the research began on 15 November 2026, in the order written."""
import re, subprocess, os
Z = "/home/claude/zeneng-pipeline"
PARTS = [
    ("Time signature research and song data (research report)", f"{Z}/reports/Time signature research and song data.md"),
    ("Accompaniment corpora and music theory (research report)", f"{Z}/reports/Accompaniment corpora and music theory.md"),
    ("Shapes of music like story arcs (research report)", f"{Z}/reports/Shapes of music like story arcs.md"),
    ("Shapes of songs: the first study", f"{Z}/studies/shapes/shapes_study_report.md"),
    ("Surprise against expectation and YouTube views", f"{Z}/studies/surprise/surprise_study_report.md"),
    ("Moments people love", f"{Z}/studies/moments/moments_study_report.md"),
    ("The rhythm layer", f"{Z}/studies/rhythm/rhythm_study_report.md"),
    ("Psychoacoustics for the songwriting engine (research report)", f"{Z}/reports/Psychoacoustics for the songwriting engine.md"),
    ("What musicians re-record (covers study)", f"{Z}/studies/covers/covers_study_report.md"),
    ("Sung to Sleep (song 53): test report, first to fourth edition", "/home/claude/p63/test_report_p63.md"),
]
out = []
for i, (title, path) in enumerate(PARTS, 1):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"\A---\n.*?\n---\n", "", s, flags=re.S)                         # front matter out
    s = re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", s)            # every heading down one level
    s = s.replace("](mean_shapes.png)", "](/home/claude/zeneng-pipeline/studies/shapes/mean_shapes.png)")
    out += [f"# Part {i+3}. {title}", "", s.strip(), "", "\\newpage", ""]
open("/home/claude/handoff/reports.md", "w", encoding="utf-8").write("\n".join(out))
