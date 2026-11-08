"""Module 11.9 document 2: the Nashville number chart with band notes for 'Nothing On'. HTML -> PDF, letter landscape.
Numbers in F major; one number a bar of 4/4. The home chord (1) appears only in the bridge."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p31/song_record.pkl", "rb"))
NUMK = {"F major": {"Gm7": "2m7", "Am7": "3m7", "Bbmaj7": "4maj7", "C": "5", "F": "1", "Am": "3m", "Bb": "4"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "RIFF", ("Intro", 2): "+ BAND", ("Verse 1", 0): "VOICE", ("Pre 1", 0): "4 on floor",
        ("Pre 1", 3): "TAPE STOP", ("Chorus 1", 0): "◇ OUT", ("Chorus 1", 1): "CRASH", ("Chorus 1", 7): "pickup",
        ("Post 1", 0): "bongos", ("Verse 2", 0): "riff ans.", ("Pre 2", 0): "horns", ("Pre 2", 3): "TAPE STOP",
        ("Chorus 2", 0): "◇ OUT", ("Chorus 2", 1): "CRASH", ("Chorus 2", 7): "pickup", ("Post 2", 0): "bongos",
        ("Bridge", 0): "HUM", ("Bridge", 2): "+ bass", ("Bridge", 4): "+ kick", ("Bridge", 6): "build",
        ("Bridge", 7): "HIT · OUT", ("Chorus 3", 0): "◇ OUT", ("Chorus 3", 1): "CRASH",
        ("Chorus 3", 4): "D5 “off”", ("Post 3", 4): "STRIP", ("Outro", 0): "RIFF", ("Outro", 1): "END"}
NOTES = {"Intro": "Bars 1–2: the riff guitar (the title's tune with sixteenth fills) over sixteenth hats; a snare pickup into bar 3. Bar 3: kit, bass, muted guitar on the off-beats, Rhodes.",
         "Verse 1": "The loop 2m7–3m7, never 1. Kick 1, the a of 2, 3; snare 2 and 4 with ghosts; sixteenth hats. Bass: syncopated root line. Guitar: off-beat eighths. Rhodes holds the chord.",
         "Pre 1": "4maj7–5. Four on the floor, open hats on the off-beats, bass in octaves, guitar in sixteenths. Bar 4: snare eighths to beat 3, then a TAPE STOP (everything bends down) and the band is OUT on 'breathe'.",
         "Chorus 1": "Bar 1: SILENT — she sings 'nothing on, nothing on' alone. Bar 2: crash, everyone in: four on the floor, snare and claps on 2 and 4, open hats on the off-beats, disco octave bass, sixteenth guitar, Rhodes stabs, horn stabs on 4 and its and where she holds.",
         "Post 1": "The post-chorus hook. Groove stays; bongos; horn stabs; the backing echo '(nothing on)' in bar 3.",
         "Verse 2": "As verse 1; the riff answers in a line's second bar where there is room.",
         "Pre 2": "As pre 1, with a horn swell; the same TAPE STOP on 'are'.",
         "Chorus 2": "As chorus 1, with tambourine eighths.", "Post 2": "As post 1.",
         "Bridge": "The power comes back: 1 for the first time. Bars 1–2: a low hum (pad on F) and Rhodes only. Bars 3–4: bass whole notes. Bars 5–6: kick and hats. Bar 7: snare build, guitar in. Bar 8: everyone hits 1, then OUT — she holds 'breath' alone.",
         "Chorus 3": "Bar 1: SILENT again. Bar 2: crash, all in, tambourine sixteenths, a third horn stab, the backing voice a third under the title lines. Bar 5: the D5 on 'off' — the top of the song.",
         "Post 3": "The hook twice at full groove. Bars 5–6 (the last line): STRIP to Rhodes and bass, 4maj7.",
         "Outro": "Riff, first bar only, over 4maj7; Rhodes rings. The song ends on 4maj7, never on 1."}
def num(ch): return NUMK["F major"][ch]
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    chs = [b["chord"] for b in REC["bars"][b0:b0 + nb]]
    ns = [num(c) + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, c in enumerate(chs)]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · F major</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 8)}</table><div class="drum">{html.escape(NOTES[s])}</div></div>"""
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
<div class="hdr"><h1>Nothing On</h1>
<div class="meta">NUMBERS IN F &nbsp;·&nbsp; 4/4 ♩ = 116 &nbsp;·&nbsp; FEEL: disco-funk pop, straight sixteenths &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> F major: 1 = F, 2m7 = Gm7, 3m7 = Am7, 4maj7 = B♭maj7, 5 = C, 3m = Am, 4 = B♭. <b>The home chord (1) is played only in the bridge</b> — the loop never lands; that is the song.
<b>◇ SILENT</b> = the whole band out for the chorus's first bar (the power cut). <b>Voice.</b> Female, A3–C5; D5 once, on "off" in the last chorus. <b>The riff and the backing echo</b> are cued on the lead sheet.</div>
</body></html>"""
open("/home/claude/p31/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p31/out/Nothing On - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
