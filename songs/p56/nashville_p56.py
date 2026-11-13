"""Dry Ground -- the number chart: A minor (1m = A minor), 4/4 at 118, four on the floor; a bar with two chords shows both. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p56/song_record.pkl", "rb"))
NUM = {"i": "1m", "VI": "♭6", "III": "♭3", "VII": "♭7", "iv": "4m", "v": "5m", "V": "5", "": "N.C."}
BARS = REC["bars"]
ROM = {"Am": "i", "F": "VI", "C": "III", "G": "VII", "Dm": "iv", "Em": "v", "E": "V"}
FEEL = {"Intro": "RAIN and the low HUM; pad and arpeggio (eighths) in at bar 5 with the kick on every beat and closed hats",
        "Verse 1": "UNDERWATER: kick on every beat, closed hats, the band filtered; bass, pad (sidechained), arpeggio in eighths; no claps",
        "Pre 1": "CLAPS on 2 and 4; still filtered; snare build through the last bar",
        "Chorus 1": "OPEN WIDE: crash on 1, off-beat open hats, claps, arpeggio in sixteenths, pad an octave up; the last line's 'flood' held two bars",
        "Verse 2": "As verse 1; claps from bar 3", "Pre 2": "As pre 1", "Chorus 2": "= Chorus 1",
        "Bridge": "THE DRY GROUND: the kick OUT; pad and bass; the arpeggio back for the last four bars; snare build in the last two (eighths, then sixteenths)",
        "Last Chorus": "EVERYTHING: crash on 1 and bar 9; the last 'flood' in falsetto (B4), held two bars",
        "Outro": "Kick for four bars, then out: THE HUM AND RAIN; ONE A MINOR CHORD on 1 of bar 120, let ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    def num(c): return NUM[ROM[c.split("/")[0]]] + ("/" + c.split("/")[1] if "/" in c else "")
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
<div class="hdr"><h1>Dry Ground</h1>
<div class="meta">4/4, ♩ = 118, straight &nbsp;·&nbsp; KEY: A minor &nbsp;·&nbsp; FEEL: atmospheric pop, four on the floor; verses underwater, choruses open &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> A minor: 1m = Am, ♭3 = C, 4m = Dm, 5m = Em, 5 = E, ♭6 = F, ♭7 = G. A cell with two numbers: two beats each. <b>Form.</b> Intro 8 · Verse 10 · Pre 10 · Chorus 16 · Verse 10 · Pre 10 · Chorus 16 · Bridge 12 · Last Chorus 16 · Outro 12. Lines run three bars where the words are long, so the verses and pre-choruses are ten bars, not eight. <b>Ending.</b> One A minor chord, let ring under the rain.</div>
</body></html>"""
open("/home/claude/p56/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p56/out/Dry Ground - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
