"""Dance Anyway -- the number chart: E-flat major (1 = E-flat), 4/4, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p36/song_record.pkl", "rb"))
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "bVII": "♭7", "ii": "2m"}
BARS = REC["bars"]
FEEL = {"Intro": "keys and the synth riff (beats 3–4 of each bar); drums and bass in at bar 3",
        "Verse 1": "four on the floor, eighth hats, clap 2 and 4; bass root and octave in quarters; keys stab the 'and' of 2 and 4; no guitar",
        "Pre 1": "pad in; guitar in (muted sixteenths); snare build in bar 16",
        "Chorus 1": "crash; sixteenth hats, open on every 'and'; disco octaves in eighths; keys stab every 'and'; the synth riff answers each line (beats 3–4 of every second bar)",
        "Verse 2": "as verse 1, with the guitar", "Pre 2": "as pre-chorus 1; build in bar 44", "Chorus 2": "as chorus 1",
        "Bridge": "the floor drops: kick on 1 and 3, bass and keys held, through bar 66; hats from bar 65; quarters and a snare build in bars 67–68",
        "Last Chorus": "full; pad an octave up; crash every 4 bars", "Outro": "the chorus groove; the synth riff in bars 85–87; one hit on 1 in bar 88"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    cells = [NUM[BARS[b]["roman"]] for b in range(b0, b0 + nb)]
    if s == "Chorus 2": body += f"""<div class="sec"><div class="lab"><span class="name">CHORUS 2</span> <span class="bars">16</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= Chorus 1</div><div class="drum">{FEEL[s]}</div></div>"""; continue
    if s == "Verse 2" or s == "Pre 2":
        body += f"""<div class="sec"><div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= {s.replace('2', '1')}</div><div class="drum">{FEEL[s]}</div></div>"""; continue
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
<div class="hdr"><h1>Dance Anyway</h1>
<div class="meta">4/4, ♩ = 118 &nbsp;·&nbsp; KEY: E♭ &nbsp;·&nbsp; FEEL: four-on-the-floor disco-pop &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> E♭ major: 1 = E♭, 2m = Fm, 4 = A♭, 5 = B♭, 6m = Cm, ♭7 = D♭. One chord a bar, all in root position. <b>Form.</b> Intro 4 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Last Chorus 16 · Outro 4. The chorus's ♭7 (bar 15 of it) is the only time D♭ appears outside the bridge.</div>
</body></html>"""
open("/home/claude/p36/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p36/out/Dance Anyway - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
