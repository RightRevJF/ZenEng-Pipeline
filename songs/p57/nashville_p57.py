"""The Singer Doesn't Stop -- the number chart: G major (1 = G), 4/4 at 84, sixteenth strum; the second bridge's first fourteen bars in A (numbers in the new key, marked); a bar with two chords shows both. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p57/song_record.pkl", "rb"))
NUM = {"I": "1", "IV": "4", "V": "5", "vi": "6m", "ii": "2m", "iii": "3m", "": "N.C."}
BARS = REC["bars"]
ROM = {"G": "I", "C": "IV", "D": "V", "Em": "vi", "Am": "ii", "Bm": "iii", "A": "I", "E": "V", "F#m": "vi", "C#m": "iii"}
FEEL = {"Intro": "ACOUSTIC GUITAR ALONE: a soft sixteenth strum",
        "Verse 1": "Guitar alone, soft; the voice close and conversational",
        "Chorus 1": "BASS AND BRUSHES IN: kick on 1 and 3, brush on 2 and 4; still small",
        "Verse 2": "As chorus 1, with a low clean electric swelling the chords",
        "Chorus 2": "= Chorus 1",
        "Bridge": "GUITAR AND VOICE ONLY",
        "Bridge 2": "UP A WHOLE STEP TO A for 14 bars (numbers in A): brushes and bass from bar 5, the kick from bar 9, the electric building; the last two bars back in G (4 5)",
        "Last Chorus": "FULL BUT PLAIN: no gang vocals, no pads; a cymbal swell into bar 1",
        "Tag": "GUITAR ALONE; ONE G CHORD on 1 of bar 88, let ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    def num(c): return NUM[ROM[c.split("/")[0]]]
    cells = [num(BARS[b]["chord"]) if BARS[b]["chord"] == BARS[b]["chord2"] else num(BARS[b]["chord"]) + " " + num(BARS[b]["chord2"]) for b in range(b0, b0 + nb)]
    if s in ("Chorus 2",):
        body += f"""<div class="sec"><div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= {s.replace(" 2", " 1")}</div><div class="drum">{FEEL[s]}</div></div>"""; continue
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
<div class="hdr"><h1>The Singer Doesn't Stop</h1>
<div class="meta">4/4, ♩ = 84, sixteenth strum &nbsp;·&nbsp; KEY: G major (bridge 2 bars 1–14 in A) &nbsp;·&nbsp; FEEL: acoustic modern CCM; small and intimate &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> G major: 1 = G, 2m = Am, 3m = Bm, 4 = C, 5 = D, 6m = Em. Bridge 2, bars 1–14, in A: 1 = A, 4 = D, 5 = E, 6m = F♯m. A cell with two numbers: two beats each. <b>Form.</b> Intro 4 · Verse 8 · Chorus 12 · Verse 8 · Chorus 12 · Bridge 12 · Bridge (up a step) 16 · Last Chorus 12 · Tag 4. <b>Ending.</b> One G chord on the guitar, let ring.</div>
</body></html>"""
open("/home/claude/p57/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p57/out/The Singer Doesn't Stop - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
