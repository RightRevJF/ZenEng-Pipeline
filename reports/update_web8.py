"""The web page after the second round of reading on setting words (17 Nov): Start here re-rendered from web_start.md, and Part 23
replaced by its Doc's new PDF export turned into markdown (/home/claude/handoff/r3/clean.py, then fix_words.py). Parts 1 to 22 kept."""
import re, subprocess
H = "luthier_offline.html"; s = open(H).read()
R3 = "/home/claude/handoff/r3"
def frag(md):
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"], input=md, capture_output=True, text=True, check=True).stdout
def shift(t): return re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", t)
st = open("web_start.md").read(); st = re.sub(r"\A\s*#[^\n]*\n", "", st)
i = s.index('<h1 id="start"'); i = s.index(">", s.index("</h1>", i)) + 1; j = s.index('<h1 id="part-1"')
s = s[:i] + "\n" + frag(shift(st)) + "\n" + s[j:]
t = "Setting words for Luthier v8: stress, vowels and high notes"; url = "https://claude.ai/artifact/4xcqBYhnS8uLAFCzeuqtA2"
md = f"17 November 2026. Words and music: Jason Bryant. The live copy is the Doc [{t}]({url}).\n\n" + open(f"{R3}/words.md").read()
a = s.index('<h1 id="part-23"'); b = s.index('<a class="top"', a)
s = s[:a] + f'<h1 id="part-23">Part 23. {t}</h1>\n' + frag(shift(md)) + "\n" + s[b:]
open(H, "w").write(s); print(len(s), s.count('id="part-23"'))
