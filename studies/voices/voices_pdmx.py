"""Lead against harmony voice in PDMX (Zenodo 15571083, CC BY 4.0): scores with lyrics (n_lyrics >= 30), deduplicated, no licence
conflict, two or more tracks, already extracted by ../words/pdmx_words.py --extract. Vocal parts: parts with 10 or more lyric
syllables, or named for a voice (soprano, alto, tenor, bass, baritone, voice, vocal, choir, harmony, backing, lead, singer). The lead
is the vocal part with the most syllables (ties: the higher). For every other vocal part, at each lead note's onset, the other part's
sounding note: the signed interval (lead minus other, so positive = harmony below), whether both start together, and the motion to
the next sampled pair. Category from PDMX genre and tags as in pdmx_words.py; texture from the number of vocal parts (2, 3, 4+).
Writes voices_pdmx_results.json."""
import os, re, sys, json, collections, pandas as pd
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); D = "/home/claude/data/pdmx"
sys.path.insert(0, os.path.join(HERE, "..", "words")); sys.path.insert(0, HERE)
from pdmx_words import category
VOICE = re.compile(r"sop|alt|ten|bass|bari|voice|vocal|choir|chor|harmon|backing|bgv|lead|singer|vox|stimme|s\.|a\.|t\.|b\.", re.I)
INST = re.compile(r"piano|organ|guitar|violin|flute|drum|keyboard|string|bass guitar|synth|cello|trumpet|sax|clarinet|harp|ukulele|accordion", re.I)
def sounding(notes, t):
    # binary search on onsets
    lo, hi = 0, len(notes)
    while lo < hi:
        m = (lo + hi) // 2
        if notes[m]["on"] <= t + 1e-6: lo = m + 1
        else: hi = m
    i = lo - 1
    if i >= 0 and notes[i]["on"] + notes[i]["q"] > t + 1e-6: return notes[i]
    return None
def ivclass(iv):
    a = abs(iv)
    if a == 0: return "unison"
    m = a % 12
    if m == 0: return "octave"
    return {1: "2nd", 2: "2nd", 3: "3rd", 4: "3rd", 5: "4th", 6: "tritone", 7: "5th", 8: "6th", 9: "6th", 10: "7th", 11: "7th"}[m]
def analyse(path, cat):
    from parse_parts import parts_of
    ps = parts_of(path)
    voc = [p for p in ps if p["notes"] and (p["n_lyrics"] >= 10 or (VOICE.search(p["name"] or "") and not INST.search(p["name"] or "")))]
    if len(voc) < 2: return None
    for p in voc: p["mean"] = sum(n["p"] for n in p["notes"]) / len(p["notes"])
    lead = max(voc, key=lambda p: (p["n_lyrics"], p["mean"]))
    others = [p for p in voc if p is not lead]
    k = len(voc); tex = ("2 voices, both with words" if min(p["n_lyrics"] for p in voc) >= 10 else "2 voices, one with words") if k == 2 else "3 voices" if k == 3 else "4+ voices"
    R = collections.Counter()
    L = lead["notes"]; T = L[-1]["on"] + L[-1]["q"] if L else 1
    # is the lead the top voice? (for 4-part, melody in soprano)
    R["lead top"] += int(all(lead["mean"] >= o["mean"] for o in others)); R["songs"] += 1
    for o in others:
        prev = None
        below = o["mean"] < lead["mean"]
        side = "below" if below else "above"
        for n in L:
            h = sounding(o["notes"], n["on"])
            R["lead notes"] += 1
            if h is None: prev = None; R["harmony silent"] += 1; continue
            R["harmony sounding"] += 1
            iv = n["p"] - h["p"]   # positive: harmony below lead
            c = ivclass(iv); R["iv " + c] += 1; R[f"iv {side} {c}"] += 1; R[f"n {side}"] += 1
            if iv < 0 and below or iv > 0 and not below: R["crossed"] += 1
            a = abs(iv); R["v7 set (3,4,8,9 below)"] += int(iv in (3, 4, 8, 9)); R["v7 set compound"] += int(iv > 0 and iv % 12 in (3, 4, 8, 9))
            R["lyr both"] += 0
            R["within octave"] += int(a <= 12); R["over octave"] += int(a > 12)
            R["together"] += int(abs(h["on"] - n["on"]) < 1e-6)
            if n["syl"]: R["lead syl"] += 1; R["same syl"] += int(abs(h["on"] - n["on"]) < 1e-6 and h["syl"])
            fr = n["on"] / T; R[f"pos {min(int(fr * 5), 4)} sounding"] += 1
            if prev is not None:
                (pl, ph) = prev; dl = n["p"] - pl; dh = h["p"] - ph
                if dl == 0 and dh == 0: m = "static"
                elif dl == 0 or dh == 0: m = "oblique"
                elif (dl > 0) != (dh > 0): m = "contrary"
                elif dl == dh: m = "parallel exact"
                elif ivclass(pl - ph) == ivclass(iv): m = "parallel class"
                else: m = "similar"
                R["m " + m] += 1; R["motions"] += 1
                pc, cc = ivclass(pl - ph), ivclass(iv)
                if m != "static" and m != "oblique" and m != "contrary" and pc == cc and cc in ("5th", "octave", "unison"):
                    R["parallel P5/P8"] += 1; R["par " + cc] += 1
            prev = (n["p"], h["p"])
        for fr in range(5): R[f"pos {fr} total"] += sum(1 for n in L if min(int(n['on'] / T * 5), 4) == fr)
    return (cat, tex, dict(R))
