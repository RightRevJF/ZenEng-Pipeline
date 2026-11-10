"""Write songbook_v3.md for 'Dance Anyway (version 3)' from the version 3 record: every bar number, pitch and chord read from the record."""
import pickle, statistics, sys
sys.path.insert(0, "/home/claude/p36")
import lyric_v2 as L
REC = pickle.load(open("/home/claude/p36/song_record_v3.pkl", "rb"))
BAR = 48; lead = REC["lead"]; BARS = REC["bars"]; NB = REC["nbars"]
NM = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
CHN = {"Eb": "E♭", "Bb": "B♭", "Cm": "Cm", "Ab": "A♭", "Db": "D♭", "Fm": "Fm"}
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
                        hi=nm(hi["midi"]), hi_word=WORDS[sec][i][hi["syl"]].replace("a.m", "a.m.")))
    return out
def rng(s): ps = [n["midi"] for n in lead if n["sec"] == s]; return nm(min(ps)), nm(max(ps)), statistics.median(ps)
def t_at(bar): s = bar * 4 * 60 / 118; return f"{int(s // 60)}:{int(round(s % 60)):02d}"
secs = REC["seconds"]; L_ = f"{int(secs // 60)}:{int(round(secs % 60)):02d}"
summits = [n for n in lead if n["midi"] == max(m["midi"] for m in lead)]
lo_all, hi_all = nm(min(n["midi"] for n in lead)), nm(max(n["midi"] for n in lead))
pre_builds = [plan[s][1] + plan[s][0] for s in ("Pre 1", "Pre 2")]
bnb, bb0 = plan["Bridge"]; drop_to = bb0 + bnb - 2; hats_from = bb0 + bnb - 3; build = (bb0 + bnb - 1, bb0 + bnb)
ob0 = plan["Outro"][1]
db_bar = [b["start"] // BAR + 1 for b in BARS if b["chord"] == "Db" and b["sec"] == "Chorus 1"][0] - plan["Chorus 1"][1]
rf = [s_ for s_ in REC["synth"] if s_["on"] < BAR]
roots = sorted({e["p"][0] for e in REC["bass"]})
vlo, vhi, vmed = rng("Verse 1"); blo, bhi, bmed = rng("Bridge"); clo, chi, cmed = rng("Chorus 1"); plo, phi, _ = rng("Pre 1")
hook = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
last = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 7 and n["first"]][-1]
md = []
md.append("---\ntitle: \"Dance Anyway (version 3)\"\nsubtitle: \"Songbook and production notes\"\nauthor: \"Words and music: Jason Bryant\"\n---\n")
md.append("## At a glance\n")
md.append("*Dance Anyway* is a four-on-the-floor disco-pop song for one female voice. It is two in the morning; the dishes are done, the microwave clock has blinked 12:00 since a power cut in July, a red-stamped bill sits on the counter, and the radio finds an old song. She dances anyway. Nothing gets fixed. The joy is chosen, not caused.\n")
md.append("This is the third version of the music on the same words. The tune was written again from the start: every line takes as many bars as its words need, so the longer lines now get three bars and the song runs " + f"{NB} bars; the voice moves in eighths and quarters (no sixteenths); each line ends on a held note with a breath after it; the bridge sits above the verse; and the synth has a hook of its own.\n")
md.append(f"| | |\n|---|---|\n| Key | E♭ major throughout |\n| Tempo | ♩ = 118 |\n| Length | {NB} bars, {L_} |\n| Voice | female, {lo_all} to {hi_all} (the {hi_all} once in each chorus) |\n| Chords | one a bar, all root position: E♭, Fm, Cm, A♭, B♭, D♭ |\n")
md.append("**Form**\n")
md.append("| Section | Bars | Starts at | Chords |\n|---|---|---|---|")
for s, nb, b0, _ in REC["plan"]:
    md.append(f"| {s} | {b0 + 1}–{b0 + nb} | {t_at(b0)} | " + " ".join(CHN[BARS[b]["chord"]] for b in range(b0, b0 + nb)) + " |")
