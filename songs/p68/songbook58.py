"""'Same Time Tomorrow' (song 58): the songbook and production notes, for musicians only. Every bar number, pitch and chord named here is read
from song_record.pkl (build58.py, from lyric58.song.json); the prose around them is written for this song. Writes songbook.md (for the Doc)
and out/Same Time Tomorrow - songbook.docx (pandoc, the songbook reference document), with the producer one-sheet on its own page."""
import pickle, os, re, subprocess, collections, json
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb")); L = json.load(open(os.path.join(HERE, "lyric58.json")))
NM = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
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
title_line = [n for n in lines[("Chorus 1", 0)] if n["first"]]
hr = (nm(min(n["midi"] for n in HARM)), nm(max(n["midi"] for n in HARM)))
gr = (nm(min(min(e["p"]) for e in P["guitar"])), nm(max(max(e["p"]) for e in P["guitar"])))
br = (nm(min(e["p"][0] for e in P["bass"])), nm(max(e["p"][0] for e in P["bass"])))
fills = sorted({bar(e["on"]) for e in P["drums"] if e["p"][0] in (45, 48)})
drums_from = min(bar(e["on"]) for e in P["drums"])
gfull = sorted(b for b, c in collections.Counter(bar(e["on"]) for e in P["guitar"]).items() if c >= 6)
iv = collections.Counter()
for h in HARM:
    l = [n for n in LEAD if n["on"] <= h["on"] < n["on"] + n["dur"]]
    if l: iv[l[-1]["midi"] - h["midi"]] += 1
third_to_fifth = sum(v for k, v in iv.items() if 3 <= k <= 7) / max(1, sum(iv.values()))
def phrases():
    t = sorted(LEAD, key=lambda n: n["on"]); out = []; s0 = t[0]["on"]
    for a, b in zip(t, t[1:]):
        if b["on"] - (a["on"] + a["dur"]) >= 12: out.append((a["on"] + a["dur"] - s0) / 12 * 60 / REC["qbpm"]); s0 = b["on"]
    out.append((t[-1]["on"] + t[-1]["dur"] - s0) / 12 * 60 / REC["qbpm"]); return sorted(out)
PH = phrases()
def held_ends(k=4):
    out = []
    for key, ns in lines.items():
        fs = [n for n in ns if n["first"]]; j = len(fs) - 1
        while j > 0 and fs[j - 1]["hyph"]: j -= 1
        word = "".join(n["text"] for n in fs[j:]); tail = [n for n in ns if n["on"] >= fs[-1]["on"]]
        if sum(n["dur"] for n in tail) >= 18 and key[0] == "Verse 1": out.append(word.strip(",.;"))
    return out[:k]
HELD = held_ends()
LEVEL_WORD = lambda v: "full" if v >= 0.97 else "strong" if v >= 0.9 else "medium" if v >= 0.8 else "light" if v >= 0.7 else "soft"
WHAT = {"Intro": f"Guitar strumming eighths and bass from bar 1; drums in from bar {drums_from}; the voice picks up in bar {B1['Verse 1'] - 1}.",
        "Verse 1": f"Bass and drums under the voice; the guitar answers between lines. Tom fill in bar {B1['Chorus 1'] - 1}.",
        "Chorus 1": "The harmony voice comes in under him. Title on the downbeat.",
        "Turn 2": "Two bars of guitar strums between chorus and verse.",
        "Verse 2": f"As verse 1. Tom fill in bar {B1['Chorus 2'] - 1}.",
        "Chorus 2": "As chorus 1.",
        "Bridge": "Starts on Am. The groove holds; he sings straight through.",
        "Verse 3": f"As verse 1. Tom fill in bar {B1['Last Chorus'] - 1}.",
        "Last Chorus": "Sixteen bars, two more than the others; nine lines, the title again at the end. Last bar C F C F, a beat each.",
        "Outro": "Six bars of C, guitar strumming, band with it to the end."}
SHORTW = {"Intro": "guitar, bass; drums from bar 2", "Verse 1": "voice over bass and drums; guitar answers", "Chorus 1": "harmony voice in", "Turn 2": "guitar strums",
          "Verse 2": "as verse 1", "Chorus 2": "as chorus 1", "Bridge": "from Am; groove holds", "Verse 3": "as verse 1", "Last Chorus": "two bars longer; ends C F C F",
          "Outro": "guitar strums to the end"}
