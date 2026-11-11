"""The Water Used to Sing -- the number chart: G major (1 = G), 4/4 swung shuffle, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p41/song_record.pkl", "rb"))
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7", "": "N.C."}
BARS = REC["bars"]
FEEL = {"Intro": "Acoustic shuffle and the electric lick from bar 1 (the lick on 1 – 4 – 1 – 5); bass and BRUSHES in at bar 5",
        "Verse 1": "Brushes (kick 1 and 3, tap 2 and 4, swirl); bass root and fifth in half notes; acoustic shuffle. No organ",
        "Pre 1": "As the verse; organ swells in bars 19-20; brush fill in bar 20",
        "Chorus 1": "STICKS: kick 1, 3, and-of-4; snare 2 and 4; hats swung; crash. Bass boogie (R 3 5 6); electric chops on 2 and 4; organ held; electric fills in the voice's gaps",
        "Verse 2": "Brushes; organ held chords enter", "Pre 2": "Organ swells; brush fill in bar 40", "Chorus 2": "As chorus 1, a little bigger",
        "Bridge": "THE DRY VALLEY: acoustic in half-note strokes; bass whole notes; brushes sparse; organ a low open fifth. No electric",
        "Break": "THE GATE: 8-bar electric solo (the lick, a step up, four bars rising, the lick); sticks; boogie bass; chops low",
        "Verse 3": "Brushes for 4 bars; STICKS and the band from bar 77 ('then the whole lake leaned against the gate')",
        "Last Chorus": "THE BIGGEST: ride; crash every 4 bars; organ countermelody above the voice, chords low; the tag 'It sings.' (bar 96) held into the outro",
        "Outro": "The lick and the band for 7 bars; ONE G CHORD on 1 of bar 104, let it ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    cells = [NUM[BARS[b]["roman"]] for b in range(b0, b0 + nb)]
    if s == "Chorus 2" and False: body += f"""<div class="sec"><div class="lab"><span class="name">CHORUS 2</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= Chorus 1</div><div class="drum">{FEEL[s]}</div></div>"""; continue
    if s == "Chorus 2":
        body += f"""<div class="sec"><div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= Chorus 1</div><div class="drum">{FEEL[s]}</div></div>"""; continue
    body += f"""<div class="sec"><div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div>
<table class="nums">{rows(cells)}</table><div class="drum">{FEEL[s]}</div></div>"""
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }} .hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 5px; display: grid; grid-template-columns: 1.4in 6.2in 1fr; gap: 12px; border-bottom: 0.5px solid #bbb; padding-bottom: 5px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }} .lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .bar {{ font-size: 7.5pt; color: #555; }} .nums2 {{ font-size: 11pt; font-weight: bold; }}
table.nums {{ border-collapse: collapse; }} table.nums td {{ width: 0.74in; white-space: nowrap; height: 0.2in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10.5pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.8pt; line-height: 1.2; }} .foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>The Water Used to Sing</h1>
<div class="meta">4/4 SHUFFLE (swung eighths), ♩ = 96 &nbsp;·&nbsp; KEY: G &nbsp;·&nbsp; FEEL: Americana rock; brushes in the verses, sticks from the chorus &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> G major: 1 = G, 2m = Am, 4 = C, 5 = D, 6m = Em, ♭7 = F. One chord a bar. <b>Form.</b> Intro 8 · Verse 8 · Pre 4 · Chorus 8 · Verse 8 · Pre 4 · Chorus 8 · Bridge 12 · Break 8 · Verse 12 · Last Chorus 16 · Outro 8. The chorus runs 4 – 1 – 6m – 5 – 4 – 1 – ♭7 – 1; the ♭7 (F) is the shine. Verse 3 is the verse stretched to 12 bars (two bars a line). <b>Voice.</b> Baritone; every line.</div>
</body></html>"""
open("/home/claude/p41/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p41/out/The Water Used to Sing - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
