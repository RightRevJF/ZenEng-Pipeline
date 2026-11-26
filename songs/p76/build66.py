"""'They Did the Right Thing' (song 66): the song record for the documents, read from songs/p76/lyric66_d.hand.song.json (Luthier v52, the design run in A minor, with the writer's design notes, hand66.py) and
nothing else. Writes song_record.pkl in the form the document scripts read: bars, half-bar chords, plan, the sung notes with their syllables,
the harmony voice, and the band. No sung note is changed; syllables are spelled from the locked lyric (pyphen, fitted to the engine's count).
The band is the writer's arrangement (intake: fingerpicked acoustic guitar that opens up; the door stays shut), written here from the engine's
own chords, bass line and harmony voice: the guitar picks the engine's chord tones; the cello takes the engine's chord roots; the strings hold
its chord tones; the bass is the engine's bass line where the bass plays; the harmony voice is the engine's, kept where it sings."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo66 as KI
import json, pickle, re, os, collections
import pyphen
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "lyric66_d.hand.song.json"))); L = json.load(open(os.path.join(HERE, "lyric66.json")))
EDITION = " (first edition)"           # the design run in A minor (design66.py) with the writer's design notes (hand66.py)
BAR = R["bar"]; QBPM = R["bpm"]; DIC = pyphen.Pyphen(lang="en_US")
KIND = {"intro": "Intro", "verse": "Verse", "chorus": "Chorus", "solo": "Turn", "bridge": "Bridge", "outro": "Outro", "pre": "Pre-chorus"}
bars, plan, b = [], [], 0
for sec, kind, nb in R["form"]:
    plan.append((sec, nb, b * BAR, ["4/4"] * nb, sec))
    for k in range(nb):
        ch = R["chords"][sec][k].split(); rn = R["roman"][sec][k].split()
        bars.append(dict(sec=sec, kind=KIND[kind], k=k, n=nb, b=b + k, meter="4/4", start=(b + k) * BAR, len=BAR, chord=ch[0], chord2=ch[-1],
                         roman=rn[0], roman2=rn[-1], beats4=ch if len(ch) == 4 else ([ch[0], ch[0], ch[1], ch[2]] if len(ch) == 3 else None), beatchords=list(zip(*[(ch * 4)[:4] if len(ch) == 1 else [ch[0], ch[0], ch[1], ch[1]] if len(ch) == 2 else [ch[0], ch[0], ch[1], ch[2]] if len(ch) == 3 else ch, (rn * 4)[:4] if len(rn) == 1 else [rn[0], rn[0], rn[1], rn[1]] if len(rn) == 2 else [rn[0], rn[0], rn[1], rn[2]] if len(rn) == 3 else rn])), qbpm=QBPM, key=KI.KEYSTR, movement=sec, stop=False, chord_list=ch))
    b += nb
chords2 = [x for bb in bars for x in (bb["chord"], bb["chord2"])]
# the locked lyric, word by word, for spelling and capitals
words_by_line = {}
for sec, lines in L["sections"]:
    for i, line in enumerate(lines): words_by_line[(sec, i)] = re.findall(r"[A-Za-z’']+[,;:.!?—]*", line.replace("’", "'"))
def spell(word, n):
    """the word's syllables, n of them, from pyphen; split or merged to fit the engine's count."""
    core = re.sub(r"[^A-Za-z']", "", word); tail = word[len(core):] if word.startswith(core) else ""
    SPECIAL = {"TV's": ["T", "V's"], "TV": ["T", "V"]}
    if core in SPECIAL and n == len(SPECIAL[core]): return SPECIAL[core][:-1] + [SPECIAL[core][-1] + tail]
    parts = DIC.inserted(core).split("-") if n > 1 else [core]
    while len(parts) < n:
        j = max(range(len(parts)), key=lambda j: len(parts[j])); w = parts[j]
        m = next((k for k in range(1, len(w)) if w[k - 1] in "aeiouy" and w[k] not in "aeiouy"), len(w) // 2) if len(w) > 1 else 1
        parts[j:j + 1] = [w[:m + 1] if m + 1 < len(w) else w[:m], w[m + 1:] if m + 1 < len(w) else w[m:]]
        parts = [p for p in parts if p] or [core]
        if len(parts) < n and all(len(p) <= 1 for p in parts): parts += [""] * (n - len(parts))
    while len(parts) > n: parts[-2:] = [parts[-2] + parts[-1]]
    parts[-1] += tail; return parts
notes = sorted(R["melody"]["notes"], key=lambda n: n["on"]); lead = []
lines = collections.OrderedDict()
for n in notes: lines.setdefault((n["sec"], n["line"]), []).append(n)
for (sec, i), ns in lines.items():
    src_sec = sec; sy = [n for n in ns if n["text"] != ""]
    locked = words_by_line.get((sec, i), []); words = []; k = 0; wi = 0          # one word = a run of the engine's syllables with the same text (twice in the locked line = split evenly)
    while k < len(sy):
        j = k
        while j < len(sy) and sy[j]["text"] == sy[k]["text"]: j += 1
        reps = 1
        while wi + reps < len(locked) and re.sub(r"[^a-z']", "", locked[wi + reps].lower()) == sy[k]["text"]: reps += 1
        size = max(1, (j - k) // reps) if reps > 1 and (j - k) % reps == 0 else j - k
        for r_ in range(0, j - k, size): words.append((sy[k]["text"], sy[k + r_:k + r_ + size])); wi += 1
        k = j
    for wi, (w, syls) in enumerate(words):
        lw = locked[wi] if wi < len(locked) and re.sub(r"[^a-z']", "", locked[wi].lower()) == w else w
        if lw == w and w in ("i", "i'm", "i'll", "i'd", "i've"): lw = w.capitalize()
        pieces = spell(lw, len(syls))
        for k, n in enumerate(syls): n["_syl"] = (wi, k); n["_txt"] = pieces[k]; n["_hyph"] = k < len(syls) - 1
    last = None
    for n in ns:
        if n["text"] != "": last = n
        d = dict(on=n["on"], on_engine=n["on"], dur=n["dur"], midi=n["midi"], engine_midi=n["midi"], sec=sec, line=i, syl=(last or n)["_syl"][0] * 10 + (last or n)["_syl"][1],
                 first=n["text"] != "", text=(last or n)["_txt"], hyph=(last or n)["_hyph"], stress=n["stress"], role=sec.split()[0].lower(), singer="him")
        lead.append(d)
by_on = {n["on"]: n for n in lead if n["first"]}; harm = []
for e in R["parts"]["harmony"]:
    ln = by_on.get(e["on"])
    if ln is None:                                               # a held or melisma note of the harmony: the lead's note sounding there
        cand = [n for n in lead if n["on"] <= e["on"] < n["on"] + n["dur"]]; ln = cand[-1] if cand else None
        if ln is None: continue                                       # a harmony note where the hand edits left the lead resting (the knock line, which the harmony does not sing)
        harm.append(dict(on=e["on"], on_engine=e["on"], dur=e["dur"], midi=e["p"][0], engine_midi=e["p"][0], sec=ln["sec"], line=ln["line"], syl=ln["syl"], first=False, text=ln["text"], hyph=ln["hyph"], stress=False, role="harmony", singer="harmony"))
    else:
        harm.append(dict(on=e["on"], on_engine=e["on"], dur=e["dur"], midi=e["p"][0], engine_midi=e["p"][0], sec=ln["sec"], line=ln["line"], syl=ln["syl"], first=True, text=ln["text"], hyph=ln["hyph"], stress=ln["stress"], role="harmony", singer="harmony"))
# the harmony voice above the lead in two places ("Still", the chorus's sixth line, chorus 1 and the final chorus): an octave down, a third under the lead
RECAST = []
for n in harm:
    ld = [x["midi"] for x in lead if x["on"] <= n["on"] < x["on"] + x["dur"]]
    if ld and n["midi"] > max(ld): RECAST.append((n["on"], n["midi"])); n["midi"] -= 12; n["recast"] = "an octave down: the engine's note sat over the lead"
# ---- the band: the engine's own parts (guitar strums, bass, drums), with the writer's design notes already laid on them (hand66.py)
P = R["parts"]; LEV = R["levels"]
FORM = []; _b = 0
for sec, kind, nb in R["form"]: FORM.append((sec, kind, _b, _b + nb)); _b += nb
def sec_of(bar_i): return next(f for f in FORM if f[2] <= bar_i < f[3])
def lev(t): return LEV[sec_of(t // BAR)[0]]
TAG0 = next(f[2] for f in FORM if f[0] == "Tag") * BAR; END = len(bars) * BAR
def fade(t): return 1.0 if t < TAG0 else max(0.35, 1.0 - 0.6 * (t - TAG0) / (END - TAG0))       # the tag and outro fade (design note 5)
def scaled(e, k):
    sec = sec_of(e["on"] // BAR)[0]
    s = 0.8 if sec == "Bridge" else 1.12 if sec == "Chorus 3" else 1.0                           # the bridge the lowest level (design note 2); the final chorus the top (9.12)
    return dict(on=e["on"], dur=e["dur"], p=list(e["p"]), vel=max(20, int(round(e["vel"] * s * fade(e["on"])))), art="")
parts = {"guitar": [scaled(e, "guitar") for e in P["chords"]], "bass": [scaled(e, "bass") for e in P["bass"]], "drums": [scaled(e, "drums") for e in P["drums"]]}
C3 = next(f[2] for f in FORM if f[0] == "Chorus 3") * BAR
parts["drums"].append(dict(on=C3, dur=3, p=[49], vel=104, art=""))                               # the full band back on the downbeat: a crash (design note 4)
parts["drums"].sort(key=lambda e: e["on"])
end = len(bars) * BAR; seconds = end / 12 * 60.0 / QBPM
REC = dict(title=R["title"], file_title=R["title"] + EDITION, edition=EDITION.strip(" ()"), nbars=len(bars), bars=bars, chords2=chords2, plan=plan, lead=lead, harm=harm, parts=parts, slot="twelfth of a beat",
           qbpm=QBPM, feel="dark indie folk-rock, q = 72, 4/4, guitar-led", seconds=seconds, end=end, level=R["levels"], source="songs/p76/lyric66_d.hand.song.json", pick=R["melody"]["pick"],
           text={s: lines for s, lines in L["sections"]}, form=R["form"], hand=R["hand_edits"])
pickle.dump(REC, open(os.path.join(HERE, "song_record.pkl"), "wb"))
if __name__ == "__main__":
    print(len(bars), "bars,", len(lead), "sung notes,", len(harm), "harmony notes,", round(seconds, 1), "s")
    for (sec, i) in list(lines)[:3] + [("Bridge", 3), ("Chorus 3", 7)]:
        print(sec, i, " ".join(n["text"] + ("-" if n["hyph"] else "") for n in lead if n["sec"] == sec and n["line"] == i and n["first"]))
