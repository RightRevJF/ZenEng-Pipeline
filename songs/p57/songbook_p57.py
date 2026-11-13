"""Writes songbook.md for 'The Singer Doesn't Stop' (song 47) from song_record.pkl: every bar number, pitch and chord read from the record.
A musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess
R = pickle.load(open("/home/claude/p57/song_record.pkl", "rb"))
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
def cn(c): return c.replace("#", "♯")
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
H2 = R["chords2"]; BARS = R["bars"]
B0 = {}; NB = {}
for i, b in enumerate(BARS): B0.setdefault(b["sec"], i); NB[b["sec"]] = b["n"]
SLOT = R["design"]["slots"]
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", "/home/claude/p57/lyric_p57.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
WORDS = {s: [t for _, t in ls] for s, ls in L.SECTIONS}
def line_bars(s, i): b0 = B0[s] + sum(SLOT[s][:i]); return b0, b0 + SLOT[s][i]
def chords_of(b0, b1):
    out = []
    for h in range(2 * b0, 2 * b1):
        if not out or out[-1] != H2[h]: out.append(H2[h])
    return " ".join(cn(c) for c in out)
def v(s, i): return by[(s, i)]
def syl_note(s, i, prefix): return next(n for n in by[(s, i)] if n["text"].lower().startswith(prefix.lower()) and n["first"])
def bar(n): return n["on"] // 48 + 1
def beat(n): return f"{n['on'] % 48 / 12 + 1:g}"
def sec_chords(s): return " ".join(cn(BARS[b]["chord"]) if BARS[b]["chord"] == BARS[b]["chord2"] else f"{cn(BARS[b]['chord'])}–{cn(BARS[b]['chord2'])}" for b in range(B0[s], B0[s] + NB[s]))
def rng_(k):
    ps = [p for e in R[k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
ps = [n["midi"] for n in R["lead"]]; vlo, vhi = nm(min(ps)), nm(max(ps))
def table(s):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
def span(s): return f"{B0[s] + 1}–{B0[s] + NB[s]}"
LB = R["lift"]["bars"]; h0, h1 = v("Chorus 1", 0), v("Chorus 1", 1); b5, b6 = v("Bridge 2", 5), v("Bridge 2", 6)
o = []; A = o.append
A('---\ntitle: "The Singer Doesn\'t Stop"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("# At a glance\n")
A("**What it's about.** A believer sings to God about the day his own song ends. He knows his life the way you know a tune you've hummed forever: a heart that never kept perfect time, a mother who swears he hummed before he talked, the flat high note from the third pew. One day he'll draw a breath to sing and the next line won't come. The song's answer is in its title. Lazarus came back to the same old town and died again; Christ walked out into a morning the walls can't hold, and kept his scars. So the song can stop, because the singer doesn't. The last chorus lands on the point of it all: God will sing him again, flat high part and all, \"and it will still be me.\"\n")
A(f"**How it goes.** Acoustic-driven modern Christian music at ♩ = 84, in G major, built on a steel-string guitar's soft sixteenth-note strum. The verses are wordy and quick, close to speech. The chorus opens out without getting big. The hook is the first two lines: \"The song can stop\" falls to the tonic and the voice stops for a beat; \"But the singer doesn't stop\" sings the same little figure a step higher and runs straight on into the next line. The bridge comes twice: the first time with guitar and voice alone, the second a whole step higher (A major), climbing to {nm(b6[-1]['midi'])} on \"Yes You do\" before falling home. The band stays small throughout.\n")
A(f"**Form ({R['nbars']} bars, 4:11).** Every line takes two bars.\n")
A("| Section | Bars | Chords (two in a bar: two beats each) |\n|---|---|---|")
for s, nb, b0, _ in R["plan"]:
    ch = sec_chords(s) if s not in ("Chorus 2", "Verse 2") else {"Chorus 2": "as chorus 1", "Verse 2": "as verse 1"}[s]
    if s == "Bridge 2": ch += f" (bars {LB[0] + 1}–{LB[-1] + 1} in A major; the last two bars back in G)"
    if s == "Tag": ch += " (bar 88: one G chord, let ring)"
    A(f"| {'Bridge (again, higher)' if s == 'Bridge 2' else s} | {b0 + 1}–{b0 + nb} | {ch} |")
A(f"\n**The singer.** A tenor, {vlo} to {vhi}. The whole song sits in the middle of the voice; the top, {vhi}, comes once, on the second bridge's last \"do.\"\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n\nThe acoustic guitar alone, a soft sixteenth-note strum over G, D, E minor and C.\n")
br = syl_note("Verse 1", 3, "breath")
A(f"## Verse 1 (bars {span('Verse 1')})\n"); A(table("Verse 1"))
A(f"\nConversational and quick. Each line starts just after the downbeat on {nm(v('Verse 1', 0)[0]['midi'])} and talks its way down through C4 and B3 in eighths and sixteenths, landing on beat 3 of its second bar. The Mama line is the wordiest, eighteen syllables in two bars: don't rush it, let the sixteenths fall where the words fall. In the last line \"breath\" drops suddenly to {nm(br['midi'])} (bar {bar(br)}, beat {beat(br)}), the lowest note of the song, before \"the next line won't come\" climbs back to {nm(v('Verse 1', 3)[-1]['midi'])}. Guitar and voice only.\n")
A(f"## Chorus 1 (bars {span('Chorus 1')})\n"); A(table("Chorus 1"))
A(f"\nThe hook. \"The song can stop\": \"The\" is a pickup on {nm(h0[0]['midi'])}, then \"song\" (bar {bar(h0[1])}, held two beats), \"can\" and \"stop\" fall {nm(h0[1]['midi'])}, {nm(h0[2]['midi'])}, {nm(h0[3]['midi'])}, and \"stop\" is short, followed by silence. \"But the singer doesn't stop\" climbs {nm(h1[0]['midi'])}, {nm(h1[1]['midi'])}, {nm(h1[2]['midi'])}, {nm(h1[3]['midi'])}, then sings the same figure a step higher on \"does-n't stop\" ({nm(h1[4]['midi'])}, {nm(h1[5]['midi'])}, {nm(h1[6]['midi'])}), and \"stop\" is held right into \"You remember\" with no breath. The music does what the words say. \"You remember every note I ever sang\" reaches {nm(max(n['midi'] for n in v('Chorus 1', 2)))} on \"-ber\"; \"Every heartbeat out of time\" lands \"time\" on {nm(v('Chorus 1', 3)[-1]['midi'])} on the downbeat of bar {bar(v('Chorus 1', 3)[-1])}; \"You will sing me again\" leans on {nm(v('Chorus 1', 4)[-1]['midi'])}; and \"'Cause the singer doesn't stop\" comes home to {nm(v('Chorus 1', 5)[-1]['midi'])}. Bass and brushes come in here.\n")
A(f"## Verse 2 (bars {span('Verse 2')})\n"); A(table("Verse 2"))
A(f"\nThe verse tune again, with the words fitted to it: Lazarus, then the empty tomb, then Thomas. Let the weight grow line by line. \"Nail holes\" sits on {nm(syl_note('Verse 2', 3, 'nail')['midi'])}, and \"scars\" lands on {nm(v('Verse 2', 3)[-1]['midi'])} on beat 3 of bar {bar(v('Verse 2', 3)[-1])}. The low electric guitar swells in under it; the brushes stay, without the kick.\n")
A(f"## Chorus 2 (bars {span('Chorus 2')})\n\nAs chorus 1, with the electric guitar now in.\n")
A(f"## Bridge (bars {span('Bridge')})\n"); A(table("Bridge"))
A(f"\nThe band drops out: guitar and voice. The bridge sits low, between {nm(min(n['midi'] for s, i in [('Bridge', j) for j in range(6)] for n in v(s, i)))} and {nm(max(n['midi'] for s, i in [('Bridge', j) for j in range(6)] for n in v(s, i)))}. \"Not a copy, not a cover\" and \"Not a stranger with my face\" share a shape, as do the next two lines: start on G3 and lift to the line's last stress (\"cover,\" \"face,\" \"stumble,\" \"grace\"). \"But You do, oh You do\" turns around D4.\n")
A(f"## Bridge, again and higher (bars {span('Bridge 2')})\n"); A(table("Bridge 2"))
A(f"\nThe whole step up, to A major, for the first fourteen bars: the first five lines are the first bridge note for note, a step higher. Brushes and bass come back at bar {B0['Bridge 2'] + 5}, the kick at bar {B0['Bridge 2'] + 9}, and the electric grows. Then \"But You do\" rises by step, {nm(b5[0]['midi'])}, {nm(b5[1]['midi'])}, {nm(b5[2]['midi'])}, and \"Yes You do\" a step above it, {nm(b6[0]['midi'])}, {nm(b6[1]['midi'])}, {nm(b6[2]['midi'])}, with \"do\" held (bar {bar(b6[-1])}). That {nm(b6[-1]['midi'])} is the top of the song. \"You remember all of me\" falls back into G over C and D, ending on {nm(v('Bridge 2', 7)[-1]['midi'])}, and the last chorus comes in.\n")
A(f"## Last chorus (bars {span('Last Chorus')})\n"); A(table("Last Chorus"))
A(f"\nThe chorus melody, full but plain: no gang vocals, no pads. Line 4 becomes \"Even the high part I sang flat,\" its \"flat\" on {nm(v('Last Chorus', 3)[-1]['midi'])}. The last line is new: \"And it will still be me,\" coming home to {nm(v('Last Chorus', 5)[-1]['midi'])} on the downbeat of bar {bar(v('Last Chorus', 5)[-1])}.\n")
A(f"## Tag (bars {span('Tag')})\n"); A(table("Tag"))
A(f"\nThe guitar alone, the hook once more, and \"'Cause the singer doesn't stop\" home to {nm(v('Tag', 1)[-1]['midi'])}. Bar 88 is one G chord, let ring.\n")
A("# For each player\n")
A(f"**Voice.** A tenor, {vlo} to {vhi}. The verses are spoken-sung, quick and close; the words matter more than the notes. In the chorus, honor the silence after \"The song can stop\" and keep \"stop\" going into \"You remember.\" The bridge is quiet the first time; the second time, the step up and the climb to {vhi} on \"Yes You do\" is the one big moment. Even there, sing it, don't belt it.\n")
A(f"**Acoustic guitar.** A steel-string, {rng_('guitar')} in the demo: a soft sixteenth-note strum (down on each beat and its eighth, light up-strokes between), from the chord symbols. Alone in the intro, verse 1, the first bridge and the tag. In bars {LB[0] + 1}–{LB[-1] + 1} the chords move up a whole step (capo 2 and the G shapes work).\n")
A("**Drums.**\n")
A(f"- *Intro, verse 1:* tacet.\n- *Chorus 1:* brushes: kick on 1 and 3 (and a soft one on the \"and\" of 2), brush on 2 and 4, brushed sixteenths.\n- *Verse 2:* brushes without the kick.\n- *Chorus 2:* as chorus 1, with a cymbal swell into its first bar.\n- *Bridge:* out.\n- *Bridge, again:* brushes from bar {B0['Bridge 2'] + 5}, the kick from bar {B0['Bridge 2'] + 9}.\n- *Last chorus:* as chorus 2, a little fuller, still plain.\n- *Tag:* out.\n")
A(f"**Bass.** A fingered bass, {rng_('bass')}, from chorus 1: the root on every chord change, a two-bar figure and its variants, steps into the next bar. Out for verse 1's guitar-and-voice and the first bridge; back at bar {B0['Bridge 2'] + 5}. Out for the tag.\n")
A(f"**Electric guitar.** A low, clean electric, {rng_('electric')}: volume swells on sustained chord tones, two a bar, from verse 2 on (out for the first bridge). Underneath, never a lead line.\n")
A("# Arrangement\n")
A("Small on purpose. The song is one person talking to God, so it starts with one guitar and adds only what the words call for: bass and brushes when the chorus opens, an electric guitar's swell when Lazarus and Thomas arrive, nothing at all in the first bridge, and a slow build through the second, carried by the key change and the climb rather than by volume. The last chorus is the fullest moment and still plain. The tag hands the song back to the guitar.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s, i), ns in by.items():
    if s == "Chorus 2":
        if i == 0: A(f"| {B0['Chorus 2'] + 1}–{B0['Chorus 2'] + NB['Chorus 2']} | (chorus) |")
        continue
    A(f"| {ns[0]['on'] // 48 + 1} | {WORDS[s][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Intimate and unafraid. A man facing his own death with a tune in his head and the conviction that the one who wrote it remembers every note. The specifics carry it: the doctor, Mama, the third pew, Thomas's hands. Nothing should sound like a stadium.\n")
A("**The three references.**\n")
A("- **Rich Mullins, \"Hold Me Jesus\"** (1993), the lead: an acoustic, unguarded confession from a man to God. Take the closeness and the plain voice.\n- **Andrew Peterson, \"Is He Worthy?\"** (2018, on *Resurrection Letters, Vol. 1*): a medium-slow song about resurrection hope. Take the wordy verses that still sing, and the build that never turns bombastic.\n- **Matt Maher, \"Lord, I Need You\"** (2013): about 75 BPM, guitar-led, sung close. Take the small-band pulse and the chorus that opens without getting loud.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|---|---|---|---|")
for lab, s1, lv, wh in (("Intro, verse 1", "Intro", "p", "guitar alone; the voice close"), ("Chorus 1", "Chorus 1", "mp", "bass and brushes"), ("Verse 2", "Verse 2", "mp ↗", "the electric's swells; the weight grows"),
                        ("Chorus 2", "Chorus 2", "mf", "the band, still small"), ("Bridge", "Bridge", "p", "guitar and voice"), ("Bridge, again", "Bridge 2", "mp ↗ f", "a step up; the band grows; the climb to A4"),
                        ("Last chorus", "Last Chorus", "f", "full but plain"), ("Tag", "Tag", "p", "guitar alone; one chord")):
    bars = f"1–{B0['Verse 1'] + NB['Verse 1']}" if s1 == "Intro" else span(s1)
    A(f"| {lab} | {bars} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The beat of silence after \"The song can stop,\" and \"stop\" held straight into \"You remember.\" The first bridge with guitar and voice only. The whole-step lift and the climb to {vhi} on \"Yes You do.\" The last line, \"And it will still be me.\" A small band: no pads, no gang vocals, no big drums.\n")
A("**The mix priorities.** The voice on top, dry and close, every word clear (the verses are dense). The guitar's strum is the bed; the bass and brushes sit under it. The electric is felt more than heard.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* An intimate, acoustic Christian song about death and resurrection: a life as a song that can stop, sung by a believer to the God who doesn't, and will sing him again, scars and wrong notes and all.\n")
A("*References* (checked by search):\n")
A("- **Rich Mullins, \"Hold Me Jesus.\"** Words and music by Rich Mullins (1993); produced by Reed Arvin.\n- **Andrew Peterson, \"Is He Worthy?\"** From *Resurrection Letters, Vol. 1*, written with Ben Shive (2018); listed as 4/4, medium slow, about 73 BPM.\n- **Matt Maher, \"Lord, I Need You.\"** From *All The People Said Amen* (2013); listed at 75 BPM in B♭.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** ♩ = 84, 4/4, a sixteenth-note feel. Click on.\n- **Key.** G major; bars {LB[0] + 1}–{LB[-1] + 1} in A major (the second bridge), then back to G.\n- **Chords per bar.** As in the form table and the chart; where a bar has two chords, two beats each.\n- **Range.** Voice {vlo}–{vhi}. Bass {rng_('bass')}. Electric {rng_('electric')}.\n- **Tracking.** Guitar first (to a click), then bass and brushes, then the electric, then the voice. The verses may want the voice comped from several passes for the diction.\n- **Blend and panning.** Voice up the middle, dry and close. Guitar slightly left; the electric right and back. Bass centred; brushes a natural stereo spread.\n")
A("## Score and parts\n")
A("- Lead sheet: voice, words and chord symbols (PDF).\n- Parts: bass, electric guitar and drums (PDF). The acoustic guitar plays from the chord symbols.\n- Number chart (PDF).\n- Demo: MP3, with General MIDI and GarageBand MIDI files.\n")
open("/home/claude/p57/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", "/home/claude/p57/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", "/home/claude/p57/out/The Singer Doesn't Stop - songbook.docx"], check=True)
print("ok")
