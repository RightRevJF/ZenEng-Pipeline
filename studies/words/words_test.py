"""How songs set English words: stress and pitch, stress and the beat, function words on downbeats, the line's last stress, and vowels on
high and held notes by singer sex. Reads sung_syllables.json (parse_words.py); stress for Billboard from the CMU dictionary (pronouncing),
monosyllabic function words unstressed as in Luthier's Window 25; RollingStone stress from its **stress spine. 4/4 songs only.
Also reads the lead sheets of songs 54 and 55 (MusicXML) for the same measures."""
import json, os, re, collections, numpy as np, pronouncing
HERE = os.path.dirname(os.path.abspath(__file__))
FUNC = set("""a an the and or but nor so yet if as at by for from in into of off on onto out over to up upon with than then that this these those
i me my mine you your yours he him his she her hers it its we us our they them their who whom whose which what when where why how
is am are was were be been being do does did have has had will would shall should can could may might must not no oh ooh yeah la na hey
just there here all some""".split())
OPEN = {"AA", "AE", "AO", "AW", "AY", "EH", "EY", "ER"}; CLOSE = {"IY", "IH", "UW", "UH", "OW", "OY"}
def vclass(v, st):
    if v == "AH": return "open" if st else "reduced"
    if v == "IH" and not st: return "reduced"
    return "open" if v in OPEN else "close" if v in CLOSE else None
def lookup(word, nsyl):
    w = re.sub(r"[^a-z']", "", word.lower())
    cands = [w, w.replace("'", ""), w.rstrip("'") + ("g" if w.rstrip("'").endswith("in") else ""), re.sub(r"in'?$", "ing", w)]
    for c in cands:
        for ph in pronouncing.phones_for_word(c):
            vs = [(re.sub(r"\d", "", p), int(p[-1])) for p in ph.split() if p[-1].isdigit()]
            if len(vs) == nsyl: return vs
    return None
def words_of(notes):
    """Group syllables into words: 'sit-' '-tin' -> one word of two syllables."""
    ws = []; cur = []
    for i, n in enumerate(notes):
        cur.append(i)
        if not n["syl"].endswith("-"):
            ws.append(cur); cur = []
    if cur: ws.append(cur)
    return ws
def annotate(notes, rs):
    for w in words_of(notes):
        text = "".join(notes[i]["syl"].strip("-") for i in w)
        vs = lookup(text, len(w))
        for k, i in enumerate(w):
            n = notes[i]; n["word"] = text; n["nsyl"] = len(w); n["wi"] = k
            if rs:
                n["st"] = n["stress"]
                if len(w) == 1 and text.lower().strip("'") in FUNC: n["st"] = 0
            else:
                n["st"] = None
                if len(w) == 1: n["st"] = 0 if text.lower().strip("'") in FUNC else 1
                elif vs: n["st"] = vs[k][1]
            n["vowel"] = vclass(vs[k][0], (n["st"] or 0) > 0) if vs else None
def mclass(pos):
    if abs(pos) < 1e-6: return "beat 1"
    if abs(pos - 2) < 1e-6: return "beat 3"
    if abs(pos - round(pos)) < 1e-6: return "beats 2 and 4"
    if abs(pos * 2 - round(pos * 2)) < 1e-6: return "offbeat eighth"
    return "sixteenth or finer"
SEX = {}
for l in open("/home/claude/data/cocopops/CoCoPops/Billboard/SingerSex.txt"):
    a, s = l.rstrip("\n").split("\t")[:2]; SEX[re.sub(r"[^A-Za-z0-9]", "", a).lower()] = s