def work(a):
    try: return analyse(*a)
    except Exception as e: return None
if __name__ == "__main__":
    d = pd.read_csv(f"{D}/PDMX.csv", low_memory=False)
    d = d[(d.has_lyrics == True) & (d["subset:deduplicated"] == True) & (d["subset:no_license_conflict"] == True) & (d.n_lyrics >= 30) & (d.n_tracks >= 2) & d.mxl.notna()]
    d = d.assign(cat=d.apply(category, axis=1))
    jobs = [(os.path.join(D, "x", p.lstrip("./")), c) for c, p in zip(d.cat, d.mxl) if os.path.exists(os.path.join(D, "x", p.lstrip("./")))]
    if len(sys.argv) > 1: jobs = jobs[:int(sys.argv[1])]
    print(len(d), "selected;", len(jobs), "extracted")
    R = collections.defaultdict(collections.Counter); used = collections.Counter()
    with Pool(2) as pool:
        for res in pool.imap_unordered(work, jobs, chunksize=10):
            if res is None: used["none"] += 1; continue
            cat, tex, r = res; R[(cat, tex)].update(r); R[("all", tex)].update(r); used["used"] += 1
    out = {"counts": dict(used)}
    for k, r in sorted(R.items()):
        s = r["harmony sounding"] or 1; mo = r["motions"] or 1
        out[" | ".join(k)] = dict(songs=r["songs"], lead_top=round(r["lead top"] / max(r["songs"], 1), 3),
            harmony_present=round(r["harmony sounding"] / max(r["lead notes"], 1), 3),
            intervals={c: round(r["iv " + c] / s, 3) for c in ["unison", "2nd", "3rd", "4th", "tritone", "5th", "6th", "7th", "octave"]},
            below_share=round(r["n below"] / s, 3),
            below={c: round(r["iv below " + c] / max(r["n below"], 1), 3) for c in ["unison", "3rd", "4th", "5th", "6th", "octave"]},
            above={c: round(r["iv above " + c] / max(r["n above"], 1), 3) for c in ["unison", "3rd", "4th", "5th", "6th", "octave"]},
            v7_set=round(r["v7 set (3,4,8,9 below)"] / s, 3), v7_set_compound=round(r["v7 set compound"] / s, 3), within_octave=round(r["within octave"] / s, 3),
            crossed=round(r["crossed"] / s, 3), together=round(r["together"] / s, 3),
            same_syllable=round(r["same syl"] / max(r["lead syl"], 1), 3),
            motion={m: round(r["m " + m] / mo, 3) for m in ["static", "oblique", "contrary", "parallel exact", "parallel class", "similar"]},
            parallel_P5_P8_per_100=round(100 * r["parallel P5/P8"] / mo, 2), parallel_per_100={c: round(100 * r["par " + c] / mo, 2) for c in ("5th", "octave", "unison")},
            presence_by_fifth=[round(r[f"pos {i} sounding"] / max(r[f"pos {i} total"], 1), 3) for i in range(5)],
            n_pairs=r["harmony sounding"])
    json.dump(out, open(os.path.join(HERE, "voices_pdmx_results.json"), "w"), indent=1)
    print(json.dumps(out, indent=0)[:6000])