PB = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
md = [f"# {REC['title']}: songbook and production notes", "", "Words and music: Jason Bryant", ""]
md += ["## At a glance", "",
       "**What it is about.** An old preacher in his last days tells about the boy who comes to change his sheets, and the promise they make each other every evening: same time tomorrow. "
       "It is a small promise, kept daily, and by the last chorus it has come to hold up more than the pulpit ever did.", "",
       f"**How to play it.** C major, ♩ = 84, 4/4, a folk ballad. {len(REC['bars'])} bars, about {mm}:{ss:02d}. One baritone voice ({rng[0]} to {rng[1]}), a harmony voice in the choruses, acoustic guitar, bass and drums.", "",
       "| Section | Bars | Bar numbers | Level |", "|---|---|---|---|"]
for s, nb, st, _, _ in REC["plan"]: md.append(f"| {s} | {nb} | {st // BAR + 1}–{st // BAR + nb} | {LEVEL_WORD(REC['level'][s])} |")
md += ["", "## Section by section", ""]
for s, nb, st, _, _ in REC["plan"]:
    b0 = st // BAR + 1; md += [f"### {s} (bars {b0}–{b0 + nb - 1})", "", WHAT[s], ""]
    ks = [k for k in lines if k[0] == s]
    if not ks:
        md += ["Chords: " + " | ".join(" ".join(chord_at_bar(b)) for b in range(b0, b0 + nb)), ""]; continue
    md += ["| Bar | Line | Chords | Melody |", "|---|---|---|---|"]
    for k in ks:
        li = line_info(k); txt = TEXT.get(k, "")
        mel = f"starts {li['first']}, ends {li['last']}" + (f"; top {li['top']} on “{li['top_word']}” (bar {li['top_bar']})" if li["top"] == nm(top_m) else "")
        md.append(f"| {li['slot']} | {txt} | {li['chords']} | {mel} |")
    md.append("")
md += ["## For each player", "",
       f"**Voice.** A baritone, {rng[0]} to {rng[1]}. Tell it plainly in the verses; the choruses sit about three semitones higher, so let them open a little without pushing. "
       f"The title lands on the downbeat each time: " + " ".join(nm(n["midi"]) for n in title_line) + f", climbing to {nm(title_line[-1]['midi'])} on “-morrow”. The song’s top note, {nm(top_m)}, comes in lines 3 and 8 of each chorus.", "",
       f"**Harmony voice.** Under the lead in all three choruses, in his rhythm and on his words; {round(100 * third_to_fifth)} in 100 of its notes sit a third to a fifth below him. Range {hr[0]} to {hr[1]}: the lowest notes want a true bass, or take them up an octave. Keep it soft; he leads.", "",
       f"**Acoustic guitar.** Steady eighth-note strums in the intro, the turn (bars {B1['Turn 2']}–{B1['Turn 2'] + 1}) and the outro. In the verses and choruses you answer in the spaces between his lines and lay out while he sings. Written range {gr[0]} to {gr[1]}.", "",
       f"**Bass.** Quarter notes on every beat: roots and fifths, with a chromatic note a half step from the next root (C♯ down to C, F♯ up to G). Range {br[0]} to {br[1]}. Lock with the kick on 1 and 3.", "",
       f"**Drums.** Kick on 1 and 3, snare on 2 and 4, hat eighths, from bar {drums_from} to the end. A tom fill in the bar before each chorus that follows a verse (bars {', '.join(map(str, fills))}).", "",
       "## For the singer", "",
       f"Breathe between lines: his phrases run {PH[len(PH) // 2]:.1f} seconds at the median and {PH[-1]:.1f} at the longest, so there is room at every line end. "
       f"Lines that end on a long note (in verse 1: {', '.join('“' + w + '”' for w in HELD)}) want to be held to their length and released, not clipped. "
       "Verse 3 is the hardest to sing plainly; do not lean on it. The last chorus is longer than the others and ends on the title: leave the last word open.", "",
       "## The arrangement", "",
       "The band stays in one groove the whole way. What changes is who is singing and where the guitar plays: the harmony voice in the choruses, the guitar strumming in the intro, the turn and the outro, and a tom fill leading into each chorus that follows a verse. "
       "Keep the verses intimate and let the choruses fill out only as much as the harmony voice brings.", ""]
