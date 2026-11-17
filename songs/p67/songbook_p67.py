"""Writes songbook.md for 'Jehovah's Band' (song 57) from song_record.pkl: every bar number, pitch, chord and texture read from the record
and the band writer's report. A musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect, itertools, sys
import importlib.util as _u
H = "/home/claude/p67"; sys.path[:0] = [H]
import engrave_p67 as E
R = pickle.load(open(f"{H}/song_record.pkl", "rb")); BR = R["writers"]["band"]
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
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p67.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
WORDS = {s: [t for _, t in ls] for s, ls in L.SECTIONS}
LABEL = {"Chorus 3": "Last chorus", "Tag": "Outro"}
def lab(s): return LABEL.get(s, s)
def line_bars(s, i): b0 = B0[s] + sum(SLOT[s][:i]); return b0, b0 + SLOT[s][i]
def chords_of(b0, b1):
    out = []
    for b in range(b0, b1):
        for c in (BARS[b]["chord"], BARS[b]["chord2"]):
            if not out or out[-1] != c: out.append(c)
    return " ".join(cn(c) for c in out)
def span(s): return f"{B0[s] + 1}–{B0[s] + NBS[s]}"
def sec_chords(s):
    out = []
    for c, g in itertools.groupby(BARS[b]["chord"] if BARS[b]["chord"] == BARS[b]["chord2"] else f"{BARS[b]['chord']}–{BARS[b]['chord2']}" for b in range(B0[s], B0[s] + NBS[s])):
        k = len(list(g)); out.append(cn(c) + (f" ×{k}" if k > 1 else ""))
    return ", ".join(out)
def rng_(k):
    ps = [p for e in R["parts"][k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
def notes(ns): return ", ".join(nm(n["midi"]) for n in ns)
def table(s):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
def tex(s):
    p = BR["sections"].get(s, {}).get("patterns", {}); out = []
    if p.get("organ"): out.append("organ " + E.pat_words(p["organ"]))
    if p.get("rhythm"): out.append("rhythm guitar " + E.pat_words(p["rhythm"]))
    return ", ".join(out)
mm, ss = int(R["seconds"] // 60), int(round(R["seconds"] % 60))
HIM = [n["midi"] for n in R["lead"]]
c1 = by[("Chorus 1", 0)]; top = max(c1, key=lambda n: n["midi"])
JE = BR["sections"]["Jam"]["entries"]; NMP = dict(organ="organ", bass="bass", drums="drums", rhythm="rhythm guitar", lead="lead guitar")
jam_order = sorted(JE.items(), key=lambda x: x[1])
V3first = by[("Verse 3", 0)][0]
LV = R["level"]
def dyn(x):
    return "pp" if x < 0.15 else "p" if x < 0.35 else "mp" if x < 0.55 else "mf" if x < 0.75 else "f" if x < 0.92 else "ff"
REFS = ("- **Grateful Dead, \"Eyes of the World.\"** Robert Hunter and Jerry Garcia; on *Wake of the Flood* (Grateful Dead Records, October 15, 1973), "
        "and its second single. A song built to open into a long jam.\n"
        "- **Grateful Dead, \"Scarlet Begonias.\"** Hunter and Garcia; on *From the Mars Hotel* (June 27, 1974). A loping groove, a story told in "
        "particular images, and an instrumental section that stretches out at the end.\n"
        "- **Grateful Dead, \"Uncle John's Band.\"** Hunter and Garcia; on *Workingman's Dead* (June 14, 1970); the single, an edit, reached number 69 on the Hot 100. "
        "A singable chorus that a whole room can join.\n")
o = []; A = o.append
A(f'---\ntitle: "{R["title"]}"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("*Words and music: Jason Bryant*\n")
A("# At a glance\n")
A("**What it's about.** A night that goes too far out and a man who barely gets home. A voice like gravel and honey calls him down into the basement of the attic of his mind; he answers to a name that isn't his and carries his spark down there. He sits in with Jehovah's band across the sands of time, dancing barefoot on red dirt under the moon, until a county man in a sweat-stained cap laughs the drummer quiet, pinches out the spark and takes even the sound of his daughter's name. He comes to in a diner booth with cold coffee and no idea of the town. Then his daughter calls him by his own name, and the band he went looking for is in his kitchen: her bare feet keep the beat, she sings the angels' line over the frying pan, and he thanks God it followed him home.\n")
A("**How it goes.** A Grateful Dead–style jam in E major at ♩ = 112, a loping 4/4 with a light swing, for one baritone. Two verses and two choruses, a bridge where everything goes out, a long jam that starts from silence and builds back, a third verse that comes home, and a last chorus that turns the cosmic into the kitchen.\n")
A(f"**The title line.** \"I been sitting in with Jehovah's band\" opens every chorus and comes back as its fifth line. It starts on {nm(c1[0]['midi'])}, reaches {nm(top['midi'])} on \"{top['text'].strip('-')}\" and ends on {nm(c1[-1]['midi'])} on \"band\". The outro sings the title three times.\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Every sung line takes two bars.\n")
A("| Section | Bars | Chords |\n|---|---|---|")
for s_, nb, st, mets, mv in R["plan"]: A(f"| {lab(s_)} | {span(s_)} | {sec_chords(s_)} |")
VS = [n["midi"] for n in R["lead"] if n["sec"].startswith("Verse")]; CS = [n["midi"] for n in R["lead"] if n["sec"].startswith("Chorus")]
A(f"\n**The singer.** A baritone, {nm(min(HIM))} to {nm(max(HIM))}. The verses sit low, {nm(min(VS))} to {nm(max(VS))}; the choruses reach {nm(max(CS))}.\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n\nThe lead guitar plays the chorus's title line twice, an octave up; {tex('Intro')}; drums and bass in from bar 1.\n")
for s_ in ("Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge"):
    A(f"## {lab(s_)} (bars {span(s_)})\n"); A(table(s_))
    ns = [n["midi"] for (s, i), v in by.items() if s == s_ for n in v]
    extra = ""
    if s_ == "Verse 1": extra = f" \"Down in the basement of the attic of my mind\" starts on {nm(by[(s_, 0)][0]['midi'])} in bar {barno(by[(s_, 0)][0]['on'])}."
    if s_ == "Verse 2": extra = " Verse 1's tune with new words."
    if s_ == "Chorus 2": extra = " The same words and tune as chorus 1."
    if s_ == "Bridge": extra = f" The chords never touch E: C♯m, D and Bm. The last line, \"And I lost the sound of my daughter's name\", ends at bar {B0['Bridge'] + NBS['Bridge']}, and the band drops out but for a quiet organ."
    A(f"\nVoice {nm(min(ns))} to {nm(max(ns))}; {tex(s_)}; level {dyn(LV[s_][0])}.{extra}\n")
A(f"## Jam (bars {span('Jam')})\n\nIt starts from silence and builds back: " + ", ".join(f"{NMP[p]} from bar {B0['Jam'] + k + 1}" for p, k in jam_order) + f". The chords go round E, E, D, A–E. The lead guitar solos from its entry to the end of the jam, climbing as the band builds.\n")
for s_ in ("Verse 3", "Chorus 3", "Tag"):
    A(f"## {lab(s_)} (bars {span(s_)})\n"); A(table(s_))
    ns = [n["midi"] for (s, i), v in by.items() if s == s_ for n in v]
    extra = ""
    if s_ == "Verse 3": extra = f" It comes in fresh on {nm(V3first['midi'])} (\"I\") at bar {barno(V3first['on'])}, after the jam: verse 1's tune twice, with new words."
    if s_ == "Chorus 3": extra = " The title lines keep chorus 1's tune; the other lines take chorus 1's tune with the new words. \"Thank God the band followed me home\" is sung twice."
    if s_ == "Tag": extra = " The title three times."
    A(f"\nVoice {nm(min(ns))} to {nm(max(ns))}; {tex(s_)}; level {dyn(LV[s_][0])}.{extra}\n")
A(f"## Ending (bars {span('Ending')})\n\n{sec_chords('Ending')}; {tex('Ending')}. The last E rings.\n")
A("# For each player\n")
A(f"**Voice.** A baritone, {nm(min(HIM))} to {nm(max(HIM))}. Tell it like it happened to you. Wonder in the choruses; the bridge quiet and frightened; verse 3 empty at first, then relieved; the last chorus thankful.\n")
for k, nmk in (("organ", "Organ"), ("rhythm", "Rhythm guitar"), ("lead", "Lead guitar"), ("bass", "Bass"), ("drums", "Drums")):
    role = E.ROLE[k].split(": ", 1)[1]
    A(f"**{nmk}**" + (f" ({rng_(k)})" if k != "drums" else "") + f". {role}\n")
A("# Arrangement\n")
A("One curve carries the song: each chorus louder than its verse, the second chorus above the first, the last chorus the top, the outro a step down. The bridge keeps the band going while the chords lose E. Then the jam starts from nothing, one player at a time, and builds to where verse 3 comes in fresh. The organ is the first sound and the lead guitar the last to enter.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s_, i), ns in by.items():
    b_ = line_bars(s_, i)[0] + 1; f_ = barno(ns[0]['on'])
    A(f"| {b_}{f' (pickup in {f_})' if f_ < b_ else ''} | {WORDS[s_][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Wonder that tips into fear, then relief that feels like grace. The listener should feel the trip without ever being told what it was, and the kitchen at the end should feel bigger than the sands of time.\n")
A("**The three references.**\n")
A("- **\"Eyes of the World\"** (1973): a song that opens into a jam. Take the way the band breathes before it stretches out.\n- **\"Scarlet Begonias\"** (1974): the loping groove and the story in particular pictures. Take the swing and the room around the voice.\n- **\"Uncle John's Band\"** (1970): a chorus a room can sing. Take the plain, singable title line.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|--------|-----|----|----------------------------|")
for s_, nb, st, mets, mv in R["plan"]:
    a, b = LV[s_]; lvtxt = dyn(a) if abs(a - b) < 0.05 else f"{dyn(a)} → {dyn(b)}"
    what = tex(s_) if s_ != "Jam" else "from silence: " + ", ".join(f"{NMP[p]} at {B0['Jam'] + k + 1}" for p, k in jam_order)
    A(f"| {lab(s_)} | {span(s_)} | {lvtxt} | {what} |")
A(f"\n**The non-negotiables.** The title line the same in every chorus. The bridge's last line, then silence. The jam built one player at a time from bar {B0['Jam'] + 1}. Verse 3 coming in fresh at bar {B0['Verse 3'] + 1}. The light swing.\n")
A("**The mix priorities.** The voice forward and clear over the band in every chorus and on every title line. Organ left, rhythm guitar right, lead guitar right of centre; in the jam the lead comes forward as it enters. Nothing sits a second away from the sung note.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A man's night out past the edge of his mind and his way back home, told in pictures: a basement voice, a cosmic band, a county man who puts the spark out, a diner at dawn, a daughter's voice.\n")
A("*References* (checked by search):\n")
A(REFS)
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** ♩ = 112 throughout, 4/4, a light swing (eighths long-short, about 3 to 2).\n- **Key.** E major, with D and Bm borrowed.\n- **Chords per bar.** As in the section tables; a bar with two chords splits two beats each.\n- **Range.** Voice {nm(min(HIM))}–{nm(max(HIM))}.\n- **Tracking.** Drums, bass, organ and rhythm guitar together for the groove; the jam tracked live as a band, in the order the players enter; the lead guitar's fills after; the voice last.\n- **Blend and panning.** Voice centre; organ left, rhythm guitar right, lead guitar right of centre; bass and kick centre.\n- **The silence.** Bar {B0['Jam'] + 1}: only the organ, quiet.\n")
A("## Score and parts\n")
A("- Lead sheet: the voice, words and chord symbols (PDF).\n- Full score: every part on one set of systems (PDF).\n- Parts, each with a note on its role: voice, organ, rhythm guitar, lead guitar, bass and drums, every note written out (PDF).\n- Number chart (PDF).\n- MusicXML: the lead sheet and the full score.\n- Demo: MP3 and a General MIDI file.\n")
open(f"{H}/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", f"{H}/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", f"{H}/out/{R['file_title']} - songbook.docx"], check=True)
print("ok", len("\n".join(o)))
