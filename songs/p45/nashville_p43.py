"""Blue Movie -- the number chart: A minor (1m = A minor), 4/4 at 118, four on the floor, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p45/song_record.pkl", "rb"))
NUM = {"i": "1m", "VI": "♭6", "III": "♭3", "VII": "♭7", "iv": "4m", "v": "5m", "V": "5", "": "N.C."}
BARS = REC["bars"]
FEEL = {"Intro": "PLUCK: the 'blue movie' figure; pad and bass in at bar 5 with kick on every beat and off-beat open hats",
        "Verse 1": "Kick on every beat, off-beat open hats, synth bass eighths (root and octave), pad; no claps",
        "Pre 1": "CLAPS on 2 and 4; snare build through the last bar",
        "Chorus 1": "FULL: crash on 1, claps, sixteenth hats, pad an octave up", "Post 1": "THE CHANT: the pluck doubles the figure an octave up",
        "Verse 2": "As verse 1, with claps on 2 and 4", "Pre 2": "As pre 1", "Chorus 2": "= Chorus 1", "Post 2": "= Post 1",
        "Bridge": "DRUMS OUT: pad and bass in whole notes; the snare build in bars 7-8 (eighths, then sixteenths)",
        "Last Chorus": "EVERYTHING: the pluck plays the figure under the whole chorus; crash on 1 and bar 5", "Post 3": "THE FILM STILL LOOPS: pad and held bass; kick back for the last 2 bars only; sung softer",
        "Outro": "The figure, kick and hats; ONE A MINOR CHORD on 1 of bar 80 with a crash, let ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    cells = [NUM[BARS[b]["roman"]] for b in range(b0, b0 + nb)]
    if s in ("Chorus 2", "Post 2"):
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
<div class="hdr"><h1>Blue Movie</h1>
<div class="meta">4/4, ♩ = 118, straight &nbsp;·&nbsp; KEY: A minor &nbsp;·&nbsp; FEEL: dance-pop, four on the floor; the plucked figure is the hook &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> A minor: 1m = Am, ♭3 = C, 4m = Dm, 5m = Em, 5 = E, ♭6 = F, ♭7 = G. One chord a bar. <b>Form.</b> Intro 8 · Verse 8 · Pre 4 · Chorus 8 · Post 4 · Verse 8 · Pre 4 · Chorus 8 · Post 4 · Bridge 8 · Last Chorus 8 · Post 4 · Outro 4. The chorus runs ♭6 – ♭7 – 1m – ♭3 – ♭6 – ♭7 – ♭6 – ♭7; “blue movie, blue movie” falls over ♭6 – ♭7 (bars 5-6). <b>Voice.</b> Light tenor; every line. The last post-chorus is the quiet one.</div>
</body></html>"""
open("/home/claude/p45/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p45/out/Blue Movie - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
