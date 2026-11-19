"""When is the engine sound? A fixed set of checks, each read the same way on every kept 4/4 song and on each Luthier record, so the bar is set by the
kept songs themselves. For each check: the kept 10th, 25th, 50th, 75th and 90th by song, and where each record falls.
The rule (see SOUNDNESS.md) is about the engine, not one song: a kept song itself sits outside its middle half on about half the checks, so the test is a lean,
all three songs beyond the same kept bound on one check. Sound: no check with all three beyond the 10th or 90th on one side, and no more than two with all three
beyond the 25th or 75th on one side. The script draws three kept songs at random 20,000 times and reports how often they fail the same rule.
Two checks have no per-song kept rows here (the chorus's lift; rest share inside sung sections, from register_plan.json); they are read against their
kept percentiles and left out of the random draws.
    python3 studies/soundness/soundness.py songs/p65/lyric55.song.json songs/p64/lyric54.song.json songs/p68/lyric58.song.json"""
import os, sys, json, re, collections, statistics
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import kept_corpus as KC, atlas_build as AB, scaling as SC, word_weight as W, make_kept_word_weight as MW, make_kept_line_ends as ML
BAR, BEATS, BEAT = 48, [0, 12, 24, 36], 12
ATLAS = ["onsets on the beat", "onsets on the bar's first beat", "notes a bar", "distinct rhythms over bars", "bars on a rhythm already sung", "moves by step", "moves by leap", "repeated notes", "range", "bars on a figure already sung"]
CHECKS = [  # (name, group)
    ("stressed syllables on a beat", "words"), ("the words' fit, whole", "words"), ("fit by length", "words"), ("fit by place", "words"), ("fit by height", "words"),
    ("onsets on the beat", "rhythm"), ("onsets on the bar's first beat", "rhythm"), ("notes a bar", "rhythm"), ("distinct rhythms over bars", "rhythm"), ("bars on a rhythm already sung", "rhythm"), ("rhythm scaling", "rhythm"),
    ("moves by step", "pitch"), ("moves by leap", "pitch"), ("repeated notes", "pitch"), ("range", "pitch"), ("bars on a figure already sung", "pitch"), ("pitch scaling", "pitch"),
    ("silences of a beat or more, per 100 beats", "breath"), ("longest phrase, beats (breath at half a beat)", "breath"), ("lines run on (under a beat of rest), share", "breath"),
    ("stressed line ends held a half note or more, share", "breath")]
EXTRA = [("the chorus's median over the verse's, semitones", "form"), ("rest share inside sung sections", "form")]
HALF_LEANS = 2     # the rule: three kept songs drawn at random fail it about 6 times in 100
def scal(ns2):
    sc = SC.series([(x[0], x[2]) for x in ns2]); a_ = SC.dfa(sc["pitch"]); b_ = SC.dfa(sc["onsets on the grid"]); return (a_["alpha"] if a_ else 0.9), (b_["alpha"] if b_ else 0.66)
def breath(on, dur):
    """on, dur in beats, time order: silences of a beat or more per 100 beats (studies/breath/silences.py), and the longest phrase at half-beat breaths (906)."""
    end = on + dur; gaps = on[1:] - end[:-1]; sil = 100.0 * float(np.sum(gaps >= 1.0)) / float(on[-1] - on[0])
    endc = np.minimum(end, np.r_[on[1:], 1e9]); ph = []; s0 = on[0]
    for i in range(len(on) - 1):
        if on[i + 1] - endc[i] >= 0.5: ph.append(endc[i] - s0); s0 = on[i + 1]
    ph.append(endc[-1] - s0); return sil, float(max(ph))
