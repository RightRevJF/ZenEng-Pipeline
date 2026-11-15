"""Writes songbook.md for 'The Room Next Door' (song 52) from song_record.pkl: every bar number, pitch and chord read from the record. A
musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect, itertools
import importlib.util as _u
H = "/home/claude/p62"
R = pickle.load(open(f"{H}/song_record.pkl", "rb"))
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
def cn(c): return c.replace("#", "♯").replace("Bb", "B♭")
BARS = R["bars"]; BST = [b["start"] for b in BARS]
def barno(t): return bisect.bisect_right(BST, t)
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
B0 = {}; NBS = {}
for i, b in enumerate(BARS): B0.setdefault(b["sec"], i); NBS[b["sec"]] = b["n"]
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p62.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
WORDS = {s: [t for _, t in ls] for s, ls in L.SECTIONS}
def line_bars(s, i): b0 = B0[s] + 2 * i; return b0, b0 + 2
def chords_of(b0, b1): return " ".join(cn(BARS[b]["chord"]) for b in range(b0, b1))
def span(s): return f"{B0[s] + 1}–{B0[s] + NBS[s]}"
def sec_chords(s): return " ".join(cn(BARS[b]["chord"]) for b in range(B0[s], B0[s] + NBS[s]))
def rng_(k): ps = [p for e in R["parts"][k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
def notes(ns): return ", ".join(nm(n["midi"]) for n in ns)
ps = [n["midi"] for n in R["lead"]]; vlo, vhi = nm(min(ps)), nm(max(ps))
def table(s, only=None):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        if only is not None and i not in only: continue
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
mm, ss = int(R["seconds"] // 60), int(round(R["seconds"] % 60))
door = by[("Chorus 1", 4)]; home = by[("Last Chorus", 5)]; there = by[("Bridge", 3)]
va = [n["midi"] for n in R["lead"] if n["sec"].startswith("Verse")]; ca = [n["midi"] for n in R["lead"] if n["sec"] in ("Chorus 1", "Chorus 2", "Last Chorus") and n["role"] != "hook"]
SC = {2, 4, 6, 7, 9, 11, 1}
def near(x):
    r = round(x)
    if r % 12 in SC: return nm(r)
    return f"{nm(r - 1)} to {nm(r + 1)}"
lift = round(2 * (sum(ca) / len(ca) - sum(va) / len(va))) / 2
o = []; A = o.append
A('---\ntitle: "The Room Next Door"\nsubtitle: "Songbook and production notes, third edition"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("# At a glance\n")
A("**What it's about.** Nora's husband Bernard has died in the sitting room. She keeps his cup, his chair and the book he left face down, and she moves her own chair to the north wall, where the plaster is warm the way only a south wall should be. She talks to him through it. One morning the room next door comes as close as a breath, and she understands what she had been too close to see: a wall with a door in it is not the same as a wall without one. The song is from the writer's parable \"The Room Next Door\" in *Wild Fruit*.\n")
A(f"**How it goes.** An intimate folk ballad in 6/8, D major, at a dotted quarter of 54: count it in two, gently rocking. A fingerpicked acoustic guitar carries it; soft piano and an acoustic bass come in at the first chorus, a cello at the second. The hook, \"there's a door in the wall,\" lifts to {nm(max(n['midi'] for n in door))} on \"door\" and leaves \"wall\" open. The song climbs as it goes: the third and fourth verses sit higher than the first two, the last chorus is the highest chorus, and its first \"door\" reaches {vhi}, the song's top, once. The bridge drops to piano and cello alone. At the very end the hook is sung twice, and the second time it comes home.\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Every sung line takes two bars of 6/8, twelve eighth notes, which is about one syllable to an eighth.\n")
A("| Section | Bars | Chords |\n|---|---|---|")
for s, nb, st, mets, mv in R["plan"]:
    ch = {"Chorus 2": "as chorus 1", "Verse 2": "as verse 1", "Verse 3": "as verse 1", "Verse 4": "as verse 1"}.get(s) or sec_chords(s)
    A(f"| {s} | {span(s)} | {ch} |")
A(f"\n**The singer.** An alto, {vlo} to {vhi}. The verses sit low (around {near(sum(va) / len(va))} on average); the choruses sit about {lift:g} semitones higher (around {near(sum(ca) / len(ca))}). {nm(max(n['midi'] for n in door))} comes only on \"door\"; {vhi} only once, on the last chorus's first \"door.\"\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n\nThe acoustic guitar alone, fingerpicked in six: the bass note on the first and fourth eighths, the chord's upper notes between.\n")
A(f"## Verse 1 (bars {span('Verse 1')})\n"); A(table("Verse 1"))
_v0 = by[("Verse 1", 0)]
A(f"\nGuitar and voice only. \"Forty years\" starts on {nm(_v0[0]['midi'])} on the downbeat of bar {barno(_v0[0]['on'])}. The verse stays close to speech, {nm(min(n['midi'] for j in range(4) for n in by[('Verse 1', j)]))} to {nm(max(n['midi'] for j in range(4) for n in by[('Verse 1', j)]))}, the stressed words on the two beats of each bar. It ends on {nm(by[('Verse 1', 3)][-1]['midi'])} over Asus4, unresolved; the chorus answers it.\n")
A(f"## Chorus 1 (bars {span('Chorus 1')})\n"); A(table("Chorus 1"))
dd = next(n for n in door if n["midi"] == max(m["midi"] for m in door))
A(f"\nPiano and bass come in. \"It's the north wall, love\" starts on {nm(by[('Chorus 1', 0)][0]['midi'])} as a pickup. The hook (bars {line_bars('Chorus 1', 4)[0] + 1}–{line_bars('Chorus 1', 4)[1]}): \"there's a door in the wall\" sings {notes(door)}, reaching {nm(dd['midi'])} on \"door\" on the second beat of bar {barno(dd['on'])} and holding it; \"wall\" stays open on {nm(door[-1]['midi'])} over Asus4. Harmony joins on the hook in every chorus.\n")
A(f"## Verse 2 (bars {span('Verse 2')})\n"); A(table("Verse 2"))
A("\nVerse 1's tunes, fitted to the new words. The bass stays; the piano answers at the end of every other bar.\n")
import json as _j
VL = [e for e in _j.load(open(f"{H}/melody_varied.json"))["variation"]["log"] if e.get("now") and str(e["line"]).isdigit()]
def _lift(e):
    n = next(m for m in R["lead"] if m["on"] == e["on"] + (B0["Chorus 2"] - B0["Chorus 2"]) * 36 and m["sec"] == "Chorus 2")
    w = e["syl"].strip(",").lower()
    return f"\"{w}\" (bar {barno(n['on'])}) up from {nm(e['was'])} to {nm(e['now'])}"
A(f"## Chorus 2 (bars {span('Chorus 2')})\n\nThe same words and the same hook as chorus 1, but chorus 2 sits a little higher: three held notes are lifted, {'; '.join(_lift(e) for e in VL[:-1])}; and {_lift(VL[-1])}. The first line and the hook are exactly as before. The cello joins on long notes.\n")
A(f"## Interlude (bars {span('Interlude')})\n\nThe cello sings the hook's tune an octave down over Bm7 and Gmaj7, then holds while the guitar picks on.\n")
A(f"## Verse 3 (bars {span('Verse 3')})\n"); A(table("Verse 3"))
_SH = __import__("json").load(open(f"{H}/melody_shaped.json"))["shape"]
_shl = lambda s: sorted(e["line"] for e in _SH["log"] if e["sec"] == s and e["line"] != 4 or (e["sec"] == s and s != "Last Chorus"))
_vm = _SH["after"]["section means"]
def _st(x): r = round(2 * x) / 2; return f"{r:g} semitone" + ("" if r == 1 else "s")
A(f"\nVerse 1's tunes again, but from the second line on each tune moves up a step of the scale (the shape kept), so the verse rises as the story turns: about {_st(_vm['Verse 3'] - _vm['Verse 1'])} above verse 1 on average. The cello holds a long note every other bar.\n")
A(f"## Bridge (bars {span('Bridge')})\n"); A(table("Bridge"))
bl = [n["midi"] for j in range(3) for n in by[("Bridge", j)]]
tt = next(n for n in there if n["midi"] == max(m["midi"] for m in there))
A(f"\nThe hush: the guitar and bass stop; soft held piano chords and the cello. The first three lines stay low and level ({nm(min(bl))}–{nm(max(bl))}). Over Cadd9 (bar {B0['Bridge'] + 6}, borrowed from D minor) the room comes close. Then \"and you were there\" lifts {notes(there[:4])}, reaching {nm(tt['midi'])} on \"there\" (bar {barno(tt['on'])}), and \"gone\" holds open on {nm(there[-1]['midi'])} over A7sus4.\n")
A(f"## Verse 4 (bars {span('Verse 4')})\n"); A(table("Verse 4"))
A(f"\nThe guitar and bass return, with the piano high and soft. All four of verse 1's tunes now sit a step of the scale higher (the shape kept), about {_st(_vm['Verse 4'] - _vm['Verse 1'])} above verse 1 on average: the highest verse.\n")
A(f"## Final chorus (bars {span('Last Chorus')})\n"); A(table("Last Chorus"))
A(f"\nThe fullest the song gets, with harmony on every line. Every line before the hook sits a step of the scale above chorus 1's (the shape kept), so this is the highest chorus. Under \"and some morning it opens\" the harmony turns to B♭maj7 (bar {B0['Last Chorus'] + 6}), the one chord from outside the key. The hook comes twice: first with \"door\" lifted to {vhi}, the song's top and its only {vhi} (bar {barno(next(n for n in by[('Last Chorus', 4)] if n['midi'] == max(m['midi'] for m in by[('Last Chorus', 4)]))['on'])}), and \"wall\" open; then {notes(home)}, \"door\" on {nm(home[2]['midi'])} over Gmaj7 and \"wall\" home on {nm(home[-1]['midi'])} over Dadd9 (bar {barno(home[-1]['on'])}), held into the outro.\n")
A(f"## Outro (bars {span('Outro')})\n\nGuitar and cello, softer each bar and slowing a little; the last bar a Dadd9, let ring.\n")
A("# For each player\n")
A(f"**Voice.** An alto, {vlo} to {vhi}. Sing it as Nora would talk to Bernard through the wall: close, unhurried, not performed. Let the 6/8 rock you; the stressed words fall on the two beats. Open up on \"door\" and leave \"wall\" unfinished in choruses 1 and 2. Learn chorus 2 as its own: three held notes sit higher than in chorus 1. From verse 3 on, the tunes you know sit a step higher; let the song climb to the {vhi} on the last chorus's first \"door.\" In the bridge come right down until \"and you were there.\" Save the settled, final \"wall\" for the very end.\n")
A(f"**Harmony vocals.** Two parts with different jobs, on the hook in every chorus and on every line of the final chorus. The high part ({nm(min(n['midi'] for n in R['harm_hi']))}–{nm(max(n['midi'] for n in R['harm_hi']))}) sings the words with the lead, a third to a sixth above, as a line of its own: it often holds a note while the lead moves under it (on the hook, {nm(R['harm_hi'][0]['midi'])} held while the lead climbs to \"door\"). The low part ({nm(min(n['midi'] for n in R['harm_lo']))}–{nm(max(n['midi'] for n in R['harm_lo']))}) sings \"ooh\" in long notes under the lead, changing at most once a beat. Blend under the lead.\n")
A(f"**Acoustic guitar** ({rng_('guitar')}). Steel-string, fingerpicked in six eighths throughout: the bass note on the first and fourth, the chord between. Out in the bridge; back for verse 4.\n")
A(f"**Piano** ({rng_('piano')}). On the two beats of each bar in the choruses, soft; answers at the line ends in verse 2; held chords in the bridge; high and quiet in verse 4.\n")
A(f"**Cello** ({rng_('cello')}). Long notes from chorus 2; the hook's tune in the interlude; held notes in verse 3; with the piano in the bridge; a countermelody of long notes in the final chorus; the last D.\n")
A(f"**Acoustic bass** ({rng_('bass')}). In at chorus 1: the root on the first beat, the fifth or a step toward the next chord on the second. Out in the bridge; back for verse 4.\n")
A("**Drums.** None.\n")
A("# Arrangement\n")
A("The song is a woman alone in a quiet house, so it starts with one guitar and never gets loud. Each chorus adds one voice: piano and bass, then the cello. The interlude gives the hook to the cello, as if the house were answering her. The bridge takes the floor away (no guitar, no bass) so the morning arrives in near silence. The final chorus is the fullest, and the one chord from outside the key, B♭maj7, sits under the line where the door opens. The last \"wall\" is the only one that comes home.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s, i), ns in by.items():
    if s == "Chorus 2":
        if i == 0: A(f"| {span(s)} | (chorus) |")
        continue
    b_ = line_bars(s, i)[0] + 1; f_ = barno(ns[0]['on'])
    A(f"| {b_}{f' (pickup in {f_})' if f_ < b_ else ''} | {WORDS[s][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Grief that has found its footing. Not despair, not consolation handed down, but a widow's quiet certainty that the wall has a door in it. Warm, close, unforced.\n")
A("**The three references.**\n")
A("- **Leonard Cohen, \"Hallelujah\"** (*Various Positions*, 1984): a hymn-like song in a rolling compound meter. Take the slow rock of the meter and the hush.\n- **Alison Krauss, \"Ghost in This House\"** (*Forget About It*, 1999; written by Hugh Prestwood): a woman alone in a house after a loss, sung close. Take the closeness of the voice.\n- **Steve Wariner, \"Holes in the Floor of Heaven\"** (*Burnin' the Roadhouse Down*, 1998): a ballad about the dead still near. Take the plain, unembarrassed tenderness.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|---|---|---|---|")
for lab, s1, lv, wh in (("Intro, verse 1", "Verse 1", "pp", "one guitar and the voice"), ("Chorus 1", "Chorus 1", "p", "piano and bass in; harmony on the hook"),
                        ("Verse 2", "Verse 2", "p", "piano answers"), ("Chorus 2", "Chorus 2", "mp", "the cello joins"), ("Interlude", "Interlude", "mp", "the cello sings the hook"),
                        ("Verse 3", "Verse 3", "p", "the cello held"), ("Bridge", "Bridge", "pp", "guitar and bass out; piano and cello"), ("Verse 4", "Verse 4", "p", "the guitar back"),
                        ("Final chorus", "Last Chorus", "mp+", "the fullest; harmony on every line; B♭maj7; the hook home"), ("Outro", "Outro", "pp", "guitar and cello, slowing")):
    sp_ = f"1–{B0['Verse 1'] + NBS['Verse 1']}" if s1 == "Verse 1" else span(s1)
    A(f"| {lab} | {sp_} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The 6/8 rock, felt in two. {nm(dd['midi'])} only on \"door.\" \"Wall\" open in choruses 1 and 2, home on {nm(home[-1]['midi'])} only at the end. The bridge without guitar or bass. B♭maj7 under \"and some morning it opens.\" Nothing louder than mezzo-forte.\n")
A("**The mix priorities.** The voice close and dry enough to hear the breath. The guitar's picking at the centre, slightly left; the cello right; the piano soft and behind. In the bridge, room sound around the piano and cello.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A widow talks to her husband through the north wall of the sitting room, and comes to know the wall has a door in it.\n")
A("*References* (checked by search):\n")
A("- **Leonard Cohen, \"Hallelujah.\"** From *Various Positions* (1984), recorded June 1984, produced by John Lissauer; the original is in 12/8, a rolling triple meter of the kind found in gospel and folk.\n- **Alison Krauss, \"Ghost in This House.\"** Written by Hugh Prestwood and first a 1990 single for Shenandoah; Krauss's version is on *Forget About It* (Rounder, August 3, 1999), 4:04.\n- **Steve Wariner, \"Holes in the Floor of Heaven.\"** From *Burnin' the Roadhouse Down* (Capitol Nashville), released as a single on March 24, 1998; written by Steve Wariner and Billy Kirsch; Song of the Year from the CMA and the ACM in 1998.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** Dotted quarter = 54 (quarter = 81), 6/8 throughout; click on the dotted quarters, two a bar. The outro slows a little to its last chord: follow the guitar, no click.\n- **Key.** D major. The voice stays in the scale; the B♭maj7 and Cadd9 are in the band only.\n- **Chords per bar.** One chord a bar, as in the section tables.\n- **Range.** Voice {vlo}–{vhi}; harmony as above.\n- **Tracking.** Guitar and a guide vocal to the click first; then bass and piano; then cello; the lead vocal; the harmonies with the finished lead in the headphones.\n- **Blend and panning.** Voice centre; guitar slightly left; cello right; piano right of centre; bass centre; harmonies slightly left and right.\n- **The bridge.** Guitar and bass silent for all eight bars.\n")
A("## Score and parts\n")
A("- Lead sheet: voice, words and chord symbols (PDF).\n- Full score: every part on one set of systems (PDF).\n- Parts: harmony vocals (high, low), acoustic guitar, piano, cello and acoustic bass (PDF).\n- Number chart (PDF).\n- MusicXML: the lead sheet and the full score (.musicxml and .mxl).\n- Demo: MP3 and a General MIDI file.\n")
open(f"{H}/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", f"{H}/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", f"{H}/out/The Room Next Door (third edition) - songbook.docx"], check=True)
print("ok", len("\n".join(o)))
