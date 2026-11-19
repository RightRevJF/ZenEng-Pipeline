"""'Same Time Tomorrow' (song 58): the songbook and production notes, for musicians only. Every bar number, pitch and chord named here is read
from song_record.pkl (build58.py, from lyric58.song.json); the prose around them is written for this song. Writes songbook.md (for the Doc)
and out/Same Time Tomorrow - songbook.docx (pandoc, the songbook reference document), with the producer one-sheet on its own page."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo58 as KI
import pickle, os, re, subprocess, collections, json
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb")); L = json.load(open(os.path.join(HERE, "lyric58.json")))
NM = KI.NM
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
def title_desc(REC_):
    """where the title falls against the chorus's first bar, read from the record"""
    b0 = next(st for s, nb, st, _, _ in REC_["plan"] if s == "Chorus 1"); ns = [n for n in REC_["lead"] if n["sec"] == "Chorus 1" and n["line"] == 0 and n["first"]]
    if ns[0]["on"] >= b0: return "on the chorus's downbeat", "Title on the downbeat."
    beat = (ns[0]["on"] % 48) // 12 + 1; land = next((n for n in ns if n["on"] >= b0), None); w = land["text"].strip(",.") if land else ""
    return (f"“{ns[0]['text']}” on beat {beat} of the bar before the chorus and “{w}” on its downbeat",
            f"The title picks up on beat {beat} of the bar before; “{w}” lands on the downbeat.")