def kept_rows():
    rows = {}
    for k in KC.kept_songs():
        t, p, d = k["t"], k["p"], k["dur"]; keep2 = [i for i in range(len(t)) if i == 0 or t[i] > t[i - 1]]
        ns2 = [[int(t[i]), 6, int(p[i])] for i in keep2 if t[i] % 3 == 0]; r = AB.readings(ns2, BAR, BEATS, BEAT); s = {a: r[a] for a in ATLAS if a in r}
        import make_kept_4_4_tables as MK; s.update({a: v for a, v in MK.structure(ns2, BAR).items()})
        s["pitch scaling"], s["rhythm scaling"] = scal(ns2)
        s["silences of a beat or more, per 100 beats"], s["longest phrase, beats (breath at half a beat)"] = breath(t / 12.0, d / 12.0)
        tr, _ = MW.tiers(k["words"])
        if len(tr) == len(t):
            idx = [i for i in range(len(tr)) if tr[i] is not None]
            if len(idx) >= 40:
                S = W.salience(t, d, p, k["lines"]); w = np.array([W.WEIGHT[tr[i]] for i in idx]); f = {c: W.spearman(w, S[c][idx]) for c in S}
                s.update({"the words' fit, whole": f["all"], "fit by length": f["length"], "fit by place": f["place"], "fit by height": f["height"]})
        rows[k["song"]] = s
    for s, ends, S in ML.line_ends():
        if s not in rows: continue
        words = []; cur = ""; n_ = 0
        for on, end, w, new in S:
            cont = w.endswith("-"); cur += re.sub(r"[^A-Za-z']", "", w); n_ += 1
            if not cont: words.append((cur, n_)); cur = ""; n_ = 0
        if n_: words.append((cur, n_))
        tr_, _ = MW.tiers(words); sb = [0, 0]
        for i, (on, end, w, new) in enumerate(S):
            if tr_[i] == 2: sb[1] += 1; sb[0] += on % 12 == 0
        if sb[1] >= 40: rows[s]["stressed syllables on a beat"] = sb[0] / sb[1]
        if ends: rows[s]["lines run on (under a beat of rest), share"] = float(np.mean([r < 12 for _, _, _, r in ends]))
        st_ = [min(D, G) >= 24 for tr, G, D, r in ends if tr == 2]                         # as make_kept_line_ends counts a held line end (D to the next line at most)
        if len(st_) >= 8: rows[s]["stressed line ends held a half note or more, share"] = float(np.mean(st_))
    return rows
def record_row(R):
    ns = sorted(R["melody"]["notes"], key=lambda n: n["on"]); sung = [n for n in ns if n.get("melisma") != "second"]
    ns2 = [[n["on"], 6, n["midi"]] for n in ns]; r = AB.readings(ns2, BAR, BEATS, BEAT); s = {a: r[a] for a in ATLAS if a in r}
    import make_kept_4_4_tables as MK; s.update(MK.structure(ns2, BAR)); s["pitch scaling"], s["rhythm scaling"] = scal(ns2)
    on = np.array([n["on"] for n in ns]) / 12.0; du = np.array([n["dur"] for n in ns]) / 12.0
    s["silences of a beat or more, per 100 beats"], s["longest phrase, beats (breath at half a beat)"] = breath(on, du)
    f = W.fit(sung, BAR, BEAT, parts=True); s.update({"the words' fit, whole": f["all"], "fit by length": f["length"], "fit by place": f["place"], "fit by height": f["height"]})
    st = [n for n in sung if n["stress"]]; s["stressed syllables on a beat"] = float(np.mean([n["on"] % BEAT == 0 for n in st]))
    lines = collections.OrderedDict()
    for n in ns: lines.setdefault((n["sec"], n["line"]), []).append(n)
    L = list(lines.values()); rests = [b[0]["on"] - (a[-1]["on"] + a[-1]["dur"]) for a, b in zip(L, L[1:])]
    s["lines run on (under a beat of rest), share"] = float(np.mean([x < 12 for x in rests]))
    held = []
    for a_, b_ in zip(L, L[1:] + [None]):
        last = [n for n in a_ if n.get("melisma") != "second"][-1]; D = sum(n["dur"] for n in a_ if n["on"] >= last["on"]); G = (b_[0]["on"] - last["on"]) if b_ else D
        if last["stress"]: held.append(min(D, G) >= 24)
    s["stressed line ends held a half note or more, share"] = float(np.mean(held))
    c = R["checks"]; s["the chorus's median over the verse's, semitones"] = c[next(k for k in c if k.startswith("the chorus's median over the verse's"))]
    s["rest share inside sung sections"] = c[next(k for k in c if k.startswith("rest share inside sung sections"))]
    return s
def side(q, x, band):
    """-1 below, +1 above, 0 inside: band 'half' is the 25th to 75th, 'wide' the 10th to 90th"""
    lo, hi = (q[1], q[3]) if band == "half" else (q[0], q[4])
    return -1 if x < lo else 1 if x > hi else 0
def same_side(Q, rows, names, band):
    """the checks on which every song lies outside the band on the same side: a lean of the engine, not of one song"""
    out = []
    for nm in names:
        sd = [side(Q[nm], r[nm], band) for r in rows]
        if all(x == -1 for x in sd) or all(x == 1 for x in sd): out.append((nm, "low" if sd[0] < 0 else "high"))
    return out
