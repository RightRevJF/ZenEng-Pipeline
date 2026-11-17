"""The web page with Part 30 added (the hook; 17 Nov): Start here re-rendered from web_start.md, Part 30 appended from its Doc's PDF
export turned into markdown (clean.py, fix_tables.py; the chart embedded as an image), with a contents entry. Parts 1 to 29 kept."""
import re, subprocess
H = "luthier_offline.html"; s = open(H).read(); R3 = "/home/claude/handoff/r3"
def frag(md): return subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"], input=md, capture_output=True, text=True, check=True).stdout
def shift(t): return re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", t)
st = open("web_start.md").read(); st = re.sub(r"\A\s*#[^\n]*\n", "", st)
i = s.index('<h1 id="start"'); i = s.index(">", s.index("</h1>", i)) + 1; j = s.index('<h1 id="part-1"')
s = s[:i] + "\n" + frag(shift(st)) + "\n" + s[j:]
for n, t, url, f in [(30, "The hook for Luthier v8: what makes a chorus stick", "https://claude.ai/artifact/NnkTkwF3cFxbtZjrz2NSLn", "hooks.md")]:
    md = f"17 November 2026. Words and music: Jason Bryant. The live copy is the Doc [{t}]({url}).\n\n" + open(f"{R3}/{f}").read()
    part = f'<h1 id="part-{n}">Part {n}. {t}</h1>\n' + frag(shift(md)) + '\n<a class="top" href="#start">Top</a>\n'
    if f'id="part-{n}"' in s:
        a = s.index(f'<h1 id="part-{n}"'); b = s.index('<a class="top"', a); b = s.index("</a>", b) + 5; s = s[:a] + part + s[b:]
    else:
        a = s.index(f'<h1 id="part-{n - 1}"'); b = s.index('<a class="top"', a); b = s.index("</a>", b) + 5; s = s[:b] + "\n" + part + s[b:]
    if f'id="toc-part-{n}"' not in s:
        k = s.index(f'id="toc-part-{n - 1}"'); k = s.index("</li>", k) + 5
        s = s[:k] + f'\n<li><a href="#part-{n}" id="toc-part-{n}">Part {n}. {t}</a></li>' + s[k:]
open(H, "w").write(s); print(len(s), [s.count(f'id="part-{n}"') for n in (29, 30)], [s.count(f'href="#part-{n}"') for n in (29, 30)])
