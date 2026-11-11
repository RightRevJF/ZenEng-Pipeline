"""Nothing Else on Earth -- the number chart: D major (1 = D), 4/4, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p40/song_record_d.pkl", "rb"))
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7", "": "N.C."}
BARS = REC["bars"]
FEEL = {"Intro": "MANDOLIN RIFF ALONE for 4 bars (picked eighths over open D and A); acoustic guitar strums in at bar 5 with hand percussion (floor tom 1 and 3, tambourine 2 and 4)",
        "Verse 1": "LARK. Folk: mandolin riff (bars 9-16), acoustic eighths, hand percussion; mandolin strums bars 17-20. No bass, no kit",
        "Pre 1": "floor tom on every beat, building; bass in (half notes); strings swell; drum fill into the chorus (bar 24)",
        "Chorus 1": "BRIAR. THE STORM: the kit (kick 1, 3, 'and' of 3; snare 2 and 4; ride; crash), bass eighths, electric power chords in eighths, strings held, acoustic and mandolin strumming; lead-guitar fills in the gaps",
        "Verse 2": "LARK. As verse 1 (the band drops out)", "Pre 2": "as pre-chorus 1; fill into the chorus (bar 56)", "Chorus 2": "BRIAR, Lark's harmony a third above; tambourine on 2 and 4",
        "Bridge": "LARK. Back to the folk band: acoustic, mandolin strum, hand percussion, strings held, bass whole notes; fill into the break (bar 80)",
        "Riff break": "8-bar lead-guitar solo; the mandolin riff in its first and last two bars; the kit; electric guitar quarters",
        "Last Chorus": "BOTH VOICES, the biggest: tambourine eighths, strings an octave up; bars 101-102 Lark alone ('she sat down hungry'); the tag 'Nothing else on earth' home to D (bars 105-106)",
        "Outro": "MANDOLIN RIFF for 3 bars, floor tom; ONE D CHORD on 1 of bar 110 (everyone who plays); let it ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    cells = [NUM[BARS[b]["roman"]] for b in range(b0, b0 + nb)]
    if s == "Chorus 2": body += f"""<div class="sec"><div class="lab"><span class="name">CHORUS 2</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= Chorus 1</div><div class="drum">{FEEL[s]}</div></div>"""; continue
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
<div class="hdr"><h1>Nothing Else on Earth</h1>
<div class="meta">4/4, ♩ = 116 &nbsp;·&nbsp; KEY: D &nbsp;·&nbsp; FEEL: folk rock after The Battle of Evermore, straight eighths; the band arrives at the chorus &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> D major: 1 = D, 2m = Em, 4 = G, 5 = A, 6m = Bm, ♭7 = C. One chord a bar, root position (power chords on the rhythm guitar). <b>Form.</b> Intro 8 · Verse 12 · Pre 4 · Chorus 16 · Verse 12 · Pre 4 · Chorus 16 · Bridge 8 · Riff break 8 · Last Chorus 18 · Outro 4. The mandolin riff turns on 1 – ♭7 – 4 – 1; the chorus runs 1 – 5 – 6m – 4 under "It used to taste like nothing else on earth"; the last chorus is two bars longer for the tag.</div>
</body></html>"""
open("/home/claude/p40/out_d/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p40/out_d/Nothing Else on Earth (Evermore version) - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
