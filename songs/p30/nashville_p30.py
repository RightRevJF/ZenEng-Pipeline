"""Module 11.9 document 2: the Nashville number chart with band notes for 'She Left the Light On'. HTML -> PDF, letter landscape.
Numbers in D major; one number a bar of 4/4 (the G minor under THUMB is 4m)."""
import asyncio, html, pickle
REC = pickle.load(open("/home/claude/p30/song_record.pkl", "rb"))
NUMK = {"D major": {"D": "1", "G": "4", "A": "5", "Bm": "6m", "Em": "2m", "Gm": "4m"}}
CUE = lambda t: f"<span class=cue>{t}</span>"
CUES = {("Intro", 0): "AC + LICK", ("Intro", 2): "+ BASS, KIT", ("Verse 1", 0): "VOICE · x-stick", ("Verse 1", 7): "“she left the light on”",
        ("Chorus 1", 0): "CRASH · full", ("Chorus 1", 7): "snare pickup", ("Post 1", 0): "THE LICK", ("Verse 2", 0): "steel answers",
        ("Chorus 2", 0): "CRASH", ("Chorus 2", 7): "snare pickup", ("Post 2", 0): "THE LICK", ("Bridge", 0): "KIT OUT · kick on 1",
        ("Bridge", 4): "4m · B♭ (thumb)", ("Bridge", 5): "tom swell", ("Chorus 3", 0): "THE DROP · ac + steel", ("Chorus 3", 1): "tom fill",
        ("Chorus 3", 2): "CRASH · ALL · F♯4 “light”", ("Chorus 3", 4): "+ organ, tamb", ("Outro", 0): "THE LICK", ("Outro", 3): "END ON 4 · ring"}
NOTES = {"Intro": "Bars 1–2: strummed acoustic and the lick (the title's tune up an octave) alone. Bass and kit in at bar 3: kick 1 and 3, cross-stick 2 and 4, soft eighth hats.",
         "Verse 1": "Light: acoustic strums down on 1 and 3, up on the 'and' of 2 and 4. Bass root on 1 and 3 (fifth on 3). Steel swells, a bar at a time. The last line sings the title quickly: the hook, foreshadowed.",
         "Chorus 1": "Full: acoustic D . D U . U D U; kick 1, the 'and' of 2, 3; snare 2 and 4; eighth hats, open on the 'and' of 4; crash on 1. Bass two-beat with an eighth walk into each change. Steel answers where the singer holds.",
         "Post 1": "The lick (bars 3–4 of the intro) over 1 · 5. Kit stays in.",
         "Verse 2": "Band stays in (no open hat). Steel answers each line end where there is room.",
         "Chorus 2": "As chorus 1.", "Post 2": "The lick again.",
         "Bridge": "Pull back: kit out but the kick on 1; acoustic picks the chord in eighths; bass whole notes; steel swells. Bars 5–6 are 4m (G minor): the steel holds B♭ under 'thumb'. Bar 6: a low-tom swell.",
         "Chorus 3": "Bars 1–2: THE DROP — one acoustic strum let ring, steel alone, the voice almost bare ('now you're the one out late'); a tom fill on the last beat and a half. Bar 3: crash, everyone in, the F♯4 on 'light'. From bar 5: organ and tambourine.",
         "Outro": "The lick twice. The last bar is 4 (G), not 1: one strum, the lick's B held. Let it ring — the song ends open."}
def num(ch): return NUMK["D major"][ch]
def rows(ns, w): return "".join("<tr>" + "".join(f"<td>{n}</td>" for n in ns[i:i + w]) + "</tr>" for i in range(0, len(ns), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    chs = [b["chord"] for b in REC["bars"][b0:b0 + nb]]
    ns = [num(c) + (" " + CUE(CUES[(s, i)]) if (s, i) in CUES else "") for i, c in enumerate(chs)]
    body += f"""<div class="sec"><div class="lab"><span class="name">{html.escape(s.upper())}</span> <span class="bars">{nb}</span>
<span class="who">{met} · D major</span><div class="bar">bar {b0 + 1}</div></div><table class="nums">{rows(ns, 8)}</table><div class="drum">{html.escape(NOTES[s])}</div></div>"""
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
<div class="hdr"><h1>She Left the Light On</h1>
<div class="meta">NUMBERS IN D &nbsp;·&nbsp; 4/4 ♩ = 84 &nbsp;·&nbsp; FEEL: mid-tempo country, straight &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> D major: 1 = D, 4 = G, 5 = A, 6m = Bm, 4m = Gm (borrowed, bridge bars 5–6 only).
<b>Voice.</b> Male, D3–E4; F♯4 once, on "light" in the last chorus. <b>The lick</b> is cued on the lead sheet wherever it plays.</div>
</body></html>"""
open("/home/claude/p30/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p30/out/She Left the Light On - Nashville chart.pdf", format="Letter", landscape=True,
                     margin=dict(top="0.3in", bottom="0.25in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
