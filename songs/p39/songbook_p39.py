"""Write songbook.md for 'Fixed by Fall' from the song record: every bar number, pitch and chord read from the record. For musicians only."""
import pickle, sys
sys.path.insert(0, "/home/claude/p39")
import lyric_p39 as L
REC = pickle.load(open("/home/claude/p39/song_record.pkl", "rb"))
BAR = 48; lead = REC["lead"]; BARS = REC["bars"]; NB = REC["nbars"]; QB = REC["qbpm"]
NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
CHN = {"A": "A", "E": "E", "F#m": "F♯m", "D": "D", "B": "B", "C#m": "C♯m"}
BEATW = {0: "", 3: " (just after)", 6: " (the 'and')", 9: " (late)"}
def pos(t): b, r = divmod(t, BAR); return f"bar {b + 1}, beat {r // 12 + 1}" + BEATW[r % 12]
plan = {s: (nb, b0) for s, nb, b0, _ in REC["plan"]}
def words_of(sec):
    out = []
    for toks in REC["text"][sec]:
        ws, cur, owner = [], "", []
        for t, hy in toks:
            cur += t; owner.append(len(ws))
            if not hy: ws.append(cur.strip(",.;:—")); cur = ""
        out.append([ws[o] for o in owner])
    return out
WORDS = {s: words_of(s) for s in REC["text"]}
def line_rows(sec):
    out = []
    for i, (role, text) in enumerate(dict(L.SECTIONS)[sec]):
        ns = [n for n in lead if n["sec"] == sec and n["line"] == i]
        b0, b1 = ns[0]["on"] // BAR, ns[-1]["on"] // BAR
        hi = max(ns, key=lambda n: (n["midi"], -n["on"]))
        out.append(dict(i=i, text=text, bar=b0 + 1, bars=f"{b0 + 1}–{b1 + 1}" if b1 > b0 else f"{b0 + 1}",
                        chords=" – ".join(CHN[BARS[b]["chord"]] for b in range(b0, b1 + 1)), first=nm(ns[0]["midi"]), last=nm(ns[-1]["midi"]),
                        hi=nm(hi["midi"]), hi_word=WORDS[sec][i][hi["syl"]]))
    return out
