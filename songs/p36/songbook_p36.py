"""Write songbook.md for 'Dance Anyway' from the song record: every bar number, pitch and chord read from the record."""
import pickle, collections
REC = pickle.load(open("/home/claude/p36/song_record.pkl", "rb"))
BAR = 48; lead = REC["lead"]; BARS = REC["bars"]
NM = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
CHN = {"Eb": "E♭", "Bb": "B♭", "Cm": "Cm", "Ab": "A♭", "Db": "D♭", "Fm": "Fm"}
def pos(t):
    b, r = divmod(t, BAR); beat = r // 12 + 1; sub = r % 12
    return f"bar {b + 1}, beat {beat}" + ("" if sub == 0 else " (just after)" if sub == 3 else " (the 'and')" if sub == 6 else " (late)")
def line_rows(sec):
    out = []
    for i, (role, text) in enumerate([x for s, x in [(s, x) for s, xs in [(s, REC["text"][s]) for s in REC["text"]] for x in []]]): pass
    import lyric as L
    words = dict(L.SECTIONS)[sec]
    for i, (role, text) in enumerate(words):
        ns = [n for n in lead if n["sec"] == sec and n["line"] == i]
        b0, b1 = ns[0]["on"] // BAR, ns[-1]["on"] // BAR
        chords = " – ".join(CHN[BARS[b]["chord"]] for b in range(max(b0, ns[0]["on"] // BAR), b1 + 1))
        hi = max(ns, key=lambda n: n["midi"])
        word = REC_WORDS[sec][i][hi["syl"]].replace("facedown", "face-down")
        out.append(dict(i=i, text=text, start=ns[0]["on"], bar=b0 + 1, chords=chords, first=nm(ns[0]["midi"]), last=nm(ns[-1]["midi"]), hi=nm(hi["midi"]), hi_word=word, lo=nm(min(n["midi"] for n in ns))))
    return out
import sys; sys.path.insert(0, "/home/claude/p36")
import lyric as L
def words_of(sec):
    out = []
    for toks in REC["text"][sec]:
        ws, cur = [], ""; owner = []
        for t, hy in toks:
            cur += t; owner.append(len(ws))
            if not hy: ws.append(cur.strip(",.;:—")); cur = ""
        out.append([ws[o] for o in owner])
    return out
REC_WORDS = {s: words_of(s) for s in REC["text"]}
plan = {s: (nb, b0) for s, nb, b0, _ in REC["plan"]}
def sec_range(s):
    ns = [n["midi"] for n in lead if n["sec"] == s]; return nm(min(ns)), nm(max(ns))
secs = REC["seconds"]
def t_at(bar): s = bar * 4 * 60 / 118; return f"{int(s // 60)}:{int(round(s % 60)):02d}"
md = []
md.append("---\ntitle: \"Dance Anyway\"\nsubtitle: \"Songbook and production notes\"\nauthor: \"Words and music: Jason Bryant\"\n---\n")
md.append("## At a glance\n")
md.append("*Dance Anyway* is a four-on-the-floor disco-pop song for one female voice. It is two in the morning; the dishes are done, the microwave clock has blinked 12:00 since a power cut in July, a red-stamped bill sits on the counter, and the radio finds an old song. She dances anyway. Nothing gets fixed. The joy is chosen, not caused.\n")
md.append("| | |\n|---|---|\n| Key | E♭ major throughout |\n| Tempo | ♩ = 118, straight sixteenths |\n| Length | 88 bars, 2:59 |\n| Voice | female, B♭3 to D5 (the D5 once, in the last chorus) |\n| Chords | one a bar, all root position: E♭, Fm, Cm, A♭, B♭, D♭ |\n")
md.append("**Form**\n")
md.append("| Section | Bars | Starts at | Chords |\n|---|---|---|---|")
for s, nb, b0, _ in REC["plan"]:
    ch = " ".join(CHN[BARS[b]["chord"]] for b in range(b0, b0 + nb))
    md.append(f"| {s} | {b0 + 1}–{b0 + nb} | {t_at(b0)} | {ch} |")
md.append("")
md.append("**How to play it.** Keep the kick on every beat from bar 3 to bar 87 except in the bridge, where the floor drops away and comes back. The verses are light (eighth hats, keys on the off-beats, bass in quarters); each pre-chorus adds the pad and the guitar and ends in a one-bar snare build; each chorus opens with a crash and runs sixteenth hats, octave bass in eighths and keys stabbing every 'and'. The song's one new chord, D♭, arrives in bar 15 of each chorus, just before it lands home.\n")
md.append("## Section by section\n")
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]; lo, hi = sec_range(s)
    md.append(f"### {s} (bars {b0 + 1}–{b0 + nb})\n")
    note = {"Verse 1": "Conversational and low: the verse sits between " + lo + " and " + hi + ". Lines 1 and 3 share a tune; so do lines 2 and 4.",
            "Pre 1": "The voice climbs into the chorus's register (" + lo + "–" + hi + "); the last bar is the snare build.",
            "Chorus 1": "Two halves of eight bars, the second singing the first again; the last line comes home to E♭. The hook, 'So I dance anyway', jumps a sixth up on 'dance'.",
            "Verse 2": "Verse 1's tune with the new words.", "Pre 2": "Pre-chorus 1's tune with the new words.", "Chorus 2": "Chorus 1 exactly.",
            "Bridge": "The floor drops. Lines 1 and 3 share a tune. Low (" + lo + "–" + hi + ") and close to speech; the last two bars build back.",
            "Last Chorus": "Chorus 1's tune with the new words, two changes: the one D5 in the song, on 'for-EV-er' (bar 82), and the last line sings the hook a third time and comes home to E♭."}[s]
    md.append(note + "\n")
    md.append("| Bar | Line | Chords | First – last note | Top note |\n|---|---|---|---|---|")
    for r in line_rows(s):
        md.append(f"| {r['bar']} | {r['text']} | {r['chords']} | {r['first']} – {r['last']} | {r['hi']} ({r['hi_word']}) |")
    md.append("")
# the summit and the hook, from the record
summit = max(lead, key=lambda n: n["midi"])
hook = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
md.append("## For each player\n")
md.append("**Drums.** Four on the floor from bar 3; snare and clap together on 2 and 4. Verses: eighth hats. Choruses: crash on the first bar, sixteenth hats with the open hat on every 'and'. Pre-choruses: the last bar is a sixteenth snare build (bars 16 and 44). Bridge (bars 61–68): kick on 1 and 3 only through bar 66, closed hats in quarters in bars 65–66, then quarters on the kick and a snare build through bars 67–68. Last chorus: a crash every four bars. Bar 88: one hit on 1 with the crash.\n")
md.append("**Bass.** Root on every beat, octave on every 'and' in the choruses and the outro (disco octaves in eighths); root and octave in quarters in the verses; whole notes for bridge bars 61–66. The roots run E♭2–D3. Bar 88: one hit, root and octave.\n")
md.append("**Electric piano.** Close triads around middle C. Verses: stabs on the 'and' of 2 and 4. Pre-choruses and choruses: stabs on every 'and'. Bridge bars 61–66: hold each chord for the bar.\n")
md.append("**Guitar.** Muted sixteenths with the chord on the 'and' of each beat (top three strings, triad around E4). In from pre-chorus 1, out for verse 1, in for verse 2, out for bridge bars 61–66.\n")
md.append("**Pad.** Held triads in every pre-chorus and chorus, the bridge and the outro (out in the verses); in the last chorus voice it an octave higher (around G4).\n")
md.append(f"**Synth.** The hook, an octave over the voice: bars 3–4 (the intro's second half) and bars 86–87 (the outro). It is the voice's own 'So I dance anyway' figure.\n")
last = sorted(lead, key=lambda n: n["on"])[-1]; lw = [n for n in lead if n["sec"] == last["sec"] and n["line"] == last["line"] and n["first"]][-1]
LAND = f"its last word, '{lw['text'].strip('.')}', lands on {pos(lw['on'])}"
md.append(f"**Singer.** Range B♭3–D5; most of the song lives between D4 and C5. The verses are close to speech and full of sixteenths: keep them light and on the grid. Hold every line's last word through to the breath (the band leaves room). The one D5 is on 'for-EV-er' in the last chorus, {pos(summit['on'])}; every other note is C5 or lower, so save it. The last line sings the hook a third time; {LAND}, and holds into the outro.\n")
md.append("**Arrangement.** Intro: keys alone for two bars, then drums, bass and the synth hook. Verse 1 light; verse 2 adds the guitar. Each pre-chorus builds; each chorus opens up. The bridge drops to kick, held bass, held keys and pad, and builds back for the last chorus, which is the fullest section (pad up an octave, a crash every four bars). Outro: the chorus groove with the synth hook, one final hit on E♭.\n")
md.append("## Production notes\n")
md.append("### Lyric sheet\n")
for s in ("Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"):
    nb, b0 = plan[s]
    md.append(f"**{s}** (bar {b0 + 1})  ")
    for r in line_rows(s): md.append(f"{r['bar']}: {r['text']}  ")
    md.append("")
md.append("### Production brief\n")
md.append("**The song.** One woman alone in her kitchen at 2 a.m. dances to an old song on the radio while the bill stays unpaid and the clock stays wrong. It should feel like a small, private act of defiance: warm, bright, a little reckless, never triumphant. The bridge remembers the night in July when the power went out and she didn't move; the last chorus is on that same floor.\n")
md.append("**References.**\n")
md.append("- Robyn, \"Dancing On My Own\" (2010), 117 BPM: the tempo, and a woman dancing alone with the feeling under it.\n")
md.append("- Dua Lipa, \"Don't Start Now\" (2019), 124 BPM: the four-on-the-floor kick, the funk-disco bass and the handclaps locked to the grid.\n")
md.append("- Lizzo, \"About Damn Time\" (2022), 109 BPM: retro disco used for coming out of a dark time; joy as something you decide.\n")
md.append("**Non-negotiables.** The kick on every beat outside the bridge. The bridge must drop and rebuild. The D5 on 'forever' happens once. The last line sings the hook a third time and ends on E♭; the song ends on one hit in bar 88. The voice stays in front of the band (it reads about 5 dB over the band in the demo).\n")
md.append("### Session notes\n")
md.append(f"- **Tempo and click:** ♩ = 118 throughout, no tempo changes; 2:59 for 88 bars. Count in two bars.\n- **Key:** E♭ major; no modulation.\n- **Chords:** one per bar, root position (the form table above lists every bar).\n- **Range:** voice B♭3–D5; bass E♭2–D3 (octaves to D♭3–D4).\n")
md.append("- **Tracking order:** drums and bass to the click, then keys and guitar, then pad and synth, then the lead vocal. The guitar's muted sixteenths and the chord on each 'and' are one part for one player; track it in one pass.\n")
md.append("- **Blend and panning:** kick and bass centre; keys left of centre, guitar right; pad wide; synth slightly right; lead vocal centre and on top (at least 3 dB over the band).\n")
md.append("### Score and parts\n")
md.append("- Lead sheet (voice, lyrics, chord symbols): *Dance Anyway - lead sheet.pdf*\n- Parts (synth, electric piano, guitar, pad, bass, drums): *Dance Anyway - parts.pdf*\n- Number chart: *Dance Anyway - Nashville chart.pdf*\n- Demo: *Dance Anyway - demo.mp3*, with General MIDI and GarageBand MIDI files\n")
open("/home/claude/p36/songbook.md", "w").write("\n".join(md))
print("songbook.md written:", len(md), "lines")
