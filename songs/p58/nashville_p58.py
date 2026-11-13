"""The Ratios Hold -- the number chart: E major (1 = E), q = 92; the instrumentals' meters marked per section (7/8 grouped 2+2+3, 5/4); a bar
with two chords shows both. HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p58/song_record.pkl", "rb"))
NUM = {"E": "1", "F#m": "2m", "G#m": "3m", "A": "4", "B": "5", "C#m": "6m", "D": "♭7"}
BARS = REC["bars"]
FEEL = {"Overture": "I. 16 bars of 7/8 (2+2+3): THE PATTERN THEME on Moog over Hammond; pick bass in eighths, accents on the groups; kick 1 and 3rd group, snare 2nd. Then 8 bars of 4/4: clean guitar plays the hook's figure, Mellotron strings swell; light kit from bar 21",
        "Verse 1": "II. THE LETTER. Bass leads; clean guitar eighth-note arpeggios; light kit (rim on 2 and 4). The words race in sixteenths",
        "Chorus 1": "OPEN UP: Hammond and Mellotron choir; full kit, crash on 1; three-part harmony on “The ratios hold” (bars 7–8)",
        "Verse 2": "= Verse 1, a little more drive",
        "Chorus 2": "= Chorus 1",
        "Study": "III. THE STUDY. 16 bars 7/8 (theme: Moog 8, guitar 8) · 8 bars 5/4 (guitar's long line) · 8 bars 7/8 (Moog and guitar trade bars) · 8 bars 4/4 ACOUSTIC ALONE · 8 bars 4/4 BUILD (theme in octaves, toms into the next)",
        "Window": "IV. THE WINDOW CLOSES. Piano alone, softer each bar, 8 bars; then 2 BARS OF SILENCE",
        "Bridge": "Piano and voice; each pair a step higher. Bass and drums back on the last pair (bar 9); toms into the last chorus",
        "Last Chorus": "V. CHURCH ORGAN at the summit; Mellotron choir; ride; three-part harmony on every line",
        "Tag": "“The ratios hold” twice, harmony",
        "Coda": "The theme in quarters on Moog over church organ, half-time; END on the organ's E chord (last 2 bars), let it ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    def num(c):
        base, _, bs = c.partition("/"); BN = {"E": "1", "F#": "2", "G#": "3", "A": "4", "B": "5", "C#": "6", "D#": "7"}
        return NUM[base] + (f"/{BN[bs]}" if bs else "")
    rng = range(b, b + nb)
    cells = []
    for bi in rng:
        x = BARS[bi]; met = x["meter"]; tag = "" if met == "4/4" else f"<sup>{met}</sup>"
        cells.append((num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"])) + tag)
    mc = collections.Counter(mets); mtxt = " · ".join(f"{v}×{k}" for k, v in mc.items())
    lab = f"""<div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b + 1}–{b + nb} · {mtxt}</div></div>"""
    if s in ("Chorus 2",):
        body += f"""<div class="sec">{lab}<div class="nums2">= Chorus 1</div><div class="drum">{FEEL[s]}</div></div>"""
    else:
        body += f"""<div class="sec">{lab}<table class="nums">{rows(cells)}</table><div class="drum">{FEEL[s]}</div></div>"""
    b += nb
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }} .hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 5px; display: grid; grid-template-columns: 1.5in 6.1in 1fr; gap: 12px; border-bottom: 0.5px solid #bbb; padding-bottom: 5px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }} .lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .bar {{ font-size: 7.5pt; color: #555; }} .nums2 {{ font-size: 11pt; font-weight: bold; }}
table.nums {{ border-collapse: collapse; }} table.nums td {{ width: 0.74in; white-space: nowrap; height: 0.2in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10.5pt; font-weight: bold; }}
table.nums td sup {{ font-size: 6.5pt; font-weight: normal; color: #444; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.8pt; line-height: 1.2; }} .foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>The Ratios Hold</h1>
<div class="meta">♩ = 92 &nbsp;·&nbsp; KEY: E major &nbsp;·&nbsp; 4/4 with 7/8 (2+2+3) and 5/4 in the instrumentals &nbsp;·&nbsp; FEEL: symphonic prog suite in five movements &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> E major: 1 = E, 2m = F♯m, 3m = G♯m, 4 = A, 5 = B, 6m = C♯m, ♭7 = D. A cell with two numbers: two beats each. A small 7/8 or 5/4 marks the bar's meter; unmarked bars are 4/4; the quarter note stays at 92 throughout. <b>Form.</b> I Overture 24 · II Verse 8 · Chorus 12 · Verse 8 · Chorus 12 · III Study 48 · IV Window 10 · Bridge 12 · V Last Chorus 12 · Tag 4 · Coda 24. <b>Ending.</b> The church organ's E chord, let ring.</div>
</body></html>"""
open("/home/claude/p58/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p58/out/The Ratios Hold - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
asyncio.run(main()); print("ok")
