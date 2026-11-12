"""Keeping Time -- the number chart: each section numbered in its own key (Intro, Verse, Pre, Outro in C minor, 1m = C minor; Chorus, Post,
Bridge in E-flat, 1 = E-flat); 4/4 at 112, four on the floor, one chord a bar; every section with its feel. HTML -> PDF, letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p48/song_record.pkl", "rb"))
NUM_CM = {"Cm": "1m", "Fm": "4m", "Gm": "5m", "G": "5", "Ab": "♭6", "Eb": "♭3", "Bb": "♭7"}
NUM_EB = {"Eb": "1", "Fm": "2m", "Gm": "3m", "Ab": "4", "Bb": "5", "Cm": "6m", "G": "3"}
MINOR = ("Intro", "Verse 1", "Pre 1", "Verse 2", "Pre 2", "Outro")
BARS = REC["bars"]
FEEL = {"Intro": "THE PULSE alone in dotted eighths (it drifts against the beat); kick, bass (quarters) and pad in at bar 5; hats in dotted eighths with the pulse",
        "Verse 1": "Kick on every beat; pulse and hats in DOTTED EIGHTHS (drifting); bass in quarters; pad; no claps",
        "Pre 1": "CLAPS on 2 and 4; the pulse and hats still drifting, then LOCK to eighths in the last bar with a snare build",
        "Chorus 1": "LOCKED: crash on 1, claps, off-beat open hats, sixteenth hats, bass eighths (root and octave), pad an octave up. BAR 5: EVERYTHING OUT but the pulse, tick and tock on the clocks' two notes; crash and back in on bar 6",
        "Post 1": "Locked; every phrase lands on the one", "Verse 2": "As verse 1: drifting again", "Pre 2": "As pre 1", "Chorus 2": "= Chorus 1", "Post 2": "= Post 1",
        "Bridge": "NO KICK for six bars: pad wide, bass whole notes, the pulse in quarters (space); bars 7-8 on G (III): kick, claps and the snare build back in",
        "Last Chorus": "EVERYTHING, sixteenth hats throughout; bar 5 out as before", "Post 3": "Locked; the last line home to E-flat",
        "Outro": "The pulse drifts again over the kick; ONE E-FLAT CHORD on 1 of bar 80 with a crash, let ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    NUM = NUM_CM if s in MINOR else NUM_EB
    cells = [NUM[BARS[b]["chord"]] for b in range(b0, b0 + nb)]
    key_ = "C minor" if s in MINOR else "E♭"
    if s in ("Chorus 2", "Post 2"):
        body += f"""<div class="sec"><div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= {s.replace(" 2", " 1")}</div><div class="drum">{FEEL[s]}</div></div>"""; continue
    body += f"""<div class="sec"><div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb} · {key_}</div></div>
<table class="nums">{rows(cells)}</table><div class="drum">{FEEL[s]}</div></div>"""
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }} .hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 5px; display: grid; grid-template-columns: 1.4in 6.2in 1fr; gap: 12px; border-bottom: 0.5px solid #bbb; padding-bottom: 5px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }} .lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .bar {{ font-size: 7.5pt; color: #555; }} .nums2 {{ font-size: 11pt; font-weight: bold; }}
table.nums {{ border-collapse: collapse; }} table.nums td {{ width: 0.74in; white-space: nowrap; height: 0.2in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10.5pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.8pt; line-height: 1.2; }} .foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>Keeping Time</h1>
<div class="meta">4/4, ♩ = 112, straight &nbsp;·&nbsp; KEY: C minor (verses) / E♭ major (chorus), three flats throughout &nbsp;·&nbsp; FEEL: dance-pop, four on the floor; the pulse drifts, then locks &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> Verses, pre-choruses, intro and outro in C minor: 1m = Cm, ♭3 = E♭, 4m = Fm, 5m = Gm, ♭6 = A♭, ♭7 = B♭. Chorus, post-chorus and bridge in E♭: 1 = E♭, 2m = Fm, 4 = A♭, 5 = B♭, 6m = Cm, 3 = G (major). The same three flats; the chorus hears them from a new home. One chord a bar. <b>Form.</b> Intro 8 · Verse 8 · Pre 4 · Chorus 8 · Post 4 · Verse 8 · Pre 4 · Chorus 8 · Post 4 · Bridge 8 · Last Chorus 8 · Post 4 · Outro 4. <b>Voice.</b> Mezzo; every line. The verses stay narrow; the chorus opens over them.</div>
</body></html>"""
open("/home/claude/p48/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p48/out/Keeping Time - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
