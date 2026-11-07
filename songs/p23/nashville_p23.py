"""Module 11.9 document 2: the Nashville number chart with drummer notes for 'What Holds'. HTML -> PDF, letter landscape.
Numbers in each section's own key (the riff and the verses E minor; the choruses and the bridge G major); one number a bar."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p23/song_record.pkl", "rb"))
NUMK = {"E minor": {"Em": "1m", "C": "♭6", "D": "♭7"}, "G major": {"G": "1", "D": "5", "Em": "6m", "C": "4", "Am": "2m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "RIFF ALONE", ("Intro", 4): "band in", ("Verse 1", 0): "VOICE · tight", ("Chorus 1", 0): "crash · open",
        ("Chorus 1", 7): "STAND", ("Riff", 0): "RIFF · crash", ("Verse 2", 0): "tight", ("Chorus 2", 0): "crash · open",
        ("Bridge", 0): "BUILD", ("Bridge", 6): "snare 8ths", ("Chorus 3", 0): "BAND OUT", ("Chorus 3", 7): "snare build",
        ("Chorus 4", 0): "ALL IN · crash", ("Chorus 4", 7): "STAND A4 · crash+china", ("Chorus 4", 8): "HOLDS · crash", ("Chorus 4", 9): "tom fill",
        ("Outro", 0): "RIFF · crash", ("Outro", 7): "hit · ring"}
DRUMS = {"Intro": "Riff guitar alone for four bars. Then the band: kick on 1, the 'and' of 2 and 3; snare 2 and 4; eighth hats. Every chord change is pushed: the band hits the next chord on the 'and' of 4.",
         "Verse 1": "Coiled. Kick 1 and the 'and' of 2, snare 2 and 4, closed eighth hats. Bass and palm-muted guitar locked on 1, the 'and' of 2, 3 and 4; the push into each new chord. Organ low.",
         "Chorus 1": "Released. Crash on bar 1, ride eighths, kick 1, the 'and' of 2 and 3, snare 2 and 4. Open power chords and bass in straight eighths, the changes pushed. HOLDS and STAND on G4.",
         "Riff": "The riff over the full band; crash on bar 1, open hats.", "Verse 2": "As verse 1.", "Chorus 2": "As chorus 1.",
         "Bridge": "A build over 8 bars: kick quarters with floor tom (1-2); the backbeat and hats (3-4); snare on every beat (5-6); snare eighths, rising (7-8). Bass quarters then eighths; guitar eighths, full chords in 7-8.",
         "Chorus 3": "Band out. Clean guitar rings one chord a bar, organ soft. A snare build in the last bar.",
         "Chorus 4": "Everything, crash on bar 1. The last line spreads over four bars: STAND on A4 over D (crash and china), HOLDS on G (crash), a tom fill into the outro.",
         "Outro": "The riff over the full band; the last bar one hit on E minor, let ring."}
def num(sec, ch):
    k = next(b["key"] for b in REC["bars"] if b["sec"] == sec); return NUMK[k][ch]
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    chs = [b["chord"] for b in REC["bars"][b0:b0 + nb]]
    ns = [num(s, c) + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, c in enumerate(chs)]
    key = REC["bars"][b0]["key"]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · {key}</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 8)}</table><div class="drum">{html.escape(DRUMS[s])}</div></div>"""
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }}
.hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 3px; display: grid; grid-template-columns: 1.5in 5.3in 1fr; gap: 12px;
        border-bottom: 0.5px solid #bbb; padding-bottom: 4px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }}
.lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .who {{ display: block; font-size: 8pt; font-style: italic; }} .lab .bar {{ font-size: 7.5pt; color: #555; }}
table.nums {{ border-collapse: collapse; }}
table.nums td {{ width: 0.62in; white-space: nowrap; height: 0.17in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.6pt; line-height: 1.15; }} .cue {{ font-size: 6.8pt; font-variant: small-caps; font-weight: bold; }}
.foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>What Holds</h1>
<div class="meta">NUMBERS IN EACH SECTION'S KEY &nbsp;·&nbsp; 4/4 ♩ = 104 &nbsp;·&nbsp; FEEL: driving rock, every change pushed an eighth early &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> E minor: 1m = Em, ♭6 = C, ♭7 = D. G major: 1 = G, 5 = D, 6m = Em, 4 = C, 2m = Am. One key signature throughout (one sharp):
the D that ends each verse line pulls into the G major chorus. <b>The push.</b> Bass and rhythm guitar play each new chord on the 'and' of 4 and tie it over the bar line.
<b>Voice.</b> E3–G4; A4 once, on the last "stand". <b>The riff</b> (intro, after chorus 1, outro) is written out as a cue on the lead sheet and in the parts.</div>
</body></html>"""
open("/home/claude/p23/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p23/out/What Holds - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.95, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
