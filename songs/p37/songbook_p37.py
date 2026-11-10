"""Write songbook.md for 'Windows Down' from the song record: every bar number, pitch and chord read from the record."""
import pickle, statistics, sys
sys.path.insert(0, "/home/claude/p37")
import lyric_p37 as L
REC = pickle.load(open("/home/claude/p37/song_record.pkl", "rb"))
BAR = 48; lead = REC["lead"]; BARS = REC["bars"]; NB = REC["nbars"]
NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
CHN = {"A": "A", "E": "E", "F#m": "F♯m", "D": "D", "Bm": "Bm", "C#m": "C♯m"}
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
def line_rows(sec, only=None):
    out = []
    for i, (role, text) in enumerate(dict(L.SECTIONS)[sec]):
        if only is not None and i not in only: continue
        ns = [n for n in lead if n["sec"] == sec and n["line"] == i]
        b0, b1 = ns[0]["on"] // BAR, ns[-1]["on"] // BAR
        hi = max(ns, key=lambda n: (n["midi"], -n["on"]))
        out.append(dict(i=i, text=text, bar=b0 + 1, bars=f"{b0 + 1}–{b1 + 1}" if b1 > b0 else f"{b0 + 1}",
                        chords=" – ".join(CHN[BARS[b]["chord"]] for b in range(b0, b1 + 1)), first=nm(ns[0]["midi"]), last=nm(ns[-1]["midi"]),
                        hi=nm(hi["midi"]), hi_word=WORDS[sec][i][hi["syl"]].replace("twentysix", "twenty-six")))
    return out
def rng(s): ps = [n["midi"] for n in lead if n["sec"] == s]; return nm(min(ps)), nm(max(ps))
def t_at(bar): s = bar * 4 * 60 / 122; return f"{int(s // 60)}:{int(round(s % 60)):02d}"
secs = REC["seconds"]; LEN = f"{int(secs // 60)}:{int(round(secs % 60)):02d}"
summits = [n for n in lead if n["midi"] == max(m["midi"] for m in lead)]
lo_all, hi_all = nm(min(n["midi"] for n in lead)), nm(max(n["midi"] for n in lead))
second = max(n["midi"] for n in lead if n["midi"] != max(m["midi"] for m in lead))
pre_fills = [plan[s][1] + plan[s][0] for s in ("Pre 1", "Pre 2")]
bnb, bb0 = plan["Bridge"]; snb, sb0 = plan["Solo"]; ob0 = plan["Outro"][1]
hook = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
riff = [s_ for s_ in REC["lgtr"] if s_["on"] < BAR]
roots = sorted({e["p"][0] for e in REC["bass"] if len(e["p"]) == 1 and e["on"] % 12 == 0})
vlo, vhi = rng("Verse 1"); plo, phi = rng("Pre 1"); clo, chi = rng("Chorus 1"); blo, bhi = rng("Bridge")
pl = REC["plans"]
def same(letters, a, b): return letters[a] == letters[b]
md = []
md.append("---\ntitle: \"Windows Down\"\nsubtitle: \"Songbook and production notes\"\nauthor: \"Words and music: Jason Bryant\"\n---\n")
md.append("## At a glance\n")
md.append("*Windows Down* is a heartland rock song for a male baritone. A man walks out of his plant on its last day after twenty-six years: the time clock that always ran four minutes fast, her picture peeled off his locker door, the gate's squeal. He calls his wife from the lot with oil on his thumb, and she doesn't ask what comes next. He drives home with the windows down to air the cutting oil out of his clothes, in November, with the heater on. The job ended; he didn't.\n")
md.append(f"| | |\n|---|---|\n| Key | A major throughout |\n| Tempo | ♩ = 122, straight eighths |\n| Length | {NB} bars, {LEN} |\n| Voice | male baritone, {lo_all} to {hi_all} (the {hi_all} once in each chorus pass, five times) |\n| Chords | one a bar, root position: A, Bm, D, E, F♯m |\n")
md.append("**Form**\n")
md.append("| Section | Bars | Starts at | Chords |\n|---|---|---|---|")
for s, nb, b0, _ in REC["plan"]:
    md.append(f"| {s} | {b0 + 1}–{b0 + nb} | {t_at(b0)} | " + " ".join(CHN[BARS[b]["chord"]] for b in range(b0, b0 + nb)) + " |")
