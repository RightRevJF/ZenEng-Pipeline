"""Module 11.9 document 2: the Nashville number chart with band notes for 'Through Its Breaking'. HTML -> PDF, letter landscape.
Numbers in each section's key (A minor: intro, verses, interludes, bridge; C major: choruses, tag, outro); one number a bar of 6/8."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p25/song_record.pkl", "rb"))
NUMK = {"A minor": {"Am": "1m", "C": "♭3", "Dm": "4m", "E": "5", "Em": "5m", "F": "♭6", "G": "♭7"},
        "C major": {"C": "1", "Dm": "2m", "Em": "3m", "E": "3", "F": "4", "G": "5", "Am": "6m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "THE BELL · toll + crack", ("Verse 1", 0): "VOICE · piano thin", ("Chorus 1", 3): "TRUE: A4", ("Chorus 1", 7): "THROUGH: G4",
        ("Interlude 1", 0): "the bell", ("Verse 2", 0): "+ CELLO", ("Chorus 2", 0): "+ STRINGS", ("Interlude 2", 0): "the bell",
        ("Bridge", 0): "piano thins", ("Bridge", 4): "strings: one line", ("Bridge", 8): "THE BELL IN · swell", ("Bridge", 15): "REACHED: B4",
        ("Chorus 3", 0): "FULL · the bell", ("Chorus 3", 8): "THROUGH: C5", ("Tag", 0): "DROP · bell, cello, voice", ("Outro", 3): "C · B–C ring"}
DRUMS = {"Intro": "The bell on the piano: a low octave toll on the downbeat, and on beat 2 the crack, the chord's root with the half step below it, struck together and let ring (Am: A + G♯). Left hand holds root and fifth.",
         "Verse 1": "Piano thin: root held on 1, fifth-octave-tenth on beat 2. The voice low and close (A3–E4).",
         "Chorus 1": "6/8 ballad figure in the left hand (R-5-8-10-8-5), right-hand chord on 1. Cello enters for the second couplet. TRUE on A4 over F; THROUGH on G4 over G.",
         "Interlude 1": "Two bars of the bell over Am.",
         "Verse 2": "The full left-hand figure; cello on the root, a bar each.",
         "Chorus 2": "Add strings (held pad). Cello answers on beat 2 with the fifth.",
         "Interlude 2": "Two bars of the bell over Am, then the night.",
         "Bridge": "A build: bars 1–4 piano thinned, cello on roots; bars 5–8 one held string line; bars 9–16 the pad and the bell, swelling bar by bar. REACHED on B4, the bridge's top.",
         "Chorus 3": "Everyone, and the bell rings through it: toll every bar, the crack on beat 2. The last line is four bars (F G C C): THROUGH on C5 at the third bar's downbeat, held; BREAKing falls home.",
         "Tag": "Drop: no strings, no figure. Bell, cello, piano root-fifth-octave held; the voice low (C4).",
         "Outro": "The bell alone over C. Last bar: C held, B4 against C5 left ringing -- the crack, unresolved."}
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
<div class="hdr"><h1>Through Its Breaking</h1>
<div class="meta">NUMBERS IN EACH SECTION'S KEY &nbsp;·&nbsp; 6/8 ♩. = 54 &nbsp;·&nbsp; KEY: Am / C &nbsp;·&nbsp; FEEL: piano ballad, in two &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> A minor: 1m = Am, ♭3 = C, 4m = Dm, 5 = E, ♭6 = F, ♭7 = G. C major: 1 = C, 3m = Em, 4 = F, 5 = G, 6m = Am.
<b>Voice.</b> Female, A3–B4 in the song; C5 once, on the last "through". <b>The bell</b> is cued on the lead sheet (toll and crack) wherever it plays.</div>
</body></html>"""
open("/home/claude/p25/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p25/out/Through Its Breaking - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.95, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
