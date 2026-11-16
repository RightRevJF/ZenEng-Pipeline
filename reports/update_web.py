"""The web page, updated after song 54 (16 Nov): Start here re-rendered from web_start.md, Part 1 from the fix list's fresh Doc export
(/home/claude/handoff/fixlist.md), Part 15 (song 54's test report) added; Parts 2 to 14 kept as built on 15 November."""
import re, subprocess
H = "luthier_offline.html"; s = open(H).read()
def frag(md):
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"], input=md, capture_output=True, text=True, check=True).stdout
def shift(t): return re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", t)
def between(a, b, new):
    global s
    i = s.index(a); i = s.index(">", s.index("</h1>", i)) + 1; j = s.index(b)
    s = s[:i] + "\n" + new + "\n" + s[j:]
st = open("web_start.md").read()
st = re.sub(r"\A\s*#[^\n]*\n", "", st)
between('<h1 id="start"', '<h1 id="part-1"', frag(shift(st)))
fx = open("/home/claude/handoff/fixlist.md").read()
between('<h1 id="part-1"', '<h1 id="part-2"', frag(shift(re.sub(r"\A# .*\n", "", fx))))
tr = open("/home/claude/zeneng-pipeline/songs/p64/test_report_p64.md").read()
tr = re.sub(r"\A---\n.*?\n---\n", "", tr, flags=re.S)
p15 = '<h1 id="part-15">Part 15. The Man Mama Prayed I’d Be (song 54): test report</h1>\n' + frag(shift(tr))
k = s.index('<a class="top"'); s = s[:k] + p15 + "\n" + s[k:]
toc_end = s.index("</ul>", s.index('<nav id="TOC"'))
s = s[:toc_end] + '<li><a href="#part-15" id="toc-part-15">Part 15. The Man Mama Prayed I’d Be (song 54): test report</a></li>\n' + s[toc_end:]
s = s.replace("everything learned while the engine was offline</title>", "everything learned while the engine was offline, and since</title>", 1)
open(H, "w").write(s); print(len(s))
