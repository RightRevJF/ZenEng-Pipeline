"""Module 11.9 document 2: the Nashville number chart with drummer notes for 'The Seam'. HTML -> PDF, letter landscape.
Numbers in each section's own key (her verses E minor, his verses F minor, the choruses C major, the instrumental and ending F minor);
the key is printed beside each section. One number a bar; the instrumental's bars are 7/8 (2+2+3)."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p22/song_record.pkl", "rb"))
NUMK = {"E minor": {"Em": "1m", "C": "♭6", "Am": "4m"}, "F minor": {"Fm": "1m", "Db": "♭6", "Bbm": "4m", "C": "5", "F": "1"},
        "C major": {"C": "1", "G": "5", "Am": "6m", "F": "4"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "SYNTH LINE · pad", ("Intro", 4): "drums in", ("Verse 1", 0): "HER · half-time", ("Verse 2", 0): "HIM · up a half step",
        ("Chorus 1", 0): "BOTH · crash · ride", ("Interlude", 0): "synth line", ("Verse 3", 0): "HER", ("Verse 4", 0): "HIM",
        ("Chorus 2", 0): "BOTH · crash", ("Instrumental", 0): "7/8 · BUILD: synth, pad", ("Instrumental", 12): "+ bass", ("Instrumental", 24): "+ drums",
        ("Instrumental", 36): "+ everything", ("Instrumental", 47): "tom fill", ("Chorus 3", 0): "BOTH · all in", ("Chorus 3", 7): "WE: her C5 / him A4",
        ("Ending", 0): "HIM ALONE · pad, keys", ("Ending", 5): "F major", ("Outro", 0): "synth line", ("Outro", 7): "F · ring"}
DRUMS = {"Intro": "Synth line and pad for four bars, then half-time: kick on 1, snare on 3, quarter hats.",
         "Verse 1": "Her verse, E minor. Half-time (kick 1, snare 3), quiet eighth hats. Clean guitar arpeggios, Rhodes, the pad. Bass on 1 and 3.",
         "Verse 2": "His verse, F minor -- the same groove a half step up. Bass adds the fifth on 4; muted guitar on the quarters.",
         "Chorus 1": "Both voices (his a third or sixth under hers). Full time: kick 1 and 'and' of 2 and 3, snare 2 and 4, ride; overdriven guitar in eighths; crash on bar 1. SEAM on G4 (her), held.",
         "Interlude": "Synth line over Rhodes and pad; drums out.", "Verse 3": "As verse 1.", "Verse 4": "As verse 2.", "Chorus 2": "As chorus 1.",
         "Instrumental": "48 bars of 7/8 (2+2+3), the quarter steady. A BUILD (synth lead written out as a cue on the lead sheet): bars 1-12 synth, pad and Rhodes; 13-24 + bass (2+2+3 pattern); 25-36 + drums (kick on 1 and 3 of the groups, snare on the second and in the 3-group); 37-48 everything, ride, overdriven guitar; velocities rising; a tom fill in bar 48.",
         "Chorus 3": "Everything. The last line turns: 'the seam won't close, and neither will WE' -- her C5 over his A4, held, crash and china.",
         "Ending": "Him alone, F minor, pad and Rhodes, a bass note a bar; drums out. The last chord F major.", "Outro": "Synth line over pad and Rhodes; the last bar F major, let ring."}
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
.sec {{ break-inside: avoid; margin-bottom: 2px; display: grid; grid-template-columns: 1.5in 5.3in 1fr; gap: 12px;
        border-bottom: 0.5px solid #bbb; padding-bottom: 3px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 9.5pt; }}
.lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .who {{ display: block; font-size: 8pt; font-style: italic; }} .lab .bar {{ font-size: 7.5pt; color: #555; }}
table.nums {{ border-collapse: collapse; }}
table.nums td {{ width: 0.62in; white-space: nowrap; height: 0.15in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 9.5pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7pt; line-height: 1.12; }} .cue {{ font-size: 6.8pt; font-variant: small-caps; font-weight: bold; }}
.foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>The Seam</h1>
<div class="meta">NUMBERS IN EACH SECTION'S KEY &nbsp;·&nbsp; 4/4 ♩ = 80 (instrumental 7/8) &nbsp;·&nbsp; FEEL: prog rock, a duet, half-time verses &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> In each section's key, printed beside it. E minor: 1m = Em, ♭6 = C, 4m = Am. F minor: 1m = Fm, ♭6 = D♭, 4m = B♭m, 5 = C, 1 = F (major).
C major: 1 = C, 5 = G, 6m = Am, 4 = F. <b>Keys.</b> Her verses E minor; his a half step up, F minor; the C chord that ends each verse leads into the C major chorus.
<b>Voices.</b> Her A3–B4 (C5 once); him E3–G4 (A4 once). <b>The synth lines</b> (intro, interlude, instrumental, outro) are written out as a cue on the lead sheet.</div>
</body></html>"""
open("/home/claude/p22/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p22/out/The Seam - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.25in", bottom="0.2in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