def top_desc(REC_, nm_f):
    """where the song's top note falls, read from the record"""
    lead = REC_["lead"]; top = max(n["midi"] for n in lead); b1 = {s: st // 48 + 1 for s, nb, st, _, _ in REC_["plan"]}
    hits = [n for n in lead if n["midi"] == top and n["first"]] or [n for n in lead if n["midi"] == top]
    ch = [s for s in b1 if s.startswith(("Chorus", "Last Chorus"))]; rel = {s: sorted({n["on"] // 48 + 1 - b1[s] + 1 for n in hits if n["sec"] == s}) for s in ch}
    if all(rel[s] and rel[s] == rel[ch[0]] for s in ch) and all(n["sec"] in ch for n in hits):
        return f"The song’s top note, {nm_f(top)}, comes in bar{'s' if len(rel[ch[0]]) > 1 else ''} " + " and ".join(map(str, rel[ch[0]])) + " of each chorus."
    where = "; ".join(f"on “{n['text']}” in {n['sec'].lower() if n['sec'][-1].isdigit() else 'the ' + n['sec'].lower()} (bar {n['on'] // 48 + 1})" for n in hits[:3])
    return f"The song’s top note, {nm_f(top)}, comes {'once' if len(hits) == 1 else str(len(hits)) + ' times'}: {where}."
TD = title_desc(REC)
CHK = json.load(open(os.path.join(HERE, 'lyric58.song.json')))['checks']; LIFT = next(v for k, v in CHK.items() if k.startswith("the chorus's median over the verse's"))
PH = phrases()
TOPB = sorted({bar(n["on"]) - B1["Chorus 1"] + 1 for n in LEAD if n["sec"] == "Chorus 1" and n["midi"] == top_m})
def held_ends(k=4):
    out = []
    for key, ns in lines.items():
        fs = [n for n in ns if n["first"]]; j = len(fs) - 1
        while j > 0 and fs[j - 1]["hyph"]: j -= 1
        word = "".join(n["text"] for n in fs[j:]); tail = [n for n in ns if n["on"] >= fs[-1]["on"]]
        if sum(n["dur"] for n in tail) >= 18 and key[0] == "Verse 1": out.append(word.strip(",.;"))
    return out[:k]
HELD = held_ends()
_ks = list(lines); RUNON = [bar(lines[b_][0]["on"]) for a_, b_ in zip(_ks, _ks[1:]) if lines[b_][0]["on"] - (lines[a_][-1]["on"] + lines[a_][-1]["dur"]) < 12]
LEVEL_WORD = lambda v: "full" if v >= 0.97 else "strong" if v >= 0.9 else "medium" if v >= 0.8 else "light" if v >= 0.7 else "soft"
_lastbar = REC["bars"][B1["Last Chorus"] + NB["Last Chorus"] - 2]; _lb = " ".join(_lastbar["beats4"]) if _lastbar.get("beats4") else (_lastbar["chord"] + (" " + _lastbar["chord2"] if _lastbar["chord2"] != _lastbar["chord"] else ""))
_oc = " | ".join(" ".join(chord_at_bar(b)) for b in range(B1["Outro"], B1["Outro"] + NB["Outro"]))
_bc = REC["bars"][B1["Bridge"] - 1]["chord"]
_fill_in = lambda s: next((f for f in fills if B1[s] <= f < B1[s] + NB[s]), None)
WHAT = {"Intro": f"Guitar strumming eighths and bass from bar 1; drums in from bar {drums_from}; the voice picks up in bar {min(bar(n['on']) for n in LEAD)}.",
        "Verse 1": "The guitar strums eighths under the voice; bass and drums with it." + (f" Tom fill in bar {_fill_in('Verse 1')}." if _fill_in('Verse 1') else ""),
        "Chorus 1": "The harmony voice comes in under him. " + TD[1],
        "Verse 2": "As verse 1." + (f" Tom fill in bar {_fill_in('Verse 2')}." if _fill_in('Verse 2') else ""),
        "Chorus 2": "As chorus 1.",
        "Bridge": f"Starts on {_bc}. The groove holds; he sings straight through.",
        "Verse 3": "As verse 1." + (f" Tom fill in bar {_fill_in('Verse 3')}." if _fill_in('Verse 3') else ""),
        "Last Chorus": f"Sixteen bars, two more than the others; nine lines, the title again at the end. The last bar: {_lb}.",
        "Outro": f"{NB['Outro']} bars: {_oc}. Band to the end."}
SHORTW = {"Intro": f"guitar, bass; drums from bar {drums_from}", "Verse 1": "guitar strums under the voice", "Chorus 1": "harmony voice in",
          "Verse 2": "as verse 1", "Chorus 2": "as chorus 1", "Bridge": f"from {_bc}; groove holds", "Verse 3": "as verse 1", "Last Chorus": "two bars longer; the title again at the end",
          "Outro": _oc.replace(" | ", ", ")}
_NW = {1: "one", 2: "two", 3: "three", 4: "four", 6: "six", 8: "eight", 9: "nine", 10: "ten", 12: "twelve", 14: "fourteen", 16: "sixteen", 18: "eighteen", 20: "twenty"}
_dlc = NB["Last Chorus"] - NB["Chorus 1"]; _nlc = len([k for k in lines if k[0] == "Last Chorus"])
WHAT["Last Chorus"] = (f"{_NW.get(NB['Last Chorus'], NB['Last Chorus']).capitalize()} bars, {_NW.get(_dlc, _dlc)} more than the others; {_NW.get(_nlc, _nlc)} lines, the title again at the end. The last bar: {_lb}." if _dlc > 0
                       else f"As chorus 1; {_NW.get(_nlc, _nlc)} lines. The last bar: {_lb}.")
SHORTW["Last Chorus"] = f"{_NW.get(_dlc, _dlc)} bars longer; the title again at the end" if _dlc > 0 else "as chorus 1"
TURNS = [(s_, nb_) for s_, nb_, _, _, _ in REC["plan"] if s_.startswith("Turn")]                # the band alone between sections, where the record has a turn
for s_, nb_ in TURNS: WHAT[s_] = f"{_NW.get(nb_, nb_).capitalize()} bars, the band alone; he rests."; SHORTW[s_] = "the band alone; he rests"
_after = lambda s_: [x[0] for x in REC["plan"]][[x[0] for x in REC["plan"]].index(s_) - 1]
TURN_LINE = (" " + " ".join(f"After {_after(s_).lower()} the band plays {_NW.get(nb_, nb_)} bars alone." for s_, nb_ in TURNS)) if TURNS else ""
PB = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
md = [f"# {REC['title']} ({REC['edition']}): songbook and production notes", "", "Words and music: Jason Bryant", ""]
md += ["## At a glance", "",
       "**What it is about.** An old preacher in his last days tells about the boy who comes to change his sheets, and the promise they make each other every evening: same time tomorrow. "
       "It is a small promise, kept daily, and by the last chorus it has come to hold up more than the pulpit ever did.", "",
       f"**How to play it.** {KI.KEYSTR}, ♩ = 84, 4/4, a folk ballad. {len(REC['bars'])} bars, about {mm}:{ss:02d}. One baritone voice ({rng[0]} to {rng[1]}), a harmony voice in the choruses, acoustic guitar, bass and drums." + (f" The guitar plays {KI.CAPO}." if KI.CAPO else ""), "",
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
       f"**Voice.** A baritone, {rng[0]} to {rng[1]}. Tell it plainly in the verses; the choruses sit about {LIFT:g} semitones higher, so let them open a little without pushing. "
       f"Sing the title as written, {TD[0]}: " + " ".join(nm(n["midi"]) for n in title_line) + ". " + top_desc(REC, nm), "",
       f"**Harmony voice.** Under the lead in all three choruses, in his rhythm and on his words; {round(100 * third_to_fifth)} in 100 of its notes sit a third to a fifth below him. Range {hr[0]} to {hr[1]}: the lowest notes want a true bass, or take them up an octave. Keep it soft; he leads.", "",
       f"**Acoustic guitar.** Steady eighth-note strums from bar 1 to the end, under his voice; where a chord tone would sit a step from the note he sings, leave it out. Range {gr[0]} to {gr[1]}." + (" " + KI.capo_line([c for b_ in REC['bars'] for c in (b_['chord'], b_['chord2'])]) + "." if KI.CAPO else ""), "",
       f"**Bass.** Quarter notes on every beat: roots and fifths, with chromatic passing notes a half step from the next root. Range {br[0]} to {br[1]}. Lock with the kick on 1 and 3.", "",
       f"**Drums.** Kick on 1 and 3, snare on 2 and 4, hat eighths, from bar {drums_from} to the end. A tom fill in the bar before each chorus that follows a verse (bars {', '.join(map(str, fills))}).", "",
       "## For the singer", "",
       f"Breathe between lines: his phrases run {PH[len(PH) // 2]:.1f} seconds at the median. " + (f"Some lines run straight into the next with less than a beat between them (into bars {', '.join(map(str, RUNON[:8]))}{' and others' if len(RUNON) > 8 else ''}); take a quick breath in the gap or sing through, as feels natural; the longest stretch without a full beat's rest is {PH[-1]:.1f} seconds. " if RUNON else "There is room at every line end. ") +
       f"Lines that end on a long note (in verse 1: {', '.join('“' + w + '”' for w in HELD)}) want to be held to their length and released, not clipped. "
       "Verse 3 is the hardest to sing plainly; do not lean on it. The last chorus is longer than the others and ends on the title: leave the last word open.", "",
       "## The arrangement", "",
       "The band stays in one groove the whole way: the guitar strums eighths under him from the first bar to the last, with the bass on every beat and the drums on 1 and 3, 2 and 4. "
       "What changes is the harmony voice in the choruses, a tom fill leading into each chorus that follows a verse, and the last chorus" + (f", {_NW.get(_dlc, _dlc)} bars longer than the others." if _dlc > 0 else ".") + TURN_LINE + " Keep the verses intimate and let the choruses fill out only as much as the harmony voice brings.", ""]
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
       "- ♩ = 84, steady; no push into the choruses.", f"- The title as written every time: {TD[0]}.", "- The harmony voice below the lead, never above.",
       "- The guitar under him, never a step from the note he sings.", f"- The last chorus’s last bar: {_lb}.", "",
       "**Mix priorities.** The voice in front and centre, dry and close. The harmony voice tucked under it, slightly right. The guitar left of centre, under the voice. Bass and kick locked together under everything. Nothing may cover the title line.", "",
       PB, "### Production brief", "",
       f"**The song.** “{REC['title']}”, words and music by Jason Bryant: a folk ballad in {KI.KEYSTR} at ♩ = 84, {mm}:{ss:02d}, for a baritone with a harmony voice, acoustic guitar, bass and drums.", "",
       "**References** (checked): Jason Isbell, “Elephant” (2013); John Prine, “Hello in There” (1971); Johnny Cash, “Hurt” (2002). What to take from each is on the one-sheet.", "",
       "**Non-negotiables.** As on the one-sheet.", "",
       "### Session notes", "",
       f"- Tempo and click: ♩ = 84 throughout, 4/4. The voice enters in bar {min(bar(n['on']) for n in LEAD)}.",
       f"- Key: {KI.KEYSTR}" + (f"; guitar {KI.CAPO}" if KI.CAPO else "") + ". Chords bar by bar are on the number chart and above the lead sheet.",
       f"- Range: voice {rng[0]} to {rng[1]}; harmony {hr[0]} to {hr[1]}.",
       "- Tracking: guitar and click first, then bass and drums, then the lead voice, then the harmony voice.",
       "- Blend and panning: voice centre; harmony slightly right; guitar left of centre; bass and kick centre.",
       "- Every part can be played by one player at once; no extra passes are needed.", "",
       "### Score and parts", "",
       "- Lead sheet (voice, lyrics, chord symbols), PDF and MusicXML.", "- Full score (voice, harmony voice, acoustic guitar, bass, drums), PDF and MusicXML.",
       "- Parts, one PDF: voice, harmony voice, acoustic guitar, bass, drums; each with a note on its role, rehearsal marks and chord symbols.",
       "- Number chart (Nashville), PDF.", "- Demo, MP3 and General MIDI."]
text = "\n".join(md) + "\n"
for i_, (s_, _) in enumerate(TURNS):                                                           # the record names a turn by its count from the end; a musician reads "Turn", or "Turn 1", "Turn 2" in order
    text = text.replace(s_, "Turn" if len(TURNS) == 1 else f"Turn {i_ + 1}")
open(os.path.join(HERE, "songbook.md"), "w").write(text)
doc_md = re.sub(r"\n```\{=openxml\}\n.*?\n```\n", "\n", text, flags=re.S)
open(os.path.join(HERE, "songbook_doc.md"), "w").write(doc_md)
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    subprocess.run(["pandoc", os.path.join(HERE, "songbook.md"), "-o", os.path.join(OUT, f"{REC['file_title']} - songbook.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("songbook:", len(text.split()), "words; phrases median", round(PH[len(PH) // 2], 1), "longest", round(PH[-1], 1), "; harmony third-to-fifth", round(third_to_fifth, 2))
