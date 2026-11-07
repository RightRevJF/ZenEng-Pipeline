"""Module 11.9 document 2: the Nashville number chart with band notes for 'Tinted Glass'. HTML -> PDF, letter landscape. Eb major
throughout (no key change); 6/8 felt in two, one number a bar."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p28/song_record.pkl", "rb"))
NUMK = {"Eb major": {"Eb": "1", "Fm": "2m", "Gm": "3m", "Ab": "4", "Bb": "5", "Cm": "6m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "E.P. ALONE", ("Verse 1", 0): "HIM · + BASS", ("Verse 2", 0): "HER · + BRUSHES", ("Chorus 1", 0): "HIM · RIDE · ORGAN",
        ("Verse 3", 0): "HIM", ("Verse 4", 0): "HER · organ low", ("Chorus 2", 0): "HER", ("Bridge", 0): "HER · hats only", ("Bridge", 4): "HIM",
        ("Bridge", 8): "HER", ("Bridge", 12): "HIM", ("Verse 5", 0): "HIM · sparse", ("Verse 6", 0): "HER · sparse", ("Chorus 3", 0): "HIM · FULL",
        ("Chorus 3", 4): "FOG: C4", ("Chorus 4", 0): "HER · FULL", ("Chorus 4", 4): "FOG: C5", ("Outro", 0): "E.P. ALONE · ring"}
DRUMS = {"Intro": "6/8, felt in two (two big beats, each three eighths). Electric piano alone: a low chord on 1, the triplet climb on 4-5-6.",
         "Verse 1": "Him. Electric piano and bass only (root on 1, fifth on 4, an approach into a new chord). Each four-bar line: he's done by bar 3, the piano answers in bar 4.",
         "Verse 2": "Her. Brushes in: hats on the eighths, side-stick on 4, soft kick on 1.",
         "Chorus 1": "Him. Kick 1, snare 4, ride eighths, crash on the downbeat; piano chords on 1 and 4 (pushed an eighth early on each line's second bar); organ pad.",
         "Verse 3": "Him. As verse 2.", "Verse 4": "Her. As verse 2, the organ low under it.", "Chorus 2": "Her. As chorus 1.",
         "Bridge": "Lines traded: her, him, her, him (four bars each). Drums drop to hats and a soft kick on 1; bass holds the root; organ held. Quiet: don't build.",
         "Verse 5": "Him. Sparse: hats and side-stick only, the piano softer. This is the settling in.", "Verse 6": "Her. As verse 5.",
         "Chorus 3": "Him. Full, the hardest the band plays, but no key change: the song refuses the lift.",
         "Chorus 4": "Her, alone, the same: full. They never sing together. The last chord of the chorus (5) goes to the outro's 4.",
         "Outro": "Electric piano alone: 4, 5, 1, 1. Let the last chord ring. No drums."}
def num(sec, ch):
    k = next(b["key"] for b in REC["bars"] if b["sec"] == sec); return NUMK[k][ch]
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    chs = [b["chord"] for b in REC["bars"][b0:b0 + nb]]
    ns = [num(s, c) + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, c in enumerate(chs)]
    key = REC["bars"][b0]["key"]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · E♭</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 8)}</table><div class="drum">{html.escape(DRUMS[s])}</div></div>"""
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
<div class="hdr"><h1>Tinted Glass</h1>
<div class="meta">6/8 FELT IN TWO, ♩. = 54 &nbsp;·&nbsp; KEY: E♭ (no change) &nbsp;·&nbsp; FEEL: slow-burn soul duet &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> E♭ major: 1 = E♭, 2m = Fm, 3m = Gm, 4 = A♭, 5 = B♭, 6m = Cm.
<b>Voices.</b> Him (baritone) C3–B♭3, C4 once; her B♭3–B♭4, C5 once: both on "fog" in the last choruses. They never sing at the same time. <b>Verses and bridge:</b> four bars a line, the piano's answer in bar 4.</div>
</body></html>"""
open("/home/claude/p28/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p28/out/Tinted Glass - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
