"""This Side of the Door (song 61) -- the number chart, in the record's key (keyinfo61), q = 80, a ballad, all 4/4; one cell a bar; a bar with two chords
shows both. Every section's notes are read from the record (where the stop falls, the hook's bars). HTML -> PDF, letter landscape."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo61 as KI
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p71/song_record.pkl", "rb"))
BARS = REC["bars"]
QN = {"": "", "m": "m", "7": "7", "m7": "m7", "sus4": "sus4", "sus2": "sus2", "maj7": "maj7"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return KI.number(rt_) + QN[base[len(rt_):]] + (f"/{KI.number(bs)}" if bs else "")
B0 = {s: st // 48 for s, nb, st, mets, mv in REC["plan"]}
_b1 = {s: st // 48 + 1 for s, nb, st, mets, mv in REC["plan"]}; _sung = min(n_["on"] for n_ in REC["lead"]) // 48 + 1
def _secbars(s_): return [x for x in BARS if x["sec"] == s_]                                  # the section's bars, read from the record
def _cell(x): return " ".join(num(c) for c in (x["beats4"] or [])) if x.get("beats4") else (num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"]))
def _nw(n): return {2: "two", 4: "four", 6: "six", 8: "eight", 10: "ten", 12: "twelve", 14: "fourteen", 16: "sixteen", 18: "eighteen", 20: "twenty"}.get(n, str(n))
def _line_bar(s_, i): return min(n_["on"] for n_ in REC["lead"] if n_["sec"] == s_ and n_["line"] == i) // 48 + 1
_top = max(x["midi"] for x in REC["lead"]); _topw = next(n_ for n_ in REC["lead"] if n_["sec"] == "Chorus 1" and n_["midi"] == _top)
_bare = _line_bar("Last Chorus", 6); _cel = min(e["on"] for e in REC["parts"]["cello"]) // 48 + 1; _str = min(e["on"] for e in REC["parts"]["strings"]) // 48 + 1
FEEL = {"Intro": f"Fingerpicked guitar alone, steady eighths. Voice picks up in bar {_sung}",
        "Verse 1": "Guitar alone under her, fingerpicked eighths, soft",
        "Chorus 1": f"Guitar alone, a little fuller. Top note on “{_topw['text']}” (bar {_topw['on'] // 48 + 1}). The title line in bar {_line_bar('Chorus 1', 7)}: let “door” ring",
        "Verse 2": f"As verse 1. CELLO enters (bar {_cel}), the chord's root held",
        "Bridge": f"Starts on {_cell(_secbars('Bridge')[0])}. OPENS UP: STRINGS and BASS in (bar {_str}), cello on. She sings low and plain",
        "Verse 3": "Strings and bass out: guitar and cello, quieter",
        "Last Chorus": f"Strings, bass and cello back; a HARMONY voice with her. At “Three, and then two” (bar {_bare}) all out but the guitar",
        "Outro": f"{_nw(len(_secbars('Outro'))).capitalize()} bars, guitar alone: " + ", ".join(_cell(x) for x in _secbars('Outro')) + ". Let the last chord ring"}
for _s in [x[0] for x in REC["plan"]]:
    if _s.startswith("Turn"): FEEL[_s] = f"{_nw(len(_secbars(_s))).capitalize()} bars, the guitar alone: " + ", ".join(_cell(x) for x in _secbars(_s)) + ". She rests"
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
<div class="meta">♩ = 80 &nbsp;·&nbsp; KEY: {KI.KEYSTR}{(' &nbsp;·&nbsp; GUITAR: ' + KI.CAPO) if KI.CAPO else ''} &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: ballad, fingerpicked &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> {KI.numbers_line()}. One cell is one bar; two numbers in a cell split it, two beats each; four numbers, a beat each.
<b>Band.</b> Fingerpicked acoustic guitar throughout; cello from verse 2; strings and bass in the bridge and the last chorus; no drums. <b>Voices.</b> One singer, an alto; a harmony voice with her in the last chorus.</div>
</body></html>"""
open("/home/claude/p71/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path=f"/home/claude/p71/out/{REC['file_title']} - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
if __name__ == "__main__":
    asyncio.run(main()); print("ok")
