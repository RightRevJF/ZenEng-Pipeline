"""Writes songbook.md for 'The Man Mama Prayed I'd Be' (song 54) from song_record.pkl: every bar number, pitch and chord read from the record.
A musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect, itertools
import importlib.util as _u
H = "/home/claude/p64"
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
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p64.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
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
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
mm, ss = int(R["seconds"] // 60), int(round(R["seconds"] % 60))
HIM = [n["midi"] for n in R["lead"] if n["singer"] == "him"]; HER = [n["midi"] for n in R["lead"] if n["singer"] == "her"]
VS = [n["midi"] for n in R["lead"] if n["sec"].startswith("Verse")]; CS = [n["midi"] for n in R["lead"] if n["sec"] in ("Chorus 1", "Chorus 2", "Chorus 3") and n["role"] != "hook"]
hk = v("Chorus 1", 5); h4 = v("Chorus 4", 5); t0, t1 = v("Tag", 0), v("Tag", 1)
br = R["breath"]; brbar = br["bar"] + 1; her0 = v("Chorus 4", 0)[0]
def avg(xs): return sum(xs) / len(xs)
def near(x):
    SC = {7, 9, 11, 0, 2, 4, 6}; r = round(x)
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
harm = R["harm"]; HH = [n["midi"] for n in harm if n["singer"] == "harmony"]
o = []; A = o.append
A(f'---\ntitle: "{R["title"]}"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("*Words and music: Jason Bryant*\n")
A("# At a glance\n")
A("**What it's about.** A young man sleeping on a mildewed couch in a buddy's double wide, broke, short a dime for a honey bun at the Git 'n' Split at two in the morning. The girl on the overnight shift covers the dime and smiles, and he decides to become the man his mama prayed he'd be. He finds his boots, begs a job, works sunup to sundown, leaves a dime in her tip jar every morning at five, and saves his twenties in a coffee can. Before he can ask her out, she drives out to the job site and kisses him in front of the whole crew. She has been watching him change, and he has been changing her too.\n")
A(f"**How it goes.** A mid-tempo country story song, a neotraditional two-step in G major at ♩ = 120. A man tells the story and sings the first three choruses. A woman sings the fourth chorus, and in the tag they sing together. Four verses, each followed by a chorus; the chorus's middle lines stay the same while its first and fifth lines change with whoever is singing it: the narrator, then him to the boss, then him to his buddies, then her.\n")
A(f"**The hook.** \"The man Mama prayed I'd be\" ends every chorus. It climbs {nm(hk[0]['midi'])}, {nm(hk[1]['midi'])} to {nm(hk[2]['midi'])} on \"Ma-\", the chorus's top note, then falls through {nm(hk[-2]['midi'])} and stops on {nm(hk[-1]['midi'])} over D. That ending is left open on purpose: he isn't that man yet. Only when she sings \"The woman Daddy prayed I'd be\" does the {nm(h4[-2]['midi'] - 12)} step up to G, home, over G. The tag sings both lines home.\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Every sung line takes two bars.\n")
A("| Section | Bars | Chords |\n|---|---|---|")
for s, nb, st, mets, mv in R["plan"]: A(f"| {s} | {span(s)} | {sec_chords(s)} |")
A(f"\n**The singers.** He is a baritone, {nm(min(HIM))} to {nm(max(HIM))}. The verses sit low, mostly around {near(avg(VS))}, close to speech; the choruses sit higher, around {near(avg(CS))}, and the only {nm(max(HIM))} is the hook's \"Ma-\". She sings {nm(min(HER))} to {nm(max(HER))}, the same tune an octave above him.\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n\nThe fiddle plays the hook's tune (bars {B0['Intro'] + 1}–{B0['Intro'] + 2}), then a run and a held note; the band comes in light under it: acoustic boom-chick, bass on 1 and 3, cross-stick on 2 and 4, a steel swell.\n")
for k in (1, 2, 3, 4):
    vs = f"Verse {k}"
    A(f"## Verse {k} (bars {span(vs)})\n"); A(table(vs))
    v0 = v(vs, 0); vps = [n["midi"] for j in range(8) for n in v(vs, j)]
    if k == 1:
        A(f"\nTold, not sung at you: {nm(min(vps))} to {nm(max(vps))}. \"He was sleepin' on a mildewed couch\" starts on {nm(v0[0]['midi'])} in bar {barno(v0[0]['on'])}. Lines 4 and 8 sit on the D chord and stay close to one note, almost spoken. The acoustic plays boom-chick, the drums cross-stick, and the steel answers in the gaps.\n")
    elif k in (2, 3):
        A(f"\nThe verse 1 tunes with new words, {nm(min(vps))} to {nm(max(vps))}. Sticks now (snare on 2 and 4). The Telecaster answers at the ends of lines" + (", and the steel trades the gaps with it" if k == 3 else "") + ".\n")
    else:
        A(f"\nThinner at first: cross-stick to bar {B0[vs] + 8}, then sticks and the steel swelling. **Bar {brbar}: everyone stops on beat 3, after \"kiss.\"** Two beats of silence; she comes in on her own.\n")
    cs = f"Chorus {k}"
    A(f"## Chorus {k} (bars {span(cs)})\n"); A(table(cs))
    chg = [j + 1 for j in range(6) if WORDS[cs][j] != WORDS["Chorus 1"][j]]
    if k == 1:
        c0 = v(cs, 0)
        A(f"\nThe snare moves to 2 and 4 with a crash on bar {B0[cs] + 1}; the acoustic goes to straight eighths, the steel swells and the Telecaster fills the gaps. \"And he saw her\" starts on {nm(c0[0]['midi'])}. Hook (bars {line_bars(cs, 5)[0] + 1}–{line_bars(cs, 5)[1]}): {notes(hk)}, \"be\" left open on {nm(hk[-1]['midi'])} over D.\n")
    elif k in (2, 3):
        A(f"\nThe same tune as chorus 1; the words change on lines {bl(chg)}, and the bars sung differently are {bl(chorus_diffs(cs))}. " + ("The piano comes in on the offbeats." if k == 2 else "The ride cymbal, the fiddle's long notes and a harmony voice on lines 2–4 and the hook.") + "\n")
    else:
        A(f"\nHers. She sings chorus 1's tune an octave above him, starting on {nm(her0['midi'])} over {cn(BARS[her0['on'] // 48]['chord'])} (bar {barno(her0['on'])}), with the words changed on lines {bl(chg)}. The band is all in, the fiddle and steel kept under her. On the title line he comes in under her, and \"be\" comes home: {notes(h4)}, over D then G (bar {barno(h4[-1]['on'])}).\n")
    if k == 3:
        A(f"## Turnaround (bars {span('Turnaround')})\n\nThe fiddle plays the hook's tune again (bars {B0['Turnaround'] + 1}–{B0['Turnaround'] + 2}); the steel answers with two held double-stops and a bend; a fill in the last bar. This is the release before the last verse.\n")
A(f"## Tag (bars {span('Tag')})\n"); A(table("Tag"))
A(f"\nHe sings \"The man Mama prayed I'd be\" with her a third above, home on {nm(t0[-1]['midi'])}; she sings \"The woman Daddy prayed I'd be\" with him an octave below, home on {nm(t1[-1]['midi'])}. The band eases off, cross-stick from bar {B0['Tag'] + 3}.\n")
A(f"## Ending (bars {span('Ending')})\n\nThe fiddle plays the hook's tune one last time, and this time it comes home to G. The last G rings: acoustic, steel, piano, kick and crash. No fade.\n")
A("# For each player\n")
A(f"**Him (lead vocal).** A baritone, {nm(min(HIM))} to {nm(max(HIM))}. Tell the verses like a man on a porch: plain, dry, every word clear. The humor is in the details, so don't play it for laughs. Lean into the choruses and leave the last \"be\" open, unresolved: he isn't finished yet. In chorus 4 come in under her on the title line; in the tag sing your line home and then double hers an octave down.\n")
A(f"**Her (vocal).** {nm(min(HER))} to {nm(max(HER))}. Chorus 4 is hers alone: she has been watching him every morning, and she has her own change to tell. Enter clean after the stop. Her \"be\" is the first time the song comes home. In the tag sing above his line, then your own.\n")
A(f"**Harmony voice** ({nm(min(HH))}–{nm(max(HH))}). A third above him on the hook in choruses 1–3, and on lines 2–4 of chorus 3. Blend under him; never louder.\n")
A(f"**Acoustic guitar** ({rng_('acoustic')}). Steel-string. Boom-chick in the intro and verses: the root on 1, the fifth on 3, the chord on 2 and 4 with an upstroke after. Straight eighths in the choruses and the tag. Stop on beat 3 of bar {brbar}.\n")
A(f"**Telecaster** ({rng_('tele')}). Short answers at the ends of lines, never under a sung word: three or four eighths down the major pentatonic, a double-stop on the first note. Verses 2 and 3, the choruses, the turnaround.\n")
A(f"**Fiddle** ({rng_('fiddle')}). The hook's tune in the intro, the turnaround and the ending (home to G the last time). Long notes under choruses 3 and 4 and the tag; in chorus 4 and the tag, stay below her.\n")
A(f"**Pedal steel** ({rng_('steel')}). Swells under the chords in the choruses, verse 3 and late verse 4; answers in the verse gaps with a bend from the note above into a chord tone. The second half of the turnaround is yours.\n")
A(f"**Piano** ({rng_('piano')}). Light: chords on 2 and 4 from chorus 2 on. The last G rings.\n")
A(f"**Bass** ({rng_('bass')}). A two-step: on 1 and 3 with the kick, roots and fifths with walk-ups into the changes. Root–five in the intro, turnaround and ending. Stop with the band on beat 3 of bar {brbar}.\n")
A("**Drums.** A two-step with sticks: kick on 1 and 3, snare on 2 and 4, hat in eighths.\n\n- *Intro, verse 1:* cross-stick.\n- *Verses 2–3:* sticks; a fill into each chorus.\n- *Choruses 1–2:* snare 2 and 4, crash on the first bar.\n- *Choruses 3–4:* ride; in chorus 4 a crash on every line.\n- *Turnaround:* a fill in the last bar.\n" + f"- *Verse 4:* cross-stick to bar {B0['Verse 4'] + 8}, sticks after; **stop on beat 3 of bar {brbar}.**\n- *Tag:* easing, cross-stick from bar {B0['Tag'] + 3}.\n- *Ending:* kick and crash on the last G.\n")
A("# Arrangement\n")
A(f"The band grows with him. Verse 1 is the couch and the convenience store: acoustic, bass, cross-stick and a little steel. Each chorus adds something (the full snare, then piano, then the ride and the fiddle's long notes), and each return is bigger than the last. The turnaround lets the air out before the last verse; verse 4 starts thin and builds to the kiss, and then the whole band stops for two beats. She comes in alone over the full band, the loudest point of the song, and the tag lets it settle. The fiddle carries the hook's tune at the start, the middle and the end, and only at the end does it come home.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s, i), ns in by.items():
    b_ = line_bars(s, i)[0] + 1; f_ = barno(ns[0]['on'])
    A(f"| {b_}{f' (pickup in {f_})' if f_ < b_ else ''} | {WORDS[s][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** A funny, warm story that turns out to be about grace: a no-account boy who becomes somebody because a girl was kind to him, and finds out she was changing too. Keep it light on top and true underneath, so the last chorus lands as a surprise and a homecoming.\n")
A("**The three references.**\n")
A("- **George Strait, \"Check Yes or No\"** (1995): a love story told across verses. Take the steady two-step and the plain, unhurried delivery.\n- **Zach Top, \"I Never Lie\"** (2024): today's traditional country with the steel out front. Take the steel's place in the mix and the dry humor sung straight.\n- **Kane Brown featuring Shania Twain, \"Boots\"** (2026): a man and a woman answering each other. Take the way her voice arrives as the story's reply.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|--------|-----|----|----------------------------|")
for lab, s1, s2, lv, wh in (("Intro, verse 1", "Intro", "Verse 1", "mp", "fiddle hook; acoustic, bass, cross-stick, steel"), ("Chorus 1", "Chorus 1", "Chorus 1", "mf", "snare 2 and 4, crash; steel, Telecaster"),
                            ("Verse 2", "Verse 2", "Verse 2", "mp", "sticks; Telecaster answers"), ("Chorus 2", "Chorus 2", "Chorus 2", "mf+", "piano in"),
                            ("Verse 3", "Verse 3", "Verse 3", "mf", "steel and Telecaster trade"), ("Chorus 3", "Chorus 3", "Chorus 3", "f", "ride, fiddle long notes, harmony"),
                            ("Turnaround", "Turnaround", "Turnaround", "mf", "fiddle hook, steel answer: the release"), ("Verse 4", "Verse 4", "Verse 4", "mp → f", f"thin, building; STOP on beat 3 of bar {brbar}"),
                            ("Chorus 4", "Chorus 4", "Chorus 4", "ff", "her; everything in, crashes on each line"), ("Tag, ending", "Tag", "Ending", "f → mp", "both voices; easing; the last G rings")):
    A(f"| {lab} | {B0[s1] + 1}–{B0[s2] + NBS[s2]} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The open ending of the hook in choruses 1–3 (\"be\" on {nm(hk[-1]['midi'])} over D) and its first homecoming only when she sings. The stop on beat 3 of bar {brbar}: true silence for two beats. Her entrance alone. The fiddle's hook at the start, the turnaround and the end. The two-step, never a rock backbeat.\n")
A("**The mix priorities.** His voice forward and dry, every word of the story clear. Steel and fiddle wide, under the vocal, never over a sung word; in chorus 4 everything sits below her. In the stop, nothing: no reverb tails.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A country story song about a broke young man who turns his life around for a girl at the Git 'n' Split, and the twist when she tells him he changed her too.\n")
A("*References* (checked by search):\n")
A("- **George Strait, \"Check Yes or No.\"** Written by Danny Wells and Dana Hunt Black; produced by Tony Brown and George Strait; released in September 1995 as the lead single from the box set *Strait Out of the Box*. It follows two schoolchildren from a classroom crush into a marriage, and it held number one on the Billboard country chart for four weeks.\n- **Zach Top, \"I Never Lie.\"** From *Cold Beer & Country Music* (Leo33, 2024), produced by Carson Chamberlain; neotraditional country with a comic lyric, compared to George Strait's \"Ocean Front Property.\" Top called it the countriest song on the record, with steel guitar all over it.\n- **Kane Brown featuring Shania Twain, \"Boots.\"** Released September 4, 2026 on Sony Music Nashville, produced by Dann Huff: a male answer to Twain's 1995 \"Whose Bed Have Your Boots Been Under?\", which Twain described as a call and response that continues the story.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** ♩ = 120 throughout, 4/4, straight (not swung). A two-step feel.\n- **Key.** G major. Every note in the voice is in the scale.\n- **Chords per bar.** As in the section tables; a bar with two chords splits two beats each.\n- **Range.** Him {nm(min(HIM))}–{nm(max(HIM))}; her {nm(min(HER))}–{nm(max(HER))}; harmony {nm(min(HH))}–{nm(max(HH))}.\n- **Tracking.** Bass, drums and acoustic together for the feel; then steel, fiddle, Telecaster and piano. Track him first with a scratch of her chorus; her chorus and both tag lines as their own passes. The fiddle's three hook statements must match note for note, except the last note of the ending.\n- **Blend and panning.** Vocals centre; acoustic left of centre, Telecaster right; fiddle left, steel right; piano wide left, low in the mix. Harmony voice tucked right of centre.\n- **The stop.** Bar {brbar}, beat 3: every instrument cuts with the drums. Leave the two beats empty.\n")
A("## Score and parts\n")
A("- Lead sheet: him, her, words and chord symbols (PDF).\n- Full score: every part on one set of systems (PDF).\n- Parts, each with a note on its role: him, her, harmony voice, acoustic guitar, Telecaster, fiddle, pedal steel, piano, bass and drums, every note written out (PDF).\n- Number chart (PDF).\n- MusicXML: the lead sheet and the full score.\n- Demo: MP3 and a General MIDI file.\n")
open(f"{H}/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", f"{H}/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", f"{H}/out/{R['file_title']} - songbook.docx"], check=True)
print("ok", len("\n".join(o)))
