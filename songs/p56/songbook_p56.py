"""Writes songbook.md for 'Dry Ground' (song 46) from song_record.pkl: every bar number, pitch and chord read from the record.
A musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess
R = pickle.load(open("/home/claude/p56/song_record.pkl", "rb"))
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
H2 = R["chords2"]; BARS = R["bars"]
B0 = {}; NB = {}
for i, b in enumerate(BARS): B0.setdefault(b["sec"], i); NB[b["sec"]] = b["n"]
SLOT = R["design"]["slots"]
TEXT = {}
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", "/home/claude/p56/lyric_p56.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
WORDS = {s: [t for _, t in ls] for s, ls in L.SECTIONS}
def line_bars(s, i): b0 = B0[s] + sum(SLOT[s][:i]); return b0, b0 + SLOT[s][i]
def chords_of(b0, b1):
    out = []
    for h in range(2 * b0, 2 * b1):
        if not out or out[-1] != H2[h]: out.append(H2[h])
    return " ".join(out)
def first_bar(s, i): return by[(s, i)][0]["on"] // 48 + 1
def bb(t): return f"bar {t // 48 + 1}, beat {t % 48 / 12 + 1:g}"
def note(s, i, k): return by[(s, i)][k]
def syl_note(s, i, prefix):
    return next(n for n in by[(s, i)] if n["text"].lower().startswith(prefix) and n["first"])
def sec_chords(s): return " ".join(BARS[b]["chord"] if BARS[b]["chord"] == BARS[b]["chord2"] else f"{BARS[b]['chord']}–{BARS[b]['chord2']}" for b in range(B0[s], B0[s] + NB[s]))
def rng_(k):
    ps = [p for e in R[k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
ps = [n["midi"] for n in R["lead"]]; fal = [n for n in R["lead"] if n.get("falsetto")][0]
vlo, vhi = nm(min(ps)), nm(max(p for p in ps if p != fal["midi"]))
def table(s):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
def span(s): return f"{B0[s] + 1}–{B0[s] + NB[s]}"
o = []; A = o.append
A('---\ntitle: "Dry Ground"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("# At a glance\n")
A("**What it's about.** A man remembers an affair as a flood. It happened in a parked car on grey afternoons: foil on the glass, the little quarter window forced shut, the windows fogging until the world outside went under. Now he is back on dry ground, in a safe house with every window painted shut, where the only water left is a sprinkler throwing a toy rainbow on the lawn. He knows it will never flood again, and he misses the water. The ark is never named. It is in the images (the dove that comes back empty, the bird that comes home with a leaf, a library sitting on its hill like a boat run aground) and in one line in the bridge: \"And Noah stood there missing the rain.\"\n")
A(f"**How it goes.** Atmospheric pop at ♩ = 118, four on the floor, straight, in A minor. The verses are sung long over a fast pulse with the band filtered, as if underwater; each chorus opens out. The hook is the end of the chorus: \"And I miss the water\" climbs to the chorus's high note on \"water,\" and \"God I miss the flood\" falls home to A and holds for two bars. In the last chorus the same \"flood\" leaps instead to a falsetto {nm(fal['midi'])}. The bridge drops the kick for the dry ground. The outro thins to a low hum and rain and ends on one A minor chord.\n")
A(f"**Form ({R['nbars']} bars, 4:04).** Several lines are long, so they get three bars instead of two. That is why the verses and pre-choruses run ten bars.\n")
A("| Section | Bars | Chords (two in a bar: two beats each) |\n|---|---|---|")
for s, nb, b0, _ in R["plan"]:
    lab = {"Pre 1": "Pre-chorus 1", "Pre 2": "Pre-chorus 2"}.get(s, s)
    ch = sec_chords(s) if s not in ("Chorus 2", "Verse 2", "Pre 2") else {"Chorus 2": "as chorus 1", "Verse 2": "as verse 1", "Pre 2": "as pre-chorus 1"}[s]
    if s == "Outro": ch += " (bar 120: one A minor chord, let ring)"
    A(f"| {lab} | {b0 + 1}–{b0 + nb} | {ch} |")
A(f"\n**The singer.** A tenor, {vlo} to {vhi}, plus one falsetto {nm(fal['midi'])} near the end. The whole song sits low and close; the only real height is that last \"flood.\"\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n")
A("Rain, a low hum on A (the car idling) and the arpeggio in eighths for four bars. At bar 5 the kick comes in on every beat with closed hats, and the pad starts pumping against it.\n")
v = lambda s, i: by[(s, i)]
w1 = syl_note("Verse 1", 0, "lit"); t1 = syl_note("Verse 1", 0, "tle"); car = v("Verse 1", 0)[-1]
A(f"## Verse 1 (bars {span('Verse 1')})\n"); A(table("Verse 1"))
A(f"\nThe first line enters just before beat 2 of bar {first_bar('Verse 1', 0)} on {nm(v('Verse 1', 0)[0]['midi'])}, lifts through \"lit-tle\" ({nm(w1['midi'])}, {nm(t1['midi'])}) and settles back to \"car\" on the downbeat of bar {car['on'] // 48 + 1}, slipping down to {nm(car['midi'])}. \"Foil on the glass\" is the same tune. The two long lines that follow get three bars each and sit lower: \"thumb\" touches {nm(syl_note('Verse 1', 2, 'thumb')['midi'])}, the bottom of the song, and \"drifted away\" stays between {nm(min(n['midi'] for n in v('Verse 1', 3)))} and {nm(max(n['midi'] for n in v('Verse 1', 3)))}, unhurried, with \"grey\" and \"came\" held a dotted quarter each. Sing it like a memory, close to the microphone.\n")
A(f"## Pre-chorus 1 (bars {span('Pre 1')})\n"); A(table("Pre 1"))
A(f"\nThe pre-chorus starts higher, on {nm(v('Pre 1', 0)[0]['midi'])}, and walks down. \"The windows running thick with breath\" begins as a pickup at the end of bar {first_bar('Pre 1', 1)} and reaches {nm(max(n['midi'] for n in v('Pre 1', 1)))} on \"win-.\" Lines 3 and 4 share one shape: \"red\" and \"last\" are each held two beats on {nm(syl_note('Pre 1', 2, 'red')['midi'])}, then the line steps down to {nm(min(n['midi'] for n in v('Pre 1', 2)))}. \"Under\" sinks to {nm(v('Pre 1', 3)[-1]['midi'])} and holds. Claps arrive on 2 and 4; a snare build fills bar {B0['Pre 1'] + NB['Pre 1']}.\n")
wa = syl_note("Chorus 1", 4, "wa"); fl = v("Chorus 1", 5)[-1]; god = v("Chorus 1", 5)[0]; mi = syl_note("Chorus 1", 5, "miss")
A(f"## Chorus 1 (bars {span('Chorus 1')})\n"); A(table("Chorus 1"))
A(f"\nThe chorus doesn't jump up; it opens out. \"Now I'm living on dry ground\" sits on {nm(v('Chorus 1', 0)[0]['midi'])}, almost spoken, and \"ground\" drops to {nm(v('Chorus 1', 0)[-1]['midi'])} on the downbeat of bar {v('Chorus 1', 0)[-1]['on'] // 48 + 1}. \"Every window painted shut\" is all on {nm(v('Chorus 1', 1)[0]['midi'])}, as flat as the line says. \"The sprinkler hangs a rainbow on the lawn\" takes three bars and lands \"lawn\" on {nm(v('Chorus 1', 2)[-1]['midi'])}. \"It's never gonna flood again\" reaches {nm(max(n['midi'] for n in v('Chorus 1', 3)))} on \"-na\" and falls to {nm(min(n['midi'] for n in v('Chorus 1', 3)))} on \"gain.\"\n")
A(f"Then the hook. \"And I miss the water\": \"wa-\" is the chorus's high note, {nm(wa['midi'])}, on the downbeat of bar {wa['on'] // 48 + 1}. \"God I miss the flood\": \"God\" stays up on {nm(god['midi'])} (bar {god['on'] // 48 + 1}, beat 3), \"miss\" drops to {nm(mi['midi'])}, and \"flood\" lands on {nm(fl['midi'])} on beat 3 of bar {fl['on'] // 48 + 1} and holds for two bars, to bar {(fl['on'] + fl['dur']) // 48 + 1}. Let it ring; don't push.\n")
A(f"## Verse 2 (bars {span('Verse 2')})\n"); A(table("Verse 2"))
A(f"\nThe verse tune again, fitted to the new words. \"Pulled me under and up again\" climbs to {nm(max(n['midi'] for n in v('Verse 2', 1)))} on \"un-\" and \"and,\" then sinks; \"backbone\" dips to {nm(syl_note('Verse 2', 2, 'back')['midi'])} as verse 1's \"thumb\" did. The claps come in from bar {B0['Verse 2'] + 3}.\n")
A(f"## Pre-chorus 2 (bars {span('Pre 2')})\n"); A(table("Pre 2"))
A(f"\nAs pre-chorus 1. \"The little coo you couldn't keep\" starts on {nm(v('Pre 2', 0)[0]['midi'])} and drops a sixth on \"-tle\"; \"back\" is held two beats on {nm(syl_note('Pre 2', 2, 'back')['midi'])} where \"red\" was. \"So we went down again\" opens with \"So\" held two beats and sinks to {nm(v('Pre 2', 3)[-1]['midi'])}.\n")
A(f"## Chorus 2 (bars {span('Chorus 2')})\n\nThe same melody as chorus 1, with the same two-bar \"flood\" on {nm(v('Chorus 2', 5)[-1]['midi'])} (bars {v('Chorus 2', 5)[-1]['on'] // 48 + 1}–{(v('Chorus 2', 5)[-1]['on'] + v('Chorus 2', 5)[-1]['dur']) // 48 + 1}).\n")
li = syl_note("Bridge", 0, "li"); bi = syl_note("Bridge", 2, "bird"); no = syl_note("Bridge", 3, "no")
A(f"## Bridge (bars {span('Bridge')})\n"); A(table("Bridge"))
A(f"\nThe kick drops out: this is the dry ground. Every line has three bars and room to breathe. \"Every day I pass the li-brar-y\" turns on one note, {nm(v('Bridge', 0)[0]['midi'])}, until \"li-\" lifts to {nm(li['midi'])} (bar {li['on'] // 48 + 1}). \"High on the hill like it ran aground\" stays between {nm(min(n['midi'] for n in v('Bridge', 1)))} and {nm(max(n['midi'] for n in v('Bridge', 1)))}, with \"like,\" \"it\" and \"ran\" each held two beats, so the boat sits still. \"The bird came home\" starts high, {nm(v('Bridge', 2)[0]['midi'])} then {nm(bi['midi'])} on \"bird,\" held. \"And Noah stood there missing the rain\" is the line the song is about: \"No-\" is held on {nm(no['midi'])}, the line climbs through \"missing\" to {nm(max(n['midi'] for n in v('Bridge', 3)))} on \"the,\" over the E chord, and the snare build in bars {B0['Bridge'] + NB['Bridge'] - 1}–{B0['Bridge'] + NB['Bridge']} brings the kick back.\n")
lf = v("Last Chorus", 5)[-1]; lm = v("Last Chorus", 5)[-2]
A(f"## Last chorus (bars {span('Last Chorus')})\n"); A(table("Last Chorus"))
A(f"\nThe chorus melody, with the band at its fullest. Line 4 changes to \"I stand out in it till I'm soaked\" on the same tune: he walks out into the sprinkler. Then the last \"flood\" doesn't fall. From \"the\" on {nm(lm['midi'])} it leaps to a falsetto {nm(lf['midi'])} on beat 3 of bar {lf['on'] // 48 + 1} and holds for two bars over E minor and G. It is the only time the voice goes up there.\n")
A(f"## Outro (bars {span('Outro')})\n"); A(table("Outro"))
A(f"\nThe kick stays for four bars, then goes, leaving the hum and the rain. \"Same cold hum\" brings back verse 1's first image; \"Roll the little window down\" opens the quarter window that verse 1 forced shut. \"And let the grey come in\" walks down to {nm(v('Outro', 3)[-1]['midi'])} on \"in\" (bar {v('Outro', 3)[-1]['on'] // 48 + 1}). Bar 120 is one A minor chord, let ring under the rain.\n")
A("# For each player\n")
A(f"**Voice.** A tenor, {vlo} to {vhi}, and the one falsetto {nm(fal['midi'])}. Keep it intimate: this is a man talking to himself in a parked car. The long verse lines want an even, unhurried line across their three bars, not rushed syllables. In the chorus, let \"water\" ring at the top and let \"flood\" settle, warm and held, rather than belted. Save everything for the last \"flood\": the falsetto should feel like it breaks loose.\n")
A("**Drums.**\n")
A(f"- *Intro:* tacet bars 1–4; kick on every beat and closed hats on the off-beats from bar 5.\n- *Verses:* kick and off-beat closed hats; claps on 2 and 4 from bar {B0['Verse 2'] + 3} of verse 2.\n- *Pre-choruses:* claps on 2 and 4; a snare build through the last bar.\n- *Choruses:* crash on 1, off-beat open hats, claps.\n- *Bridge:* the kick out for bars {B0['Bridge'] + 1}–{B0['Bridge'] + NB['Bridge'] - 2}; a snare build in bars {B0['Bridge'] + NB['Bridge'] - 1}–{B0['Bridge'] + NB['Bridge']}, eighths then sixteenths.\n- *Last chorus:* everything, with a crash on 1 and at bar {B0['Last Chorus'] + 9}.\n- *Outro:* kick and hats for four bars (bars {B0['Outro'] + 1}–{B0['Outro'] + 4}), then out.\n")
A(f"**Bass.** A synth bass locked to the kick, {rng_('bass')}. Each section has a two-bar figure and its variants, with the root on every change. Where the kick fills every beat, the figures vary by note and by touch: one bar legato, one with short off-beats, one staccato, one with the off-beats accented. Thinner in the bridge. One low A to end.\n")
A(f"**Synth arpeggio.** The chord's tones in a pulsing pattern, {rng_('arp')}: eighths in the intro, the verses, the bridge's last four bars and the outro's first four; sixteenths in the choruses, with the top note jumping up an octave every half bar. Filtered in the verses.\n")
A(f"**Pad.** The chord, retriggered on each beat and sidechained to the kick so it breathes, {rng_('pad')}. Filtered in the verses and pre-choruses, an octave doubled in the choruses, a little louder in the bridge. One A minor chord to end.\n")
A(f"**Rain and hum.** Rain in the intro and the outro. A low hum on A and E ({rng_('hum')}) in the intro's first four bars and the outro's last eight: the car idling.\n")
A("# Arrangement\n")
A("The song is built on the difference between underwater and open air. The verses and pre-choruses are filtered and close, so the listener is inside the fogged car. Each chorus opens wide, but the melody stays low and flat: dry ground is safe and dull, and the band gets bigger while the voice doesn't. The bridge takes the kick away so \"Noah stood there missing the rain\" lands in silence. The last chorus is the fullest moment, and its last note is the song's one real height: the falsetto \"flood.\" The outro takes the beat away and leaves the hum and the rain from the intro, with the window rolled down.\n")
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
A("**The emotional target.** Longing, not drama. A man who chose the safe life, and is mostly fine with it, admitting what he gave up. The flood was the best thing that happened to him and it nearly drowned him. The groove should be something you could dance to while feeling this, like a sad song in a club.\n")
A("**The three references.**\n")
A("- **Robyn, \"Dancing on My Own\"** (2010), the lead: about 117 BPM, a bright dance track about being lonely. Take the tempo, the four on the floor under heartbreak, and the way the band lifts while the feeling doesn't.\n- **M83, \"Midnight City\"** (2011): 105 BPM in B minor, nocturnal and synth-driven. Take the haze, the wide pads and the sense of a car at night.\n- **Kate Bush, \"Running Up That Hill (A Deal With God)\"** (1985): about 108 BPM in C minor, a pulsing drum machine under synths and a voice full of longing. Take the drive under the yearning, and a deal with God that can't be made.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|---|---|---|---|")
for lab, s1, s2, lv, wh in (("Intro", "Intro", "Intro", "p → mf", "rain and hum, then kick, pad, arpeggio"), ("Verses", "Verse 1", "Verse 2", "mf", "underwater: kick and hats, filtered bass, pad and arpeggio"),
                            ("Pre-choruses", "Pre 1", "Pre 2", "mf ↗", "claps; the snare build"), ("Choruses", "Chorus 1", "Chorus 2", "f", "open wide; the arpeggio in sixteenths; 'flood' held"),
                            ("Bridge", "Bridge", "Bridge", "mp ↗", "the kick out, then the build"), ("Last chorus", "Last Chorus", "Last Chorus", "ff", "everything; the falsetto 'flood'"),
                            ("Outro", "Outro", "Outro", "mp → p", "kick four bars, then the hum and rain; one chord")):
    bars = span(s1) if s1 == s2 else f"{span(s1)}, {span(s2)}"
    A(f"| {lab} | {bars} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The verses filtered and the choruses open. \"Water\" on the chorus's high note and \"flood\" falling home to A and held two bars. The kick out for the bridge, so the Noah line lands in quiet. The last \"flood\" in falsetto on {nm(fal['midi'])}, held. The rain and hum at both ends. The lyric stays as written: the ark is only ever hinted, apart from that one line.\n")
A("**The mix priorities.** The voice on top and close, every word clear. The kick and bass locked; the pad pumping against the kick. Bring the filter up slowly through each pre-chorus so the chorus feels like surfacing. In the bridge, voice, pad and bass only.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* An atmospheric pop song about a man on dry ground missing the flood: an affair remembered as the water, a safe life as the ark run aground. Danceable and sad at once, with one falsetto release at the end.\n")
A("*References* (checked by search):\n")
A("- **Robyn, \"Dancing on My Own.\"** Released in 2010 on *Body Talk Pt. 1*; listed at 117 BPM; NPR called it a fun, energetic dance song about being lonely and heartbroken.\n- **M83, \"Midnight City.\"** Released in 2011; listed at 105 BPM in B minor.\n- **Kate Bush, \"Running Up That Hill (A Deal With God).\"** Released in 1985 on *Hounds of Love*; listed at about 108 BPM in C minor, driven by synthesizers and a pulsing drum machine.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** ♩ = 118, 4/4, straight. Click on.\n- **Key.** A minor. The E chord at the end of the bridge brings a G♯; the voice's G♯3 in each chorus's last line is a passing note.\n- **Chords per bar.** As in the form table and the chart; where a bar has two chords, two beats each.\n- **Range.** Voice {vlo}–{vhi}, falsetto {nm(fal['midi'])} once. Bass {rng_('bass')}. Arpeggio {rng_('arp')}. Pad {rng_('pad')}. Hum {rng_('hum')}.\n- **Tracking.** Drums and bass first, then the pad, arpeggio, rain and hum, then the voice. Track the last \"flood\" as its own pass if it needs a separate approach.\n- **Blend and panning.** Voice up the middle and close. Kick and bass centred. Pad wide; arpeggio slightly right. Rain wide and low. Hats slightly left, claps centred.\n- **The filter.** A low-pass on the band (not the voice) in the verses and pre-choruses, opening fully on the first beat of each chorus.\n")
A("## Score and parts\n")
A("- Lead sheet: voice, words and chord symbols (PDF).\n- Parts: bass, synth arpeggio, pad and drums (PDF).\n- Number chart (PDF).\n- Demo: MP3, with General MIDI and GarageBand MIDI files.\n")
open("/home/claude/p56/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", "/home/claude/p56/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", "/home/claude/p56/out/Dry Ground - songbook.docx"], check=True)
print("ok")