def rng(s): ps = [n["midi"] for n in lead if n["sec"] == s]; return nm(min(ps)), nm(max(ps))
def t_at(bar): s = bar * 4 * 60 / QB; return f"{int(s // 60)}:{int(round(s % 60)):02d}"
secs = REC["seconds"]; LEN = f"{int(secs // 60)}:{int(round(secs % 60)):02d}"
top = max(n["midi"] for n in lead); summits = [n for n in lead if n["midi"] == top]
lo_all, hi_all = nm(min(n["midi"] for n in lead)), nm(top)
second = max(n["midi"] for n in lead if n["midi"] != top)
seconds_at = [n for n in lead if n["midi"] == second]
vlo, vhi = rng("Verse 1"); clo, chi = rng("Chorus 1"); blo, bhi = rng("Bridge")
c1 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; c2 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 1]
tag = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 8]
tune = [e for e in REC["lgtr"] if e["art"] == "tune:intro"][:len(REC["riff"]["ons"])]
fills = sorted({e["art"].split(":", 1)[1] for e in REC["lgtr"] if e["art"].startswith("fill:")}, key=lambda x: [n["on"] for n in lead if f"{n['sec']}:{n['line']}" == x][0])
fill_bars = [min(e["on"] for e in REC["lgtr"] if e["art"] == "fill:" + f) // BAR + 1 for f in fills]
def LINE_OF(f):
    sec, i = f.split(':'); t = dict(L.SECTIONS)[sec][int(i)][1].rstrip(',.;—: ')
    return f"'{t}' ({sec.lower()})"
sb0 = plan["Solo"][1]; bb0 = plan["Bridge"][1]; lb0 = plan["Last Chorus"][1]
roots = sorted({e["p"][0] for e in REC["bass"] if e["on"] % BAR == 0})
md = []
md.append("---\ntitle: \"Fixed by Fall\"\nsubtitle: \"Songbook and production notes\"\nauthor: \"Words and music: Jason Bryant\"\n---\n")
md.append("## At a glance\n")
md.append("*Fixed by Fall* is a sneering rock shuffle for one gritty baritone. An all-seeing narrator cuts between the rooms where both sides of the political class take the same money: the same fundraiser on consecutive nights, a minute of rage on the floor and then the cough drops passed along, the stock trade at 9:31, the bill written down the street, the bridge study paid to both families. The chorus is their campaign promise sung back as a bright jingle (\"Vote for me, I'll fix it all\"), with 'fix' turning from a promise to a rigged deal. The bridge follows them out of office to one cake, one board, one lake, one firm. In the last chorus the two candidates are the same singer on two tracks: they start apart and end in unison, \"Vote for us\", and the punchline lands on the listener. No party, colour, side or name is ever said.\n")
md.append(f"| | |\n|---|---|\n| Key | E major throughout (D, the flat seventh, under the second 'vote for me') |\n| Tempo | ♩ = {QB}; shuffle (eighths swung) in the verses, bridge, solo, intro and outro; the choruses straight |\n| Length | {NB} bars, {LEN} |\n| Voice | one gritty baritone, {lo_all} to {hi_all} (the {hi_all} four times, always on 'Vote'); double-tracked in chorus 2 and the last chorus |\n| Chords | one a bar, root position: E, F♯m, A, B, C♯m, D |\n")
md.append("**Form**\n")
md.append("| Section | Bars | Starts at | Feel | Chords |\n|---|---|---|---|---|")
for s_, nb, b0, _ in REC["plan"]:
    md.append(f"| {s_} | {b0 + 1}–{b0 + nb} | {t_at(b0)} | {'straight' if s_ not in REC['swung'] else 'shuffle'} | " + " ".join(CHN[BARS[b]["chord"]] for b in range(b0, b0 + nb)) + " |")
md.append("")
md.append(f"**How to play it.** Two feels. The verses (and the intro, bridge, solo and outro) are a dry shuffle: swung eighths, kick on 1 and 3, snare on 2 and 4, the guitar playing the boogie (root-fifth, root-sixth), the bass walking root, root, fifth, fifth, sixth, sixth, fifth, root, the piano on the 'and's. Every chorus snaps into a straight rally march: kick on every beat, a marching snare, straight eighths on the ride and the guitar, piano in quarters, a crash on 1. It should sound like the band switched into a campaign jingle. The bridge pulls back; the solo goes back to the shuffle; the last chorus is the fullest, with a tambourine and the duet; the outro is the shuffle again, ending on one hit in bar {NB}.\n")
md.append("## Section by section\n")
pl = REC["plans"]
NOTE = {
    "Verse 1": f"Low, dry and conversational, between {rng('Verse 1')[0]} and {rng('Verse 1')[1]}, the words landing on the 'and's as much as on the beats (sneer it, don't croon it). Lines 1–2 make a pair and lines 3–4 sing the same pair again; lines 5–8 bring lines 1–4 back with new words. Each line ends on a held note with a breath after it.",
    "Chorus 1": f"Straight, bright, a jingle. 'VOTE' on beat 1 at the top of the song, {hi_all}, then down through the chord ({' – '.join(nm(n['midi']) for n in c1)}). 'Vote for me' again a whole step down, on {nm(c2[0]['midi'])} over D. 'Fixed' lands on beat 3 and 'fall' drops to {nm([n for n in lead if n['sec'] == 'Chorus 1' and n['line'] == 3][-1]['midi'])}: deadpan.",
    "Verse 2": "Verse 1's tune and cadence notes, the rhythm fitted again to the new words, so the bars do not line up note for note with verse 1. Back to the shuffle.",
    "Chorus 2": "Chorus 1's tune, sung flatter, and double-tracked (the same singer twice, in unison). The last line changes: 'he's paid, I'm paid, that's all.'",
    "Bridge": f"A new tune, higher than the verse ({rng('Bridge')[0]}–{rng('Bridge')[1]}) but under the chorus's top. One cake, the board, the lake, the names in gold: keep it light and nasty, it sets up the duet.",
    "Last Chorus": f"The duet, one singer on two tracks. Line 1 voice one alone, line 2 voice two alone, lines 3–4 both (voice two a third under). Then unison: 'Vote for us' returns the {hi_all}, the words turn past tense ('we fixed it all', 'we shook hands') and the punchline: 'and you got fixed by fall.' The tag, both voices, falling: {' – '.join(nm(n['midi']) for n in tag)}."}
for s_ in ("Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s_]
    md.append(f"### {s_} (bars {b0 + 1}–{b0 + nb})\n")
    md.append(NOTE[s_] + "\n")
    md.append("| Bars | Line | Chords | First – last note | Top note |\n|---|---|---|---|---|")
    for r in line_rows(s_): md.append(f"| {r['bars']} | {r['text']} | {r['chords']} | {r['first']} – {r['last']} | {r['hi']} ({r['hi_word']}) |")
    md.append("")
md.append("## For each player\n")
md.append(f"**Drums.** Shuffle sections: kick on 1 and 3, snare on 2 and 4, swung hats (the ride in the solo); a crash on bar 1. Choruses: straight, kick on every beat, the snare on 2 and 4 with a pickup on the 'and' of 4, straight eighths on the ride, a crash on each chorus's first bar; the last chorus adds a tambourine in eighths and a crash every four bars. A fill in the last two beats of every section (bars {', '.join(str(plan[s][1] + plan[s][0]) for s in ('Intro', 'Verse 1', 'Chorus 1', 'Verse 2', 'Chorus 2', 'Bridge', 'Solo', 'Last Chorus'))}). Bar {NB}: one hit.\n")
md.append(f"**Bass.** In at the verse. Every bar starts on the root. Shuffle sections: the boogie, root, root, fifth, fifth, sixth, sixth, fifth, root, swung. Choruses: straight eighths (root, fifth, octave). Bridge: half notes, root and fifth. Roots {nm(roots[0])}–{nm(roots[-1])}. Bar {NB}: one hit.\n")
md.append("**Rhythm guitar.** The boogie in the shuffle sections (root-fifth, root-sixth, swung eighths); open power chords in straight eighths in the choruses; held chords in the bridge and under the solo. Bar 90: one E chord, let it ring.\n")
md.append("**Piano.** Barroom: triads on the 'and's in the verses and outro (swung), quarter-note chords in the choruses like a rally piano, held chords in the bridge, out for the solo.\n")
md.append(f"**Lead guitar.** The intro tune is a one-bar figure of four notes ({' '.join(nm(e['p'][0]) for e in tune)} over E), played in the four intro bars and again in the outro. Fills in the gaps after {'; '.join(LINE_OF(f) for f in fills)} (bars {', '.join(map(str, fill_bars))}); never over a sung word. The solo (bars {sb0 + 1}–{sb0 + 8}) states the tune, answers it two steps higher, sings a line over the chorus changes in the shuffle and ends on a chord tone.\n")
md.append(f"**Singer.** Range {lo_all}–{hi_all}. The verses sit low ({rng('Verse 1')[0]}–{rng('Verse 1')[1]}): sneer, lean on the off-beats, keep it dry. The chorus is bright and fake, a jingle; by chorus 2 let it go flat and bored. The {hi_all} comes four times, always on 'Vote' over E: " + "; ".join(pos(n["on"]) for n in summits) + f". The next highest note is {nm(second)}. Double-track chorus 2. For the last chorus, record two passes as two candidates (pass one sings line 1, pass two line 2, then a third under on lines 3–4), and sing the unison lines as nearly identical as you can: the point is that it's the same man.\n")
md.append("**Arrangement.** Shuffle verses, march choruses: the switch is the joke, so make it clean. The bridge pulls back; the solo pushes in the shuffle; the last chorus is the fullest (tambourine, crashes every four bars, the duet), then the tag, then the shuffle out to one hit.\n")
md.append("## Production notes\n")
md.append("### Lyric sheet\n")
for s_ in ("Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s_]; md.append(f"**{s_}** (bar {b0 + 1})  ")
    for r in line_rows(s_): md.append(f"{r['bar']}: {r['text']}  ")
    md.append("")
md.append("### Production brief\n")
md.append("**The song.** An all-seeing narrator shows the political class on both sides as one business: the same donors, the same staged rage, the same trade, the same families paid, the same retirement. The chorus is their own jingle, sung back. It must not favour either side: the lyric names no party, colour, person or issue, and the production shouldn't either (no campaign samples of real people, no party colours in any artwork).\n")
md.append("**References.**\n")
md.append(open("/home/claude/p39/refs.md").read().strip() + "\n")
md.append(f"**Non-negotiables.** The shuffle in the verses and the straight march in the choruses, switched cleanly. The {hi_all} on 'VOTE', beat 1 over E, four times and nowhere else. The same singer on both tracks of the duet, ending in unison. The tag 'Fixed by fall' falling to E. One hit on bar {NB}. The voice in front (about 6 dB over the band in the demo).\n")
md.append("### Session notes\n")
md.append(f"- **Tempo and click:** ♩ = {QB} throughout; {LEN} for {NB} bars. Click in quarters; the shuffle sections swung (a triplet feel), the choruses straight. Count in one bar.\n- **Key:** E major; no modulation.\n- **Chords:** one per bar, root position (the form table lists every bar).\n- **Range:** voice {lo_all}–{hi_all}; bass {nm(roots[0])}–{nm(roots[-1])} with octaves above.\n")
md.append("- **Tracking order:** drums and bass to the click (the feel switch locked first), the boogie guitar (double it), piano, lead guitar, then the lead vocal, chorus 2's double, and the last chorus's second candidate.\n")
md.append("- **Blend and panning:** kick, snare and bass centre; the boogie guitars wide; piano right; lead guitar slightly right. Lead vocal just left of centre; the second track just right, so the duet opens out and closes to the middle in the unison.\n")
md.append("- **Separate passes:** chorus 2's double and the last chorus's second candidate are passes of their own.\n")
md.append("### Score and parts\n")
md.append("- Lead sheet (voice, lyrics, chord symbols, the feel marks): *Fixed by Fall - lead sheet.pdf*\n- Parts (lead guitar, rhythm guitar, piano, voice 2, bass, drums): *Fixed by Fall - parts.pdf*\n- Number chart: *Fixed by Fall - Nashville chart.pdf*\n- Demo: *Fixed by Fall - demo.mp3*, with General MIDI and GarageBand MIDI files\n")
open("/home/claude/p39/songbook.md", "w").write("\n".join(md))
print("songbook.md written:", len(md), "lines")
