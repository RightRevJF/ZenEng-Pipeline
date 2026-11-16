"""Your Yard Man -- the number chart: A major (1 = A), q = 120, a two-step, all 4/4; one cell a bar; a bar with two chords
shows both. Every section's notes are read from the record (where the stop falls, the hook's bars). HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p65/song_record.pkl", "rb"))
BARS = REC["bars"]
RN = {"A": "1", "B": "2", "C#": "3", "D": "4", "E": "5", "F#": "6", "G#": "7", "G": "♭7"}
QN = {"": "", "m": "m", "7": "7", "m7": "m7", "sus4": "sus4", "sus2": "sus2", "maj7": "maj7"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return RN[rt_] + QN[base[len(rt_):]] + (f"/{RN[bs]}" if bs else "")
B0 = {s: st // 48 for s, nb, st, mets, mv in REC["plan"]}
FEEL = {"Intro": "Fiddle plays the call and the answer (bars 1–2); band in, light; cross-stick",
        "Verse 1": "Acoustic boom-chick, bass on 1 and 3, cross-stick. Steel answers in the gaps",
        "Chorus 1": "SNARE 2 and 4, crash bar 1. Straight-eighth acoustic, steel swells, Tele fills. Bar 1 the call (\u201cI\u2019m your yard man\u201d, up to E), bars 13–14 the call and the ANSWER home on 1",
        "Verse 2": "His daddy. PULL BACK: cross-stick, soft; steel holds under it",
        "Chorus 2": "PIANO IN, offbeats. As chorus 1",
        "Turnaround": "The break: fiddle plays the call and the answer (bars 1–2), steel replies (bar 3). Bar 4: ACOUSTIC ALONE",
        "Verse 3": "Sunday: piano half-note chords and cross-stick to bar 8, then sticks; Tele answers",
        "Chorus 3": "RIDE, crash on each line, fiddle long notes; harmony on lines 2–4 and the hook",
        "Tag": "Bar 1: the call over a STOP (one kick and crash). Bar 2: everyone back for the answer, hold it",
        "Ending": "Fiddle plays the answer home. Last bar: 1, ring it. No fade"}
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
<div class="meta">♩ = 120 &nbsp;·&nbsp; KEY: A major &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: country two-step &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> A major: 1 = A, 2m = Bm, 3m = C♯m, 4 = D, 5 = E, 6m = F♯m; /3 = over the third. One cell is one bar; two numbers in a cell split it, two beats each.
<b>Drums.</b> Two-step: kick 1 and 3, snare 2 and 4, hat eighths. <b>Voices.</b> One singer; a harmony voice on the call and the answer.</div>
</body></html>"""
open("/home/claude/p65/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p65/out/{REC['file_title']} - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
if __name__ == "__main__":
    asyncio.run(main()); print("ok")
