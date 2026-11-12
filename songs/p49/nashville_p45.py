"""Before It's Done -- the number chart: each section numbered in its own key (1 = G through the bridge; the last chorus and the tag in A,
1 = A); 4/4 at 72, fingerpicked; the guitar's shapes as numbers, a bar split where the guitar's sus resolves at the half bar. HTML -> PDF,
letter landscape."""
import asyncio, pickle
REC = pickle.load(open("/home/claude/p49/song_record.pkl", "rb"))
NUM_G = {"G": "1", "Gsus4": "1sus", "Gres": "1", "D/F#": "5/7", "Em7": "6m7", "Cadd9": "4add9", "Am7": "2m7", "Dsus4": "5sus", "D": "5", "E": "6", "Esus4": "6sus"}
NUM_A = {"A": "1", "Asus4": "1sus", "E/G#": "5/7", "F#m7": "6m7", "Dadd9": "4add9", "E": "5", "Esus4": "5sus"}
LIFTED = REC["lifted"]
BARS = REC["bars"]
def cell(b, num):
    sh = [REC["shape_at"][b * 8 + e] for e in range(8)]; out = []
    for x in sh:
        n = num[x]
        if not out or out[-1] != n: out.append(n)
    return " ".join(out) if len(out) <= 2 else " ".join(out[:3])
FEEL = {"Intro": "Guitar alone, fingerpicked, let ring. Bar 4: the top strings play D C B A over the 5 (the chorus's last four notes)",
        "Verse 1": "Thumb on 1 and 3, strings 3 2 1 / 3 2 3 between; quiet; let ring. The 5 plain: the voice sings its third",
        "Chorus 1": "Pinch the top string on 1; bass walks 1 - 7 - 6 - 4 (G F# E C). Bar 1: 1sus on beat 3, resolving on 4 under 'thought'",
        "Verse 2": "As verse 1; CELLO enters: a falling line of long notes (E C B A G C A D)", "Chorus 2": "= Chorus 1; the cello high, answering the voice in its gaps",
        "Bridge": "Lighter: quarters, let ring; cello low (A B C B A G E). Bars 7-8 STRUMMED, building: 4add9 in quarters, then 6sus - 6 (E) into the new key",
        "Last Chorus": "UP A STEP: A. Pinch on 1 and 3, fullest; bass walks 1 - 7 - 6 - 4 (A G# F# D). The cello takes the suspension over 'morning', then C#5 B A",
        "Tag": "Quiet. Last bar: E D C# B on the top strings over the 4add9, arriving on the singer's last note; the cello's low D rings. Ends open, on the 4"}
def rows(cells, w=8): return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells[i:i + w]) + "</tr>" for i in range(0, len(cells), w))
body = ""
for s, nb, b0, met in REC["plan"]:
    NUM = NUM_A if s in LIFTED else NUM_G
    cells = [cell(b, NUM) for b in range(b0, b0 + nb)]
    key_ = "A" if s in LIFTED else "G"
    if s == "Chorus 2":
        body += f"""<div class="sec"><div class="lab"><span class="name">{s.upper()}</span> <span class="bars">{nb}</span><div class="bar">bars {b0 + 1}–{b0 + nb}</div></div><div class="nums2">= Chorus 1</div><div class="drum">{FEEL[s]}</div></div>"""; continue
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
<div class="hdr"><h1>Before It's Done</h1>
<div class="meta">4/4, ♩ = 72 &nbsp;·&nbsp; KEY: G major; the last chorus and the tag up a whole step to A &nbsp;·&nbsp; FEEL: fingerpicked steel-string guitar, open strings ringing; cello from verse 2 &nbsp;·&nbsp; {REC['nbars']} bars · {round(secs) // 60}:{round(secs) % 60:02d}</div>
<div class="cred">Words and music: Jason Bryant · 2026</div></div>
{body}
<div class="foot"><b>Numbers.</b> In G: 1 = G, 2m7 = Am7, 4add9 = Cadd9, 5 = D, 5/7 = D/F#, 6m7 = Em7, 6 = E (major; it turns toward the new key). In A: 1 = A, 4add9 = Dadd9, 5 = E, 5/7 = E/G#, 6m7 = F#m7. Two numbers in a bar: half a bar each (a sus and its resolution). Standard tuning, no capo; the top two strings ring D and G through the G sections. <b>Form.</b> Intro 4 · Verse 8 · Chorus 8 · Verse 8 · Chorus 8 · Bridge 8 · Last Chorus 8 (in A) · Tag 4. <b>Voice.</b> A man's middle voice; every line. "Hold that thought": "thought" held over the 1sus resolving. The tag ends on the 2nd of A over the 4: left open.</div>
</body></html>"""
open("/home/claude/p49/out/nashville.html", "w").write(doc)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(300)
        await pg.pdf(path="/home/claude/p49/out/Before It's Done - Nashville chart.pdf", format="Letter", landscape=True, margin=dict(top="0.35in", bottom="0.3in", left="0.4in", right="0.4in"), scale=0.9, print_background=True)
        await b.close()
asyncio.run(main()); print("ok")
