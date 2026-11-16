"""The Man Mama Prayed I'd Be -- the number chart: G major (1 = G), q = 120, a two-step, all 4/4; one cell a bar; a bar with two chords
shows both. Every section's notes are read from the record (where the stop falls, the hook's bars). HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p64/song_record.pkl", "rb"))
BARS = REC["bars"]
RN = {"G": "1", "A": "2", "B": "3", "C": "4", "D": "5", "E": "6", "F#": "7", "F": "♭7"}
QN = {"": "", "m": "m", "7": "7", "m7": "m7", "sus4": "sus4", "sus2": "sus2", "maj7": "maj7"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return RN[rt_] + QN[base[len(rt_):]] + (f"/{RN[bs]}" if bs else "")
B0 = {s: st // 48 for s, nb, st, mets, mv in REC["plan"]}
stop_k = REC["breath"]["bar"] - B0["Verse 4"] + 1
FEEL = {"Intro": "Fiddle plays the hook (bars 1–2); band in, light; cross-stick",
        "Verse 1": "Acoustic boom-chick, bass on 1 and 3, cross-stick. Steel answers in the gaps",
        "Chorus 1": "SNARE 2 and 4, crash bar 1. Straight-eighth acoustic, steel swells, Tele fills in the gaps. Hook bars 11–12: 1 then 5, the line stops OPEN on 5",
        "Verse 2": "Sticks. Tele answers at the line ends",
        "Chorus 2": "PIANO IN, offbeats. As chorus 1",
        "Verse 3": "As verse 2; steel and Tele trade the gaps",
        "Chorus 3": "RIDE. Fiddle long notes; harmony on lines 2–4 and the hook",
        "Turnaround": "Fiddle plays the hook (bars 1–2), steel answers (bars 3–4); fill in bar 4",
        "Verse 4": f"Thin: cross-stick to bar 8, then sticks, steel swelling. BAR {stop_k}: EVERYONE STOPS ON BEAT 3 (after “kiss”)",
        "Chorus 4": "HER CHORUS. Everything in, ride, crash on each line. Bar 12: 5 to 1 in the bar, the hook HOME on 1; he sings under her",
        "Tag": "Both voices. Bars 2 and 4: 5 to 1 in the bar. Band easing, cross-stick from bar 3",
        "Ending": "Fiddle plays the hook, home on G. Last bar: 1, ring it. No fade"}
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
<div class="meta">♩ = 120 &nbsp;·&nbsp; KEY: G major &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: country two-step &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> G major: 1 = G, 2m = Am, 3m = Bm, 4 = C, 5 = D, 6m = Em; /3 = over the third. One cell is one bar; two numbers in a cell split it, two beats each.
<b>Drums.</b> Two-step: kick 1 and 3, snare 2 and 4, hat eighths. <b>Voices.</b> He sings verses 1–4 and choruses 1–3; she sings chorus 4; both in the tag.</div>
</body></html>"""
open("/home/claude/p64/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p64/out/{REC['file_title']} - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
if __name__ == "__main__":
    asyncio.run(main()); print("ok")