def analyse(songs):
    R = collections.defaultdict(collections.Counter); per = collections.defaultdict(list)
    for name, notes in songs.items():
        rs = name.startswith("RS:")
        notes = [n for n in notes if n["meter"] == [4, 4] and n["p"] is not None]
        if len(notes) < 40: continue
        annotate(notes, rs); corp = "RS" if rs else "BB"
        sex = SEX.get(name.split(":")[1].split("_")[0].lower()) if not rs else None
        ps = [n["p"] for n in notes]; top10 = np.percentile(ps, 90); medq = np.median([n["q"] for n in notes if n["q"]])
        # M1: word-internal pitch of the primary stress against the word's unstressed syllables
        for w in words_of(notes):
            if len(w) < 2: continue
            sts = [notes[i]["st"] for i in w]
            if 1 not in sts or 0 not in sts: continue
            pp = notes[w[sts.index(1)]]["p"]; pu = np.mean([notes[i]["p"] for i, s in zip(w, sts) if s == 0])
            R[(corp, "word_pitch")]["higher" if pp > pu else "same" if pp == pu else "lower"] += 1
            first = sts.index(1) == 0
            R[(corp, "word_pitch_" + ("stress first" if first else "stress later"))]["higher" if pp > pu else "same" if pp == pu else "lower"] += 1
            q1 = notes[w[sts.index(1)]]["q"]; qu = np.mean([notes[i]["q"] for i, s in zip(w, sts) if s == 0])
            if not rs: R[(corp, "word_length")]["longer" if q1 > qu else "same" if q1 == qu else "shorter"] += 1
        # M1b: local peaks (higher than both neighbours), stressed vs unstressed
        for a, n, b in zip(notes, notes[1:], notes[2:]):
            if n["st"] is None: continue
            k = "stressed" if n["st"] > 0 else "unstressed"
            R[(corp, "peak_" + k)]["peak" if n["p"] > a["p"] and n["p"] > b["p"] else "not"] += 1
        # M2: metrical position by stress
        for n in notes:
            if n["st"] is None: continue
            R[(corp, "pos_" + ("stressed" if n["st"] > 0 else "unstressed"))][mclass(n["pos"])] += 1
        # M3: function words on beat 1 and on beats 1 or 3
        for n in notes:
            if n["nsyl"] == 1:
                fw = n["word"].lower().strip("'") in FUNC
                R[(corp, "beat1_word")]["function" if fw else "content"] += mclass(n["pos"]) == "beat 1"
                R[(corp, "strong_word")]["function" if fw else "content"] += mclass(n["pos"]) in ("beat 1", "beat 3")
                R[(corp, "all_mono")]["function" if fw else "content"] += 1
        # M4: the line's last stressed syllable (Billboard lines)
        if not rs:
            lines = []; cur = []
            for n in notes:
                if n["line_start"] and cur: lines.append(cur); cur = []
                cur.append(n)
            if cur: lines.append(cur)
            for L in lines:
                st = [n for n in L if n["st"] and n["st"] > 0]
                if len(st) < 3: continue
                last = st[-1]; others = st[:-1]; mq = np.mean([n["q"] for n in L]); mp = np.mean([n["p"] for n in L])
                R[("BB", "last_stress_pos")][mclass(last["pos"])] += 1
                for o in others: R[("BB", "other_stress_pos")][mclass(o["pos"])] += 1
                R[("BB", "last_stress_len")]["longer than line mean" if last["q"] > mq else "not"] += 1
                R[("BB", "other_stress_len")]["longer than line mean" if 0 else "x"] += 0
                for o in others: R[("BB", "other_stress_len")]["longer than line mean" if o["q"] > mq else "not"] += 1
                R[("BB", "last_stress_pitch")]["above line mean" if last["p"] > mp else "not"] += 1
                for o in others: R[("BB", "other_stress_pitch")]["above line mean" if o["p"] > mp else "not"] += 1
                if last["rhyme"] or L[-1]["rhyme"]: R[("BB", "last_stress_is_rhyme_word")]["yes" if last is L[-1] or last["word"] == L[-1]["word"] else "no"] += 1
        # M5: vowels on high and held notes, by singer sex (Billboard)
        if not rs and sex in ("M", "F"):
            hi_abs = 64 if sex == "M" else 72
            for n in notes:
                v = n["vowel"]
                if v is None: continue
                R[(sex, "vowel_all")][v] += 1
                if n["p"] >= top10: R[(sex, "vowel_top10")][v] += 1
                if n["p"] >= hi_abs: R[(sex, f"vowel_abs_{hi_abs}")][v] += 1
                if n["q"] >= 1.0: R[(sex, "vowel_held")][v] += 1
                if n["q"] >= 1.0 and n["p"] >= top10: R[(sex, "vowel_held_top10")][v] += 1
            per[sex].append(dict(name=name, median=float(np.median(ps)), top=float(max(ps))))
    return R, per
def pct(c):
    t = sum(c.values()); return {k: round(v / t, 3) for k, v in sorted(c.items(), key=lambda kv: -kv[1])} | {"n": t}
def engine_song(xml):
    from music21 import converter, note
    sc = converter.parse(xml); part = sc.parts[0]; out = []
    for n in part.recurse().getElementsByClass(note.Note):
        if n.tie is not None and n.tie.type in ("stop", "continue"):
            if out: out[-1]["q"] += float(n.quarterLength)
            continue
        if not n.lyrics: continue
        ly = n.lyrics[0]; t = ly.text or ""
        syl = ("-" if ly.syllabic in ("middle", "end") else "") + t + ("-" if ly.syllabic in ("begin", "middle") else "")
        m = n.getContextByClass("Measure")
        out.append(dict(bar=m.number if m else 0, pos=round(float(n.offset), 4), q=float(n.quarterLength), p=n.pitch.midi, syl=syl,
                        stress=None, meter=[4, 4], label=None, line_start=False, rhyme=None))
    return out
if __name__ == "__main__":
    songs = json.load(open(os.path.join(HERE, "sung_syllables.json")))
    R, per = analyse(songs)
    out = {f"{a}|{b}": pct(c) for (a, b), c in R.items() if sum(c.values())}
    for lab in ("BB", "RS"):
        for k in ("beat1_word", "strong_word"):
            a = R[(lab, k)]; t = R[(lab, "all_mono")]
            out[f"{lab}|{k}_rate"] = {kk: round(a[kk] / t[kk], 3) for kk in ("function", "content")}
    out["singers"] = {s: dict(n=len(v), median_of_medians=float(np.median([x["median"] for x in v])), median_top=float(np.median([x["top"] for x in v]))) for s, v in per.items()}
    eng = {}
    for lab, path in (("song 54", "/home/claude/p64/out/The Man Mama Prayed I'd Be - lead sheet.musicxml"),
                      ("song 55", "/home/claude/p65/out/Your Yard Man - lead sheet.musicxml")):
        Re, _ = analyse({"BB:" + lab: engine_song(path)})
        eng[lab] = {b: pct(c) for (a, b), c in Re.items() if sum(c.values())}
        for k in ("beat1_word", "strong_word"):
            a = Re[("BB", k)]; t = Re[("BB", "all_mono")]
            eng[lab][k + "_rate"] = {kk: round(a[kk] / t[kk], 3) if t[kk] else None for kk in ("function", "content")}
    out["engine"] = eng
    json.dump(out, open(os.path.join(HERE, "words_results.json"), "w"), indent=1)
    for k, v in out.items():
        if k != "engine": print(k, v)
    for lab, d in eng.items():
        print(lab, {k: d.get(k) for k in ("word_pitch", "peak_stressed", "peak_unstressed", "pos_stressed", "pos_unstressed", "beat1_word_rate", "strong_word_rate", "word_length")})