def counts(Q, r, names):
    return sum(side(Q[nm], r[nm], "half") != 0 for nm in names), sum(side(Q[nm], r[nm], "wide") != 0 for nm in names)
if __name__ == "__main__":
    import random
    K = kept_rows(); RP = json.load(open(os.path.join(ROOT, "tables", "register_plan.json")))
    Q = {}
    for nm, _ in CHECKS:
        v = [r[nm] for r in K.values() if nm in r and r[nm] == r[nm]]; Q[nm] = [float(x) for x in np.percentile(v, (10, 25, 50, 75, 90))]
    Q[EXTRA[0][0]] = [float(x) for x in np.percentile(RP["lifts"], (10, 25, 50, 75, 90))]; Q[EXTRA[1][0]] = [float(x) for x in RP["rest_share"]]
    names = [nm for nm, _ in CHECKS]; full = [r for r in K.values() if all(nm in r for nm in names)]
    C = np.array([counts(Q, r, names) for r in full])
    rng = random.Random(1); B = 20000; fa = collections.Counter(); HL = collections.Counter()
    for _ in range(B):
        tri = rng.sample(full, 3); w = len(same_side(Q, tri, names, "wide")); h = len(same_side(Q, tri, names, "half")); HL[h] += 1
        fa["a lean beyond the 10th or 90th"] += w > 0; fa["more than HALF_LEANS leans beyond the 25th or 75th"] += h > HALF_LEANS; fa["the rule"] += (w > 0 or h > HALF_LEANS)
    out = dict(rule=f"sound when no check has all three songs beyond the kept 10th or 90th on the same side, and no more than {HALF_LEANS} checks have all three beyond the kept 25th or 75th on the same side",
               kept_songs_with_every_reading=len(full), per_kept_song_checks_outside_middle_half_quartiles=[float(x) for x in np.percentile(C[:, 0], (25, 50, 75, 90))],
               per_kept_song_checks_outside_10th_90th_quartiles=[float(x) for x in np.percentile(C[:, 1], (25, 50, 75, 90))],
               three_kept_songs_drawn_at_random_fail_share={k.replace("HALF_LEANS", str(HALF_LEANS)): round(v / B, 3) for k, v in fa.items()},
               leans_beyond_25th_75th_in_three_random_kept_songs={k: round(v / B, 4) for k, v in sorted(HL.items())}, kept=Q, songs={})
    recs = []
    for f in sys.argv[1:]:
        R = json.load(open(f)); s_ = record_row(R); recs.append(s_)
        m, o = counts(Q, s_, names + [EXTRA[0][0], EXTRA[1][0]])
        out["songs"][os.path.basename(f)] = dict(readings={k: round(v, 3) if isinstance(v, float) else v for k, v in s_.items()},
            places={nm: ("in" if side(Q[nm], s_[nm], "half") == 0 else "near" if side(Q[nm], s_[nm], "wide") == 0 else "out") for nm in names + [e for e, _ in EXTRA]}, outside_middle_half=m, outside_10th_90th=o)
    allnames = names + [e for e, _ in EXTRA]
    out["engine"] = dict(lean_beyond_10th_90th=same_side(Q, recs, allnames, "wide"), lean_beyond_25th_75th=same_side(Q, recs, allnames, "half"))
    out["engine"]["sound"] = not out["engine"]["lean_beyond_10th_90th"] and len(out["engine"]["lean_beyond_25th_75th"]) <= HALF_LEANS
    out["engine"]["checks_outside_the_middle_half_all_three_songs"] = sum(v["outside_middle_half"] for v in out["songs"].values())
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "soundness.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("rule", "per_kept_song_checks_outside_middle_half_quartiles", "per_kept_song_checks_outside_10th_90th_quartiles", "three_kept_songs_drawn_at_random_fail_share", "leans_beyond_25th_75th_in_three_random_kept_songs")}))
    for nm in allnames:
        q = Q[nm]; print(f"{nm:52s} kept {[round(x, 3) for x in q]}  " + "  ".join(f"{os.path.basename(f)[5:7]} {out['songs'][os.path.basename(f)]['readings'].get(nm)} {out['songs'][os.path.basename(f)]['places'][nm]}" for f in sys.argv[1:]))
    for k, v in out["songs"].items(): print(k, "outside the middle half", v["outside_middle_half"], "outside 10th-90th", v["outside_10th_90th"])
    print("engine:", json.dumps(out["engine"]))
