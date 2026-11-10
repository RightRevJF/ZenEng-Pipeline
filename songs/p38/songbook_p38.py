"""Write songbook.md for 'Stay Tuned' from the song record: every bar number, pitch and chord read from the record. For musicians only."""
import pickle, sys
sys.path.insert(0, "/home/claude/p38")
import lyric_p38 as L
REC = pickle.load(open("/home/claude/p38/song_record.pkl", "rb"))
BAR = 48; lead = REC["lead"]; BARS = REC["bars"]; NB = REC["nbars"]; QB = REC["qbpm"]
NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
CHN = {"A": "A", "E": "E", "F#m": "F♯m", "D": "D", "Bm": "Bm", "G": "G", "N.C.": "N.C."}
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
vlo, vhi = rng("Verse 1"); plo, phi = rng("Pre 1"); clo, chi = rng("Chorus 1"); blo, bhi = rng("Bridge")
c1 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; c2 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 1]
tag = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 8]
stop = [b + 1 for b in REC["stop_bars"]]; outro = plan["Outro"][1] + 1
tune = [e for e in REC["lgtr"] if e["art"] == "tune:intro"][:len(REC["riff"]["ons"])]
fills = sorted({e["art"].split(":", 1)[1] for e in REC["lgtr"] if e["art"].startswith("fill:")}, key=lambda x: [n["on"] for n in lead if f"{n['sec']}:{n['line']}" == x][0])
fill_bars = [min(e["on"] for e in REC["lgtr"] if e["art"] == "fill:" + f) // BAR + 1 for f in fills]
cm = REC["counter"]; cm_lo, cm_hi = nm(min(e["p"][0] for e in cm)), nm(max(e["p"][0] for e in cm))
def LINE_OF(f):
    sec, i = f.split(':'); t = dict(L.SECTIONS)[sec][int(i)][1].rstrip(',.;—: ')
    return f"'{t}' ({sec.lower()})"
kb0 = plan["Breakdown"][1]; sb0 = plan["Solo"][1]; bb0 = plan["Bridge"][1]
pre_fill_bars = [plan[s][1] + plan[s][0] for s in ("Pre 1", "Pre 2")]
roots = sorted({e["p"][0] for e in REC["bass"] if e["on"] % BAR == 0})
md = []
md.append("---\ntitle: \"Stay Tuned\"\nsubtitle: \"Songbook and production notes\"\nauthor: \"Words and music: Jason Bryant\"\n---\n")
md.append("## At a glance\n")
md.append("*Stay Tuned* is a rock song for a male high baritone, angry and sarcastic. It is sung by the man behind the camera on a cable shouting show. He powders and frames both sides the same; on air they go to war, off air they laugh in the hall, share a car and the same owner. He is paid to light the fight, and it has split his own family. The chorus is the network talking to you (stay tuned, stay mad, don't touch that dial) until the last one, when he cuts the cameras himself and tells you to turn it off. No party and no name is ever said: both sides are the same act.\n")
md.append(f"| | |\n|---|---|\n| Key | A major throughout (G, the flat seventh, in the riff and the chorus) |\n| Tempo | ♩ = {QB}, straight eighths |\n| Length | {NB} bars, {LEN} |\n| Voice | male high baritone, {lo_all} to {hi_all} (the {hi_all} six times, always on 'tuned') |\n| Chords | one a bar, root position: A, Bm, D, E, F♯m, G |\n")
md.append("**Form**\n")
md.append("| Section | Bars | Starts at | Chords |\n|---|---|---|---|")
for s, nb, b0, _ in REC["plan"]:
    md.append(f"| {s} | {b0 + 1}–{b0 + nb} | {t_at(b0)} | " + " ".join(CHN[BARS[b]["chord"]] for b in range(b0, b0 + nb)) + " |")
md.append("")
md.append(f"**How to play it.** Straight eighths, hard. The synth pulse starts alone (four bars), the drums and the lead guitar's intro tune join it, and the bass and rhythm guitar wait for the verse. Verses and pre-choruses are a rock beat with palm-muted guitar; every chorus goes to four on the floor with open power chords. Each chorus opens on A – D – G – D under 'Stay tuned, stay mad / stay tuned, stay scared'. The bridge drops the pulse and holds the chords; an eight-bar guitar solo takes the chorus changes; the breakdown strips back to pulse, kick and hats and builds into the last chorus. The last chorus is the fullest, then everybody stops for two bars (bars {stop[0]}–{stop[1]}) while the singer says 'Turn it off' alone. One hit on beat 1 of bar {outro}, and let it ring out.\n")
md.append("## Section by section\n")
pl = REC["plans"]
NOTE = {
    "Verse 1": f"Low and close to speech, between {vlo} and {vhi}, lots of repeated notes: the cameraman is talking, not singing out." + (" Lines 1 and 3 share a tune." if pl["Verse"][0] == pl["Verse"][2] else "") + " Each line ends on a held note with a breath after it.",
    "Pre 1": f"The voice climbs ({plo}–{phi}); the last word, 'home', jumps up to {nm(max(n['midi'] for n in lead if n['sec'] == 'Pre 1'))} to set up the chorus. The drums fill in bar {pre_fill_bars[0]}.",
    "Chorus 1": f"Sixteen bars. 'Stay tuned, stay mad': the pickup on {nm(c1[0]['midi'])}, then 'TUNED' on beat 1 at the top of the song, {hi_all}, held three beats over A. 'Stay tuned, stay scared' answers it a whole step down ('tuned' on {nm(c2[1]['midi'])}, over G). Lines 5–6 bring the chant back; the chorus ends hanging on E ('so don't you touch that dial') so the verse can drop back to A.",
    "Verse 2": "Verse 1's tune and cadence notes, the rhythm fitted again to the new words (so the bars do not line up note for note with verse 1).",
    "Pre 2": "Pre-chorus 1's shape with the new words; 'Danny now' climbs to the chorus as 'home' did.",
    "Chorus 2": "Chorus 1 exactly; a gang vocal joins the chant lines an octave under.",
    "Bridge": f"The pulse drops out. A new tune, higher than the verse ({blo}–{bhi}) but under the chorus's top. 'They just need you to' is the turn: let it hang over the Bm–E into the solo.",
    "Last Chorus": f"Chorus 1's first six lines as written. Lines 7–8 change their words and keep the tune: 'so I cut camera left, / and camera right goes dark.' Then the band stops dead: 'Turn it off' alone, {' – '.join(nm(n['midi']) for n in tag)}, falling to the tonic. One hit on bar {outro}."}
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]
    md.append(f"### {s} (bars {b0 + 1}–{b0 + nb})\n")
    md.append(NOTE[s] + "\n")
    md.append("| Bars | Line | Chords | First – last note | Top note |\n|---|---|---|---|---|")
    for r in line_rows(s): md.append(f"| {r['bars']} | {r['text']} | {r['chords']} | {r['first']} – {r['last']} | {r['hi']} ({r['hi_word']}) |")
    md.append("")
