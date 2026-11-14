"""The World Is Asking -- the number chart: G major (1 = G), q = 84, all 4/4; a bar with two chords shows both. HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p59/song_record.pkl", "rb"))
NUM = {"G": "1", "Am": "2m", "Bm": "3m", "C": "4", "D": "5", "Em": "6m", "F": "♭7"}
BARS = REC["bars"]
FEEL = {"Intro": "Fingerpicked acoustic guitar alone (thumb on the root and fifth). Piano states the hook's figure softly in bars 3–4",
        "Verse 1": "Guitar picking and voice only; ACOUSTIC BASS IN at bar 9 (halfway). Plain, close, spoken",
        "Chorus 1": "OPEN: guitar strums quarters; piano half-note chords; strings low; brushes (rim on 2 and 4); soft crash on 1. The hook “The world is asking” (bars 1–2, 13–14) holds on D, unresolved",
        "Verse 2": "Guitar picking, bass; piano answers at each bar's end; brushes on the rim",
        "Chorus 2": "= Chorus 1, strings higher, brushes on the snare",
        "Bridge": "DROP: piano alone, low and close; strings in from bar 5. BAR 9 SILENT, EVERYONE OUT. “Here I am” bar 10; “Speak, I'm listening” held on D (bars 11–12); a ride swell into the last chorus",
        "Last Chorus": "EVERYTHING OPEN: guitar strums eighths, strings high, kit with sticks, crash on 1; harmony on every line. Last bar 5 → 1: “Speak, I'm listening” comes home to G",
        "Outro": "Guitar picking over held strings, softer each bar; END on G, let it ring"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    def num(c):
        base, _, bs = c.partition("/"); BN = {"G": "1", "A": "2", "B": "3", "C": "4", "D": "5", "E": "6", "F#": "7", "F": "♭7"}
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
<div class="hdr"><h1>The World Is Asking</h1>
<div class="meta">♩ = 84 &nbsp;·&nbsp; KEY: G major &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: indie folk, walking, fingerpicked &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> G major: 1 = G, 2m = Am, 3m = Bm, 4 = C, 5 = D, 6m = Em, ♭7 = F. A cell with two numbers: two beats each. Every line of the lyric is two bars; the chorus and the verse are sixteen bars each.</div>
</body></html>"""
open("/home/claude/p59/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p59/out/The World Is Asking - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
asyncio.run(main()); print("ok")
