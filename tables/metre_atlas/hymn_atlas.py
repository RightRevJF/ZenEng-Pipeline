"""The hymn part of the metre atlas, from the Open Hymnal Project (301 public-domain hymns, four voices, English words under the soprano).
  1. Hymn tunes by metre: the soprano's readings and their quartiles (the same readings as atlas_build.py), bar rhythms, onset weights.
  2. Four-part settings: how the alto, tenor and bass move against the soprano (with it, against it, holding), parallel fifths and octaves,
     how often an inner voice moves in notes shorter than the beat (passing notes), notes per bar in each voice.
  3. English stress against the bar (749.5): every stanza's syllables, their stress from the CMU Pronouncing Dictionary (monosyllables:
     content words stressed, function words not), and where in the bar they fall, by metre.
Writes tables/hymns.json."""
import json, collections, re, itertools
import numpy as np
import pronouncing
import hymn_parse as HP
import atlas_build as AB
BEATS = {"4/4": ([0, 24], [0, 12, 24, 36], 12), "3/4": ([0], [0, 12, 24], 12), "6/4": ([0, 36], [0, 36], 36), "3/2": ([0], [0, 24, 48], 24),
         "6/8": ([0, 18], [0, 18], 18), "2/4": ([0], [0, 12], 12), "2/2": ([0], [0, 24], 24)}
FUNCTION = set("a an the and but or nor for so yet of to in on at by with from up as is are was were be been am do does did has have had will shall would should may might can could must not no "
               "i me my mine we us our ours you your yours thou thee thy thine ye he him his she her hers it its they them their theirs this that these those who whom whose which what "
               "o oh if than then there where when while all each".split())
def word_stresses(word, nsyl):
    w = re.sub(r"[^a-z']", "", word.lower()).strip("'")
    if not w: return None
    if nsyl == 1: return [0 if w in FUNCTION else 1]
    for pr in pronouncing.phones_for_word(w) or pronouncing.phones_for_word(w.replace("'", "")):
        st = [int(c) for c in pronouncing.stresses(pr)]
        if len(st) == nsyl: return [1 if x == 1 else (2 if x == 2 else 0) for x in st]
    return None
def stanza_words(al):
    words = []; cur = []
    for x in al:
        cur.append(x)
        if not x["joins"]: words.append(cur); cur = []
    if cur: words.append(cur)
    return words
def readings_tune(ns, metre):
    barlen, beats, beat, _ = AB.METRES[metre]
    return AB.readings([[n["on"], n["dur"], n["p"]] for n in ns if n["p"] is not None], barlen, beats, beat)
def sounding(v, t):
    for n in v:
        if n["on"] <= t < n["on"] + n["dur"] and n["p"] is not None: return n["p"]
    return None
def motion(sop, other):
    sim = con = obl = par = 0; s = [n for n in sop if n["p"] is not None]
    for a, b in zip(s, s[1:]):
        ha, hb = sounding(other, a["on"]), sounding(other, b["on"])
        if ha is None or hb is None: continue
        dl, dh = b["p"] - a["p"], hb - ha
        if not dl and not dh: continue
        if dl and dh and (dl > 0) == (dh > 0):
            sim += 1
            if abs(hb - b["p"]) % 12 in (0, 7) and abs(ha - a["p"]) % 12 == abs(hb - b["p"]) % 12: par += 1
        elif dl and dh: con += 1
        else: obl += 1
    tot = max(1, sim + con + obl)
    return dict(similar=sim / tot, contrary=con / tot, oblique=obl / tot, parallels=par, moves=tot)
