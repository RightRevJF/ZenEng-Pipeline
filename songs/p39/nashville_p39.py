"""Fixed by Fall -- the number chart: A major (1 = A), 4/4, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p39/song_record.pkl", "rb"))
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7"}
BARS = REC["bars"]
FEEL = {"Intro": "SHUFFLE. Boogie guitar (root-fifth, root-sixth) and drums; the lead guitar's tune; bass waits for the verse",
        "Verse 1": "shuffle: kick 1 and 3, snare 2 and 4, swung hats; bass boogie (root, root, 5, 5, 6, 6, 5, 5); piano on the 'and's; fill in the last bar",
        "Chorus 1": "STRAIGHT: a rally march. Kick on every beat, marching snare, ride eighths; open guitar and piano in straight eighths; crash on 1",
        "Verse 2": "as verse 1 (shuffle)", "Chorus 2": "as chorus 1 (straight), sung flatter",
        "Bridge": "shuffle, pulled back: held power chords and piano, half-note bass",
        "Solo": "8-bar guitar solo over the chorus changes, but SHUFFLE on the ride; guitar holds, piano out",
        "Last Chorus": "STRAIGHT, full: tambourine, crash every 4 bars; the duet (one singer, two tracks); bars 85–86 the tag 'Fixed by fall'",
        "Outro": "shuffle: the intro tune; ONE HIT on 1 of bar 90"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    cells = [NUM[BARS[b]["roman"]] for b in range(b0, b0 + nb)]
    if s == "Chorus 2": body += f"""<div class="sec"><div class="lab"><span class="name">CHORUS 2</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= Chorus 1</div><div class="drum">{FEEL[s]}</div></div>"""; continue
    if s == "Verse 2":
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
<div class="hdr"><h1>Fixed by Fall</h1>
<div class="meta">4/4, ♩ = 108 &nbsp;·&nbsp; KEY: E &nbsp;·&nbsp; FEEL: shuffle (swung eighths); the choruses straight, a march &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> E major: 1 = E, 2m = F♯m, 4 = A, 5 = B, 6m = C♯m, ♭7 = D. One chord a bar, root position. <b>Form.</b> Intro 4 · Verse 16 · Chorus 8 · Verse 16 · Chorus 8 · Bridge 8 · Solo 8 · Last Chorus 18 · Outro 4. The chorus opens 1 – 4 – ♭7 – 4 under "Vote for me, I'll fix it all" twice (the second a step down, over ♭7); the last chorus is the chorus twice plus a two-bar tag.</div>
</body></html>"""
open("/home/claude/p39/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p39/out/Fixed by Fall - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
