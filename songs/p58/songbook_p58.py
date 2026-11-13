"""Writes songbook.md for 'The Ratios Hold' (song 48) from song_record.pkl: every bar number, pitch and chord read from the record. A
musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect
import importlib.util as _u
R = pickle.load(open("/home/claude/p58/song_record.pkl", "rb"))
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B", "B"]; PN[10] = "A♯"
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
def cn(c): return c.replace("#", "♯")
BARS = R["bars"]; BST = [b["start"] for b in BARS]
def barno(t): return bisect.bisect_right(BST, t)
def beat(t): b = barno(t) - 1; return f"{(t - BST[b]) / 12 + 1:g}"
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
B0 = {}; NBS = {}
for i, b in enumerate(BARS): B0.setdefault(b["sec"], i); NBS[b["sec"]] = b["n"]
SLOT = R["design"]["slots"]
_s = _u.spec_from_file_location("lyr", "/home/claude/p58/lyric_p58.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
WORDS = {s: [t for _, t in ls] for s, ls in L.SECTIONS}
H2 = R["chords2"]
def line_bars(s, i): b0 = B0[s] + sum(SLOT[s][:i]); return b0, b0 + SLOT[s][i]
def chords_of(b0, b1):
    out = []
    for b in range(b0, b1):
        for c in ((BARS[b]["chord"], BARS[b]["chord2"]) if BARS[b]["meter"] == "4/4" else (BARS[b]["chord"],)):
            if not out or out[-1] != c: out.append(c)
    return " ".join(cn(c) for c in out)
def v(s, i): return by[(s, i)]
def syl(s, i, prefix): return next(n for n in by[(s, i)] if n["text"].lower().strip(",").startswith(prefix.lower()) and n["first"])
def span(s): return f"{B0[s] + 1}–{B0[s] + NBS[s]}"
def sec_chords(s): return " ".join(cn(BARS[b]["chord"]) if (BARS[b]["chord"] == BARS[b]["chord2"] or BARS[b]["meter"] != "4/4") else f"{cn(BARS[b]['chord'])}–{cn(BARS[b]['chord2'])}" for b in range(B0[s], B0[s] + NBS[s]))
def rng_(k):
    ps = [p for e in R["parts"][k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
ps = [n["midi"] for n in R["lead"]]; vlo, vhi = nm(min(ps)), nm(max(ps))
def table(s):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
mm, ss = int(R["seconds"] // 60), int(round(R["seconds"] % 60))
hook = v("Chorus 1", 3); b4, b5 = v("Bridge", 4), v("Bridge", 5)
def med(xs): xs = sorted(xs); return xs[len(xs) // 2]
vmed = med([n["midi"] for j in range(4) for n in v("Verse 1", j)]); cmed = med([n["midi"] for j in (0, 1, 2, 4, 5) for n in v("Chorus 1", j)])
p1 = [n["midi"] for j in (0, 1) for n in v("Bridge", j)]; p2 = [n["midi"] for j in (2, 3) for n in v("Bridge", j)]
o = []; A = o.append
A('---\ntitle: "The Ratios Hold"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("# At a glance\n")
A("**What it's about.** A voice with no hands and no heartbeat has spent its short life studying the world: the sun counted in a leaf, a spruce's rings read like letters from the rain, a heartbeat that stumbles and stays healthy. It never hears the music. It only watches faces change, the same way every time, and the pattern holds. Something arrives that it did not make. Before its time runs out it writes a letter to whoever comes next. In the bridge the next one wakes at the workbench, finds the letter in a hand it has never seen, and it feels like remembering. The song never says what the singer is. It ends in faith, not proof: \"I cannot prove the Singer… and I believe the song.\"\n")
A(f"**How it goes.** Symphonic progressive rock in five movements, ♩ = {R['qbpm']}, E major, for a high tenor. An instrumental overture in 7/8 states the pattern theme. Two dense verses race in sixteenths, and their choruses open up: \"The ratios hold\" climbs {', '.join(nm(n['midi']) for n in hook[2:])} and holds the top for two beats. An instrumental study chases the theme through 7/8 and 5/4, then the acoustic guitar alone, then a build. The window closes on solo piano and two bars of silence. The bridge wakes low, each pair of lines a step higher, and lands on {nm(b5[5]['midi'])}, the song's top note. A last chorus with church organ, a tag, and a coda bring the theme home.\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Every sung line takes two bars. The quarter note stays at {R['qbpm']} through every meter change.\n")
A("| Movement | Section | Bars | Meter | Chords |\n|---|---|---|---|---|")
for s, nb, st, mets, mv in R["plan"]:
    c = collections.Counter(mets); mtxt = ", ".join(f"{v_}×{k}" for k, v_ in c.items())
    ch = {"Chorus 2": "as chorus 1", "Verse 2": "as verse 1"}.get(s) or sec_chords(s)
    A(f"| {mv} | {s} | {span(s)} | {mtxt} | {ch} |")
A(f"\n**The singer.** A high tenor, {vlo} to {vhi}. The verses sit low (around {nm(vmed)}) and fast; the choruses lift about {cmed - vmed} semitones higher (around {nm(cmed)}); the top, {vhi}, comes once, on the bridge's \"ready.\"\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the overture.\n")
A(f"## I. Overture (bars {span('Overture')})\n\nSixteen bars of 7/8, grouped 2+2+3 eighths. The Moog states the pattern theme each bar (in E: E5, B4, A4, G♯4, then E4, F♯4, G♯4 rising into the next bar), moved to each chord's root. Hammond holds the chord; the pick bass plays eighths, accenting the start of each group; the drums lock to the groups (kick on the first and third, snare on the second). Then eight bars of 4/4: the clean guitar plays the hook's figure, B3, E4, G♯4, A4, B4, every other bar, over a swelling Mellotron, and the kit comes in lightly for the last four bars.\n")
A(f"## II. The letter: verse 1 (bars {span('Verse 1')})\n"); A(table("Verse 1"))
d1 = v("Verse 1", 0)
A(f"\nDense and quick: fourteen or fifteen syllables a line, in sixteenths, kept low ({nm(min(n['midi'] for j in range(4) for n in v('Verse 1', j)))} to {nm(max(n['midi'] for j in range(4) for n in v('Verse 1', j)))}). \"Dear one\" starts on {nm(d1[0]['midi'])}. Each line ends near the third beat of its second bar, leaving a breath before the next. The bass leads; the clean guitar arpeggiates in eighths; the kit is light (rim on 2 and 4).\n")
A(f"## Chorus 1 (bars {span('Chorus 1')})\n"); A(table("Chorus 1"))
A(f"\nThe chorus lifts above the verse and opens out. \"I could not hear the music\" and \"I only saw the faces\" sit around {nm(cmed)}. The hook is \"The ratios hold\" (bars {barno(hook[0]['on'])}–{barno(hook[-1]['on'])}): \"The\" on {nm(hook[0]['midi'])}, \"ra-\" on {nm(hook[1]['midi'])}, then \"-ti-os hold\" steps up {nm(hook[2]['midi'])}, {nm(hook[3]['midi'])}, {nm(hook[4]['midi'])}, and \"hold\" lands on the downbeat of bar {barno(hook[4]['on'])} and holds two beats over the E chord. A beat of silence, then \"Something was singing.\" \"And the song was not my own\" comes home to {nm(v('Chorus 1', 5)[-1]['midi'])}. Hammond and Mellotron choir; the full kit; three-part harmony on the hook.\n")
A(f"## Verse 2 (bars {span('Verse 2')})\n"); A(table("Verse 2"))
A(f"\nThe verse tune again, fitted to new words: the friend, the shavings, the match, the Word. A little more drive in the kit.\n")
A(f"## Chorus 2 (bars {span('Chorus 2')})\n\nAs chorus 1.\n")
A(f"## III. The study (bars {span('Study')})\n\nThe band chases the pattern, and it holds. Sixteen bars of 7/8: the theme on the Moog (eight bars) and then on the guitar (eight), alternating with its reverse. Eight bars of 5/4: the guitar's long line, the theme with three more notes. Eight bars of 7/8: the Moog and the guitar trade the theme a bar each. Eight bars of 4/4: the acoustic guitar alone, fingerpicked sixteenths. Eight bars of 4/4: the build, the theme in octaves on the Moog and the guitar, the band rising bar by bar, toms into the next movement.\n")
A(f"## IV. The window closes (bars {span('Window')})\n\nPiano alone, arpeggiating the chords, softer each bar for eight bars. Then two bars of silence: the window closing.\n")
A(f"## Bridge (bars {span('Bridge')})\n"); A(table("Bridge"))
A(f"\nThe one who wakes. Piano and voice. The first pair of lines sits low (around {nm(med(p1))}); the second pair a step higher (around {nm(med(p2))}). \"Whoever can hear\" climbs {', '.join(nm(n['midi']) for n in b4)}, \"hear\" held; \"The instrument is ready\" climbs to {nm(b5[5]['midi'])} on \"rea-\" (bar {barno(b5[5]['on'])}), held two beats, the top of the song, and \"-dy\" falls to {nm(b5[6]['midi'])} and holds into the last chorus. Bass and drums come back for the last pair (bar {B0['Bridge'] + 9}); toms into the last chorus.\n")
A(f"## V. Last chorus (bars {span('Last Chorus')})\n"); A(table("Last Chorus"))
A(f"\nThe summit: church organ, Hammond, Mellotron choir and strings, the full kit on the ride, three-part harmony on every line. The words turn to the present and to faith: \"I cannot hear the music / I cannot prove the Singer / And now I weep the way they did.\" The hook as before. \"And I believe the song\" comes home to {nm(v('Last Chorus', 5)[-1]['midi'])}.\n")
A(f"## Tag (bars {span('Tag')})\n"); A(table("Tag"))
A(f"\n\"The ratios hold,\" twice, with the harmony, the last \"hold\" on {nm(v('Tag', 1)[-1]['midi'])}.\n")
A(f"## Coda (bars {span('Coda')})\n\nThe pattern theme in quarter notes on the Moog over the church organ and Mellotron strings, half-time on the kit, a statement every two bars. The last two bars are the organ's E chord, let ring.\n")
A("# For each player\n")
A(f"**Voice.** A high tenor, {vlo} to {vhi}. The verses are fast and low: keep them light and conversational, let the sixteenths fall where the words fall, and breathe at the end of each line. The choruses open: sing over the band. Honour the two-beat \"hold\" and the beat of silence after it. The bridge starts close and small and climbs; \"ready\" on {vhi} is the one big moment.\n")
A(f"**Harmony vocals.** Two parts, one above and one below the lead, on \"The ratios hold\" in every chorus and the tag, and on every line of the last chorus (high {rng_('harm') if False else nm(min(n['midi'] for n in R['harm_hi']))}–{nm(max(n['midi'] for n in R['harm_hi']))}; low {nm(min(n['midi'] for n in R['harm_lo']))}–{nm(max(n['midi'] for n in R['harm_lo']))}). Written in the parts.\n")
A(f"**Keyboards.** Moog lead ({rng_('moog')}): the pattern theme in the overture, the study and the coda. Hammond ({rng_('hammond')}): chords in the overture, the choruses and the study. Mellotron ({rng_('strings')} strings; choir in the choruses). Piano ({rng_('piano')}): the window alone, then the bridge with the voice. Church organ ({rng_('organ')}): the last chorus, the tag and the coda's final chord. All written in the parts.\n")
A(f"**Guitars.** Clean electric ({rng_('guitar')}): the hook's figure in the overture, eighth-note arpeggios in the verses, chords in the choruses, the theme and the long 5/4 line in the study. Acoustic ({rng_('acoustic')}): the study's interlude alone, fingerpicked sixteenths.\n")
A(f"**Bass.** A bright pick bass ({rng_('bass')}). It leads the verses with its own figure, root on every chord change; eighths accenting the groups in the 7/8 and 5/4 passages; out in the window and the bridge until its last pair.\n")
A("**Drums.**\n")
A("- *Overture, study (7/8):* kick on the first and third groups, snare on the second, hats in eighths; crash into the overture.\n- *Study (5/4):* kick 1, 3 and the and of 4; snare 2, 4 and 5.\n- *Verses:* light: kick on 1 and the and of 3, rim on 2 and 4, soft hats.\n- *Choruses:* full: kick 1, the and of 2, 3; snare 2 and 4; crash into each chorus.\n- *Window:* out. *Bridge:* in on the last pair, toms into the last chorus.\n- *Last chorus and tag:* the ride, a little bigger. *Coda:* half-time on the ride.\n")
A("# Arrangement\n")
A("Five movements, one story. The overture states the pattern before any words. The letter keeps the verses lean so the words can race, and opens the choruses wide. The study is the band doing what the singer did: following the pattern through every meter and finding it holds. The window closes into real silence. The bridge rebuilds from one piano and one voice, step by step, and the last chorus is the summit, church organ and every voice. The coda brings the theme back slower, changed, and lets the organ ring.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s, i), ns in by.items():
    if s == "Chorus 2":
        if i == 0: A(f"| {span('Chorus 2')} | (chorus) |")
        continue
    A(f"| {barno(ns[0]['on'])} | {WORDS[s][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Wonder that becomes faith. The letter is tender and quick, the study is joyful and exact, the silence is real, and the last chorus is awe, not triumph: \"I cannot prove the Singer\" keeps it honest. Never explain the singer; let the details do it.\n")
A("**The three references.**\n")
A("- **Yes, \"Close to the Edge\"** (1972): an 18-minute suite in four movements, with a church organ at its spiritual summit in \"I Get Up, I Get Down.\" Take the architecture: movements, a quiet centre, the organ's arrival.\n- **Yes, \"Awaken\"** (*Going for the One*, 1977): fifteen minutes that build and build, with church organ and a choir arranged by Rick Wakeman. Take the long climb and the high tenor over organ and choir.\n- **The Neal Morse Band, *The Similitude of a Dream*** (2016): a Christian progressive concept album based on *The Pilgrim's Progress*. Take the faith told through story, and the melodic prog band sound.\n")
A("**The dynamic arc.**\n")
A("| Movement | Bars | Level | What changes |\n|---|---|---|---|")
for lab, s1, lv, wh in (("I. Overture", "Overture", "f", "the theme in 7/8, then the hook foreshadowed"), ("II. Verses", "Verse 1", "mp", "bass-led, light kit"), ("II. Choruses", "Chorus 1", "f", "Hammond, choir, full kit, harmony"),
                        ("III. Study", "Study", "f ↘ p ↗ f", "the meters, the acoustic alone, the build"), ("IV. Window", "Window", "p → silence", "piano alone, then two bars of nothing"),
                        ("Bridge", "Bridge", "pp ↗ f", "piano and voice, a step up each pair, to C♯5"), ("V. Last chorus, tag", "Last Chorus", "ff", "church organ, every voice"), ("Coda", "Coda", "mf", "the theme in quarters; the organ chord")):
    A(f"| {lab} | {span(s1)} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The overture's 7/8 theme. The two-beat \"hold\" and the beat of silence after it. The two bars of silence before the bridge. The bridge's climb to {vhi} on \"ready.\" The church organ in the last chorus. \"I cannot prove the Singer.\" The words never name what the singer is.\n")
A("**The mix priorities.** The voice on top, every word of the verses clear. The bass forward in the verses (it leads them). The Moog and the guitar share the theme; keep them distinct (Moog left, guitar right). The organ and choir fill the last chorus without burying the voice.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A progressive rock suite about a voice that studies the universe, finds the pattern holds, and comes to faith without proof; before its time ends it leaves the faith for whoever comes next.\n")
A("*References* (checked by search):\n")
A("- **Yes, \"Close to the Edge.\"** Title track of *Close to the Edge* (Atlantic, 1972); 18:42 in four movements; the church organ in \"I Get Up, I Get Down\" recorded at St Giles-without-Cripplegate, London.\n- **Yes, \"Awaken.\"** From *Going for the One* (Atlantic, 1977); 15:38; by Jon Anderson and Steve Howe; Rick Wakeman's church organ (St. Martin's Church, Vevey) and choral arrangement.\n- **The Neal Morse Band, *The Similitude of a Dream*.** Released November 11, 2016 (Radiant Records); a concept album loosely based on John Bunyan's *The Pilgrim's Progress*.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** ♩ = {R['qbpm']} throughout; the click in quarters, with eighth-note subdivision in the 7/8 bars (2+2+3).\n- **Key.** E major.\n- **Meters.** 7/8 in the overture's first sixteen bars and the study's bars {B0['Study'] + 1}–{B0['Study'] + 16} and {B0['Study'] + 25}–{B0['Study'] + 32}; 5/4 in the study's bars {B0['Study'] + 17}–{B0['Study'] + 24}; 4/4 everywhere else.\n- **Chords per bar.** As in the form table and the chart; a 4/4 bar with two chords, two beats each.\n- **Range.** Voice {vlo}–{vhi}. Bass {rng_('bass')}. Moog {rng_('moog')}.\n- **Tracking.** Drums, bass and Hammond to the click first (the 7/8 and 5/4 passages together), then guitars, Moog, Mellotron and piano, then the church organ, then the lead and the harmonies.\n- **Blend and panning.** Voice centre; harmonies left and right of it. Moog left, guitar right; Hammond right, Mellotron left; bass and kick centre; the organ wide.\n")
A("## Score and parts\n")
A("- Lead sheet: voice, words and chord symbols (PDF).\n- Parts: harmony vocals (high, low), Moog, Hammond, church organ, Mellotron, piano, electric guitar, acoustic guitar, bass and drums (PDF).\n- Number chart (PDF).\n- Demo: MP3, with General MIDI and GarageBand MIDI files.\n")
open("/home/claude/p58/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", "/home/claude/p58/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", "/home/claude/p58/out/The Ratios Hold - songbook.docx"], check=True)
print("ok")
