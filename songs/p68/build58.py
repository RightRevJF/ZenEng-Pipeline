"""'Same Time Tomorrow' (song 58): the song record for the documents, read from songs/p68/lyric58.song.json (Luthier v22, song_from_lyric.py) and
nothing else. Writes song_record.pkl in the form the p65 document scripts read: bars, half-bar chords, plan, the sung notes with their syllables,
the harmony voice, the band's parts. No note is changed; syllables are spelled from the locked lyric (pyphen, fitted to the engine's count)."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo58 as KI
import json, pickle, re, os, collections
import pyphen
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "lyric58.song.json"))); L = json.load(open(os.path.join(HERE, "lyric58.json")))
EDITION = " (fourteenth edition)"          # the first edition from the v22 record (commit 9ef68b2), the second from v24 (160e1ca), the third from v25 (686cd39), the fourth from v26 (e50969d, key A), the fifth from v27 (0328845, key B), the sixth from v28 (4dd66b3), the seventh from v29 (edda7b7), the eighth from v30 (1d7f174), the ninth from v31 (d334171, key D), the tenth from v32 (271e03a, key E), the eleventh from v33 (c104201, key E); none from v34 (the hold-out cycle), the twelfth from v35 (85a62b1, key A); the thirteenth from v36 (14f7eeb, key E); none from v37 (merged with v38); this one from the v37 record, which v38 leaves byte for byte (key A)
BAR = R["bar"]; QBPM = R["bpm"]; DIC = pyphen.Pyphen(lang="en_US")
KIND = {"intro": "Intro", "verse": "Verse", "chorus": "Chorus", "solo": "Turn", "bridge": "Bridge", "outro": "Outro"}
bars, plan, b = [], [], 0
for sec, kind, nb in R["form"]:
    plan.append((sec, nb, b * BAR, ["4/4"] * nb, sec))
    for k in range(nb):
        ch = R["chords"][sec][k].split(); rn = R["roman"][sec][k].split()
        bars.append(dict(sec=sec, kind=KIND[kind], k=k, n=nb, b=b + k, meter="4/4", start=(b + k) * BAR, len=BAR, chord=ch[0], chord2=ch[-1],
                         roman=rn[0], roman2=rn[-1], beats4=ch if len(ch) == 4 else None, qbpm=QBPM, key=KI.KEYSTR, movement=sec, stop=False))
    b += nb
chords2 = [x for bb in bars for x in (bb["chord"], bb["chord2"])]
# the locked lyric, word by word, for spelling and capitals
words_by_line = {}
for sec, lines in L["sections"]:
    for i, line in enumerate(lines): words_by_line[(sec, i)] = re.findall(r"[A-Za-z’']+[,;:.!?—]*", line.replace("’", "'"))
def spell(word, n):
    """the word's syllables, n of them, from pyphen; split or merged to fit the engine's count."""
    core = re.sub(r"[^A-Za-z']", "", word); tail = word[len(core):] if word.startswith(core) else ""
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
        harm.append(dict(on=e["on"], on_engine=e["on"], dur=e["dur"], midi=e["p"][0], engine_midi=e["p"][0], sec=ln["sec"], line=ln["line"], syl=ln["syl"], first=False, text=ln["text"], hyph=ln["hyph"], stress=False, role="harmony", singer="harmony"))
    else:
        harm.append(dict(on=e["on"], on_engine=e["on"], dur=e["dur"], midi=e["p"][0], engine_midi=e["p"][0], sec=ln["sec"], line=ln["line"], syl=ln["syl"], first=True, text=ln["text"], hyph=ln["hyph"], stress=ln["stress"], role="harmony", singer="harmony"))
parts = {"guitar": [dict(e, art="") for e in R["parts"]["chords"]], "bass": [dict(e, art="") for e in R["parts"]["bass"]], "drums": [dict(e, art="") for e in R["parts"]["drums"]]}
end = len(bars) * BAR; seconds = end / 12 * 60.0 / QBPM
REC = dict(title=R["title"], file_title=R["title"] + EDITION, edition=EDITION.strip(" ()"), nbars=len(bars), bars=bars, chords2=chords2, plan=plan, lead=lead, harm=harm, parts=parts, slot="twelfth of a beat",
           qbpm=QBPM, feel="a folk ballad, q = 84, 4/4", seconds=seconds, end=end, level=R["levels"], source="songs/p68/lyric58.song.json", pick=R["melody"]["pick"],
           text={s: lines for s, lines in L["sections"]})
pickle.dump(REC, open(os.path.join(HERE, "song_record.pkl"), "wb"))
if __name__ == "__main__":
    print(len(bars), "bars,", len(lead), "sung notes,", len(harm), "harmony notes,", round(seconds, 1), "s")
    for (sec, i) in list(lines)[:3] + [("Bridge", 3)]:
        print(sec, i, " ".join(n["text"] + ("-" if n["hyph"] else "") for n in lead if n["sec"] == sec and n["line"] == i and n["first"]))
