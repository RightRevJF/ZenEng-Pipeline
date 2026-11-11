"""Nothing Important -- the number chart: B-flat major (1 = B-flat), 4/4 straight eighths, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p42/song_record.pkl", "rb"))
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "iii": "3m", "": "N.C."}
BARS = REC["bars"]
FEEL = {"Intro": "PIANO ALONE: the right-hand figure over half notes",
        "Verse 1": "Piano: broken chords in eighths under the voice; left hand root and fifth in half notes",
        "Chorus 1": "Piano: broken chords a step higher; left hand in quarters (root, fifth, octave, fifth)",
        "Verse 2": "As verse 1; CELLO in, held notes", "Chorus 2": "As chorus 1, cello held",
        "Bridge": "THE LAST NIGHT: half-note chords over whole notes; the cello's countermelody in the voice's gaps",
        "Verse 3": "THREE DAYS: bars 1-4 one held chord a bar, cello out; bars 5-8 the broken chords return, cello held",
        "Last Chorus": "THE BAND, bars 1-10 only: bass, clean guitar arpeggios, brushes (1-6) then sticks (7-10); cello countermelody; bars 11-12 ('I'll call you back') piano alone, quiet",
        "Outro": "PIANO ALONE: the figure for 3 bars; ONE B-FLAT CHORD on 1 of bar 68, let ring"}
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
<div class="hdr"><h1>Nothing Important</h1>
<div class="meta">4/4, ♩ = 76, straight eighths &nbsp;·&nbsp; KEY: B♭ &nbsp;·&nbsp; FEEL: piano ballad; the piano carries the whole song; the band only in the last chorus &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> B♭ major: 1 = B♭, 2m = Cm, 3m = Dm, 4 = E♭, 5 = F, 6m = Gm. One chord a bar. <b>Form.</b> Intro 4 · Verse 8 · Chorus 8 · Verse 8 · Chorus 8 · Bridge 8 · Verse 8 · Last Chorus 12 · Outro 4. The chorus runs 4 – 5 – 6m – 4 – 2m – 5 – 1 – 1; the last chorus holds 2m – 5 under “Nothing important” and comes home 1 – 1 under “I'll call you back.” <b>Voice.</b> Alto; every line.</div>
</body></html>"""
open("/home/claude/p42/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p42/out/Nothing Important - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
