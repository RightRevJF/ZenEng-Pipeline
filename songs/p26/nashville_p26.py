"""Module 11.9 document 2: the Nashville number chart with drummer notes for 'Five-Oh-One'. HTML -> PDF, letter landscape.
Numbers in each section's key (Eb major to the lift, F major from chorus 3); one number a bar of 4/4."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p26/song_record.pkl", "rb"))
NUMK = {"Eb major": {"Eb": "1", "Ab": "4", "Bb": "5", "Cm": "6m", "Gm": "3m", "C": "6"},
        "F major": {"F": "1", "Bb": "4", "C": "5", "Dm": "6m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "GTR + HORNS · the chant", ("Intro", 2): "+ DRUMS, BASS", ("Verse 1", 0): "VOICE · 8th hats", ("Pre 1", 0): "build",
        ("Pre 1", 3): "FILL", ("Chorus 1", 0): "CRASH · 16th hats", ("Hook 1", 0): "THE CHANT · claps", ("Hook 1", 1): "HEY!", ("Hook 1", 3): "GO!",
        ("Verse 2", 0): "8th hats", ("Pre 2", 3): "FILL", ("Chorus 2", 0): "CRASH", ("Hook 2", 1): "HEY!", ("Hook 2", 3): "GO!",
        ("Breakdown", 0): "KIT OUT · kick on 1", ("Breakdown", 1): "claps x3", ("Lift", 0): "hats", ("Lift", 2): "SNARE BUILD",
        ("Lift", 3): "ALL: FIVE-OH-ONE", ("Chorus 3", 0): "KEY UP · F", ("Chorus 4", 6): "HERE: B♭4", ("Hook 3", 1): "HEY!", ("Hook 3", 3): "GO!",
        ("Ending", 0): "HIT · stop"}
DRUMS = {"Intro": "Bars 1–2: scratch guitar and the horns' chant (FIVE-oh FIVE-oh FIVE-oh-ONE, a 3+3+2 tresillo) alone. Drums and bass in at bar 3: kick 1 and 3, snare 2 and 4, eighth hats.",
         "Verse 1": "Pocket: kick 1 and 3, snare 2 and 4, eighth hats. Bass: root on 1, octave on the 'and' of 2, root on 3, approach into the next bar. Guitar stabs on each 'and'; ghosts from bar 3.",
         "Pre 1": "Kick adds the 'a' of 2. Electric piano holds the chords. Last bar: snare-and-tom fill in sixteenths on beats 3–4.",
         "Chorus 1": "Full groove: kick 1, 'a' of 2, 3; sixteenth hats, open on the 'and' of 4; crash on 1. Horns stab on 1 and the 'and' of 2.",
         "Hook 1": "The chant: horns double the voice. Claps on 2 and 4. Band shouts HEY! after line 1 and GO! after line 2 (beat 3 'and' of bar 2).",
         "Verse 2": "As verse 1, ghost notes throughout.", "Pre 2": "As pre 1, with the fill.", "Chorus 2": "As chorus 1.", "Hook 2": "As hook 1.",
         "Breakdown": "Kit out: kick on 1 only. Bass gets busy (sixteenths, octave pops). Three claps answer every CLAP the singer calls.",
         "Lift": "Bars 1–2: hats and kick, the guitar rings. Bars 3–4 over C: a sixteenth snare build, crescendo. Everybody shouts FIVE-OH-ONE on beats 1, 2 and 3 of bar 3.",
         "Chorus 3": "Up a whole step into F. Everything harder: open hats on every 'and', crash every two bars, horns stab and hold, the gang shouts the title with him.",
         "Chorus 4": "As chorus 3. Line 4: 'and you'll find me HERE', the B♭4 on beat 4 of bar 7, held across the C bar.",
         "Hook 3": "The chant in F, claps, HEY! and GO!", "Outro": "The chant once more, ONE held.", "Ending": "One hit on F, beat 1. Stop."}
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
<div class="hdr"><h1>Five-Oh-One</h1>
<div class="meta">NUMBERS IN EACH SECTION'S KEY &nbsp;·&nbsp; 4/4 ♩ = 112 &nbsp;·&nbsp; KEY: E♭ → F &nbsp;·&nbsp; FEEL: funk-pop, straight 16ths &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> E♭ major: 1 = E♭, 4 = A♭, 5 = B♭, 6m = Cm, 6 = C (the lift's pivot). F major (from chorus 3): 1 = F, 4 = B♭, 5 = C, 6m = Dm.
<b>Voice.</b> Tenor, E♭3–A4; B♭4 once, on the last "here". <b>The chant</b> (FIVE-oh FIVE-oh FIVE-oh-ONE) is cued on the lead sheet wherever the horns play it.</div>
</body></html>"""
open("/home/claude/p26/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p26/out/Five-Oh-One - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
