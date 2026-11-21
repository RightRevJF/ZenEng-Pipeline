"""'This Side of the Door' (song 61): the song record for the documents, read from songs/p71/lyric61.hand.song.json (Luthier v44, song_from_lyric.py) and
nothing else. Writes song_record.pkl in the form the document scripts read: bars, half-bar chords, plan, the sung notes with their syllables,
the harmony voice, and the band. No sung note is changed; syllables are spelled from the locked lyric (pyphen, fitted to the engine's count).
The band is the writer's arrangement (intake: fingerpicked acoustic guitar that opens up; the door stays shut), written here from the engine's
own chords, bass line and harmony voice: the guitar picks the engine's chord tones; the cello takes the engine's chord roots; the strings hold
its chord tones; the bass is the engine's bass line where the bass plays; the harmony voice is the engine's, kept where it sings."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo61 as KI
import json, pickle, re, os, collections
import pyphen
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "lyric61.hand.song.json"))); L = json.load(open(os.path.join(HERE, "lyric61.json")))
EDITION = " (second edition)"          # the first edition from the v44 record (main at 3b83673, 7ef0367); this one with the writer's hand edits (hand61.py)
BAR = R["bar"]; QBPM = R["bpm"]; DIC = pyphen.Pyphen(lang="en_US")
KIND = {"intro": "Intro", "verse": "Verse", "chorus": "Chorus", "solo": "Turn", "bridge": "Bridge", "outro": "Outro"}
bars, plan, b = [], [], 0
for sec, kind, nb in R["form"]:
    plan.append((sec, nb, b * BAR, ["4/4"] * nb, sec))
    for k in range(nb):
        ch = R["chords"][sec][k].split(); rn = R["roman"][sec][k].split()
        bars.append(dict(sec=sec, kind=KIND[kind], k=k, n=nb, b=b + k, meter="4/4", start=(b + k) * BAR, len=BAR, chord=ch[0], chord2=ch[-1],
                         roman=rn[0], roman2=rn[-1], beats4=ch if len(ch) == 4 else ([ch[0], ch[0], ch[1], ch[2]] if len(ch) == 3 else None), beatchords=list(zip(*[(ch * 4)[:4] if len(ch) == 1 else [ch[0], ch[0], ch[1], ch[1]] if len(ch) == 2 else [ch[0], ch[0], ch[1], ch[2]] if len(ch) == 3 else ch, (rn * 4)[:4] if len(rn) == 1 else [rn[0], rn[0], rn[1], rn[1]] if len(rn) == 2 else [rn[0], rn[0], rn[1], rn[2]] if len(rn) == 3 else rn])), qbpm=QBPM, key=KI.KEYSTR, movement=sec, stop=False))
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
# ---- the arrangement (intake): the guitar alone, then the cello (verse 2), the strings and the bass (the bridge, and the last chorus to its
# last two lines), the harmony voice in the last chorus to the same place; the last two lines and the outro the guitar alone again.
FORM = []; _b = 0
for sec, kind, nb in R["form"]: FORM.append((sec, kind, _b, _b + nb)); _b += nb
def sec_of(bar_i): return next(f for f in FORM if f[2] <= bar_i < f[3])
LC = next(f for f in FORM if f[0] == "Last Chorus"); _bare = min(n["on"] for n in lead if n["sec"] == "Last Chorus" and n["line"] == 6 and n["first"])
BARE_FROM = _bare // BAR                                      # the bar where "Three, and then two" begins in the last chorus: from here the guitar alone
TONES = R["chord_tones"]
def half_chords(bb):
    rn = R["roman"][bb["sec"]][bb["k"]].split(); ch = R["chords"][bb["sec"]][bb["k"]].split()
    return [(ch[0], rn[0]), (ch[-1], rn[-1])]
def place(pc, lo, hi):
    p = lo + (pc - lo) % 12
    return p if p < hi else p - 12
def sung_at(t0, t1): return [n["midi"] for n in lead if n["on"] < t1 and n["on"] + n["dur"] > t0]
def clash(p, sung): return any(abs(p - q) % 12 in (1, 2, 10, 11) for q in sung)
VEL = {"intro": 58, "verse": 62, "chorus": 70, "solo": 66, "bridge": 74, "outro": 56}
gtr, cello, strings, bass = [], [], [], []
for bb in bars:
    sec, kind, s0, s1 = sec_of(bb["b"]); hc = half_chords(bb); same = hc[0] == hc[1]; v = VEL[kind] - (8 if kind == "verse" and sec == "Verse 3" else 0)
    last_bar = bb["b"] == len(bars) - 1
    if last_bar:                                               # the last bar: the tonic chord let ring
        ch, rn = hc[0]; pcs = TONES[rn]; root = KI.root_pc(ch)
        gtr.append(dict(on=bb["start"], dur=BAR, p=sorted({place(root, 40, 52), place(pcs[2], 47, 59), place(root, 52, 64), place(pcs[0], 55, 67), place(pcs[1], 59, 71)}), vel=v, art=""))
        continue
    for h in range(2):
        t0 = bb["start"] + h * 24
        for e8 in range(4):
            t = t0 + e8 * 6; ch, rn = bb["beatchords"][(t - bb["start"]) // 12]; pcs = TONES[rn]; root = KI.root_pc(ch)
            fifth = next(x for x in pcs if (x - root) % 12 == 7); third = next(x for x in pcs if (x - root) % 12 in (3, 4))
            new_chord = e8 == 0 or bb["beatchords"][(t - bb["start"]) // 12] != bb["beatchords"][(t - 6 - bb["start"]) // 12]
            if e8 == 0 or (new_chord and e8 == 2): want = place(root if (h == 0 or not same or new_chord) else fifth, 40, 52)
            else: want = place(third, 55, 67) if e8 % 2 else place(fifth if fifth != third else root, 59, 71)
            p = want
            if want >= 55 and clash(p, sung_at(t, t + 6)):             # a step from the sung note: another tone of the chord, or none
                alt = [place(x, 55, 71) for x in pcs if not clash(place(x, 55, 71), sung_at(t, t + 6))]
                if not alt: continue
                p = min(alt, key=lambda q: abs(q - want))
            gtr.append(dict(on=t, dur=6, p=[p], vel=v + (6 if want < 55 else 0), art=""))
    cello_on = sec in ("Verse 2", "Bridge", "Verse 3") or (sec == "Last Chorus")
    if cello_on:
        for h, (ch, rn) in enumerate(hc[:1] if same else hc):
            cello.append(dict(on=bb["start"] + h * 24, dur=BAR if same else 24, p=[place(KI.root_pc(ch), 45, 57)], vel=v - 4, art=""))
    strings_on = sec == "Bridge" or (sec == "Last Chorus" and bb["b"] < BARE_FROM)
    if strings_on:
        for h, (ch, rn) in enumerate(hc[:1] if same else hc):
            t0 = bb["start"] + h * 24; t1 = t0 + (BAR if same else 24); sg = sung_at(t0, t1)
            ps = sorted(place(x, 67, 79) for x in TONES[rn]); ps = [p for p in ps if not any(abs(p - q) % 12 in (1, 11) for q in sg)]
            if ps: strings.append(dict(on=t0, dur=t1 - t0, p=ps, vel=v - 12, art=""))
for e in R["parts"]["bass"]:
    bi = e["on"] // BAR; sec = sec_of(bi)[0]
    if sec == "Bridge" or (sec == "Last Chorus" and bi < BARE_FROM): bass.append(dict(e, art=""))
harm = [n for n in harm if n["sec"] == "Last Chorus" and n["line"] < 6]
parts = {"guitar": gtr, "cello": cello, "strings": strings, "bass": bass}
end = len(bars) * BAR; seconds = end / 12 * 60.0 / QBPM
REC = dict(title=R["title"], file_title=R["title"] + EDITION, edition=EDITION.strip(" ()"), nbars=len(bars), bars=bars, chords2=chords2, plan=plan, lead=lead, harm=harm, parts=parts, slot="twelfth of a beat",
           qbpm=QBPM, feel="a ballad, q = 80, 4/4, fingerpicked acoustic guitar", seconds=seconds, end=end, level=R["levels"], source="songs/p71/lyric61.hand.song.json", pick=R["melody"]["pick"],
           text={s: lines for s, lines in L["sections"]})
pickle.dump(REC, open(os.path.join(HERE, "song_record.pkl"), "wb"))
if __name__ == "__main__":
    print(len(bars), "bars,", len(lead), "sung notes,", len(harm), "harmony notes,", round(seconds, 1), "s")
    for (sec, i) in list(lines)[:3] + [("Bridge", 3)]:
        print(sec, i, " ".join(n["text"] + ("-" if n["hyph"] else "") for n in lead if n["sec"] == sec and n["line"] == i and n["first"]))