md.append("")
md.append(f"**How to play it.** Straight eighths everywhere: the bass drives eighths on the root, the rhythm guitar plays power chords in eighths (palm-muted in the verses, open from the pre-chorus on), the drums keep kick on 1 and 3 with the 'and' of 3 and the snare on 2 and 4. The intro is the lead guitar's hook alone for four bars, then the band. Every section is a multiple of four bars and every sung line two bars. Each chorus is the 8-bar chorus sung twice; its fourth line opens on D, where the singer hits his top note, and lands on A. The bridge drops to half-time and builds; the solo takes the chorus changes for 16 bars; the last chorus is the fullest; the outro rides the chorus changes with the hook and ends on one hit in bar {NB}.\n")
md.append("## Section by section\n")
NOTE = {
    "Verse 1": f"Low and close to speech, between {vlo} and {vhi}. " + ("Lines 1 and 2 open on the same tune. " if same(pl["Verse"], 0, 1) else "") + ("Lines 1 and 3 share a tune. " if same(pl["Verse"], 0, 2) else "") + "Each line ends on a held note with a breath after it.",
    "Pre 1": f"The voice climbs a little ({plo}–{phi}) and the band opens up; the last bar is a tom fill into the chorus.",
    "Chorus 1": f"Sixteen bars: the 8-bar chorus, then the same again. 'Windows down till the oil smell's gone' sits around C♯4 and B3 (" + " ".join(nm(n["midi"]) for n in hook) + ")" + ("; 'Number Four went quiet' sings line 1's tune again" if same(pl["ChorusHead"], 0, 2) else "") + f". Line 4 jumps to the top of the song, {hi_all}, on 'HOL-lering', over D, and comes down to land on A3, over A.",
    "Verse 2": "Verse 1's tune with the new words.", "Pre 2": "Pre-chorus 1's tune with the new words.", "Chorus 2": "Chorus 1 exactly.",
    "Bridge": f"Half-time. The voice sits higher than in the verse ({blo}–{bhi}), with a shape of its own." + (" Line 3 brings line 1's tune back." if same(pl["Bridge"], 0, 2) else "") + " 'Whole damn way' rides into the snare build.",
    "Last Chorus": f"The first eight bars as in chorus 1, {hi_all} included. The second eight change their words: 'but leave a little on', 'Number Four can keep the quiet now', and the last line holds its first 'home' for a half note before the second 'I'm almost home' lands on A3."}
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]
    md.append(f"### {s} (bars {b0 + 1}–{b0 + nb})\n")
    md.append(NOTE[s] + "\n")
    md.append("| Bars | Line | Chords | First – last note | Top note |\n|---|---|---|---|---|")
    for r in line_rows(s): md.append(f"| {r['bars']} | {r['text']} | {r['chords']} | {r['first']} – {r['last']} | {r['hi']} ({r['hi_word']}) |")
    md.append("")
