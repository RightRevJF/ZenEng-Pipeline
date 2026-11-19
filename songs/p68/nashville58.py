"""Same Time Tomorrow (song 58) -- the number chart, in the record's key (keyinfo58), q = 84, a folk ballad, all 4/4; one cell a bar; a bar with two chords
shows both. Every section's notes are read from the record (where the stop falls, the hook's bars). HTML -> PDF, letter landscape."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo58 as KI
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p68/song_record.pkl", "rb"))
BARS = REC["bars"]
QN = {"": "", "m": "m", "7": "7", "m7": "m7", "sus4": "sus4", "sus2": "sus2", "maj7": "maj7"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return KI.number(rt_) + QN[base[len(rt_):]] + (f"/{KI.number(bs)}" if bs else "")
B0 = {s: st // 48 for s, nb, st, mets, mv in REC["plan"]}
def title_desc(REC_):
    """where the title falls against the chorus's first bar, read from the record"""
    b0 = next(st for s, nb, st, _, _ in REC_["plan"] if s == "Chorus 1"); ns = [n for n in REC_["lead"] if n["sec"] == "Chorus 1" and n["line"] == 0 and n["first"]]
    if ns[0]["on"] >= b0: return "on the chorus's downbeat", "Title on the downbeat."
    beat = (ns[0]["on"] % 48) // 12 + 1; land = next((n for n in ns if n["on"] >= b0), None); w = land["text"].strip(",.") if land else ""
    return (f"“{ns[0]['text']}” on beat {beat} of the bar before the chorus and “{w}” on its downbeat",
            f"The title picks up on beat {beat} of the bar before; “{w}” lands on the downbeat.")
_TD = title_desc(REC)
_dr = min(e["on"] for e in REC["parts"]["drums"]) // 48 + 1; _fills = sorted({e["on"] // 48 + 1 for e in REC["parts"]["drums"] if e["p"][0] in (45, 48)})
_b1 = {s: st // 48 + 1 for s, nb, st, mets, mv in REC["plan"]}; _sung = min(n_["on"] for n_ in REC["lead"]) // 48 + 1
_rel = lambda s: [f - _b1[s] + 1 for f in _fills if _b1[s] <= f < _b1[s] + dict((x[0], x[1]) for x in REC["plan"])[s]]
def _secbars(s_): return [x for x in BARS if x["sec"] == s_]                                  # the section's bars, read from the record
def _cell(x): return " ".join(num(c) for c in (x["beats4"] or [])) if x.get("beats4") else (num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"]))
def _nw(n): return {2: "two", 4: "four", 6: "six", 8: "eight", 12: "twelve", 14: "fourteen", 16: "sixteen", 18: "eighteen", 20: "twenty"}.get(n, str(n))
FEEL = {"Intro": f"Guitar strums eighths and bass plays quarters from bar 1; drums in at bar {_dr}. Voice picks up in bar {_sung}",
        "Verse 1": f"Guitar strums eighths under him all the way; bass quarters; kick 1 and 3, snare 2 and 4. TOM FILL in bar {_rel('Verse 1')[0] if _rel('Verse 1') else '-'}",
        "Chorus 1": _TD[1] + " Harmony voice under him all chorus. The chorus's top note in bar " + ", ".join(str(b_) for b_ in sorted({n_["on"] // 48 + 1 - _b1["Chorus 1"] + 1 for n_ in REC["lead"] if n_["sec"] == "Chorus 1" and n_["midi"] == max(x["midi"] for x in REC["lead"] if x["sec"] == "Chorus 1")})),
        "Verse 2": "As verse 1",
        "Chorus 2": "As chorus 1",
        "Bridge": f"Starts on {_cell(_secbars('Bridge')[0])}. Same groove; he sings through" if _secbars('Bridge') else "",
        "Verse 3": "As verse 1",
        "Last Chorus": (f"{_nw(len(_secbars('Last Chorus'))).capitalize()} bars, {_nw(len(_secbars('Last Chorus')) - len(_secbars('Chorus 1')))} more than the others: the last two are {_cell(_secbars('Last Chorus')[-2])}, {_cell(_secbars('Last Chorus')[-1])}" if len(_secbars('Last Chorus')) > len(_secbars('Chorus 1')) else f"As chorus 1; the last two bars {_cell(_secbars('Last Chorus')[-2])}, {_cell(_secbars('Last Chorus')[-1])}"),
        "Outro": f"{_nw(len(_secbars('Outro'))).capitalize()} bars: " + ", ".join(_cell(x) for x in _secbars('Outro')) + ". Band to the end"}
for _s in [x[0] for x in REC["plan"]]:
    if _s.startswith("Turn"): FEEL[_s] = f"{_nw(len(_secbars(_s))).capitalize()} bars, the band alone: " + ", ".join(_cell(x) for x in _secbars(_s)) + ". He rests"
_TURNS = [x[0] for x in REC["plan"] if x[0].startswith("Turn")]
def _disp(s_): return ("Turn" if len(_TURNS) == 1 else f"Turn {_TURNS.index(s_) + 1}") if s_ in _TURNS else s_      # a musician reads "Turn", not the record's count from the end
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    cells = []
    for bi in range(b, b + nb):
        x = BARS[bi]
        cells.append(" ".join(num(c_) for c_ in x["beats4"]) if x.get("beats4") else num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"]))
    lab = f"""<div class="lab"><span class="name">{_disp(s).upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b + 1}–{b + nb}</div></div>"""
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
<div class="meta">♩ = 84 &nbsp;·&nbsp; KEY: {KI.KEYSTR}{(' &nbsp;·&nbsp; GUITAR: ' + KI.CAPO) if KI.CAPO else ''} &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: folk ballad &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> {KI.numbers_line()}. One cell is one bar; two numbers in a cell split it, two beats each; four numbers, a beat each.
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
