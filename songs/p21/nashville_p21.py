"""Module 11.9 document 2: the Nashville number chart with drummer notes for 'Make Do'. HTML -> PDF, letter landscape.
Numbers in G (1 = G, 2m = Am, 3m = Bm, 4 = C, 5 = D, 6m = Em); the sevenths printed. One number a bar."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p21/song_record.pkl", "rb"))
NUM = {"Gmaj7": "1maj7", "Cmaj7": "4maj7", "D": "5", "Em7": "6m7", "Am7": "2m7", "G": "1"}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "CLEAN LINE (cue)", ("Intro", 2): "machine in", ("Verse 1", 0): "arpeggios", ("Chorus 1", 0): "open up",
        ("Chorus 1", 7): "DO = B3", ("Chorus 2", 7): "DO = B3", ("Break", 0): "THE LINE (cue) · thin", ("Break", 9): "line's peak",
        ("Verse 3", 0): "arpeggios", ("Chorus 3", 7): "DO = D4 · crash", ("Outro", 0): "clean line", ("Outro", 3): "ring"}
DRUMS = {"Intro": "The clean-guitar line alone with the pad for two bars, then the machine: kick on 1, a soft rim on 3, quiet eighth hats.",
         "Verse 1": "Machine: kick on 1, rim on 3, quiet eighth hats. Bass whole notes. Clean guitar ringing eighth arpeggios. The voice low and close (B2-A3).",
         "Chorus 1": "Open up: snare (long tail) on 3, a splash on bar 1, a second guitar holding the shapes, the pad louder. 'the afternoon will have to make DO' -- DO on B3, held.",
         "Verse 2": "As verse 1.", "Chorus 2": "As chorus 1.",
         "Break": "12 bars 'where the light comes in': the instrumental line (cue on the lead sheet) on clean guitar; the arpeggios drop out, the machine and bass stay, the pad up a little. The line peaks on E5 in its last phrase.",
         "Verse 3": "As verse 1.", "Chorus 3": "As chorus 1; the last DO on D4 with a crash.",
         "Outro": "The clean line over Gmaj7 / Cmaj7; the last bar a Gmaj7 chord, let ring."}
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    chs = [b["chord"] for b in REC["bars"][b0:b0 + nb]]
    ns = [NUM[c] + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, c in enumerate(chs)]
    key = REC["bars"][b0]["key"]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · {key}</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 4)}</table><div class="drum">{html.escape(DRUMS[s])}</div></div>"""
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 10.5pt; font-weight: bold; }}
.hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 2px; display: grid; grid-template-columns: 1.5in 5.3in 1fr; gap: 12px;
        border-bottom: 0.5px solid #bbb; padding-bottom: 3px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 9.5pt; }}
.lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .who {{ display: block; font-size: 8pt; font-style: italic; }} .lab .bar {{ font-size: 7.5pt; color: #555; }}
table.nums {{ border-collapse: collapse; }}
table.nums td {{ width: 1.0in; white-space: nowrap; height: 0.18in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10.5pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.8pt; line-height: 1.2; }} .cue {{ font-size: 6.8pt; font-variant: small-caps; font-weight: bold; }}
.foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>Make Do</h1>
<div class="meta">NUMBERS IN G &nbsp;·&nbsp; 4/4 ♩ = 72 &nbsp;·&nbsp; FEEL: dream-pop, a slow drum machine, ringing guitars, lots of air &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant (ZenEng v64) · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> In G: 1 = G, 2m = Am, 4 = C, 5 = D, 6m = Em; maj7 and m7 as printed. One number a bar. <b>Voice.</b> Baritone, B2 to A3 in the
verses, B3 on each chorus DO, D4 once on the last. <b>The intro, break and outro lines</b> are written out for clean guitar as a cue on the lead sheet.</div>
</body></html>"""
open("/home/claude/p21/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p21/out/Make Do - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.3in", left="0.5in", right="0.5in"), print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
