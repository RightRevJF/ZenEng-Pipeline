"""Module 11.9 document 2: the Nashville number chart for 'The Word Without a Word'. HTML -> PDF, letter landscape. Numbers in each
section's key (D-flat; E-flat from verse 4); 3/4, one number a bar."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p29/song_record.pkl", "rb"))
NUMK = {"Db major": {"Db": "1", "Ebm": "2m", "Fm": "3m", "Gb": "4", "Ab": "5", "Bbm": "6m", "F": "3", "Bb": "6"},
        "Eb major": {"Eb": "1", "Fm": "2m", "Gm": "3m", "Ab": "4", "Bb": "5", "Cm": "6m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "PIANO ALONE", ("Verse 1", 0): "VOICE · piano thin", ("Refrain 1", 0): "+ STRINGS", ("Verse 2", 0): "+ CELLO · answers",
        ("Interlude", 0): "CELLO SINGS", ("Interlude", 6): "SWELL", ("Verse 3", 6): "MA: HOLD", ("Bridge", 6): "ABBA: SILENT",
        ("Bridge", 7): "ALL IN · → E♭", ("Verse 4", 0): "E♭ · FULL", ("Refrain 3", 0): "♩ = 56", ("Refrain 3", 5): "B♭5: WORLD",
        ("Refrain 3", 6): "thin", ("Coda", 0): "PIANO: THE REFRAIN"}
DRUMS = {"Intro": "3/4 at ♩ = 66. Piano alone: the cradle figure in the left hand (root, fifth, tenth, octave, tenth, fifth in eighths), a right-hand chord in bars 1 and 3.",
         "Verse 1": "Voice almost whispered. Piano left hand only, thinned to root, fifth, tenth on the three beats.",
         "Refrain 1": "Piano adds the right-hand chord on beat 1, held; strings enter softly (a held pad).",
         "Verse 2": "Cello enters: the root a bar, held, and it answers each line: the singer's last three notes an octave below, in eighths, as she lands. Strings out. Every verse opens on the refrain's shape in small: a held note, a step down, back, and up a fourth to \"light\", \"bread\", \"mount\".", "Refrain 2": "As refrain 1, with the cello; a little fuller.",
         "Interlude": "Her lullaby: the cello sings the refrain's tune an octave below the voice, at half voice, over the piano's figure, with one note changed: \"world\" rises to F instead of D♭. The last two bars (2m, 3): the strings swell, leaning toward the bridge.",
         "Verse 3": "Piano and cello; the cello answers lines 1–3. On \"ma\" (bar 7 of the verse) nothing moves: hold the chord and let the voice sit alone.",
         "Bridge": "Strings build under the piano's chords; cello holds the bass. Bar 7 (\"Now: Abba\"): EVERYONE SILENT. Bar 8 (\"and Joseph turns\"): everyone back on 6 (B♭), the turn into E♭.",
         "Verse 4": "A whole step up, in E♭. Everyone, fuller: both hands of the piano, cello, strings.",
         "Refrain 3": "Broadening, ♩ = 56. Fullest: a held top line in the strings. B♭5 on \"world\" (bar 6). The last line thins to piano and strings, pianissimo; the voice ends on 5, open.",
         "Coda": "♩ = 56. Piano alone: the refrain's first phrase over 4, 2m (C, C, C, B♭, C, F); then 1; the last chord E♭ with an added F, B♭ on top. Let it ring."}
def num(sec, ch):
    k = next(b["key"] for b in REC["bars"] if b["sec"] == sec); return NUMK[k][ch]
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    chs = [b["chord"] for b in REC["bars"][b0:b0 + nb]]
    ns = [num(s, c) + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, c in enumerate(chs)]
    key = REC["bars"][b0]["key"]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · {"D♭" if key.startswith("Db") else "E♭"}</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 8)}</table><div class="drum">{html.escape(DRUMS[s])}</div></div>"""
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
<div class="hdr"><h1>The Word Without a Word</h1>
<div class="meta">3/4, ♩ = 66 (the last refrain ♩ = 56) &nbsp;·&nbsp; KEY: D♭, then E♭ from verse 4 &nbsp;·&nbsp; FEEL: a concert carol &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> D♭: 1 = D♭, 2m = E♭m, 3m = Fm, 3 = F (the interlude's lift), 4 = G♭, 5 = A♭, 6m = B♭m, 6 = B♭ (the turn). E♭: 1 = E♭, 2m = Fm, 3m = Gm, 4 = A♭, 5 = B♭, 6m = Cm.
<b>Voice.</b> Two co-equal editions: soprano, D♭4–A5 with one B♭5 ("world", A♭5 ossia); tenor, an octave lower (B♭4, A♭4 ossia). <b>Anchors:</b> "ma" (verse 3) held, nothing moves; "Abba" (bridge bar 7) the band silent.</div>
</body></html>"""
open("/home/claude/p29/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p29/out/The Word Without a Word - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
