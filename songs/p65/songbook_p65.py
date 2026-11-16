"""Writes songbook.md for 'Your Yard Man' (song 55) from song_record.pkl: every bar number, pitch and chord read from the record.
A musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect, itertools
import importlib.util as _u
H = "/home/claude/p65"
R = pickle.load(open(f"{H}/song_record.pkl", "rb"))
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
def cn(c): return c.replace("#", "♯")
BARS = R["bars"]; BST = [b["start"] for b in BARS]
def barno(t): return bisect.bisect_right(BST, t)
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
B0 = {}; NBS = {}
for i, b in enumerate(BARS): B0.setdefault(b["sec"], i); NBS[b["sec"]] = b["n"]
SLOT = R["design"]["slots"]
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p65.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
WORDS = {s: [t for _, t in ls] for s, ls in L.SECTIONS}
def line_bars(s, i): b0 = B0[s] + sum(SLOT[s][:i]); return b0, b0 + SLOT[s][i]
def chords_of(b0, b1):
    out = []
    for b in range(b0, b1):
        for c in (BARS[b]["chord"], BARS[b]["chord2"]):
            if not out or out[-1] != c: out.append(c)
    return " ".join(cn(c) for c in out)
def v(s, i): return by[(s, i)]
def span(s): return f"{B0[s] + 1}–{B0[s] + NBS[s]}"
def sec_chords(s):
    out = []
    for c, g in itertools.groupby(BARS[b]["chord"] if BARS[b]["chord"] == BARS[b]["chord2"] else f"{BARS[b]['chord']}–{BARS[b]['chord2']}" for b in range(B0[s], B0[s] + NBS[s])):
        k = len(list(g)); out.append(cn(c) + (f" ×{k}" if k > 1 else ""))
    return ", ".join(out)
def rng_(k):
    ps = [p for e in R["parts"][k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
def notes(ns): return ", ".join(nm(n["midi"]) for n in ns)
def table(s, only=None):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        if only is not None and i not in only: continue
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}{'' if b1 - b0 == 1 else f'–{b1}'} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
mm, ss = int(R["seconds"] // 60), int(round(R["seconds"] % 60))
HIM = [n["midi"] for n in R["lead"]]
VS = [n["midi"] for n in R["lead"] if n["sec"].startswith("Verse")]; CS = [n["midi"] for n in R["lead"] if n["sec"].startswith("Chorus") and n["role"] != "hook"]
cl = v("Chorus 1", 0); an = v("Chorus 1", 9); t0, t1 = v("Tag", 0), v("Tag", 1)
br = R["breath"]; brbar = br["bar"] + 1
def avg(xs): return sum(xs) / len(xs)
def near(x):
    SC = {9, 11, 1, 2, 4, 6, 8}; r = round(x)
    if r % 12 in SC: return nm(r)
    return nm(max(q for q in range(r - 2, r + 1) if q % 12 in SC))
def chorus_diffs(sec):
    out = []
    for k in range(NBS["Chorus 1"]):
        a_ = [(n["on"] - BST[B0["Chorus 1"] + k], n["engine_midi"], n["dur"]) for n in R["lead"] if barno(n["on"]) - 1 == B0["Chorus 1"] + k]
        b_ = [(n["on"] - BST[B0[sec] + k], n["engine_midi"], n["dur"]) for n in R["lead"] if barno(n["on"]) - 1 == B0[sec] + k]
        if a_ != b_: out.append(B0[sec] + k + 1)
    return out
def bl(xs): return ", ".join(str(x) for x in xs[:-1]) + (" and " if len(xs) > 1 else "") + str(xs[-1]) if xs else "none"
harm = R["harm"]; HH = [n["midi"] for n in harm]
REFS = ("- **Alan Jackson, \"Little Man.\"** Written by Alan Jackson, produced by Keith Stegall; released in May 1999 as the fourth and last single from *High Mileage*; "
        "number three on the Billboard country chart. A song for the family-owned shops pushed out of their towns.\n"
        "- **Zach Top, \"I Never Lie.\"** From *Cold Beer & Country Music* (Leo33, 2024), produced by Carson Chamberlain; neotraditional country with a comic lyric, "
        "compared to George Strait's \"Ocean Front Property.\" Top called it the countriest song on the record, with steel guitar all over it.\n"
        "- **George Strait, \"Check Yes or No.\"** Written by Danny Wells and Dana Hunt Black; produced by Tony Brown and George Strait; released in September 1995 "
        "as the lead single from *Strait Out of the Box*; a story told across verses, number one on the Billboard country chart for four weeks.\n")
o = []; A = o.append
A(f'---\ntitle: "{R["title"]}"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("*Words and music: Jason Bryant*\n")
A("# At a glance\n")
A("**What it's about.** A man who mows other people's yards for a living and wouldn't trade it. Up at a quarter past pitch black, coffee by the jug, half-ton and trailer, done by three, and no boss with a stopwatch. His daddy gave the mill thirty-one years and got a watch, a sheet cake and a heart that wouldn't wait; he spent his last summers watching his son cut his grass. So the son takes the summers his daddy never got to. On Sunday it's church, then the lake, and nobody can call him back.\n")
A("**How it goes.** A country story song with a chorus built for a crowd to sing back, a neotraditional two-step in A major at \u2669 = 120, for one baritone. Three verses, each followed by a chorus. The chorus's frame stays the same, while its middle lines change every time: Holland, then the gold watch his daddy got instead of summers, then Paris.\n")
A(f"**The hook.** Every chorus opens with \"I'm your yard man\", which jumps {nm(cl[0]['midi'])}, {nm(cl[1]['midi'])} to {nm(cl[2]['midi'])} on \"yard\", the chorus's top note. It closes with the same call and its answer, \"But I'm my own man\", on the same rhythm: {', '.join(nm(n['midi']) for n in an)}, home on \"man\". A harmony voice joins both lines, like the crowd singing back.\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Verse lines take two bars; in the chorus the frame lines take one bar each and the four middle lines two.\n")
A("| Section | Bars | Chords |\n|---|---|---|")
for s_, nb, st, mets, mv in R["plan"]: A(f"| {s_} | {span(s_)} | {sec_chords(s_)} |")
A(f"\n**The singer.** A baritone, {nm(min(HIM))} to {nm(max(HIM))}. The verses sit low, mostly around {near(avg(VS))}, close to speech; the choruses sit higher, around {near(avg(CS))}, and {nm(max(HIM))} comes only in the hook.\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n\nThe fiddle plays the call and the answer (bars {B0['Intro'] + 1}–{B0['Intro'] + 2}), then a run and a steel reply; the band comes in light: acoustic boom-chick, bass on 1 and 3, cross-stick.\n")
for k in (1, 2, 3):
    vs = f"Verse {k}"
    A(f"## Verse {k} (bars {span(vs)})\n"); A(table(vs))
    v0 = v(vs, 0); vps = [n["midi"] for j in range(8) for n in v(vs, j)]
    if k == 1:
        A(f"\nTold, not sold: {nm(min(vps))} to {nm(max(vps))}. \"Up at a quarter past pitch black\" starts on {nm(v0[0]['midi'])} in bar {barno(v0[0]['on'])}. Acoustic boom-chick and cross-stick; the steel answers in the gaps.\n")
    elif k == 2:
        A(f"\nVerse 1's tunes with new words, {nm(min(vps))} to {nm(max(vps))}. This is his daddy: the band pulls back, the drums stay on cross-stick, the steel holds long notes underneath. Sing it plainer than anything else in the song.\n")
    else:
        A(f"\nVerse 1's tunes with new words, {nm(min(vps))} to {nm(max(vps))}. Sunday: the piano plays plain half-note chords for the pew and the drums stay on cross-stick to bar {B0[vs] + 8}; from \"out on the lake\" the sticks come back and the Telecaster answers.\n")
    cs = f"Chorus {k}"
    A(f"## Chorus {k} (bars {span(cs)})\n"); A(table(cs))
    chg = [j + 1 for j in range(10) if WORDS[cs][j] != WORDS["Chorus 1"][j]]
    if k == 1:
        A(f"\nThe snare moves to 2 and 4 with a crash on bar {B0[cs] + 1}; the acoustic goes to straight eighths, the steel swells and the Telecaster fills the gaps. The call (bar {line_bars(cs, 0)[0] + 1}): {notes(cl)}. The call and the answer close it (bars {line_bars(cs, 8)[0] + 1}–{line_bars(cs, 9)[1]}), \"man\" home on {nm(an[-1]['midi'])} over A.\n")
    else:
        A(f"\nThe same tune as chorus 1; the words change on lines {bl(chg)}, and the bars sung differently are {bl(chorus_diffs(cs))}. " + ("The piano comes in on the offbeats. The middle lines turn from jokes to his daddy: no gold watch, just the summers Daddy never got to." if k == 2 else "The biggest chorus: the ride, a crash on each line, the fiddle's long notes, the harmony on lines 2–4 as well as the call and answer.") + "\n")
    if k == 2:
        A(f"## Turnaround, the break (bars {span('Turnaround')})\n\nThe fiddle plays the call and the answer (bars {B0['Turnaround'] + 1}–{B0['Turnaround'] + 2}); the steel replies; **bar {brbar}: the acoustic guitar alone.** Then Sunday comes in fresh.\n")
A(f"## Tag (bars {span('Tag')})\n"); A(table("Tag"))
A(f"\nBar {B0['Tag'] + 1}: **the call over a stop**, one kick and crash and then only the voices. Bar {B0['Tag'] + 2}: everyone back for the answer, \"man\" held on {nm(t1[-1]['midi'])}.\n")
A(f"## Ending (bars {span('Ending')})\n\nThe fiddle plays the answer home to A over D; the last A rings. No fade.\n")
A("# For each player\n")
A(f"**Voice.** A baritone, {nm(min(HIM))} to {nm(max(HIM))}. Plain and dry in verse 1, a working man telling you his day. Verse 2 is his daddy: quieter, no smile in it. Verse 3 is Sunday: easy. The choruses are proud; the call and answer belong to everybody.\n")
A(f"**Harmony voice** ({nm(min(HH))}–{nm(max(HH))}). A third above him on the call and the answer in every chorus and the tag, and on chorus 3's lines 2–4. The crowd singing back; never louder than him.\n")
A(f"**Acoustic guitar** ({rng_('acoustic')}). Steel-string. Boom-chick in the intro and verses: the root on 1, the fifth on 3, the chord on 2 and 4 with an upstroke after. Straight eighths in the choruses and the tag. The break's last bar (bar {brbar}) is yours alone.\n")
A(f"**Telecaster** ({rng_('tele')}). Short answers in the gaps, never under a sung word: three or four eighths down the major pentatonic, a double-stop on the first note. The choruses and the second half of verse 3.\n")
A(f"**Fiddle** ({rng_('fiddle')}). The call and the answer in the intro and the break, the answer home in the ending. Long notes under chorus 3 and the tag.\n")
A(f"**Pedal steel** ({rng_('steel')}). Answers in verse 1's gaps with a bend from the note above; long held notes under verse 2, quietly; swells under the choruses; the reply in the break.\n")
A(f"**Piano** ({rng_('piano')}). Offbeat chords on 2 and 4 from chorus 2 on; plain half-note chords for the church pew at the start of verse 3; the last A rings.\n")
A(f"**Bass** ({rng_('bass')}). A two-step: on 1 and 3 with the kick, roots and fifths with walk-ups into the changes. Root–five in the intro, the break and the ending. Out for the break's last bar and the tag's call.\n")
A("**Drums.** A two-step with sticks: kick on 1 and 3, snare on 2 and 4, hat in eighths.\n\n- *Intro, verses 1 and 2:* cross-stick (verse 2 softer).\n- *Choruses 1–2:* snare 2 and 4, crash on the first bar.\n" + f"- *Break:* out in bar {brbar}.\n- *Verse 3:* cross-stick to bar {B0['Verse 3'] + 8}, sticks after.\n- *Chorus 3:* ride, a crash on every line.\n- *Tag:* one kick and crash under the call, then back in.\n- *Ending:* kick and crash on the last A.\n")
A("# Arrangement\n")
A("The band follows his life. Verse 1 is the work: boom-chick and a little steel. The choruses open up, each one bigger. Verse 2, his daddy, pulls back to cross-stick and held steel, and chorus 2 carries that weight into its middle lines. The break lets the air out, down to one guitar, and Sunday comes in fresh on plain piano chords before the lake brings the band back. Chorus 3 is the biggest; the tag stops the band so everyone can shout the call, then lands the answer together. The fiddle carries the call and answer at the start, the middle and the end.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s_, i), ns in by.items():
    b_ = line_bars(s_, i)[0] + 1; f_ = barno(ns[0]['on'])
    A(f"| {b_}{f' (pickup in {f_})' if f_ < b_ else ''} | {WORDS[s_][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Pride without bragging, and a grief he doesn't dwell on. A man who chose his life because he watched what the other one cost his daddy. Keep it light and sunny on top; let verse 2 and the gold-watch chorus land quietly, so the last \"I'm my own man\" sounds earned.\n")
A("**The three references.**\n")
A("- **Alan Jackson, \"Little Man\"** (1999): a working-class song about what was lost. Take the plain, warm delivery and the respect in it.\n- **Zach Top, \"I Never Lie\"** (2024): today's traditional country with the steel out front. Take the steel's place and the dry humor sung straight.\n- **George Strait, \"Check Yes or No\"** (1995): the steady two-step and a story told across verses.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|--------|-----|----|----------------------------|")
for lab, s1, s2, lv, wh in (("Intro, verse 1", "Intro", "Verse 1", "mp", "fiddle call and answer; boom-chick, cross-stick, steel"), ("Chorus 1", "Chorus 1", "Chorus 1", "mf", "snare 2 and 4, crash; steel, Telecaster; harmony on the hook"),
                            ("Verse 2", "Verse 2", "Verse 2", "p", "his daddy: cross-stick, held steel"), ("Chorus 2", "Chorus 2", "Chorus 2", "mf+", "piano in; the gold-watch lines"),
                            ("Turnaround (break)", "Turnaround", "Turnaround", "mf → p", f"fiddle call and answer, steel reply; bar {brbar} the acoustic alone"), ("Verse 3", "Verse 3", "Verse 3", "mp → mf", "the pew on piano; the lake brings the sticks"),
                            ("Chorus 3", "Chorus 3", "Chorus 3", "f", "ride, crashes, fiddle long notes, more harmony"), ("Tag, ending", "Tag", "Ending", "f", "the call over a stop; the answer together; the last A rings")):
    A(f"| {lab} | {B0[s1] + 1}–{B0[s2] + NBS[s2]} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The call jumping to {nm(cl[2]['midi'])} on \"yard\" and the answer coming home on {nm(an[-1]['midi'])}, the same in every chorus. Verse 2 pulled back. The break's last bar on one guitar. The tag's call over a stop. The two-step, never a rock backbeat.\n")
A("**The mix priorities.** His voice forward and dry, every word clear; the harmony on the hook wide and a step behind him, a crowd not a duet. Steel and fiddle wide and under the vocal, never over a sung word. In verse 2, the steel low and long.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A country story song about a man who mows yards for a living, why he chose it (his daddy's thirty-one years at the mill), and the freedom of a Sunday nobody can take from him.\n")
A("*References* (checked by search):\n")
A(REFS)
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** \u2669 = 120 throughout, 4/4, straight (not swung). A two-step feel.\n- **Key.** A major. Every note in the voice is in the scale.\n- **Chords per bar.** As in the section tables; a bar with two chords splits two beats each.\n- **Range.** Voice {nm(min(HIM))}–{nm(max(HIM))}; harmony {nm(min(HH))}–{nm(max(HH))}.\n- **Tracking.** Bass, drums and acoustic together for the feel; then steel, fiddle, Telecaster and piano; the voice; the harmony as its own pass (double it for the crowd if you like). The fiddle's call and answer must match the voice's note for note.\n- **Blend and panning.** Voice centre; harmony split wide; acoustic left of centre, Telecaster right; fiddle left, steel right; piano wide left, low.\n- **The stops.** Bar {brbar}: the acoustic alone. Bar {B0['Tag'] + 1}: one hit, then voices only for the call.\n")
A("## Score and parts\n")
A("- Lead sheet: the voice, words and chord symbols (PDF).\n- Full score: every part on one set of systems (PDF).\n- Parts, each with a note on its role: voice, harmony voice, acoustic guitar, Telecaster, fiddle, pedal steel, piano, bass and drums, every note written out (PDF).\n- Number chart (PDF).\n- MusicXML: the lead sheet and the full score.\n- Demo: MP3 and a General MIDI file.\n")
open(f"{H}/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", f"{H}/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", f"{H}/out/{R['file_title']} - songbook.docx"], check=True)
print("ok", len("\n".join(o)))
