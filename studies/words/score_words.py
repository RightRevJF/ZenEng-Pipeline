"""Word-setting measures for scores with lyrics attached (PDMX, OpenEWLD): the measures of words_test.py and words_more.py, by
category and metre (4/4 and 3/4), English songs only (at least 85% of words found in the CMU dictionary).
4/4 strength: beat 1 = 4, beat 3 = 3, beats 2 and 4 = 2, offbeat eighths = 1, finer = 0. 3/4: beat 1 = 4, beats 2 and 3 = 2, offbeat
eighths = 1, finer = 0."""
import re, collections, numpy as np, pronouncing
from words_test import annotate, words_of, FUNC
from words_more import final_info, VOICED, VOICELESS
def english(notes):
    words = [w for w in ("".join(n["syl"].strip("-") for n in [notes[i] for i in w]) for w in words_of(notes))]
    words = [re.sub(r"[^a-z']", "", w.lower()) for w in words if re.search(r"[A-Za-z]", w)]
    if len(words) < 20: return False
    hit = sum(1 for w in words if pronouncing.phones_for_word(w.replace("'", "")) or pronouncing.phones_for_word(w))
    return hit / len(words) >= 0.85
def strength(pos, meter):
    if meter == [3, 4]:
        if abs(pos) < 1e-6: return 4
        if abs(pos - round(pos)) < 1e-6: return 2
        if abs(pos * 2 - round(pos * 2)) < 1e-6: return 1
        return 0
    if abs(pos) < 1e-6: return 4
    if abs(pos - 2) < 1e-6: return 3
    if abs(pos - round(pos)) < 1e-6: return 2
    if abs(pos * 2 - round(pos * 2)) < 1e-6: return 1
    return 0
def measure(notes, cat, R):
    if not notes: return False
    meters = collections.Counter(tuple(n["meter"]) for n in notes)
    m = list(meters.most_common(1)[0][0])
    if m not in ([4, 4], [3, 4]): return False
    notes = [n for n in notes if n["meter"] == m]
    if len(notes) < 30 or not english(notes): return False
    annotate(notes, False); key = (cat, "/".join(map(str, m)))
    med = np.median([n["q"] for n in notes if n["q"]]); top10 = np.percentile([n["p"] for n in notes], 90)
    wid = {}
    for k, w in enumerate(words_of(notes)):
        for i in w: wid[i] = k
    for i, n in enumerate(notes):
        if n["st"] is None: continue
        s = strength(n["pos"], m)
        if n["st"] == 0:
            R[key + ("weak on beat 1",)]["yes" if s == 4 else "no"] += 1
            if n["nsyl"] == 1: R[key + ("function words on beat 1",)]["yes" if s == 4 else "no"] += 1
        else: R[key + ("stress on beat 1",)]["yes" if s == 4 else "no"] += 1
        if i:
            a = notes[i - 1]
            if a["st"] is not None and (a["st"] > 0) != (n["st"] > 0):
                sa = strength(a["pos"], m)
                if sa != s and (n["bar"] - a["bar"]) * 4 + n["pos"] - a["pos"] <= 4:
                    opp = (n["st"] > 0 and s < sa) or (n["st"] == 0 and s > sa)
                    R[key + ("opposed inside words" if wid[i] == wid[i - 1] else "opposed across words",)]["yes" if opp else "no"] += 1
        if n["nsyl"] == 1 and n["word"].lower().strip("'") not in FUNC and n["q"]:
            fi = final_info(n["word"])
            if fi:
                if fi[1] in VOICED: R[key + ("voiced ending long",)]["yes" if n["q"] > med else "no"] += 1
                if fi[1] in VOICELESS: R[key + ("voiceless ending long",)]["yes" if n["q"] > med else "no"] += 1
        if n.get("vowel") and n["q"] >= 1.0 and n["p"] >= top10: R[key + ("vowel held top",)][n["vowel"]] += 1
        if n.get("vowel"): R[key + ("vowel all",)][n["vowel"]] += 1
    for w in words_of(notes):
        if len(w) < 2: continue
        sts = [notes[i]["st"] for i in w]
        if 1 not in sts or 0 not in sts: continue
        pp = notes[w[sts.index(1)]]["p"]; pu = np.mean([notes[i]["p"] for i, s in zip(w, sts) if s == 0])
        R[key + ("stress lower than its word",)]["yes" if pp < pu else "no"] += 1
    R[key + ("songs",)]["n"] += 1
    return True
def summarise(R):
    out = {}
    for k, c in sorted(R.items()):
        cat, met, meas = k
        t = sum(c.values())
        if meas == "songs": v = c["n"]
        elif meas.startswith("vowel"): v = {x: round(c[x] / t, 3) for x in ("open", "close", "reduced")} | {"n": t}
        else: v = dict(n=t, share=round(c["yes"] / t, 3))
        out.setdefault(f"{cat} {met}", {})[meas] = v
    return out