md.append("## For each player\n")
md.append(f"**Drums.** Tacet for bars 1–4; in with a crash at bar 5. Verses, pre-choruses and the bridge: kick on 1 and 3 (the pre-chorus adds the 'and' of 3), snare on 2 and 4, eighth hats. Choruses and the solo: four on the floor, snare on 2 and 4, eighths on the ride, a crash on each chorus's first bar. A fill in the last two beats of every section (bars {', '.join(str(plan[s][1] + plan[s][0]) for s in ('Intro', 'Verse 1', 'Pre 1', 'Chorus 1', 'Verse 2', 'Pre 2', 'Chorus 2', 'Bridge', 'Solo', 'Breakdown'))}, and bar {plan['Last Chorus'][1] + 16} before the stop). Breakdown (bars {kb0 + 1}–{kb0 + 8}): kick on 1 and 3 and the hats for four bars, then the snare in eighths, building. Last chorus: a crash every four bars. Bars {stop[0]}–{stop[1]}: nothing. Bar {outro}: one hit, kick and crash.\n")
md.append(f"**Bass.** In at the verse. Every bar starts on the root; the eighth-note cell is root, root, fifth, root, root, octave, fifth, then a step or a fifth into the next bar's root. Bridge: quarters (root, fifth, root, approach). Breakdown: half notes for four bars, then the eighths again. Roots {nm(roots[0])}–{nm(roots[-1])}. Bar {outro}: one hit, root and octave, let it ring.\n")
md.append(f"**Rhythm guitar.** In at the verse. Power chords (root, fifth, octave): palm-muted eighths in the verses and the breakdown, quarters in the pre-choruses, open eighths in the choruses and the solo, held whole notes in the bridge. Bar {outro}: one A chord, let it ring.\n")
md.append(f"**Synth pulse.** The song's hum. An eighth-note figure on each bar's chord (root, fifth, octave, fifth, root, fifth, octave, third), in the register around A3–A4: alone for bars 1–4, then under everything except the bridge and the two stop bars. Think of the Lowrey-through-a-filter pulse on 'Won't Get Fooled Again', not a modern arpeggiator: chopped, organ-like, steady.\n")
md.append(f"**Organ.** Held three-note chords in the pre-choruses, the bridge and the solo; quarter-note stabs in the choruses. The last chorus adds a second organ line above the voice ({cm_lo}–{cm_hi}): it moves where the singer holds and holds where the singer moves. Bar {outro}: one A chord held to the end.\n")
md.append(f"**Lead guitar.** The intro tune is a one-bar figure of four notes ({' '.join(nm(e['p'][0]) for e in tune)} over A), played in intro bars 5–8 and again in breakdown bars {kb0 + 5}–{kb0 + 8}. Short fills (two beats, four to six notes) in the gaps after {'; '.join(LINE_OF(f) for f in fills)} (bars {', '.join(map(str, fill_bars))}); never over a sung word. The solo (bars {sb0 + 1}–{sb0 + 8}) states the intro tune, answers it two steps higher, sings a line over the chorus changes and ends on a chord tone of E into the breakdown.\n")
md.append(f"**Backing vocals.** Chorus 2: a gang vocal an octave under the chant lines ('Stay tuned, stay mad', 'stay tuned, stay scared', the second 'Stay tuned, stay mad'). Last chorus: the gang plus a third under on the same lines. Nothing on 'Turn it off'.\n")
md.append(f"**Singer.** Range {lo_all}–{hi_all}. The verses are low and nearly spoken, mostly between {vlo} and {vhi}, many repeated notes: keep them flat and dry, a man describing his job. The chorus is a chant: 'stay' is a pickup, 'TUNED' lands on beat 1 and holds three beats. The {hi_all} comes six times, always on 'tuned' over A: " + "; ".join(pos(n["on"]) for n in summits) + f". The next highest note is {nm(second)}. Sing 'Turn it off' to the room, not to the band; there is no band.\n")
md.append(f"**Arrangement.** Pulse alone, then drums and the guitar's tune, then the band at the verse. Verse tight and muted; each pre-chorus opens up and fills into the chorus; each chorus pounds (four on the floor), the second with a gang vocal. The bridge pulls back (no pulse); the solo pushes; the breakdown pulls back again and builds. The last chorus is the fullest (gang plus harmony, organ countermelody, crashes every four bars), then silence for 'Turn it off', then one hit.\n")
md.append("## Production notes\n")
md.append("### Lyric sheet\n")
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]; md.append(f"**{s}** (bar {b0 + 1})  ")
    for r in line_rows(s): md.append(f"{r['bar']}: {r['text']}  ")
    md.append("")
