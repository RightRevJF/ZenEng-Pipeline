"""One web page with everything: Start here, the fix list (Doc export), avenues and atlas (Doc PDFs converted), Parts 4 to 13 (reports.md), Part 14."""
import re, subprocess
def shift(s): return re.sub(r"(?m)^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", s)
def clean_pdf_md(s, title):
    s = "\n".join(l for l in s.split("\n") if l.strip() != title and not re.fullmatch(r"\s*Page \d+ of \d+\s*", l))
    s = s.replace("<br>", " ")
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s
parts = ["---", 'title: "Luthier: everything learned while the engine was offline"', 'subtitle: "14 to 15 November 2026. The fix list for v8, the new rules, and every report and study"', "---", "", open("web_start.md").read(), ""]
fx = open("fixlist.md").read()
parts += ["# Part 1. Luthier fix list for v8 (since v7) {#part-1}", "", shift(re.sub(r"\A# .*\n", "", fx)), ""]
av = clean_pdf_md(open("avenues_pdf.md").read(), "For Luthier's maintainer: avenues and new rules")
parts += ["# Part 2. For Luthier's maintainer: avenues and new rules {#part-2}", "", shift(re.sub(r"(?m)\A\s*# .*\n", "", av.lstrip())), ""]
at = clean_pdf_md(open("atlas_pdf.md").read(), "Metre atlas: a head start for Luthier beyond 4/4")
parts += ["# Part 3. Metre atlas: a head start for Luthier beyond 4/4 {#part-3}", "", shift(re.sub(r"(?m)\A\s*# .*\n", "", at.lstrip())), ""]
rp = open("reports.md").read().replace("\\newpage", "")
rp = re.sub(r"(?m)^# Part (\d+)\. (.*)$", lambda m: f"# Part {m.group(1)}. {m.group(2)} {{#part-{m.group(1)}}}", rp)
parts += [rp, ""]
p14 = open("part14.md").read()
p14 = re.sub(r"(?m)^# Part 14\. (.*)$", lambda m: f"# Part 14. {m.group(1)} {{#part-14}}", p14)
parts += [p14]
open("web.md", "w").write("\n".join(parts))
CSS = """<style>
:root{--ink:#1f2328;--mute:#57606a;--line:#d0d7de;--accent:#1d4ed8;--bg:#fff}
@media (prefers-color-scheme:dark){:root{--ink:#e6edf3;--mute:#9da7b3;--line:#30363d;--accent:#7aa2ff;--bg:#0d1117}}
html{background:var(--bg)}body{color:var(--ink);font:17px/1.6 Georgia,'Times New Roman',serif;max-width:46rem;margin:0 auto;padding:1.25rem 1rem 4rem}
h1,h2,h3,h4,h5{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;line-height:1.3;margin:2em 0 .5em}
h1{font-size:1.6rem;border-top:3px solid var(--accent);padding-top:.8em}h1.title{border:0;font-size:1.9rem;margin-top:.5em}
p.subtitle{color:var(--mute);font-style:italic;margin-top:-.4em}
h2{font-size:1.3rem}h3{font-size:1.1rem}h4,h5{font-size:1rem}
a{color:var(--accent)}code{font-size:.9em}
table{display:block;overflow-x:auto;border-collapse:collapse;margin:1em 0;font:14px/1.45 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
th,td{border:1px solid var(--line);padding:.35em .55em;vertical-align:top;text-align:left;min-width:4.5em}
th{background:color-mix(in srgb,var(--line) 35%,transparent)}
img{max-width:100%;height:auto}
nav#TOC{font:15px/1.5 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif;border:1px solid var(--line);border-radius:8px;padding:.6em 1em;margin:1em 0}
nav#TOC ul{padding-left:1.1em;margin:.2em 0}nav#TOC>ul>li{margin:.15em 0}
.top{position:fixed;right:.8rem;bottom:.8rem;font:14px sans-serif;background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:.35em .8em;text-decoration:none}
</style>"""
open("web_head.html", "w").write('<meta name="viewport" content="width=device-width, initial-scale=1">\n' + CSS)
open("web_after.html", "w").write('<a class="top" href="#start">Top</a>')
subprocess.run(["pandoc", "web.md", "-s", "--embed-resources", "--toc", "--toc-depth=1", "--resource-path=.:/home/claude/zeneng-pipeline/studies/shapes",
                "-H", "web_head.html", "-A", "web_after.html", "-o", "luthier_offline.html", "--metadata", "pagetitle=Luthier: everything learned while the engine was offline", "-c", "/dev/null"], check=True)
import os; print(os.path.getsize("luthier_offline.html"))
