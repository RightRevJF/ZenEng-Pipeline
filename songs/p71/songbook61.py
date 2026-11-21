"""'This Side of the Door' (song 61): the songbook and production notes, for musicians only. Every bar number, pitch and chord named here is read
from song_record.pkl (build61.py, from lyric61.song.json); the prose around them is written for this song. Writes songbook.md (for the Doc)
and out/This Side of the Door (first edition) - songbook.docx (pandoc, the songbook reference document), with the producer one-sheet on its own page."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo61 as KI
import pickle, os, re, subprocess, collections, json
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb")); L = json.load(open(os.path.join(HERE, "lyric61.json")))
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
title_line = [n for n in lines[("Chorus 1", 7)] if n["first"]]
hr = (nm(min(n["midi"] for n in HARM)), nm(max(n["midi"] for n in HARM)))
gr = (nm(min(min(e["p"]) for e in P["guitar"])), nm(max(max(e["p"]) for e in P["guitar"])))
br = (nm(min(e["p"][0] for e in P["bass"])), nm(max(e["p"][0] for e in P["bass"])))
cr = (nm(min(e["p"][0] for e in P["cello"])), nm(max(e["p"][0] for e in P["cello"])))
sr = (nm(min(min(e["p"]) for e in P["strings"])), nm(max(max(e["p"]) for e in P["strings"])))
cello_from = min(bar(e["on"]) for e in P["cello"]); strings_from = min(bar(e["on"]) for e in P["strings"])
bare_from = bar(min(n["on"] for n in lines[("Last Chorus", 6)]))
gfull = sorted(b for b, c in collections.Counter(bar(e["on"]) for e in P["guitar"]).items() if c >= 6)
iv = collections.Counter()
for h in HARM:
    l = [n for n in LEAD if n["on"] <= h["on"] < n["on"] + n["dur"]]
    if l: iv[l[-1]["midi"] - h["midi"]] += 1
third_to_fifth = sum(v for k, v in iv.items() if 3 <= k <= 7) / max(1, sum(iv.values()))
def phrases():
    """his phrases in seconds, a breath read at half a beat of silence, as kept singers take one (906)"""
    t = sorted(LEAD, key=lambda n: n["on"]); out = []; s0 = t[0]["on"]
    for a, b in zip(t, t[1:]):
        if b["on"] - (a["on"] + a["dur"]) >= 6: out.append((a["on"] + a["dur"] - s0) / 12 * 60 / REC["qbpm"]); s0 = b["on"]
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
    def word_of(n):                                                                          # the whole word the note's syllable belongs to, as the line tables print it
        fs = [x for x in lead if x["first"] and (x["sec"], x.get("line")) == (n["sec"], n.get("line"))]; tsyl = max((x for x in fs if x["on"] <= n["on"]), key=lambda x: x["on"]); j = fs.index(tsyl); a = j
        while a > 0 and fs[a - 1]["hyph"]: a -= 1
        z = j
        while z < len(fs) - 1 and fs[z]["hyph"]: z += 1
        return "".join(x["text"] for x in fs[a:z + 1]).strip(",.;")
    seen_ = set(); hits = [n for n in hits if not ((word_of(n), n["sec"], n.get("line")) in seen_ or seen_.add((word_of(n), n["sec"], n.get("line"))))]      # one mention a word, where its syllables share the top note
    where = "; ".join(f"on “{word_of(n)}” in {n['sec'].lower() if n['sec'][-1].isdigit() else 'the ' + n['sec'].lower()} (bar {n['on'] // 48 + 1})" for n in hits[:3])
    return f"The song’s top note, {nm_f(top)}, comes {'once' if len(hits) == 1 else str(len(hits)) + ' times'}: {where}."
TD = title_desc(REC)
CHK = json.load(open(os.path.join(HERE, 'lyric61.song.json')))['checks']; LIFT = next(v for k, v in CHK.items() if k.startswith("the chorus's median over the verse's"))
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
_top_n = next(n for n in LEAD if n["sec"] == "Chorus 1" and n["midi"] == top_m); _tl1 = bar(lines[("Chorus 1", 7)][0]["on"]); _tl2 = bar(lines[("Last Chorus", 7)][0]["on"])
WHAT = {"Intro": f"The guitar alone, fingerpicked eighths; the voice picks up in bar {min(bar(n['on']) for n in LEAD)}.",
        "Verse 1": "She sings over the guitar alone, close and quiet.",
        "Chorus 1": f"The guitar a little fuller, still alone with her. The top of the song, {nm(top_m)}, on “wood” (bar {bar(_top_n['on'])}). The title line in bar {_tl1}: let “door” ring.",
        "Verse 2": f"As verse 1, with a cello under her from bar {cello_from}, holding each chord's root.",
        "Bridge": f"Starts on {_bc}. The song opens up: strings and bass come in (bar {strings_from}), the cello stays. She sings low here; let the band carry the size.",
        "Verse 3": "The strings and bass drop out: guitar and cello, quieter than verse 2.",
        "Last Chorus": f"Strings, bass and cello back, and a harmony voice with her. At “Three, and then two” (bar {bare_from}) everything but the guitar falls away. The last bar: {_lb}.",
        "Outro": f"{NB['Outro']} bars, the guitar alone: {_oc}. Let the last chord ring."}
SHORTW = {"Intro": "guitar alone", "Verse 1": "voice and guitar", "Chorus 1": "guitar a little fuller", "Verse 2": f"cello in (bar {cello_from})",
          "Bridge": "strings and bass in; the peak", "Verse 3": "strings and bass out", "Last Chorus": f"all in, harmony voice; all out at bar {bare_from} but the guitar",
          "Outro": "guitar alone"}
_NW = {1: "one", 2: "two", 3: "three", 4: "four", 6: "six", 8: "eight", 9: "nine", 10: "ten", 12: "twelve", 14: "fourteen", 16: "sixteen", 18: "eighteen", 20: "twenty"}
TURNS = [(s_, nb_) for s_, nb_, _, _, _ in REC["plan"] if s_.startswith("Turn")]                # the band alone between sections, where the record has a turn
for s_, nb_ in TURNS: WHAT[s_] = f"{_NW.get(nb_, nb_).capitalize()} bars, the guitar alone; she rests."; SHORTW[s_] = "the guitar alone; she rests"
PB = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
md = [f"# {REC['title']} ({REC['edition']}): songbook and production notes", "", "Words and music: Jason Bryant", ""]
md += ["## At a glance", "",
       "**What it is about.** A woman stands all night at her brother's door. He has shut himself in with his addiction, and she has come without anyone, only soup and a key that no longer fits. "
       "She presses her ear to the wood and listens for the sound of him living, and it has gone down to one note. The door never opens. She leaves the soup, and knocks the way they knocked as children.", "",
       f"**How to play it.** {KI.KEYSTR}, ♩ = 80, 4/4, a ballad. {len(REC['bars'])} bars, about {mm}:{ss:02d}. One alto voice ({rng[0]} to {rng[1]}), fingerpicked acoustic guitar throughout; a cello from verse 2; strings and bass in the bridge and the last chorus; a harmony voice in the last chorus. No drums." + (f" The guitar plays {KI.CAPO}." if KI.CAPO else ""), "",
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
       f"**Voice.** An alto, {rng[0]} to {rng[1]}. She is talking through a door: plain, close, never performed. " + (f"The choruses sit about {LIFT:g} semitone{'' if LIFT == 1 else 's'} higher; let them open a little without pushing. " if LIFT > 0 else "The choruses sit where the verses do; let the band lift them, not the voice. ") +
       f"The bridge sits low ({nm(min(n['midi'] for n in LEAD if n['sec'] == 'Bridge'))} to {nm(max(n['midi'] for n in LEAD if n['sec'] == 'Bridge'))}) while the band opens up around her: stay small there. The title line ends each chorus: " + " ".join(nm(n["midi"]) for n in title_line) + ". " + top_desc(REC, nm), "",
       f"**Harmony voice.** The last chorus only, with her in her rhythm and on her words, from its first line until “Three, and then two” (bar {bare_from}), where she is left alone. {round(100 * third_to_fifth)} in 100 of its notes sit a third to a fifth below her. Range {hr[0]} to {hr[1]}" + ("; the notes under G3 want a low alto, or take them up an octave" if min(n["midi"] for n in HARM) < 55 else "") + ". Keep it soft and under her.", "",
       f"**Acoustic guitar.** Fingerpicked eighths from bar 1 to the end: the thumb on the chord's root (the fifth when a chord holds the whole bar), the fingers on its third and fifth. Where a chord tone would sit a step from the note she sings, pick another tone of the chord. The last bar: let the chord ring. Range {gr[0]} to {gr[1]}." + (" " + KI.capo_line([c for b_ in REC['bars'] for c in (b_['chord'], b_['chord2'])]) + "." if KI.CAPO else ""), "",
       f"**Cello.** From verse 2 (bar {cello_from}) through the last chorus: the chord's root, held a bar, or a half bar where the chord changes. Long, even bows; no swell. Range {cr[0]} to {cr[1]}.", "",
       f"**Strings.** The bridge (from bar {strings_from}) and the last chorus until bar {bare_from - 1}: the chord held high and soft. Notes a half step from the singer are left out. Range {sr[0]} to {sr[1]}.", "",
       f"**Bass.** The bridge and the last chorus, until “Three, and then two”: quarter notes, roots and fifths, with passing notes into the next root. Range {br[0]} to {br[1]}. Under the cello, never over it.", "",
       "## For the singer", "",
       f"Breathe between lines: her phrases run {PH[len(PH) // 2]:.1f} seconds at the median, the longest stretch without half a beat's rest {PH[-1]:.1f} seconds. " +
       (f"Lines that end on a long note (in verse 1: {', '.join('“' + w + '”' for w in HELD)}) want to be held to their length and released, not clipped. " if HELD else "") +
       "Do not act the grief: the words carry it. The verses are reported, the choruses are the plea. In the last chorus the band falls away at “Three, and then two”: sing those words like a knock, and leave the last line almost spoken.", "",
       "## The arrangement", "",
       "The song opens up while the door stays shut. The guitar is alone with her through the first verse and chorus. A cello comes in under the second verse. "
       "The bridge is the peak: strings and bass arrive while she sings at her lowest, so the size is in the room, not in her voice. The third verse drops back to guitar and cello, the vigil. "
       "The last chorus brings everything back with a harmony voice, then at “Three, and then two” it all falls away and she finishes with the guitar alone; the outro is the guitar by itself. No drums anywhere.", ""]
md += ["## Production notes", "", "### Lyric sheet", ""]
cur = None
for k in lines:
    if k[0] != cur: cur = k[0]; md += ["", f"**{cur}**", ""]
    md.append(f"{line_info(k)['slot']}: {TEXT.get(k, '')}  ")
md += ["", PB, "### Producer one-sheet", "",
       "**Emotional target.** A sister talking through a locked door to a brother she cannot reach, with no anger left, only patience. It should break the listener's heart by staying calm: the door never opens, and she will be back.", "",
       "**References.**", "",
       "- Neil Young, “The Needle and the Damage Done” (Harvest, 1972): take the plainness, one voice and one guitar watching and telling, recorded live, short, without a sermon.",
       "- Brandi Carlile, “Sugartooth” (By the Way, I Forgive You, 2018): take how an addiction is told from outside, through small observed details, and how the band grows under the voice.",
       "- Lucinda Williams, “Sweet Old World” (Sweet Old World, 1992): take a woman's voice speaking straight to the one she is losing, an inventory of ordinary, tender things.", "",
       "**Dynamic arc.**", "", "| Section | Bars | Level | What changes |", "|---|---|---|---|"]
for s, nb, st, _, _ in REC["plan"]: md.append(f"| {s} | {st // BAR + 1}–{st // BAR + nb} | {LEVEL_WORD(REC['level'][s])} | {SHORTW[s]} |")
md += ["", "**Non-negotiables.**", "",
       "- ♩ = 80, steady; no push anywhere.", "- No drums.", f"- The bridge is the band's peak, not the singer's: she stays low and plain.",
       f"- At “Three, and then two” (bar {bare_from}) everything but the guitar stops.", "- The harmony voice only in the last chorus, under her.", f"- The last chorus ends on {_lb}, unresolved; only the guitar's outro comes home, to {chord_at_bar(len(REC['bars']))[-1]}.", "",
       "**Mix priorities.** The voice in front, dry and very close, as if through wood. The guitar just left of centre, under her. The cello left, the strings right and back. Bass felt more than heard. Nothing may cover the words; nothing may swell over the last two lines.", "",
       PB, "### Production brief", "",
       f"**The song.** “{REC['title']}”, words and music by Jason Bryant: a ballad in {KI.KEYSTR} at ♩ = 80, {mm}:{ss:02d}, for an alto with fingerpicked acoustic guitar, cello, strings, bass and a harmony voice.", "",
       "**References** (checked): Neil Young, “The Needle and the Damage Done” (1972); Brandi Carlile, “Sugartooth” (2018); Lucinda Williams, “Sweet Old World” (1992). What to take from each is on the one-sheet.", "",
       "**Non-negotiables.** As on the one-sheet.", "",
       "### Session notes", "",
       f"- Tempo and click: ♩ = 80 throughout, 4/4. The voice enters in bar {min(bar(n['on']) for n in LEAD)}.",
       f"- Key: {KI.KEYSTR}" + (f"; guitar {KI.CAPO}" if KI.CAPO else "") + ". Chords bar by bar are on the number chart and above the lead sheet.",
       f"- Range: voice {rng[0]} to {rng[1]}; harmony {hr[0]} to {hr[1]}.",
       "- Tracking: guitar and voice together if the singer can, for the live feel of the reference; then cello, strings, bass, and the harmony voice last.",
       "- Blend and panning: voice centre; guitar slightly left; cello left; strings right; harmony slightly right; bass centre.",
       "- Every part can be played by one player at once; the strings are one section, or one player overdubbed.", "",
       "### Score and parts", "",
       "- Lead sheet (voice, lyrics, chord symbols), PDF and MusicXML.", "- Full score (voice, harmony voice, acoustic guitar, strings, cello, bass), PDF and MusicXML.",
       "- Parts, one PDF: voice, harmony voice, acoustic guitar, cello, strings, bass; each with a note on its role, rehearsal marks and chord symbols.",
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
