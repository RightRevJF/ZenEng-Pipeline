"""The web page, updated after the genre study (17 Nov): Start here re-rendered from web_start.md, and Part 22 added
(the genre study), from its Doc's PDF export turned into markdown by /home/claude/handoff/r3/clean.py.
Parts 1 to 21 are kept as they stand."""
import re, subprocess
H = "luthier_offline.html"; s = open(H).read()
R3 = "/home/claude/handoff/r3"
def frag(md):
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"], input=md, capture_output=True, text=True, check=True).stdout
def shift(t): return re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", t)
st = open("web_start.md").read(); st = re.sub(r"\A\s*#[^\n]*\n", "", st)
i = s.index('<h1 id="start"'); i = s.index(">", s.index("</h1>", i)) + 1; j = s.index('<h1 id="part-1"')
s = s[:i] + "\n" + frag(shift(st)) + "\n" + s[j:]
assert 'id="part-22"' not in s
P = [("22", "Melody by genre for Luthier v8: scales, blue notes and the divorce", "genre", "https://claude.ai/artifact/QYV56dyEeDLUfVb3xTnhAZ")]
add = ""; toc = ""
for n, t, f, url in P:
    md = open(f"{R3}/{f}.md").read()
    md = f"17 November 2026. Words and music: Jason Bryant. The live copy is the Doc [{t}]({url}).\n\n" + md
    add += f'<h1 id="part-{n}">Part {n}. {t}</h1>\n' + frag(shift(md)) + "\n"
    toc += f'<li><a href="#part-{n}" id="toc-part-{n}">Part {n}. {t}</a></li>\n'
k = s.index('<a class="top"'); s = s[:k] + add + s[k:]
e = s.index("</ul>", s.index('<nav id="TOC"')); s = s[:e] + toc + s[e:]
open(H, "w").write(s); print(len(s))