md += ["## Production notes", "", "### Lyric sheet", ""]
cur = None
for k in lines:
    if k[0] != cur: cur = k[0]; md += ["", f"**{cur}**", ""]
    md.append(f"{line_info(k)['slot']}: {TEXT.get(k, '')}  ")
md += ["", PB, "### Producer one-sheet", "",
       "**Emotional target.** A dying man telling, without self-pity, about a boy whose daily visit has come to mean more than his whole ministry. It should feel like a kept promise, not a farewell.", "",
       "**References.**", "",
       "- Jason Isbell, “Elephant” (Southeastern, 2013): take the plain, unsentimental telling of a friend’s dying, and the quiet, patient acoustic setting.",
       "- John Prine, “Hello in There” (John Prine, 1971): take the conversational phrasing and the way small details of ordinary lives carry the weight.",
       "- Johnny Cash, “Hurt” (American IV, 2002): take the low voice right in front, with a sparse acoustic guitar that leaves room around every word.", "",
       "**Dynamic arc.**", "", "| Section | Bars | Level | What changes |", "|---|---|---|---|"]
for s, nb, st, _, _ in REC["plan"]: md.append(f"| {s} | {st // BAR + 1}–{st // BAR + nb} | {LEVEL_WORD(REC['level'][s])} | {SHORTW[s]} |")
md += ["", "**Non-negotiables.**", "",
       "- ♩ = 84, steady; no push into the choruses.", "- The title on the downbeat, every time.", "- The harmony voice below the lead, never above.",
       "- The guitar out of the way while he sings; it answers in the spaces.", "- The last chorus’s last bar: C F C F, a beat each.", "",
       "**Mix priorities.** The voice in front and centre, dry and close. The harmony voice tucked under it, slightly right. The guitar left of centre, up when he rests. Bass and kick locked together under everything. Nothing may cover the title line.", "",
       PB, "### Production brief", "",
       f"**The song.** “{REC['title']}”, words and music by Jason Bryant: a folk ballad in C major at ♩ = 84, {mm}:{ss:02d}, for a baritone with a harmony voice, acoustic guitar, bass and drums.", "",
       "**References** (checked): Jason Isbell, “Elephant” (2013); John Prine, “Hello in There” (1971); Johnny Cash, “Hurt” (2002). What to take from each is on the one-sheet.", "",
       "**Non-negotiables.** As on the one-sheet.", "",
       "### Session notes", "",
       f"- Tempo and click: ♩ = 84 throughout, 4/4. The voice enters with a pickup in bar {B1['Verse 1'] - 1}.",
       "- Key: C major. Chords bar by bar are on the number chart and above the lead sheet.",
       f"- Range: voice {rng[0]} to {rng[1]}; harmony {hr[0]} to {hr[1]}.",
       "- Tracking: guitar and click first, then bass and drums, then the lead voice, then the harmony voice.",
       "- Blend and panning: voice centre; harmony slightly right; guitar left of centre; bass and kick centre.",
       "- Every part can be played by one player at once; no extra passes are needed.", "",
       "### Score and parts", "",
       "- Lead sheet (voice, lyrics, chord symbols), PDF and MusicXML.", "- Full score (voice, harmony voice, acoustic guitar, bass, drums), PDF and MusicXML.",
       "- Parts, one PDF: voice, harmony voice, acoustic guitar, bass, drums; each with a note on its role, rehearsal marks and chord symbols.",
       "- Number chart (Nashville), PDF.", "- Demo, MP3 and General MIDI."]
text = "\n".join(md) + "\n"
open(os.path.join(HERE, "songbook.md"), "w").write(text)
doc_md = re.sub(r"\n```\{=openxml\}\n.*?\n```\n", "\n", text, flags=re.S)
open(os.path.join(HERE, "songbook_doc.md"), "w").write(doc_md)
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    subprocess.run(["pandoc", os.path.join(HERE, "songbook.md"), "-o", os.path.join(OUT, f"{REC['file_title']} - songbook.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("songbook:", len(text.split()), "words; phrases median", round(PH[len(PH) // 2], 1), "longest", round(PH[-1], 1), "; harmony third-to-fifth", round(third_to_fifth, 2))