md.append("## For each player\n")
md.append(f"**Drums.** Bars 1–4 tacet; a crash and in at bar 5. Kick on 1, 3 and the 'and' of 3; snare on 2 and 4; eighth hats in the verses and pre-choruses, eighths on the ride in the choruses. A tom fill in the last two beats of each pre-chorus (bars {pre_fills[0]} and {pre_fills[1]}). Bridge (bars {bb0 + 1}–{bb0 + bnb}): half-time, kick on 1 and snare on 3, through bar {bb0 + bnb - 2}, then a snare build over bars {bb0 + bnb - 1}–{bb0 + bnb}. Solo (bars {sb0 + 1}–{sb0 + snb}): hats for eight bars, the ride from bar {sb0 + 9}. Last chorus: a crash every four bars and the open hat on every 'and'. Bar {NB}: one hit with the crash.\n")
md.append(f"**Bass.** From bar 5, driving eighths on the root; in the choruses, the solo and the outro, the octave on the 'and' of 4. Bridge bars {bb0 + 1}–{bb0 + bnb - 2}: half notes. The roots run {nm(roots[0])}–{nm(max(roots))}. Bar {NB}: one hit, root and octave.\n")
md.append(f"**Rhythm guitar.** Power chords (root, fifth, octave) in eighths from bar 5: palm-muted in the intro and verses, open from each pre-chorus through the chorus, the solo and the outro. Held chords for bridge bars {bb0 + 1}–{bb0 + bnb - 2}.\n")
md.append(f"**Organ.** Held triads in the pre-choruses, the choruses and the bridge; in from bar {sb0 + 9} for the second half of the solo; the outro. Voiced higher in the last chorus.\n")
md.append(f"**Lead guitar.** A one-bar hook of its own, four notes ({' '.join(nm(s_['p'][0]) for s_ in riff)} over A): the 'and' of 1, beat 2, its 'and', and the 'and' of 3, a jump up a fifth and back down. It plays alone for the first four bars, then over the band to bar 8; in the holds after chorus lines where two beats or more are free (it moves with each bar's chord and never plays over a sung word); and in outro bars {ob0 + 1}–{ob0 + 7}. The solo (bars {sb0 + 1}–{sb0 + snb}) states the hook, answers it a third higher, sings a line over the chorus changes that climbs to the middle and comes back, and ends with the hook landing on A.\n")
md.append(f"**Singer.** Range {lo_all}–{hi_all}; most of the song lives between E3 and D4, close and conversational in the verses. Every line ends on a held note (a quarter, a dotted quarter or a half) with a breath after it. The {hi_all} comes five times, always on 'HOL-lering' over D: " + "; ".join(f"{pos(n['on'])}" for n in summits) + f". Every other note is {nm(second)} or lower. In the last line, hold the first 'home' (a half note) before the second 'I'm almost home'.\n")
md.append("**Arrangement.** The guitar's hook alone, then the band. Verse 1 tight and muted; each pre-chorus opens up and fills into the chorus; each chorus rides. The bridge drops to half-time and builds to the solo; the solo builds again to the last chorus, the fullest section. Outro: the chorus changes with the hook, one final hit on A.\n")
md.append("## Production notes\n")
md.append("### Lyric sheet\n")
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]; md.append(f"**{s}** (bar {b0 + 1})  ")
    for r in line_rows(s): md.append(f"{r['bar']}: {r['text']}  ")
    md.append("")
md.append("### Production brief\n")
md.append("**The song.** A man's last shift at a plant that's closing, and the drive home to his wife. The verses are the small, exact things of the last day; the chorus is the drive, loud and a little reckless, defiant without being angry. It is not a protest song and it names no one. The bridge is the marriage: they had his hands for twenty-six years, she had him the whole way. The last chorus lets him keep a little of the smell.\n")
md.append("**References.**\n")
REFS = open("/home/claude/p37/refs.md").read().strip()
md.append(REFS + "\n")
md.append(f"**Non-negotiables.** Straight eighths on the bass and the rhythm guitar. The guitar's hook opens the song alone. The {hi_all} on 'HOL-lering' over D, five times, and nowhere else. The bridge drops to half-time and builds. The hook never plays over a sung word. The last line holds the first 'home' and ends on A; one hit in bar {NB}. The voice in front (it reads about 6 dB over the band in the demo).\n")
md.append("### Session notes\n")
md.append(f"- **Tempo and click:** ♩ = 122 throughout; {LEN} for {NB} bars. Count in one bar; the guitar starts alone.\n- **Key:** A major; no modulation.\n- **Chords:** one per bar, root position (the form table lists every bar).\n- **Range:** voice {lo_all}–{hi_all}; bass {nm(roots[0])}–{nm(max(roots))} with octaves above.\n")
md.append("- **Tracking order:** drums and bass to the click, then the rhythm guitar (double it, left and right, if the room allows), organ, the lead guitar's hook and solo, then the lead vocal.\n")
md.append("- **Blend and panning:** kick, snare and bass centre; rhythm guitars wide; organ right of centre; lead guitar slightly right; lead vocal centre and on top (at least 3 dB over the band).\n")
md.append("### Score and parts\n")
md.append("- Lead sheet (voice, lyrics, chord symbols): *Windows Down - lead sheet.pdf*\n- Parts (lead guitar, rhythm guitar, organ, bass, drums): *Windows Down - parts.pdf*\n- Number chart: *Windows Down - Nashville chart.pdf*\n- Demo: *Windows Down - demo.mp3*, with General MIDI and GarageBand MIDI files\n")
open("/home/claude/p37/songbook.md", "w").write("\n".join(md))
print("songbook.md written:", len(md), "lines")
