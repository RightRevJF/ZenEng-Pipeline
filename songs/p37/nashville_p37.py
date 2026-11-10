"""Windows Down -- the number chart: A major (1 = A), 4/4, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p37/song_record.pkl", "rb"))
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "iii": "3m"}
BARS = REC["bars"]
FEEL = {"Intro": "lead guitar's hook alone for 4 bars, then the band: drums, bass eighths, muted power chords",
        "Verse 1": "kick 1, 3 and the 'and' of 3; snare 2 and 4; eighth hats; bass driving eighths on the root; rhythm guitar palm-muted eighths",
        "Pre 1": "organ in; guitars open up; tom fill in bar 20",
        "Chorus 1": "crash; ride in eighths; open power chords; bass octave on the 'and' of 4; the lead guitar's hook in the holds after lines 2, 4, 6 and 8",
        "Verse 2": "as verse 1", "Pre 2": "as pre-chorus 1; fill in bar 48", "Chorus 2": "as chorus 1",
        "Bridge": "half-time: kick 1, snare 3, held chords and half-note bass through bar 70; snare build bars 71–72",
        "Solo": "16-bar guitar solo over the chorus changes; hats for 8 bars, then the ride and the organ (bar 81)",
        "Last Chorus": "full; organ voiced higher; open hat on every 'and'; crash every 4 bars", "Outro": "the chorus changes with the lead guitar's hook; one hit on 1 in bar 112"}
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
<div class="hdr"><h1>Windows Down</h1>
<div class="meta">4/4, ♩ = 122 &nbsp;·&nbsp; KEY: A &nbsp;·&nbsp; FEEL: heartland rock, straight eighths &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> A major: 1 = A, 2m = Bm, 4 = D, 5 = E, 6m = F♯m. One chord a bar, all in root position (power chords on the rhythm guitar). <b>Form.</b> Intro 8 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Solo 16 · Last Chorus 16 · Outro 8. Each chorus is the 8-bar chorus twice; its line 4 opens on 4 (the singer's top note, F♯) and lands on 1.</div>
</body></html>"""
open("/home/claude/p37/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p37/out/Windows Down - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