if __name__ == "__main__":
    H = [HP.parse(f) for f in HP.all_hymns()]
    H = [h for h in H if h["metre"] in BEATS and h["barlen"] and len(h["voices"].get("S1V1", [])) >= 8]
    by = collections.defaultdict(list)
    for h in H: by[h["metre"]].append(h)
    out = {"source": "Open Hymnal Project (github.com/mzealey/openhymnal), public domain", "hymns": len(H), "by_metre": {}}
    for metre, hs in sorted(by.items(), key=lambda x: -len(x[1])):
        R = [readings_tune(h["voices"]["S1V1"], metre) for h in hs]
        Q = {k: [float(np.percentile([r[k] for r in R], q)) for q in (25, 50, 75)] for k in R[0]}
        barlen = AB.METRES[metre][0]
        BAR = collections.Counter(); POS = collections.Counter()
        for h in hs:
            bars = collections.defaultdict(list)
            for n in h["voices"]["S1V1"]:
                if n["p"] is not None: bars[n["on"] // barlen].append(n["on"] % barlen); POS[n["on"] % barlen] += 1
            for v in bars.values(): BAR[tuple(v)] += 1
        # four-part motion
        M = {v: [] for v in ("S1V2", "S2V1", "S2V2")}; SHORT = {v: [] for v in ("S1V1", "S1V2", "S2V1", "S2V2")}; NPB = {v: [] for v in SHORT}
        beat = BEATS[metre][2]
        for h in hs:
            if not all(v in h["voices"] for v in SHORT): continue
            for v in M: M[v].append(motion(h["voices"]["S1V1"], h["voices"][v]))
            for v in SHORT:
                ns = [n for n in h["voices"][v] if n["p"] is not None]
                if ns:
                    SHORT[v].append(np.mean([n["dur"] < beat for n in ns]))
                    bars = (max(n["on"] for n in ns) // barlen) + 1; NPB[v].append(len(ns) / bars)
        def agg(L, k): return float(np.median([x[k] for x in L])) if L else None
        harmony = {v: dict(similar=agg(M[v], "similar"), contrary=agg(M[v], "contrary"), oblique=agg(M[v], "oblique"),
                            parallels_per_100_moves=float(100 * sum(x["parallels"] for x in M[v]) / max(1, sum(x["moves"] for x in M[v])))) for v in M}
        texture = {v: dict(notes_shorter_than_beat=float(np.median(SHORT[v])) if SHORT[v] else None, notes_a_bar=float(np.median(NPB[v])) if NPB[v] else None) for v in SHORT}
        # stress against the bar
        strong, beats_all, _ = BEATS[metre]
        S = collections.Counter(); n_words = n_skip = 0
        for h in hs:
            for k, al in h["stanzas"].items():
                for w in stanza_words(al):
                    text = "".join(x["syl"] for x in w); st = word_stresses(text, len(w))
                    if st is None: n_skip += 1; continue
                    n_words += 1
                    for x, s_ in zip(w, st):
                        pos = x["on"] % barlen
                        lvl = "downbeat" if pos == 0 else ("strong beat" if pos in strong else ("beat" if pos in beats_all else "off the beat"))
                        S[(["unstressed", "primary", "secondary"][s_], lvl)] += 1
        stress = {}
        for cls in ("primary", "secondary", "unstressed"):
            tot = sum(v for (c, l), v in S.items() if c == cls)
            stress[cls] = {l: round(S[(cls, l)] / tot, 3) for l in ("downbeat", "strong beat", "beat", "off the beat")} if tot else {}
            stress[cls]["syllables"] = tot
        out["by_metre"][metre] = dict(hymns=len(hs), readings_quartiles=Q, bar_rhythms=[[list(k), v] for k, v in BAR.most_common(15)], bars_total=sum(BAR.values()),
                                      onset_weights={str(k): round(v / sum(POS.values()), 4) for k, v in sorted(POS.items())}, harmony=harmony, texture=texture,
                                      stress=stress, words_scored=n_words, words_skipped=n_skip, examples=[h["path"].split("/")[-1] for h in hs[:6]])
        print(metre, len(hs), "hymns; words", n_words, "skipped", n_skip)
        print("  stress", stress); print("  harmony", {k: {a: round(b, 2) for a, b in v.items()} for k, v in harmony.items()})
        print("  texture", texture)
    json.dump(out, open("/home/claude/atlas/tables/hymns.json", "w"))
