"""The Small Things -- the number chart: D major (1 = D), q = 88 swung, all 4/4; a bar with two chords shows both. HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p60/song_record.pkl", "rb"))
NUM = {"D": "1", "Em": "2m", "F#m": "3m", "G": "4", "A": "5", "Bm": "6m", "C": "♭7"}
BARS = REC["bars"]
FEEL = {"Intro": "Fingerpicked acoustic guitar alone, swung. Piano hints at the hook softly in bars 3–4",
        "Verse 1": "Guitar picking and voice only; ACOUSTIC BASS IN at bar 9 (halfway). Plain, unhurried",
        "Chorus 1": "Guitar picking fuller; piano soft half-note chords; bass; brushes (rim on 2 and 4). Hook “I think God likes the small things” (bars 13–14) up to D on “small”, held; “I think He always will” home to D (bars 15–16)",
        "Verse 2": "Guitar picking, bass; piano answers at each line's end; no drums",
        "Chorus 2": "= Chorus 1, brushes on the snare",
        "Bridge": "DROP: guitar alone, low and quiet. Bar 7: ONE BEAT OF SILENCE, everyone out; “and the holy showed up clear” rises, held on A (bars 7–8), open",
        "Last Chorus": "= Chorus 1, fullest: brushes on the snare, harmony on every line. LAST LINE SLOWS (ritardando) to the end",
        "Outro": "Guitar picking, softer each bar; piano echoes the hook's last line; END on D, let it ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    def num(c):
        base, _, bs = c.partition("/"); BN = {"D": "1", "E": "2", "F#": "3", "G": "4", "A": "5", "B": "6", "C#": "7", "C": "♭7"}
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
<div class="hdr"><h1>The Small Things</h1>
<div class="meta">♩ = 88 &nbsp;·&nbsp; KEY: D major &nbsp;·&nbsp; 4/4, SWUNG &nbsp;·&nbsp; FEEL: gentle acoustic folk, fingerpicked &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> D major: 1 = D, 2m = Em, 3m = F♯m, 4 = G, 5 = A, 6m = Bm, ♭7 = C. A cell with two numbers: two beats each. Every line of the lyric is two bars; the chorus and the verse are sixteen bars each, the bridge eight.</div>
</body></html>"""
open("/home/claude/p60/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p60/out/The Small Things - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
asyncio.run(main()); print("ok")