md.append("")
md.append(f"**How to play it.** Keep the kick on every beat from bar 3 to bar {NB - 1} except in the bridge, where the floor drops away and comes back. The verses are light (eighth hats, keys on the off-beats, bass in quarters); each pre-chorus adds the pad and the guitar and ends in a one-bar snare build; each chorus opens with a crash and runs sixteenth hats, octave bass in eighths and keys stabbing every 'and'. A line with more words takes three bars instead of two: verse lines 2 and 4, chorus lines 4 and 8, bridge line 2. The chorus's D♭ arrives in bar {db_bar} of it, just before it lands home.\n")
md.append("## Section by section\n")
NOTE = {
    "Verse 1": f"Conversational and low, between {vlo} and {vhi}. Lines 1 and 3 share a tune; so do lines 2 and 4. Every line ends on a held note on beat 3 or the next downbeat.",
    "Pre 1": f"Both lines sing the same tune ({plo}–{phi}), touching C5 early in each line's second bar; the last bar is the snare build.",
    "Chorus 1": f"Eighteen bars in two halves; the second half sings the first again. The hook, 'So I dance anyway', is a small step-wise figure (" + " ".join(nm(n["midi"]) for n in hook) + f") with 'dance' on the downbeat. The top of the song, {hi_all}, comes on 'twelve' at the end of line 6, over B♭; the last line sings line 4's tune again and holds B♭4 over the D♭, and the band lands on E♭ in the chorus's last bar.",
    "Verse 2": "Verse 1's tune with the new words.", "Pre 2": "Pre-chorus 1's tune with the new words.", "Chorus 2": "Chorus 1 exactly.",
    "Bridge": f"The floor drops. The voice moves up: the bridge sits between {blo} and {bhi}, two semitones above the verse at the middle, with a shape of its own (it does not open like the verse or the chorus). Each of its four lines has its own tune; the top, C5, comes on 'dripping in' and on 'hear'. The last word, 'all', holds on G4 into the build.",
    "Last Chorus": f"Chorus 1's tune with the new words. The {hi_all} falls on 'July' (end of line 6). The last line has a bar more than the hook: 'I'm still here' takes the first bar, then the hook comes in a bar later than in the chorus and ends on E♭."}
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]
    md.append(f"### {s} (bars {b0 + 1}–{b0 + nb})\n")
    md.append(NOTE[s] + "\n")
    md.append("| Bars | Line | Chords | First – last note | Top note |\n|---|---|---|---|---|")
    for r in line_rows(s): md.append(f"| {r['bars']} | {r['text']} | {r['chords']} | {r['first']} – {r['last']} | {r['hi']} ({r['hi_word']}) |")
    md.append("")
md.append("## For each player\n")
md.append(f"**Drums.** Four on the floor from bar 3; snare and clap together on 2 and 4. Verses: eighth hats. Choruses: crash on the first bar, sixteenth hats with the open hat on every 'and'. Pre-choruses: the last bar is a sixteenth snare build (bars {pre_builds[0]} and {pre_builds[1]}). Bridge (bars {bb0 + 1}–{bb0 + bnb}): kick on 1 and 3 only through bar {drop_to}, closed hats in quarters from bar {hats_from}, then quarters on the kick and a snare build through bars {build[0]}–{build[1]}. Last chorus: a crash every four bars. Bar {NB}: one hit on 1 with the crash.\n")
md.append(f"**Bass.** Root on every beat, octave on every 'and' in the choruses and the outro (disco octaves in eighths); root and octave in quarters in the verses; whole notes for bridge bars {bb0 + 1}–{drop_to}. The roots run {nm(roots[0])}–{nm(max(r for r in roots if r < 51))}. Bar {NB}: one hit, root and octave.\n")
md.append(f"**Electric piano.** Close triads around middle C. Verses: stabs on the 'and' of 2 and 4. Pre-choruses and choruses: stabs on every 'and'. Bridge bars {bb0 + 1}–{drop_to}: hold each chord for the bar.\n")
md.append(f"**Guitar.** Muted sixteenths with the chord on the 'and' of each beat (triad around E4). In from pre-chorus 1, out for verse 1, in for verse 2, out for bridge bars {bb0 + 1}–{drop_to}.\n")
md.append("**Pad.** Held triads in every pre-chorus and chorus, the bridge and the outro (out in the verses); in the last chorus voice it an octave higher (around G4).\n")
md.append(f"**Synth.** A one-bar hook of its own, five notes (" + " ".join(nm(s_["p"][0]) for s_ in rf) + " over E♭): the root on the downbeat, a quick drop to C and a jump up to G, then B♭ and down to E♭, all but the first off the beat. It plays every intro bar (bars 1–4), in the holds after chorus lines 2, 4, 6 and 8 (in the last chorus after line 7 instead of 8, since the last line runs into the outro; moved to each bar's chord, starting a beat after the singer's last word and stopping before she sings again; shorter where the hold is short), and in outro bars " + f"{ob0 + 1}–{ob0 + 3}" + ". It never plays over a sung word, and it is not the vocal hook.\n")
md.append(f"**Singer.** Range {lo_all}–{hi_all}; most of the song lives between D4 and C5. The voice moves in eighths and quarters; keep it light and on the grid. Every line ends on a held note (a half or a dotted quarter) with a breath after it: hold through to the breath. The {hi_all} comes once in each chorus, on the last word of line 6 (" + "; ".join(f"'{WORDS[n['sec']][n['line']][n['syl']]}', {pos(n['on'])}" for n in summits) + "); every other note is C5 or lower. The last line sings the hook a third time; its last word, 'way', lands on " + pos(last["on"]) + " and holds into the outro.\n")
md.append(f"**Arrangement.** Intro: keys and the synth's hook for two bars, then drums and bass. Verse 1 light; verse 2 adds the guitar. Each pre-chorus builds; each chorus opens up. The bridge drops to kick, held bass, held keys and pad, and builds back for the last chorus, which is the fullest section (pad up an octave, a crash every four bars). Outro: the chorus groove with the synth's hook, one final hit on E♭.\n")
md.append("## Production notes\n")
md.append("### Lyric sheet\n")
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]; md.append(f"**{s}** (bar {b0 + 1})  ")
    for r in line_rows(s): md.append(f"{r['bar']}: {r['text']}  ")
    md.append("")
