"""Module 11.9 document 2: the Nashville number chart for 'Sadie'. HTML -> PDF, letter landscape. Numbers in A major (1 = A); 4/4,
one number a bar; N.C. in the drop."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p33/song_record.pkl", "rb"))
NUMK = {"A major": {"A": "1", "D": "4", "E": "5", "F#m": "6m", "Bm": "2m", "C#m": "3m", "N.C.": "N.C."}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "RIFF ALONE", ("Intro", 4): "BAND IN", ("Verse 1", 0): "PALM", ("Pre 1", 0): "TOMS", ("Pre 1", 3): "FILL",
        ("Chorus 1", 0): "4 ON FLOOR", ("Riff", 0): "RIFF", ("Chorus 2", 0): "+ TAMB", ("Bridge", 0): "HALF TIME", ("Bridge", 4): "BUILD",
        ("Drop", 0): "HIT · STOP", ("Drop", 1): "HEARTBEAT", ("Chorus 3", 0): "ALL IN", ("Chorus 4", 0): "THE CROWD", ("Outro", 0): "RIFF",
        ("Outro", 7): "RING"}
DRUMS = {"Intro": "4/4 at ♩ = 124, straight eighths. Bars 1-4: the riff alone on the lead guitar (the title's notes, then the open-A chug and lick). Bar 5: the band in -- kick 1 and 3 (and the and of 3), snare 2 and 4, eighth hats, palm-muted rhythm guitar, bass on the root in eighths.",
         "Verse 1": "Palm-muted. The lead guitar answers each line in the gap after it (two or three notes, as written).",
         "Pre 1": "Floor tom eighths, snare 2 and 4; rhythm guitar opens up; organ pad. A snare fill in the last bar.",
         "Chorus 1": "Four on the floor, snare 2 and 4, open hats on the off-beats, crash on 1. Bass root-fifth-octave eighths; acoustic strums eighths. The gang shouts 'Sadie! Sadie!' at the top.",
         "Riff": "The riff again over the verse groove; crash on 1.",
         "Verse 2": "As verse 1, the lead guitar answering.",
         "Pre 2": "As pre 1.",
         "Chorus 2": "As chorus 1, plus a tambourine on the off-beats.",
         "Bridge": "Half time: kick on 1, rim click on 3 for four bars; then the kit (snare on 3, hats) builds; a snare build in the last bar. Rhythm guitar rings one chord a bar; bass half notes.",
         "Drop": "Bar 61: EVERYONE hits 5 on beat 1 and stops. The singer: 'It's up.' alone. Bars 62-64: N.C. -- nothing but the kick drum's heartbeat, lub-dub on 1 and 3. Do not fill.",
         "Chorus 3": "Everyone back in on 1 with a crash. As chorus 2.",
         "Chorus 4": "The crowd: the gang sings the whole chorus with the lead; tambourine eighths; crash on bars 73 and 77; the lead guitar doubles 'Sadie! Sadie!' an octave up.",
         "Outro": "The riff over the band; the gang shouts 'Sadie! Sadie!' in bars 83 and 87. Last bar: everyone on 1, let it ring."}
def num(b): return NUMK[b["key"]][b["chord"]]
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    bs = REC["bars"][b0:b0 + nb]
    ns = [num(b) + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, b in enumerate(bs)]
    key = REC["bars"][b0]["key"]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · A</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 8)}</table><div class="drum">{html.escape(DRUMS[s])}</div></div>"""
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
<div class="hdr"><h1>Sadie</h1>
<div class="meta">4/4, ♩ = 124, straight eighths &nbsp;·&nbsp; KEY: A &nbsp;·&nbsp; FEEL: country-rock anthem, four on the floor in the choruses &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> A major: 1 = A, 2m = Bm, 4 = D, 5 = E, 6m = F♯m. <b>Voice.</b> Baritone lead, C♯3–F♯4 (one F♯4, “never”, the last chorus); the gang on “Sadie! Sadie!” in every chorus and the whole last chorus. <b>The drop</b> (bars 61–64): one hit on 5, then N.C. with the kick’s heartbeat only; everyone back on bar 65.</div>
</body></html>"""
open("/home/claude/p33/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p33/out/Sadie - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
