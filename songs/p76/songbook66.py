"""'They Did the Right Thing' (song 66): the songbook and production notes, for musicians only. Every bar number, pitch and chord named here is read
from song_record.pkl (build66.py, from lyric66_d.hand.song.json); the prose around them is written for this song. Writes songbook.md (for the Doc)
and out/They Did the Right Thing (first edition) - songbook.docx (pandoc, the songbook reference document), with the producer one-sheet on its own page."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo66 as KI
import pickle, os, re, subprocess, collections, json
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb")); L = json.load(open(os.path.join(HERE, "lyric66.json")))
NM = KI.NM
def nm(p): return KI.pitch_name(p)
BAR = 48; bar = lambda t: t // BAR + 1
B1 = {s: st // BAR + 1 for s, nb, st, _, _ in REC["plan"]}; NB = {s: nb for s, nb, _, _, _ in REC["plan"]}
LEAD = REC["lead"]; HARM = REC["harm"]; P = REC["parts"]
lines = collections.OrderedDict()
for n in LEAD: lines.setdefault((n["sec"], n["line"]), []).append(n)
TEXT = {(s, i): t for s, ls in L["sections"] for i, t in enumerate(ls)}
def chord_at_bar(b): x = REC["bars"][b - 1]; return x["beats4"] if x.get("beats4") else ([x["chord"]] if x["chord"] == x["chord2"] else [x["chord"], x["chord2"]])
def chords_span(b0, b1):
    out = []
    for b in range(b0, b1 + 1):
        for c in chord_at_bar(b):
            if not out or out[-1] != c: out.append(c)
    return out
def line_info(k):
    ns = lines[k]; first = ns[0]; st = next((n for n in ns if n["stress"] and n["first"]), first)
    b0, bs, b1 = bar(first["on"]), bar(st["on"]), bar(ns[-1]["on"])
    bs = max(bs, B1.get(k[0], bs))                                                            # a line sung before its section's first bar (a stressed opening come in early) is the section's, with a pickup
    slot = f"{bs} (pickup in {b0})" if b0 < bs else f"{b0}"
    top = max(ns, key=lambda n: (n["midi"], -n["on"]))
    fs = [n for n in ns if n["first"]]; tsyl = max((n for n in fs if n["on"] <= top["on"]), key=lambda n: n["on"])
    j = fs.index(tsyl); a = j
    while a > 0 and fs[a - 1]["hyph"]: a -= 1
    z = j
    while z < len(fs) - 1 and fs[z]["hyph"]: z += 1
    top_word = "".join(n["text"] for n in fs[a:z + 1]).strip(",.;")
    return dict(slot=slot, b0=b0, b1=b1, first=nm(first["midi"]), last=nm(ns[-1]["midi"]), top=nm(top["midi"]), top_word=top_word, top_bar=bar(top["on"]),
                chords=" ".join(chords_span(bs, b1)))
secs = REC["seconds"]; mm, ss = int(secs // 60), int(round(secs % 60))
rng = (nm(min(n["midi"] for n in LEAD)), nm(max(n["midi"] for n in LEAD))); top_m = max(n["midi"] for n in LEAD)
hr = (nm(min(n["midi"] for n in HARM)), nm(max(n["midi"] for n in HARM)))
gr = (nm(min(min(e["p"]) for e in P["guitar"])), nm(max(max(e["p"]) for e in P["guitar"])))
br = (nm(min(e["p"][0] for e in P["bass"])), nm(max(e["p"][0] for e in P["bass"])))
iv = collections.Counter()
for h in HARM:
    l = [n for n in LEAD if n["on"] <= h["on"] < n["on"] + n["dur"]]
    if l: iv[l[-1]["midi"] - h["midi"]] += 1
under = sum(v for k, v in iv.items() if k > 0) / max(1, sum(iv.values())); third_to_fifth = sum(v for k, v in iv.items() if 3 <= k <= 7) / max(1, sum(iv.values()))
def phrases():
    t = sorted(LEAD, key=lambda n: n["on"]); out = []; s0 = t[0]["on"]
    for a, b in zip(t, t[1:]):
        if b["on"] - (a["on"] + a["dur"]) >= 6: out.append((a["on"] + a["dur"] - s0) / 12 * 60 / REC["qbpm"]); s0 = b["on"]
    out.append((t[-1]["on"] + t[-1]["dur"] - s0) / 12 * 60 / REC["qbpm"]); return sorted(out)
PH = phrases()
HOLDS = [n for n in LEAD if n["midi"] == 64 and n["dur"] >= 96]; HB = {n["sec"]: (bar(n["on"]), n["dur"] // BAR) for n in HOLDS}
TAGW = next(n for n in sorted(LEAD, key=lambda n: -n["on"]) if n["first"])
STOP = REC["hand"]["stop"]["bar"]
def chords_bars(s): return " | ".join(" ".join(chord_at_bar(b)) for b in range(B1[s], B1[s] + NB[s]))
DESC = chords_bars("Chorus 3").split(" | ")[-5:]
TOPS = sorted({(n["sec"], bar(n["on"])) for n in LEAD if n["midi"] == top_m and n["first"]})
def word_at(n):
    fs = [x for x in lines[(n["sec"], n["line"])] if x["first"]]; tsyl = max((x for x in fs if x["on"] <= n["on"]), key=lambda x: x["on"]); j = fs.index(tsyl); a = j
    while a > 0 and fs[a - 1]["hyph"]: a -= 1
    z = j
    while z < len(fs) - 1 and fs[z]["hyph"]: z += 1
    return "".join(x["text"] for x in fs[a:z + 1]).strip(",.;")
TOPW = []
for n in sorted(LEAD, key=lambda n: n["on"]):
    if n["midi"] == top_m and n["first"] and (word_at(n), n["sec"]) not in [(w, s) for w, s, _ in TOPW]: TOPW.append((word_at(n), n["sec"], bar(n["on"])))
LEVEL_WORD = lambda v: "full" if v >= 0.97 else "strong" if v >= 0.9 else "medium" if v >= 0.8 else "light" if v >= 0.7 else "soft" if v >= 0.6 else "quietest"
TURNS = [(s_, nb_) for s_, nb_, _, _, _ in REC["plan"] if s_.startswith("Turn")]
WHAT = {"Intro": f"The band in on {chords_bars('Intro')}; the voice picks up in bar {min(bar(n['on']) for n in LEAD)}.",
        "Verse 1": "Steady strummed eighths, kick and snare, bass on the roots. The story is told plainly.",
        "Pre-chorus 1": "The band leans in a little; the harmony voice joins on the Sunday-morning lines.",
        "Chorus 1": f"Full, with the harmony voice. The chorus ends “And still be gone”, with “gone” held on E4 for {HB['Chorus 1'][1]} bars from bar {HB['Chorus 1'][0]}; under it the bass starts down by half steps from E.",
        "Verse 2": "As verse 1.", "Pre-chorus 2": "As pre-chorus 1.",
        "Chorus 2": f"As chorus 1; “gone” held on E4 from bar {HB['Chorus 2'][0]}, and the bass walks down again.",
        "Bridge": f"Voice, guitar and bass only, the quietest part of the song, on {chord_at_bar(B1['Bridge'])[0]} throughout. On beats 3 and 4 of bar {STOP} everything stops: no fill.",
        "Chorus 3": f"Everyone back together on the downbeat of bar {B1['Chorus 3']}, with a crash. “Gone” is held on E4 for {HB['Chorus 3'][1]} bars from bar {HB['Chorus 3'][0]} while the bass walks E, D♯, D, C♯, C ({' | '.join(DESC)}).",
        "Tag": f"Voice and guitar only, fading. The last word, “{TAGW['text']}”, held on E4 (bar {bar(TAGW['on'])}).",
        "Outro": f"{NB['Outro']} bars, the guitar alone on {chords_bars('Outro')}. End on A minor and let it ring."}
SHORTW = {"Intro": "band in", "Verse 1": "the story, plain", "Pre-chorus 1": "leans in", "Chorus 1": f"full; E4 held from bar {HB['Chorus 1'][0]}", "Verse 2": "as verse 1",
          "Pre-chorus 2": "leans in", "Chorus 2": f"full; E4 held from bar {HB['Chorus 2'][0]}", "Bridge": f"voice, guitar, bass; stop in bar {STOP}",
          "Chorus 3": f"all in on the downbeat; E4 held {HB['Chorus 3'][1]} bars, the bass walks down", "Tag": "voice and guitar, fading", "Outro": "guitar alone, A minor"}
for s_, nb_ in TURNS: WHAT[s_] = f"{nb_} bars, the band: {chords_bars(s_)}. The held E4 rings into it; the bass keeps walking down. The voice rests after the hold."; SHORTW[s_] = "the band; the bass walks down"
PB = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
md = [f"# {REC['title']} ({REC['edition']}): songbook and production notes", "", "Words and music: Jason Bryant", ""]
md += ["## At a glance", "",
       "**What it is about.** Two people who work in the same building, married to others, meet in a parking garage. Then one of the spouses walks in, reads the messages, and asks for it to end. "
       "They end it. They go home, keep their vows and stay, as decent people do. The song does not argue with that. It only says that doing the right thing and being gone can be true at once.", "",
       f"**How to play it.** {KI.KEYSTR}, ♩ = 72, 4/4, dark indie folk-rock. {len(REC['bars'])} bars, about {mm}:{ss:02d}. One tenor ({rng[0]} to {rng[1]}) with a harmony voice in the choruses; "
       "strummed guitar, bass and drums. Each chorus ends on a long held E4 while the bass walks down by half steps. The bridge drops to voice, guitar and bass, stops dead, and the final chorus comes in all together.", "",
       "| Section | Bars | Bar numbers | Level |", "|---|---|---|---|"]
for s, nb, st, _, _ in REC["plan"]: md.append(f"| {s} | {nb} | {st // BAR + 1}–{st // BAR + nb} | {LEVEL_WORD(REC['level'][s])} |")
md += ["", "## Section by section", ""]
for s, nb, st, _, _ in REC["plan"]:
    b0 = st // BAR + 1; md += [f"### {s} (bars {b0}–{b0 + nb - 1})", "", WHAT[s], ""]
    ks = [k for k in lines if k[0] == s]
    if not ks:
        md += ["Chords: " + chords_bars(s), ""]; continue
    md += ["| Bars | Line | Chords | Melody |", "|---|---|---|---|"]
    for k in ks:
        li = line_info(k); txt = TEXT.get(k, "")
        held = next((n for n in HOLDS if n["sec"] == k[0] and n["line"] == k[1]), None)
        mel = f"starts {li['first']}, ends {li['last']}" + (f" (held {held['dur'] // BAR} bars)" if held else "") + (f"; top {li['top']} on “{li['top_word']}” (bar {li['top_bar']})" if li["top"] == nm(top_m) else "")
        _bs = int(li['slot'].split()[0]); _span = f"{_bs}–{li['b1']}" if li['b1'] > _bs else f"{_bs}"
        md.append(f"| {_span + li['slot'][len(str(_bs)):]} | {txt} | {li['chords']} | {mel} |")
    md.append("")
md += ["## For each player", "",
       f"**Voice.** A tenor, {rng[0]} to {rng[1]}. Tell the verses plainly, like a report; the pre-choruses lean in. The song's top note, {nm(top_m)}, comes on " + "; ".join(f"“{w}” ({s.lower()}, bar {b})" for w, s, b in TOPW[:3]) + ". "
       f"Every chorus ends “And still be gone” with “gone” held on E4: {HB['Chorus 1'][1]} bars in the first two choruses, {HB['Chorus 3'][1]} in the last. Hold it steady and level while the chords move under you; do not swell. The bridge is close and quiet.", "",
       f"**Harmony voice.** A lower voice (a baritone suits it), with the lead in the pre-choruses and choruses, in its rhythm and on its words; {round(100 * third_to_fifth)} in 100 of its notes sit a third to a fifth under the lead. It drops out on the held E4s, in the bridge and in the tag. Range {hr[0]} to {hr[1]}.", "",
       f"**Guitar.** Steady eighth-note strums from the chord names, the whole song. Under each held E4 the chords walk down from E to E/D♯; after the first chorus on to E7/D and Am/C, after the second back to E for the bridge, and after the last on to E7/D, A/C♯ and C. Softer in the bridge; stop dead on beat 3 of bar {STOP}; come back on the downbeat of bar {B1['Chorus 3']}. The tag is you and the voice, fading; the outro you alone, ending on A minor.", "",
       f"**Bass.** Quarter notes on the roots, as written. Under each held E4 walk down by half steps from E. Softly in the bridge; stop on beat 3 of bar {STOP}; out for the tag and outro. Range {br[0]} to {br[1]}.", "",
       f"**Drums.** Kick, snare and eighth-note hi-hat. Out for the whole bridge (bars {B1['Bridge']}–{B1['Chorus 3'] - 1}): no fill into the final chorus, which you start with a crash on its downbeat (bar {B1['Chorus 3']}). Out for the tag and outro.", "",
       "## For the singer", "",
       f"Breathe between lines: the phrases run {PH[len(PH) // 2]:.1f} seconds at the median, the longest stretch without half a beat's rest {PH[-1]:.1f} seconds (the held E4s). "
       "Take a full breath before each “And still be gone”: the hold is long, and it should end because you let it go, not because you ran out. "
       "Take no side with or against the people in the song. The verses are what happened; the chorus is what decent people do; the last line is the cost.", "",
       "## The arrangement", "",
       "The band plays it straight and steady, like the people in it. The choruses are full, but each ends on one held note while the bass slides down under it, so the chorus keeps sinking after the words stop. "
       f"The bridge strips to voice, guitar and bass, the quietest part of the song, and stops dead for two beats in bar {STOP}. The final chorus comes back all at once, nothing in the bar before, and its held E4 lasts three bars over the whole descent: E, D♯, D, C♯, C. "
       "The tag is the voice and the guitar alone, fading, and the guitar ends on A minor without resolving.", ""]
md += ["## Production notes", "", "### Lyric sheet", ""]
cur = None
for k in lines:
    if k[0] != cur: cur = k[0]; md += ["", f"**{cur}**", ""]
    md.append(f"{line_info(k)['slot']}: {TEXT.get(k, '')}  ")
md += ["", PB, "### Producer one-sheet", "",
       "**Emotional target.** Two people who did what they should, told without blame and without comfort. The listener should feel the decency and the loss at the same time, and leave unresolved, the way the song ends.", "",
       "**References.**", "",
       "- Jason Isbell, “Elephant” (Southeastern, 2013): take how a heavy story is told as a plain character sketch, with no sermon.",
       "- Bon Iver, “Skinny Love” (For Emma, Forever Ago, 2007): take the close, dry acoustic guitar and voice, and a hurt that stays steady in a minor key.",
       "- Damien Rice, “The Blower's Daughter” (O, 2002): take the slow, minimalist pace and the long held lines that let the room fill in.", "",
       "**Dynamic arc.**", "", "| Sections | Bars | Level | What changes |", "|---|---|---|---|",
       f"| Intro, verses | {B1['Intro']}–{B1['Pre-chorus 1'] - 1}, {B1['Verse 2']}–{B1['Pre-chorus 2'] - 1} | light | the story, plain |",
       f"| Pre-choruses | {B1['Pre-chorus 1']}–{B1['Chorus 1'] - 1}, {B1['Pre-chorus 2']}–{B1['Chorus 2'] - 1} | strong | leans in |",
       f"| Choruses 1, 2 and turns | {B1['Chorus 1']}–{B1['Verse 2'] - 1}, {B1['Chorus 2']}–{B1['Bridge'] - 1} | full | E4 held, the bass walks down |",
       f"| Bridge | {B1['Bridge']}–{B1['Chorus 3'] - 1} | quietest | voice, guitar, bass; silent from beat 3 of bar {STOP} |",
       f"| Final chorus | {B1['Chorus 3']}–{B1['Tag'] - 1} | full, the top | all in on the downbeat; E4 held three bars over E, D♯, D, C♯, C |",
       f"| Tag, outro | {B1['Tag']}–{len(REC['bars'])} | soft, fading | voice and guitar; the guitar alone to A minor |"]
md += ["", "**Non-negotiables.**", "",
       "- ♩ = 72, steady; no push.", f"- Every chorus's “gone” held on E4 (bars {', '.join(str(HB[s][0]) for s in ('Chorus 1', 'Chorus 2', 'Chorus 3'))}; {HB['Chorus 1'][1]}, {HB['Chorus 2'][1]} and {HB['Chorus 3'][1]} bars), the bass walking down by half steps under it; the tag's last word held on E4 too (bar {HB['Tag'][0]}).",
       f"- The bridge: voice, guitar and bass only, the quietest part of the song.", f"- All stop on beats 3 and 4 of bar {STOP}, no fill; the final chorus all in on its downbeat.",
       "- The tag: voice and guitar only, fading. End on A minor; no cadence.", "",
       "**Mix priorities.** The voice in front and close, the words always clear. The guitar just left of centre; bass and kick together, felt under the holds. The harmony voice right and behind the lead. "
       "Nothing may cover a held E4; the bass's half steps under it must be heard. The stop in the bridge must be silent: no reverb tails left hanging.", "",
       PB, "### Production brief", "",
       f"**The song.** “{REC['title']}”, words and music by Jason Bryant: dark indie folk-rock in {KI.KEYSTR} at ♩ = 72, {mm}:{ss:02d}, for a tenor with a harmony voice, strummed guitar, bass and drums.", "",
       "**References** (checked): Jason Isbell, “Elephant” (2013); Bon Iver, “Skinny Love” (2007); Damien Rice, “The Blower's Daughter” (2002). What to take from each is on the one-sheet.", "",
       "**Non-negotiables.** As on the one-sheet.", "",
       "### Session notes", "",
       f"- Tempo and click: ♩ = 72 throughout, 4/4. The voice enters in bar {min(bar(n['on']) for n in LEAD)}.",
       f"- Key: {KI.KEYSTR}. Chords bar by bar are on the number chart and above the lead sheet.",
       f"- Range: voice {rng[0]} to {rng[1]}; harmony {hr[0]} to {hr[1]}.",
       "- Tracking: guitar, bass and drums together for the feel; then the voice; the harmony voice last.",
       f"- The stop (bar {STOP}, beats 3 and 4): track it with the band, not as an edit, so the final chorus's entry is played together.",
       "- Blend and panning: voice centre; guitar slightly left; harmony slightly right; bass and kick centre; hi-hat a little right.",
       "- Every part can be played by one player at once.", "",
       "### Score and parts", "",
       "- Lead sheet (voice, lyrics, chord symbols), PDF and MusicXML.", "- Full score (voice, harmony voice, guitar, bass, drums), PDF and MusicXML.",
       "- Parts, one PDF: voice, harmony voice, guitar (rhythm slashes under the chord names), bass, drums; each with a note on its role, rehearsal marks and chord symbols.",
       "- Number chart (Nashville), PDF.", "- Demo, MP3 and General MIDI."]
text = "\n".join(md) + "\n"
for i_, (s_, _) in enumerate(TURNS): text = text.replace(s_, "Turn" if len(TURNS) == 1 else f"Turn {i_ + 1}")
text = text.replace("Chorus 3", "Final chorus"); text = re.sub(r"(?<=[A-G])#", "♯", text)
open(os.path.join(HERE, "songbook.md"), "w").write(text)
doc_md = re.sub(r"\n```\{=openxml\}\n.*?\n```\n", "\n", text, flags=re.S)
open(os.path.join(HERE, "songbook_doc.md"), "w").write(doc_md)
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    subprocess.run(["pandoc", os.path.join(HERE, "songbook.md"), "-o", os.path.join(OUT, f"{REC['file_title']} - songbook.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("songbook:", len(text.split()), "words; phrases median", round(PH[len(PH) // 2], 1), "longest", round(PH[-1], 1), "; harmony under", round(under, 2), "third-to-fifth", round(third_to_fifth, 2))
