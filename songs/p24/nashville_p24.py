"""Module 11.9 document 2: the Nashville number chart with drummer notes for 'The Song You Sang Me'. HTML -> PDF, letter landscape.
Numbers in F major throughout; one number a bar of 3/4; the capo-3 shapes noted."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p24/song_record.pkl", "rb"))
NUMK = {"F major": {"F": "1", "Bb": "4", "C": "5", "Dm": "6m", "Gm": "2m", "Am": "3m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "GUITAR ALONE · the lullaby's tune", ("Verse 1", 0): "VOICE · fingerpicked", ("Verse 1", 12): "refrain", ("Verse 2", 12): "refrain",
        ("Chorus 1", 0): "THE LULLABY · pinch on 1", ("Chorus 1", 8): "DARK: A4", ("Verse 3", 0): "fingerpicked", ("Verse 3", 12): "refrain",
        ("Verse 4", 0): "ONE CHORD A BAR · let ring", ("Verse 4", 12): "SONG", ("Chorus 2", 0): "THE LULLABY · full", ("Chorus 2", 8): "WAKE: B♭4",
        ("Outro", 0): "the tune alone", ("Outro", 7): "F · ring"}
DRUMS = {"Intro": "Guitar alone: the lullaby's tune (the chorus's first two lines) on the top strings over bass on 1 and the chord on 2 and 3. Capo 3, D shapes.",
         "Verse 1": "Fingerpicked waltz in eighths: bass on 1 (root, then the fifth the next bar), the chord's three upper notes up and back. Each verse's last line is the refrain: it's me. I'm your son.",
         "Verse 2": "As verse 1.", "Chorus 1": "The lullaby. The same pattern with the top note pinched with the bass on beat 1. DARK on A4 (bar 3 of line 1).",
         "Verse 3": "As verse 1.", "Verse 4": "Thin it out: one chord a bar, struck on 1 and left to ring. The refrain turns: it's me. I'm your song.",
         "Chorus 2": "The lullaby again, fuller, sung by both. WAKE on B♭4 (line 3), the top of the song.",
         "Outro": "Guitar alone: the lullaby's last two lines, ending on F; the last chord left to ring."}
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
<div class="hdr"><h1>The Song You Sang Me</h1>
<div class="meta">NUMBERS IN EACH SECTION'S KEY &nbsp;·&nbsp; 3/4 ♩ = 76 &nbsp;·&nbsp; KEY: F major (guitar capo 3, D shapes) &nbsp;·&nbsp; FEEL: slow fingerpicked waltz &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> F major: 1 = F, 4 = B♭, 5 = C, 6m = Dm, 2m = Gm, 3m = Am. <b>Capo 3:</b> play D, G, A, Bm, Em, F♯m shapes for F, B♭, C, Dm, Gm, Am.
<b>Voice.</b> Tenor, E3–A4 in the song; B♭4 once, on the last "wake". <b>The guitar</b> is written out in full on the lead sheet: the tune in the intro and outro, the fingerpicking throughout.</div>
</body></html>"""
open("/home/claude/p24/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p24/out/The Song You Sang Me - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.95, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
