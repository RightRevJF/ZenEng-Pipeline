"""Follow-ups from the further reading on setting words (4/4 songs; CoCoPops Billboard and Rolling Stone 200, songs 54 and 55):
1. Stress against metre as contours (after de Castro Arrazola 2018 and Hayes and Kaun 1996): for each pair of neighbouring syllables
   whose stress changes and whose metrical strength changes, do they move the same way? Rates of opposed moves by domain: inside a
   word, across a word boundary, and at a line's first pair (Billboard lines). Strength: beat 1 = 4, beat 3 = 3, beats 2 and 4 = 2,
   offbeat eighths = 1, finer = 0.
2. Allophonic length (Gilroy, Blumenfeld and Toivonen 2024): one-syllable content words ending in a voiced against a voiceless
   obstruent, and tense against lax vowels: note length against the song's median note."""
import json, os, re, collections, numpy as np, pronouncing
from words_test import annotate, words_of, engine_song, HERE, FUNC
VOICED = {"B", "D", "G", "V", "DH", "Z", "ZH", "JH"}; VOICELESS = {"P", "T", "K", "F", "TH", "S", "SH", "CH"}
TENSE = {"IY", "EY", "AA", "AO", "OW", "UW", "AY", "AW", "OY", "ER"}; LAX = {"IH", "EH", "AE", "AH", "UH"}
def strength(pos):
    if abs(pos) < 1e-6: return 4
    if abs(pos - 2) < 1e-6: return 3
    if abs(pos - round(pos)) < 1e-6: return 2
    if abs(pos * 2 - round(pos * 2)) < 1e-6: return 1
    return 0
def final_info(word):
    w = re.sub(r"[^a-z']", "", word.lower()).replace("'", "")
    ph = pronouncing.phones_for_word(w)
    if not ph: return None
    p = ph[0].split(); vs = [x for x in p if x[-1].isdigit()]
    if len(vs) != 1: return None
    v = re.sub(r"\d", "", vs[0]); last = re.sub(r"\d", "", p[-1])
    return v, last
def run(songs):
    R = collections.defaultdict(collections.Counter)
    for name, notes in songs.items():
        rs = name.startswith("RS:")
        notes = [n for n in notes if n["meter"] == [4, 4] and n["p"] is not None]
        if len(notes) < 40: continue
        annotate(notes, rs); corp = "RS" if rs else ("BB" if name.startswith("BB:") else name)
        wid = {}
        for k, w in enumerate(words_of(notes)):
            for i in w: wid[i] = k
        for i in range(1, len(notes)):
            a, b = notes[i - 1], notes[i]
            if a["st"] is None or b["st"] is None: continue
            sa, sb = (a["st"] > 0), (b["st"] > 0)
            if sa == sb: continue
            # the pair must sit close together (within a bar) to count as neighbours
            if (b["bar"] - a["bar"]) * 4 + b["pos"] - a["pos"] > 4: continue
            pa, pb = strength(a["pos"]), strength(b["pos"])
            if pa == pb: continue
            opposed = (sb and pb < pa) or ((not sb) and pb > pa)
            dom = "line start" if (b is notes[i] and a.get("line_start") and not rs) else ("inside a word" if wid[i] == wid[i - 1] else "across words")
            R[(corp, dom)]["opposed" if opposed else "parallel"] += 1
            R[(corp, dom + ", " + ("rising" if sb else "falling") + " stress")]["opposed" if opposed else "parallel"] += 1
        med = np.median([n["q"] for n in notes if n["q"]])
        if rs: continue
        for n in notes:
            if n["nsyl"] != 1 or n["word"].lower().strip("'") in FUNC or not n["q"]: continue
            fi = final_info(n["word"])
            if not fi: continue
            v, last = fi; rel = n["q"] / med
            if last in VOICED: R[(corp, "final voiced")]["n"] += 1; R[(corp, "final voiced")]["long"] += rel > 1
            if last in VOICELESS: R[(corp, "final voiceless")]["n"] += 1; R[(corp, "final voiceless")]["long"] += rel > 1
            if v in TENSE: R[(corp, "tense vowel")]["n"] += 1; R[(corp, "tense vowel")]["long"] += rel > 1
            if v in LAX: R[(corp, "lax vowel")]["n"] += 1; R[(corp, "lax vowel")]["long"] += rel > 1
    return R
if __name__ == "__main__":
    songs = json.load(open(os.path.join(HERE, "sung_syllables.json")))
    songs["song 54"] = engine_song("/home/claude/p64/out/The Man Mama Prayed I'd Be - lead sheet.musicxml")
    songs["song 55"] = engine_song("/home/claude/p65/out/Your Yard Man - lead sheet.musicxml")
    R = run(songs); out = {}
    for (c, k), v in sorted(R.items()):
        if "n" in v: out[f"{c}|{k}"] = dict(n=v["n"], share_longer_than_median=round(v["long"] / v["n"], 3))
        else:
            t = sum(v.values()); out[f"{c}|{k}"] = dict(n=t, opposed=round(v["opposed"] / t, 3))
    json.dump(out, open(os.path.join(HERE, "words_more_results.json"), "w"), indent=1)
    for k, v in out.items(): print(k, v)
