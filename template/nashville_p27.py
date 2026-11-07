"""Module 11.9 document 2: the Nashville number chart with drummer notes for 'Either Or'. HTML -> PDF, letter landscape. Numbers in each
section's key (D Dorian: verses, intro, break, build, outro; F major: refrains); one number a bar, 5/4 or 4/4 as marked."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p27/song_record.pkl", "rb"))
NUMK = {"D Dorian": {"Dm": "1m", "G": "4", "F": "♭3", "Am": "5m", "C": "♭7", "Em": "2m", "D5": "1⁵"},
        "F major": {"F": "1", "Bb": "4", "C": "5", "Dm": "6m", "Gm": "2m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "GTR 1 ALONE · 3+2", ("Intro", 2): "+ GTR 2", ("Intro", 4): "+ BASS, DRUMS", ("Verse 1", 0): "VOICE · gtr 2 out",
        ("Refrain 1", 0): "4/4 · CRASH · organ F–C", ("Verse 2", 0): "5/4 · gtr 2 in", ("Refrain 2", 0): "4/4 · CRASH", ("Break", 0): "5/4 · HOCKET",
        ("Verse 3", 0): "5/4", ("Build", 0): "hats + kick", ("Build", 2): "snare", ("Build", 6): "ROLL", ("Refrain 3", 0): "4/4 · FULL",
        ("Refrain 4", 2): "", ("Refrain 4", 5): "CRASH · SCORE: B♭4", ("Refrain 4", 6): "STOP · voice alone", ("Outro", 0): "D–A DRONE · ring"}
DRUMS = {"Intro": "5/4, felt 3+2 (count 1-2-3-4-5, accents on 1 and 4). Guitar 1's figure alone for two bars; guitar 2 answers from bar 3; bass and drums from bar 5.",
         "Verse 1": "Kick on 1 and 4, snare on 3 and 5, hats on 1 and 4 only. Guitar 1's figure; guitar 2 lays out. Bass: root (dotted quarter), root, fifth, octave, approach.",
         "Refrain 1": "Switch to 4/4. Kick 1 and 3, snare 2 and 4, ride eighths, crash on the downbeat. Guitar 1 rings chords on 1 and 3; guitar 2 drives eighths; bass eighths; organ holds F and C.",
         "Verse 2": "Back to 5/4. Eighth hats now; guitar 2 back in with its offbeat answers.", "Refrain 2": "As refrain 1.",
         "Break": "5/4. The guitars hocket: guitar 1 on the even eighths, guitar 2 on the odd. Floor tom with the kick on 1 and 4.",
         "Verse 3": "As verse 2.", "Build": "5/4. Bars 1–2 hats and kick, bass held; bars 3–6 kick and snare rising, guitar 1 eighths; bars 7–8 snare and tom on every eighth; the organ swells throughout.",
         "Refrain 3": "4/4, everything: the top of the song.",
         "Refrain 4": "As refrain 3 through bar 78 (crash on 78, under the B♭4). Bars 79–80: EVERYONE STOPS. The voice sings the last line alone.",
         "Outro": "Organ D and A, guitar 1 D and A, bass low D: a bare fifth, neither major nor minor. Let it ring out. No drums."}
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
<div class="hdr"><h1>Either Or</h1>
<div class="meta">NUMBERS IN EACH SECTION'S KEY &nbsp;·&nbsp; 5/4 (3+2) and 4/4, ♩ = 132 &nbsp;·&nbsp; KEY: D Dorian / F &nbsp;·&nbsp; FEEL: angular art rock &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> D Dorian: 1m = Dm, 4 = G (major: the B natural), ♭3 = F, 5m = Am, ♭7 = C, 1⁵ = D5 (no third). F major: 1 = F, 4 = B♭, 5 = C, 6m = Dm.
<b>Metre.</b> Verses, intro, break and build in 5/4 (3+2); refrains and outro in 4/4. <b>Voice.</b> Tenor, F3–A4; B♭4 once, on the last "score". <b>The stop:</b> bars 79–80, voice alone.</div>
</body></html>"""
open("/home/claude/p27/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p27/out/Either Or - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
