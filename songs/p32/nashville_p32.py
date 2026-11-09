"""Module 11.9 document 2: the Nashville number chart for 'I Took Him for the Gardener'. HTML -> PDF, letter landscape. Numbers in each
bar's key (D minor, 1 = D; D major from MARY, bar 55); 6/8, one number a bar."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p32/song_record.pkl", "rb"))
NUMK = {"D minor": {"Dm": "1m", "Gm": "4m", "Bb": "♭6", "F": "♭3", "C": "♭7", "A": "5", "N.C.": "N.C."},
        "D major": {"D": "1", "G": "4", "A": "5", "Bm": "6m", "Em": "2m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "PIANO", ("Verse 1", 0): "BARE", ("Refrain 1", 0): "+ STR", ("Verse 2", 0): "+ CELLO",
        ("Interlude", 0): "CELLO", ("Interlude", 2): "SWELL", ("Interlude", 3): "C♯", ("The Name", 5): "SILENT",
        ("The Name", 6): "MAJOR", ("Verse 4", 0): "FULL", ("Refrain 3", 0): "♩.=48", ("Refrain 3", 5): "A5",
        ("Refrain 3", 8): "THIN", ("Refrain 3", 10): "STR", ("Refrain 3", 11): "CLOSE", ("Coda", 0): "PIANO"}
DRUMS = {"Intro": "6/8 at ♩. = 52 (♩ = 78). Piano alone: the walking figure in the left hand (root, fifth, tenth | octave, tenth, fifth in eighths), a right-hand chord in bars 1 and 3.",
         "Verse 1": "Voice low and plain. Piano left hand only, bare: the root and the fifth in dotted quarters. The dark.",
         "Refrain 1": "Piano back to the walking figure and adds a right-hand chord on each downbeat, held; strings enter softly (a held pad).",
         "Verse 2": "Cello enters: the root a bar, held, and it answers each line: the singer's last three notes an octave below, in eighths, as she lands. Strings out. Verses 1–3 open on the refrain's first notes (F A G A) and turn down.",
         "Refrain 2": "As refrain 1, with the cello; a little fuller.",
         "Interlude": "The cello sings the refrain's first two lines an octave below the voice over the piano's figure, with one note changed: \"dawn\" rises to C♯ (over 5) instead of A, a lean toward the light. Strings swell in the last two bars.",
         "Verse 3": "Piano and cello; the cello answers lines 1–3 (line 4 if there is room). Strings out.",
         "The Name": "Strings and cello build softly under lines 1–2. Bar 54 (\"said my name\"): EVERYONE SILENT, the voice alone. Bar 55 (\"Mary\"): everyone back on 1 in D MAJOR, soft and held, one chord a bar, no figure; hold through the voice's silent bar; \"and I said, Rabboni\" over 4 and 5.",
         "Verse 4": "D major. Everyone, fuller: the piano's right hand on both beats, cello, strings.",
         "Refrain 3": "Broadening, ♩. = 48. Fullest: a held top line in the strings. A5 on \"earth\" (bar 72). The last line (bar 75) thins; bar 77 only the strings hold 5, the voice and piano silent; \"and he was\" closes on 1.",
         "Coda": "♩. = 44. Piano alone: the refrain's first phrase in D major (F♯ A G A C♯ D) over 1 and 4; then 1; the last chord D with an added E, A on top. Let it ring."}
def num(b): return NUMK[b["key"]][b["chord"]]
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    bs = REC["bars"][b0:b0 + nb]
    ns = [num(b) + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, b in enumerate(bs)]
    key = REC["bars"][b0]["key"]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · {"D minor" if key == "D minor" and REC["bars"][b0 + nb - 1]["key"] == "D minor" else ("D minor → D major" if key == "D minor" else "D major")}</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 8)}</table><div class="drum">{html.escape(DRUMS[s])}</div></div>"""
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
<div class="hdr"><h1>I Took Him for the Gardener</h1>
<div class="meta">6/8, ♩. = 52 (the last refrain ♩. = 48) &nbsp;·&nbsp; KEY: D minor, D major from “Mary” (bar 55) &nbsp;·&nbsp; FEEL: a slow lilt, walking pace &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> D minor (1 = D): 1m = Dm, ♭3 = F, 4m = Gm, 5 = A (major), ♭6 = B♭, ♭7 = C. D major: 1 = D, 2m = Em, 4 = G, 5 = A, 6m = Bm.
<b>Voice.</b> Two co-equal editions: soprano, D4–A5 (one A5, “earth”, F♯5 ossia); mezzo, a minor third lower (B minor → B major, B3–F♯5); for the mezzo edition read the same numbers in B. <b>Anchors:</b> bar 54 the band silent under “said my name”; bar 55 “Mary”: everyone back in D major.</div>
</body></html>"""
open("/home/claude/p32/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p32/out/I Took Him for the Gardener - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