md.append("### Production brief\n")
md.append("**The song.** A cameraman on a cable shouting show tells you what he sees: the same makeup brush for both sides, the script feeding them what to hate, the laughing in the hall when the red light goes off, the one car and the one billionaire. He is paid to light the fight, and his father and brother don't speak. The chorus is the network's own voice, sarcastic; the last chorus is his, when he cuts the cameras. It must not favour either side: the lyric names no party, no person and no issue, and the production shouldn't either (no news-clip samples of real people).\n")
md.append("**References.**\n")
md.append(open("/home/claude/p38/refs.md").read().strip() + "\n")
md.append(f"**Non-negotiables.** The synth pulse opens the song alone. Four on the floor in every chorus. The {hi_all} on 'TUNED', on beat 1 over A, six times and nowhere else. The band stops dead for bars {stop[0]}–{stop[1]}; 'Turn it off' is sung alone; one hit on bar {outro}. The voice in front (it reads about 6 dB over the band in the demo).\n")
md.append("### Session notes\n")
md.append(f"- **Tempo and click:** ♩ = {QB} throughout; {LEN} for {NB} bars. Count in one bar; the pulse starts alone. Leave the click running through the stop bars so the last hit lands on time.\n- **Key:** A major; no modulation.\n- **Chords:** one per bar, root position (the form table lists every bar); N.C. for bars {stop[0]}–{stop[1]}.\n- **Range:** voice {lo_all}–{hi_all}; bass {nm(roots[0])}–{nm(roots[-1])} with octaves above.\n")
md.append("- **Tracking order:** the pulse to the click first (it's the grid everyone locks to), drums and bass, rhythm guitars (double them, left and right), organ, lead guitar, then the lead vocal, the gang vocal (several voices, an octave under) and the last chorus's harmony.\n")
md.append("- **Blend and panning:** kick, snare and bass centre; the pulse slightly left; rhythm guitars wide; organ right; lead guitar slightly right; the countermelody organ further right; lead vocal centre and on top (at least 3 dB over the band). 'Turn it off' dry and close.\n")
md.append("- **Separate passes:** the organ's chords and its last-chorus countermelody are two parts; record the countermelody as its own pass.\n")
md.append("### Score and parts\n")
md.append("- Lead sheet (voice, lyrics, chord symbols): *Stay Tuned - lead sheet.pdf*\n- Parts (lead guitar, rhythm guitar, synth pulse, organ, organ 2, backing vocals, bass, drums): *Stay Tuned - parts.pdf*\n- Number chart: *Stay Tuned - Nashville chart.pdf*\n- Demo: *Stay Tuned - demo.mp3*, with General MIDI and GarageBand MIDI files\n")
open("/home/claude/p38/songbook.md", "w").write("\n".join(md))
print("songbook.md written:", len(md), "lines")
