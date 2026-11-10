"""Swallowed Up -- the number chart. B minor (1 = B); the power chords as numbers (the b2 and b5 as flats); the riff and feel for
each section; the band's notes. HTML -> PDF, letter landscape."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p34/song_record.pkl", "rb"))
NUM = {"B5": "1", "C5": "♭2", "D5": "♭3", "E5": "4", "F5": "♭5", "F#5": "5", "G5": "♭6", "A5": "♭7"}
FEEL = {None: "", 0.25: "quarter time", 0.5: "half time", 1: "normal time", 2: "double time", 4: "blast"}
NOTES = {"Intro": "Riff A. Bars 1-8: guitar 1 alone. Bar 9: guitar 2 and bass in, floor tom and china on the accents. Bar 13: normal time (kick 1 and 3, snare 2 and 4, ride eighths). Snare fill in bar 16.",
         "Riff": "Riff B, the voice not yet in: double time, the kick doubling the guitar's rhythm, ride on the beat. Every fourth bar the riff changes (♭6 to 5).",
         "Verse 1": "Riff B as before. The voice growls low.", "Verse 2": "Riff B. Growl.",
         "Verse 3": "Riff B' -- riff B moved up a half step (centre ♭2) for bars 73-80; home to B at bar 81.",
         "Chorus 1": "Riff C, tremolo picked. THE BLAST: kick and snare alternating sixteenths, ride eighths, crash every two bars. The shout: 'Swallowed up!'",
         "Chorus 2": "As chorus 1.", "Chorus 3": "As chorus 1.",
         "Solo": "Riff D, a gallop chug: 1 · ♭7 · ♭6 · 5, two bars each, twice. Double time. The lead solos; it ends on A♯ over 5, into the slowdown.",
         "Slowdown": "♩ = 100: A TRUE DROP IN TEMPO. Bars 113-120: riff E, long chords, half time, china on the beat; the shout over it. Bar 120: ♭5, ♭2 on beat 3, then beat 4 silent (the gap). Bars 121-128: THE BREAKDOWN, riff F: guitars, bass and kick in unison on low B, silence between; snare once every two bars; china every stroke, then the first stroke only, then crash, then nothing.",
         "Riff 2": "♩ = 200 again. Riff A: normal time for four bars, double time for four.",
         "Last Chorus": "Riff C, the blast; the lead doubles the tremolo two octaves up. The last 'Swallowed up!' a high scream.",
         "Outro": "Riff A twice, then riff G: unison strokes with crash and china; bar 152 one B5, let it ring."}
bars = REC["bars"]
def cell(k):
    return " ".join(NUM[n] for n in bars[k]["chords"])
def rows(cells, w): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; k = 0
for sec, n, q in REC["form"]:
    cells = [cell(k + i) for i in range(n)]
    f = FEEL.get(bars[k]["feel"]["feel"], "")
    who = f"♩ = {q}" + (f" · {f}" if f else "") + f" · riff {bars[k]['riff']}"
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(sec.upper())}</span> <span class="bars">{n}</span>
<span class="who">{html.escape(who)}</span><div class="bar">bar {k + 1}</div></div><table class="nums">{rows(cells, 8)}</table><div class="drum">{html.escape(NOTES[sec])}</div></div>"""
    k += n
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }}
.hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 3px; display: grid; grid-template-columns: 1.6in 5.4in 1fr; gap: 12px;
        border-bottom: 0.5px solid #bbb; padding-bottom: 4px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }}
.lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .who {{ display: block; font-size: 8pt; font-style: italic; }} .lab .bar {{ font-size: 7.5pt; color: #555; }}
table.nums {{ border-collapse: collapse; }}
table.nums td {{ width: 0.64in; white-space: nowrap; height: 0.17in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 9.5pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.6pt; line-height: 1.15; }}
.foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>Swallowed Up</h1>
<div class="meta">4/4, ♩ = 200 (the slowdown ♩ = 100) &nbsp;·&nbsp; KEY: B minor, tuned B E A D F♯ B &nbsp;·&nbsp; FEEL: death metal &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> Power chords in B minor: 1 = B5, ♭2 = C5, ♭3 = D5, 4 = E5, ♭5 = F5, 5 = F♯5, ♭6 = G5, ♭7 = A5. The pedal riffs (A, B) are written as 1: the palm-muted low B with open accents on ♭5, 4, ♭2, ♭3, ♭6 and 5 (see the parts). <b>Voice.</b> Harsh throughout, no pitch: verses growled low; the choruses and the taunt shouted, mid, to be understood; the last 'Swallowed up!' a high scream. <b>Two guitars</b> play the same riff, left and right.</div>
</body></html>"""
open("/home/claude/p34/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p34/out/Swallowed Up - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.84, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
