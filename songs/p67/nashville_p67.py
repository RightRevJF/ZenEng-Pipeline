"""Jehovah's Band -- the number chart: E major (1 = E), q = 112, a loping 4/4 with a light swing; one cell a bar; a bar with two chords
shows both. Every section's notes are written from the record and the band writer's report (patterns, entries, level). HTML -> PDF."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p67/song_record.pkl", "rb"))
BARS = REC["bars"]
RN = {"E": "1", "F#": "2", "G#": "3", "A": "4", "B": "5", "C#": "6", "D#": "7", "D": "♭7"}
QN = {"": "", "m": "m", "7": "7", "m7": "m7", "sus4": "sus4", "sus2": "sus2", "maj7": "maj7"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return RN[rt_] + QN[base[len(rt_):]] + (f"/{RN[bs]}" if bs else "")
B0 = {s: st // 48 for s, nb, st, mets, mv in REC["plan"]}
import sys; sys.path[:0] = ["/home/claude/p67"]
import engrave_p67 as E
BR = REC["writers"]["band"]
def feel(sec):
    r = BR["sections"].get(sec, {}); pt = r.get("patterns", {}); lv = r.get("level", (0, 0)); out = []
    if sec == "Jam": return E.NOTE2.replace("The jam starts", "Starts") + " Lead guitar solos to the end."
    if pt.get("organ"): out.append("organ " + E.pat_words(pt["organ"]))
    if pt.get("rhythm"): out.append("rhythm gtr " + E.pat_words(pt["rhythm"]))
    if lv[0] >= 0.85: out.append("RIDE")
    if lv[0] >= 0.4: out.append("crash bar 1")
    if sec not in ("Ending",): out.append("fill last bar")
    fb = [b + 1 for b in REC["writers"]["fills"] if E.BAR1[sec] <= b + 1 < E.BAR1[sec] + dict((p[0], p[1]) for p in REC["plan"])[sec]]
    if fb: out.append("lead answers bar " + ", ".join(str(b - E.BAR1[sec] + 1) for b in fb))
    if sec == "Intro": out.append("lead plays the title line twice")
    if sec.startswith("Chorus"): out.append("title line bars 1 and 9")
    return "; ".join(out).capitalize()
FEEL = {s: feel(s) for s, nb, st, mets, mv in REC["plan"]}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    cells = []
    for bi in range(b, b + nb):
        x = BARS[bi]
        cells.append(num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"]))
    lab = f"""<div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b + 1}–{b + nb}</div></div>"""
    body += f"""<div class="sec">{lab}<table class="nums">{rows(cells)}</table><div class="drum">{FEEL[s]}</div></div>"""
    b += nb
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }} .hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 5px; display: grid; grid-template-columns: 1.4in 6.1in 1fr; gap: 12px; border-bottom: 0.5px solid #bbb; padding-bottom: 5px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }} .lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .bar {{ font-size: 7.5pt; color: #555; }}
table.nums {{ border-collapse: collapse; }} table.nums td {{ width: 0.74in; white-space: nowrap; height: 0.2in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10.5pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.8pt; line-height: 1.2; }} .foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>{REC['title']}</h1>
<div class="meta">♩ = 112 &nbsp;·&nbsp; KEY: E major &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: loping, light swing &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> E major: 1 = E, 4 = A, 5 = B, ♭7 = D, 6m = C♯m, 5m = Bm; /3 = over the third. One cell is one bar; two numbers in a cell split it, two beats each.
<b>Drums.</b> {E.ROLE["drums"].replace("Drums: ", "")} <b>Voice.</b> One singer.</div>
</body></html>"""
open("/home/claude/p67/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p67/out/{REC['file_title']} - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
if __name__ == "__main__":
    asyncio.run(main()); print("ok")
