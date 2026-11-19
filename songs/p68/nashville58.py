"""Same Time Tomorrow (song 58) -- the number chart: C major (1 = C), q = 84, a folk ballad, all 4/4; one cell a bar; a bar with two chords
shows both. Every section's notes are read from the record (where the stop falls, the hook's bars). HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p68/song_record.pkl", "rb"))
BARS = REC["bars"]
RN = {"C": "1", "D": "2", "E": "3", "F": "4", "G": "5", "A": "6", "B": "7", "Bb": "♭7"}
QN = {"": "", "m": "m", "7": "7", "m7": "m7", "sus4": "sus4", "sus2": "sus2", "maj7": "maj7"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return RN[rt_] + QN[base[len(rt_):]] + (f"/{RN[bs]}" if bs else "")
B0 = {s: st // 48 for s, nb, st, mets, mv in REC["plan"]}
FEEL = {"Intro": "Guitar strums eighths and bass plays quarters from bar 1; drums in at bar 2 (kick 1 and 3, snare 2 and 4, hats). Voice picks up in bar 4",
        "Verse 1": "He tells it. Guitar answers between his lines and lays out while he sings; bass and drums carry it. TOM FILL in the last bar",
        "Chorus 1": "Bar 1: the title, up to 5 on \u201c-morrow\u201d. Harmony voice under him all chorus. His top note (1, C) in bars 4 and 14",
        "Turn 2": "Two bars: guitar strums",
        "Verse 2": "As verse 1. TOM FILL in the last bar",
        "Chorus 2": "As chorus 1",
        "Bridge": "Starts on 6m. Same groove; he sings through",
        "Verse 3": "As verse 1. TOM FILL in the last bar",
        "Last Chorus": "Sixteen bars, two more than the others. Last bar: 1 4 1 4, a beat each",
        "Outro": "Six bars of 1: guitar strums, band with it to the end"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    cells = []
    for bi in range(b, b + nb):
        x = BARS[bi]
        cells.append(" ".join(num(c_) for c_ in x["beats4"]) if x.get("beats4") else num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"]))
    lab = f"""<div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b + 1}–{b + nb}</div></div>"""
    body += f"""<div class="sec">{lab}<table class="nums">{rows(cells)}</table><div class="drum">{FEEL[s]}</div></div>"""
    b += nb
secs = REC["seconds"]
doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }}
.hdr {{ border-bottom: 2px solid #111; padding-bottom: 4px; margin-bottom: 8px; }}
.hdr h1 {{ font-size: 17pt; margin: 0; }} .hdr .meta {{ font-size: 9.5pt; font-weight: bold; }} .hdr .cred {{ font-size: 8.5pt; color: #444; }}
.sec {{ break-inside: avoid; margin-bottom: 5px; display: grid; grid-template-columns: 1.4in 6.1in 1fr; gap: 12px; border-bottom: 0.5px solid #bbb; padding-bottom: 5px; align-items: start; }}
.lab .name {{ font-weight: bold; font-size: 10pt; }} .lab .bars {{ display: inline-block; border: 1.5px solid #111; border-radius: 3px; padding: 0 4px; font-size: 8.5pt; }}
.lab .bar {{ font-size: 7.5pt; color: #555; }}
table.nums {{ border-collapse: collapse; }} table.nums td {{ width: 0.74in; white-space: nowrap; height: 0.2in; border-left: 1.5px solid #111; padding-left: 5px; font-size: 10.5pt; font-weight: bold; }}
table.nums tr td:last-child {{ border-right: 1.5px solid #111; }}
.drum {{ font-size: 7.8pt; line-height: 1.2; }} .foot {{ font-size: 8pt; border-top: 1px solid #555; margin-top: 6px; padding-top: 4px; line-height: 1.35; }}
</style></head><body>
<div class="hdr"><h1>{REC['title']}</h1>
<div class="meta">♩ = 84 &nbsp;·&nbsp; KEY: C major &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: folk ballad &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> C major: 1 = C, 2m = Dm, 3m = Em, 4 = F, 5 = G, 6m = Am. One cell is one bar; two numbers in a cell split it, two beats each; four numbers, a beat each.
<b>Drums.</b> Kick 1 and 3, snare 2 and 4, hat eighths, from bar 2. <b>Voices.</b> One singer, a baritone; a harmony voice under him in the choruses.</div>
</body></html>"""
open("/home/claude/p68/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p68/out/{REC['file_title']} - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
if __name__ == "__main__":
    asyncio.run(main()); print("ok")
