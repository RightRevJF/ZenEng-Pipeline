"""The First Wood -- the number chart: F major (1 = F), 3/4, the chords of the tune with their bass notes (1/3 = the tonic over its
third); the introduction and the four stanzas with the arrangement. HTML -> PDF, letter landscape."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p35/song_record.pkl", "rb"))
NUM = {"I": "1", "ii": "2m", "iii": "3m", "IV": "4", "V": "5", "V7": "5⁷", "vi": "6m", "vii": "7°", "I64": "1"}
ROOT = {"I": 5, "ii": 7, "iii": 9, "IV": 10, "V": 0, "V7": 0, "vi": 2, "vii": 4, "I64": 5}
DEG = {5: "1", 7: "2", 9: "3", 10: "4", 0: "5", 2: "6", 4: "7"}
def name(v): return NUM[v["chord"]] + ("" if v["bass"] % 12 == ROOT[v["chord"]] else "/" + DEG[v["bass"] % 12])
V = REC["voices"]
def bar_cells(b0, b1):
    cells = []
    for b in range(b0, b1):
        cs = [v for v in V if b * 36 <= v["on"] < (b + 1) * 36]
        held = [v for v in V if v["on"] < b * 36 < v["end"]]
        txt = []
        for v in cs:
            beat = (v["on"] % 36) // 12 + 1
            txt.append(name(v) if beat == 1 else f"<sup>{beat}</sup>{name(v)}")
        if not cs and held: txt = ["·"]
        if held and cs and cs[0]["on"] % 36 != 0: txt.insert(0, "·")
        cells.append(" ".join(txt))
    return cells
pick = [v for v in V if v["on"] < 0]
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
LINES = [("Line 1", 0, 4), ("Line 2", 4, 8), ("Line 3", 8, 12), ("Line 4", 12, 16), ("Refrain 1", 16, 20), ("Refrain 2", 20, 24)]
body = f"""<div class="sec"><div class="lab"><span class="name">INTRO</span> <span class="bars">8</span><span class="who">organ: the refrain</span><div class="bar">bars 1–8</div></div>
<table class="nums">{rows(bar_cells(16, 24))}</table><div class="drum">The organ plays the refrain (the tune's bars 17–24); its last bar ends on beat 2, and beat 3 is the pickup to stanza 1 ({name(pick[0])}).</div></div>"""
body += f"""<div class="sec"><div class="lab"><span class="name">STANZA</span> <span class="bars">24</span><span class="who">×4, pickup {name(pick[0])}</span><div class="bar">bars 9–104</div></div>
<table class="nums">{rows(bar_cells(0, 24))}</table><div class="drum">Lines 1–4 (Common Metre), then the refrain (bar 17 on). Line ends: 1, 2 and 3 on 5 (half closes) or 1 with 3 on top; line 4 and the refrain's end on 5⁷–1. The refrain's first chord after bar 16's rest: {name([v for v in V if v['on'] == 16 * 36][0])}.</div></div>"""
ARR = "Stanza 1: the choir in unison, the organ in four parts. Stanza 2: four parts with the organ. Stanza 3: four parts, the organ tacet. Stanza 4: full organ, the tune doubled an octave higher."
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }} .hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 6px; display: grid; grid-template-columns: 1.5in 6.2in 1fr; gap: 12px; border-bottom: 0.5px solid #bbb; padding-bottom: 6px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }} .lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .who {{ display: block; font-size: 8pt; font-style: italic; }} .lab .bar {{ font-size: 7.5pt; color: #555; }}
table.nums {{ border-collapse: collapse; }} table.nums td {{ width: 0.74in; white-space: nowrap; height: 0.2in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }} sup {{ font-size: 6.5pt; font-weight: normal; color: #555; }}
.drum {{ font-size: 7.8pt; line-height: 1.2; }} .foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>The First Wood</h1>
<div class="meta">3/4, ♩ = 92 &nbsp;·&nbsp; KEY: F &nbsp;·&nbsp; FEEL: a carol, choir (SATB) and organ &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> F major: 1 = F, 2m = Gm, 3m = Am, 4 = B♭, 5 = C, 6m = Dm, 7° = E°. A slash gives the bass: 1/3 is F over A, 5⁷/7 is C7 over E. A small figure before a chord is the beat it falls on (no figure: beat 1); · means the chord holds. <b>Arrangement.</b> {ARR}</div>
</body></html>"""
open("/home/claude/p35/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p35/out/The First Wood - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
