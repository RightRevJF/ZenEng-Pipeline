"""The web page with Part 24 added (harmony voices, 17 Nov): Start here re-rendered from web_start.md, Part 24 appended after Part 23 from its
Doc's PDF export turned into markdown (/home/claude/handoff/r3/clean.py voices, then fix_voices.py), and a contents entry. Parts 1 to 23 kept."""
import re, subprocess
H = "luthier_offline.html"; s = open(H).read()
R3 = "/home/claude/handoff/r3"
def frag(md):
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"], input=md, capture_output=True, text=True, check=True).stdout
def shift(t): return re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", t)
st = open("web_start.md").read(); st = re.sub(r"\A\s*#[^\n]*\n", "", st)
i = s.index('<h1 id="start"'); i = s.index(">", s.index("</h1>", i)) + 1; j = s.index('<h1 id="part-1"')
s = s[:i] + "\n" + frag(shift(st)) + "\n" + s[j:]
t = "Harmony voices for Luthier v8: duets, backing vocals and choirs"; url = "https://claude.ai/artifact/WfTuzxkKzyUPiCvhFn75Dz"
md = f"17 November 2026. Words and music: Jason Bryant. The live copy is the Doc [{t}]({url}).\n\n" + open(f"{R3}/voices.md").read()
part = f'<h1 id="part-24">Part 24. {t}</h1>\n' + frag(shift(md)) + '\n<a class="top" href="#start">Top</a>\n'
if 'id="part-24"' in s:
    a = s.index('<h1 id="part-24"'); b = s.index('<a class="top"', a); b = s.index("</a>", b) + 5; s = s[:a] + part + s[b:]
else:
    a = s.index('<h1 id="part-23"'); b = s.index('<a class="top"', a); b = s.index("</a>", b) + 5; s = s[:b] + "\n" + part + s[b:]
if 'id="toc-part-24"' not in s:
    k = s.index('id="toc-part-23"'); k = s.index("</li>", k) + 5
    s = s[:k] + f'\n<li><a href="#part-24" id="toc-part-24">Part 24. {t}</a></li>' + s[k:]
open(H, "w").write(s); print(len(s), s.count('id="part-24"'), s.count('toc-part-24'), s.count('href="#part-24"'))
