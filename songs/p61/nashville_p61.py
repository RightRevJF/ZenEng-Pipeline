"""A Wire Pulled Tight -- the number chart: A major (1 = A), written at double tempo with a half-time feel (q = 116 rising to 164, felt 58 to 82),
all 4/4; one cell a written bar; a bar with two chords shows both. HTML -> PDF, letter landscape."""
import asyncio, pickle, collections
REC = pickle.load(open("/home/claude/p61/song_record.pkl", "rb"))
BARS = REC["bars"]
RN = {"A": "1", "B": "2", "C#": "3", "D": "4", "E": "5", "F#": "6", "G": "♭7", "G#": "7", "A#": "♯1"}
QN = {"": "", "m": "m", "m7": "m7", "add9": "add9", "sus2": "sus2", "sus4": "sus4", "maj7": "maj7", "dim7": "°7"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] == "#" else base[:1]
    r_ = "♯1" if rt_ == "C#" and base.endswith("dim7") else RN[rt_]
    return r_ + QN[base[len(rt_):]] + (f"/{RN[bs]}" if bs else "")
T = REC["tempo"]
def tq(s): a, z = T[s]; return f"♩ = {a} (felt {a // 2})" if a == z else f"♩ = {a} → {z} (felt {a // 2} → {z // 2})"
FEEL = {"Intro": "Acoustic guitar alone, fingerpicked",
        "Verse 1": "Acoustic and voice only. Four bars a line",
        "Pre 1": "BASS IN, held roots; clean electric swells. Accelerate into the chorus",
        "Chorus 1": "KIT IN, light: kick, cross-stick on beat 3 (half-time), hat. Clean arpeggios, organ pad. Hook “time is breaking through”: “through” on C♯ over 4maj7, HOLD 4½ bars. Harmony on the hook",
        "Verse 2": "Brushes; bass; overdriven guitar palm-muted, quiet",
        "Pre 2": "Strummed; brushes; snare roll in the last half-bar",
        "Chorus 2": "FULL KIT, snare on 3; overdriven chords open; organ. Crash on bar 1",
        "Verse 3": "Full kit; overdriven guitar palm-muted",
        "Pre 3": "Building; last bar ♯1°7 (C♯dim7) and a fill",
        "Chorus 3": "Ride; crash on each line's downbeat; harmony on the first four lines and the hook",
        "Verse 4": "DRIVING: hats in eighths, guitars driving, organ. Crash on bar 1",
        "Bridge": "Bars 1–8: acoustic and kick alone, low (clean arpeggios from bar 5). Bars 9–16: BUILD: kit, strummed, organ, overdrive from bar 13; fill into a FULL STOP",
        "Approach": "Bar 1: SILENCE, everyone. Bars 2–8: acoustic alone, slowing. Do not fill it",
        "Last Chorus": "Full band, steady. Bars 13–15 (the ♭7): THIN to voice, acoustic, organ. Bars 16–17 (1sus4): band back under “through” on E, the song's top. Bar 18: RELEASE to 1, let it ring",
        "Tag": "Acoustic alone; the last 1 rings and decays. No fade"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""; b = 0
for s, nb, st, mets, mv in REC["plan"]:
    rng = range(b, b + nb)
    cells = []
    for bi in rng:
        x = BARS[bi]; met = x["meter"]; tag = "" if met == "4/4" else f"<sup>{met}</sup>"
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
<div class="hdr"><h1>A Wire Pulled Tight</h1>
<div class="meta">♩ = 116 → 164, HALF-TIME FEEL (felt 58 → 82) &nbsp;·&nbsp; KEY: A major &nbsp;·&nbsp; 4/4 &nbsp;·&nbsp; FEEL: slow-build alternative rock &nbsp;·&nbsp; {int(secs // 60)}:{int(round(secs % 60)):02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> A major: 1 = A, 2m = Bm, 3m = C♯m, 4 = D, 5 = E, 6m = F♯m, 6 = F♯ (major), ♭7 = G; ♯1°7 = C♯dim7; /3 = over the third (A/C♯ = 1/3, E/G♯ = 5/7, F♯/A♯ = 6/♯1). One cell is one written bar (half a felt bar): the snare on beat 3. Verse lines take four bars; every other line two; the hook's last line holds.</div>
</body></html>"""
open("/home/claude/p61/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b_ = await p.chromium.launch(); pg = await b_.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p61/out/A Wire Pulled Tight (v6) - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.86, print_background=True)
        await b_.close()
asyncio.run(main()); print("ok")
