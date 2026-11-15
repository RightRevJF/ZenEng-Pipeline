"""The Room Next Door -- the number chart: D major (1 = D), 6/8, dotted quarter = 54; one cell a bar. HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p62/song_record.pkl", "rb"))
BARS = REC["bars"]
RN = {"D": "1", "E": "2", "F#": "3", "G": "4", "A": "5", "B": "6", "C#": "7", "C": "♭7", "Bb": "♭6"}
QN = {"": "", "m": "m", "m7": "m7", "add9": "add9", "sus4": "sus4", "maj7": "maj7", "m9": "m9", "7sus4": "7sus4"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return RN[rt_] + QN[base[len(rt_):]] + (f"/{RN[bs]}" if bs else "")
def tq(s): return "♩. = 54"
FEEL = {"Intro": "Acoustic guitar alone, fingerpicked: bass note on 1 and 4, the chord between",
        "Verse 1": "Guitar and voice only. Two bars a line",
        "Chorus 1": "PIANO and BASS in: piano on the two beats, soft; bass root on 1, approach on 4. Hook “there's a door in the wall” (last two bars): up to the top D on “door”, “wall” left open on A. Harmony on the hook",
        "Verse 2": "Guitar, bass; piano answers at the end of every other bar",
        "Chorus 2": "= Chorus 1, CELLO in on long notes",
        "Interlude": "The CELLO plays the hook's tune (bars 1–2), then holds; guitar and bass under it",
        "Verse 3": "Guitar, bass; cello held notes",
        "Bridge": "HUSH: guitar and bass OUT. Soft held piano chords and cello. “and you were there” (bars 7–8) lifts; “gone” held open",
        "Verse 4": "Guitar and bass back; piano high and soft",
        "Last Chorus": "Fullest; harmony on every line. Bar 6: ♭6maj7 (B♭maj7) under “and some morning it opens”. Hook TWICE: the second time home to 1, held",
        "Outro": "Guitar and cello, softer each bar, slowing; last bar 1add9, let it ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    rng = range(b, b + nb)
    cells = []
    for bi in rng:
        x = BARS[bi]; met = x["meter"]; tag = "" if met in ("4/4", "6/8") else f"<sup>{met}</sup>"
        cells.append((num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"])) + tag)
    mc = collections.Counter(mets); mtxt = " · ".join(f"{v}×{k}" for k, v in mc.items())
    lab = f"""<div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b + 1}–{b + nb} · {tq(s)}</div></div>"""
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
<div class="hdr"><h1>The Room Next Door</h1>
<div class="meta">♩. = 54 &nbsp;·&nbsp; KEY: D major &nbsp;·&nbsp; 6/8, IN TWO &nbsp;·&nbsp; FEEL: intimate folk ballad, gently rocking &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · second edition · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> D major: 1 = D, 2m = Em, 3m = F♯m, 4 = G, 5 = A, 6m = Bm, ♭7 = C, ♭6 = B♭ (borrowed). /3 = over the third (D/F♯ = 1/3, G/B = 4/6). One cell is one bar of 6/8: two beats. Every sung line is two bars.</div>
</body></html>"""
open("/home/claude/p62/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p62/out/The Room Next Door (second edition) - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
asyncio.run(main()); print("ok")