md.append("### Production brief\n")
md.append("**The song.** One woman alone in her kitchen at 2 a.m. dances to an old song on the radio while the bill stays unpaid and the clock stays wrong. It should feel like a small, private act of defiance: warm, bright, a little reckless, never triumphant. The bridge remembers the night in July when the power went out and she didn't move; the last chorus is on that same floor.\n")
md.append("**References.**\n")
md.append("- Robyn, \"Dancing On My Own\" (2010), 117 BPM: the tempo, and a woman dancing alone with the feeling under it.\n")
md.append("- Dua Lipa, \"Don't Start Now\" (2019), 124 BPM: the four-on-the-floor kick, the funk-disco bass and the handclaps locked to the grid.\n")
md.append("- Lizzo, \"About Damn Time\" (2022), 109 BPM: retro disco used for coming out of a dark time; joy as something you decide.\n")
md.append(f"**Non-negotiables.** The kick on every beat outside the bridge. The bridge must drop, sit above the verse, and rebuild. The {hi_all} comes once a chorus, on the last word of line 6, and nowhere else. The synth's hook never plays over a sung word. The last line sings the hook a third time and ends on E♭; the song ends on one hit in bar {NB}. The voice stays in front of the band (it reads about 5 dB over the band in the demo).\n")
md.append("### Session notes\n")
md.append(f"- **Tempo and click:** ♩ = 118 throughout, no tempo changes; {L_} for {NB} bars. Count in two bars.\n- **Key:** E♭ major; no modulation.\n- **Chords:** one per bar, root position (the form table above lists every bar).\n- **Range:** voice {lo_all}–{hi_all}; bass {nm(roots[0])}–{nm(max(r for r in roots if r < 51))} (octaves above).\n")
md.append("- **Tracking order:** drums and bass to the click, then keys and guitar, then pad and synth, then the lead vocal. The guitar's muted sixteenths and the chord on each 'and' are one part for one player; track it in one pass.\n")
md.append("- **Blend and panning:** kick and bass centre; keys left of centre, guitar right; pad wide; synth slightly right; lead vocal centre and on top (at least 3 dB over the band).\n")
md.append("### Score and parts\n")
md.append("- Lead sheet (voice, lyrics, chord symbols): *Dance Anyway (version 3) - lead sheet.pdf*\n- Parts (synth, electric piano, guitar, pad, bass, drums): *Dance Anyway (version 3) - parts.pdf*\n- Number chart: *Dance Anyway (version 3) - Nashville chart.pdf*\n- Demo: *Dance Anyway (version 3) - demo.mp3*, with General MIDI and GarageBand MIDI files\n")
open("/home/claude/p36/songbook_v3.md", "w").write("\n".join(md))
print("songbook_v3.md written:", len(md), "lines")
