"""v124 Run 1: the readings v121-v123 ask for, on the runs of record (survivors of each song's main and control runs), read by the papers' own code
(cand, om and outer, from zeneng_v121_blind_spots.json, zeneng_v122_whole_song.json and zeneng_v123_bass_at_the_chord.json; onsets, pitches and
the chart's chord a bar, as those studies read the builds), beside both collections:
  426  the six measures (Verse 1 and Chorus 1 windows) beside CoCoPops' and BiMMuDa's means
  431  the four chord-tone measures beside Billboard's and Rolling Stone's
  433, 436  the second verse and the bridge, each against kept sections of its kind (and verse 1 and chorus 1 the same way); the bridge's
       highest note, notes a bar and repeated bar rhythms beside the kept bridge's
  432, 441, 442  first-beat notes that are chord tones, the chord's root, its third; notes a step above a chord tone; notes a second or
       seventh from the bass (readings only)
  443  melody against bass: motion, and fifths or octaves in a row (no rule or aim)
  437  the chorus's returns beside the first chorus (pair)
  430  song 45's hand edits (Q16 A) read measure by measure with v121's provisional judge
Usage: python3 new_readings_v124.py OUT.json [run prefix, default /home/claude/p52/melody_v124]"""
import sys, json, pickle, collections, importlib, re
import numpy as np
OUT = sys.argv[1]; PFX = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/p52/melody_v124"
T = "/home/claude/p52/tables"
T121 = json.load(open(f"{T}/zeneng_v121_blind_spots.json")); T122 = json.load(open(f"{T}/zeneng_v122_whole_song.json")); T123 = json.load(open(f"{T}/zeneng_v123_bass_at_the_chord.json"))
ns_ = {"np": np, "collections": collections}
exec(next(v for k, v in T121.items() if k.startswith("code: cand")), ns_); cand = ns_["cand"]
src122 = T122["code"]
for name in ("om", "pair"):                                                                # the functions alone, from the study's code
    m = re.search(rf"^def {name}\(.*?(?=^\S)", src122, re.S | re.M); exec(m.group(0), ns_)
ns_["SIX"] = ["equal_gap_run_max", "gap_same_as_before", "gap_entropy", "most_onsets_in_a_beat", "phrase_starts_same_place", "zigzag_of_three"]
ns_["MAJ"] = {0, 2, 4, 5, 7, 9, 11}; ns_["MIN"] = {0, 2, 3, 5, 7, 8, 10}
om, pair = ns_["om"], ns_["pair"]
src123 = T123["code"]
for name in ("sgn", "bmove", "outer"):
    m = re.search(rf"^def {name}\(.*?(?=^\S)", src123, re.S | re.M); exec(m.group(0), ns_)
outer = ns_["outer"]
NAME = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def root_minor(c):
    c = c.split("/")[0]; r = NAME[c[0]] + (1 if "#" in c[:2] else -1 if (len(c) > 1 and c[1] == "b") else 0); m = "m" in c[1:3] and "maj" not in c; return r % 12, m
def pcs(c): r, m = root_minor(c); return frozenset({r, (r + (3 if m else 4)) % 12, (r + 7) % 12})
def eng(c): r, m = root_minor(c); return (r, frozenset((0, 3 if m else 4, 7)), 0, False)
SONGS = ("40", "42", "43", "44", "45")
TON = {}
for s in SONGS:                                                                            # each song's own tonic and mode, from its module
    sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p52"]
    P = importlib.import_module(f"melody_v124_p{s}"); TON[s] = (int(getattr(P, "ETON", P.M.TONIC)) % 12, getattr(P, "MTON", None) is not None)
SECS = {"Verse 1": ("verse", 1), "Verse 2": ("verse", 2), "Chorus 1": ("chorus", 1), "Chorus 2": ("chorus", 2), "Last Chorus": ("chorus", "last"), "Bridge": ("bridge", 1)}
def windows(D):
    st = {}; i = 0
    for name, kind, nb in D["form"]: st[name] = (i, nb); i += nb
    out = []
    for b in D["all"]:
        W = {}
        for name in SECS:
            if name not in st or st[name][1] < 8: continue
            b0 = st[name][0]; sel = [t for t in b["notes"] if b0 * 48 <= t[0] < (b0 + 8) * 48 and t[3] == name]
            W[name] = dict(om=sorted(((t[0] - b0 * 48) / 12, t[2], pcs(D["chords"][t[0] // 48])) for t in sel),
                           outer=sorted(((t[0] - b0 * 48) / 12, t[2], eng(D["chords"][t[0] // 48])) for t in sel))
        out.append(W)
    return out
ROWS = collections.defaultdict(list); OUTER = collections.defaultdict(list); CNT = collections.defaultdict(collections.Counter); PAIRS = collections.defaultdict(list); TOPS = collections.defaultdict(list)
for s in SONGS:
    ton, minor = TON[s]
    for mode in ("main", "ctl"):
        D = pickle.load(open(f"{PFX}_p{s}_{mode}.pkl", "rb"))
        for W in windows(D):
            for name, w in W.items():
                f = om([x for x in w["om"] if x[0] < 32], ton, minor)
                if f: ROWS[(s, mode, name)].append(f)
                if name in ("Verse 1", "Chorus 1"):
                    o = outer([x for x in w["outer"] if x[0] < 32])
                    if o: OUTER[(s, mode, name)].append(o[0]); CNT[(s, mode)].update(o[1])
            for a_, b_ in (("Verse 1", "Verse 2"), ("Chorus 1", "Chorus 2"), ("Chorus 1", "Last Chorus")):
                if a_ in W and b_ in W and len(W[a_]["om"]) >= 12 and len(W[b_]["om"]) >= 12:
                    PAIRS[(s, f"{b_} beside {a_}")].append(pair([(x[0], x[1]) for x in W[a_]["om"]], [(x[0], x[1]) for x in W[b_]["om"]]))
            if "Bridge" in W and "Verse 1" in W and W["Bridge"]["om"] and W["Verse 1"]["om"]:
                TOPS[s].append((max(x[1] for x in W["Bridge"]["om"]) - max(x[1] for x in W["Verse 1"]["om"]),
                                max(x[1] for x in W["Bridge"]["om"]) - max(x[1] for x in W["Chorus 1"]["om"]) if "Chorus 1" in W and W["Chorus 1"]["om"] else np.nan))
def mean(rows, m):
    x = [r[m] for r in rows if r.get(m) is not None and np.isfinite(r[m])]; return round(float(np.mean(x)), 4) if x else None
def both_modes(s, name, m, src=ROWS):
    return mean(src[(s, "main", name)] + src[(s, "ctl", name)], m)
R = {"about": __doc__.split("Usage")[0].strip(), "builds read (survivors, main and control) by song": {s: len(pickle.load(open(f"{PFX}_p{s}_main.pkl", "rb"))["all"]) + len(pickle.load(open(f"{PFX}_p{s}_ctl.pkl", "rb"))["all"]) for s in SONGS}}
# 426: the six, Verse 1 and Chorus 1 windows pooled
r426 = {}
for row in T121["every candidate"]:
    m = row["measure"]
    if m not in ns_["SIX"]: continue
    sd = (row["builds"] - row["cocopops"]) / row["builds_vs_cocopops"] if row["builds_vs_cocopops"] else None
    bs = {s: mean(ROWS[(s, "main", "Verse 1")] + ROWS[(s, "ctl", "Verse 1")] + ROWS[(s, "main", "Chorus 1")] + ROWS[(s, "ctl", "Chorus 1")], m) for s in SONGS}
    lo, hi = sorted((row["cocopops"], row["bimmuda"]))
    side = {s: ("between" if lo <= x <= hi else "above" if x > hi else "below") for s, x in bs.items() if x is not None}
    r426[m] = dict(cocopops=row["cocopops"], bimmuda=row["bimmuda"], sd=round(sd, 4) if sd else None, v118_builds=row["builds"], run1=bs,
                   in_sd_from_nearer={s: round(min(abs(x - lo), abs(x - hi)) / sd * (1 if x > hi else -1 if x < lo else 0), 2) for s, x in bs.items() if x is not None and sd},
                   side=side, same_side_on_every_song=len(set(side.values())) == 1)
R["426: the six measures (Verse 1 and Chorus 1 windows), beside both collections"] = r426
# 431: chord tones beside Billboard and Rolling Stone (first verse and chorus)
r431 = {}
for row in T122["chord tones (Table EB)"]:
    m = row["measure"]; sd = (row["builds"] - row["billboard"]) / row["builds_vs_billboard"]
    bs = {s: mean(ROWS[(s, "main", "Verse 1")] + ROWS[(s, "ctl", "Verse 1")] + ROWS[(s, "main", "Chorus 1")] + ROWS[(s, "ctl", "Chorus 1")], m) for s in SONGS}
    r431[m] = dict(billboard=row["billboard"], rolling_stone=row["rolling_stone"], sd=round(sd, 4), v118_builds=row["builds"], run1=bs,
                   vs_billboard_sd={s: round((x - row["billboard"]) / sd, 2) for s, x in bs.items() if x is not None},
                   vs_rolling_stone_sd={s: round((x - row["rolling_stone"]) / sd, 2) for s, x in bs.items() if x is not None})
R["431: chord tones beside Billboard and Rolling Stone (first verse and chorus; a chord a bar, as Window 142 reads the builds)"] = r431
# 433 and 436: each section against kept sections of its kind
KS = T122["kept figures by section (both collections pooled)"]; SK = {"Verse 1": "verse 1", "Verse 2": "verse 2", "Chorus 1": "chorus 1", "Bridge": "bridge 1"}
r433 = {}
for name, k in SK.items():
    rows = {}; outside = collections.Counter(); nm = 0
    for m, kf in KS[k].items():
        if m == "windows" or not isinstance(kf, dict): continue
        bs = {s: both_modes(s, name, m) for s in SONGS}
        rows[m] = dict(kept=round(kf["mean"], 3), middle_half=(kf["q25"], kf["q75"]), run1=bs, in_sd={s: round((x - kf["mean"]) / kf["sd"], 2) for s, x in bs.items() if x is not None and kf["sd"]})
        nm += 1
        for s, x in bs.items():
            if x is not None and not (kf["q25"] <= x <= kf["q75"]): outside[s] += 1
    r433[name] = dict(kept_windows=KS[k].get("windows"), measures=nm, outside_the_kept_middle_half_by_song=dict(outside), by_measure=rows)
R["433: verse 1, verse 2, chorus 1 and the bridge, each against kept sections of its kind (means of the song's builds against the kept middle half)"] = r433
BV = T122["bridge and verse"]
r436 = {m: dict(kept_bridge=dict(billboard=BV[m]["bb bridge"], rolling_stone=BV[m]["rs bridge"], billboard_median=BV[m]["bb bridge median"], rolling_stone_median=BV[m]["rs bridge median"]),
                kept_verse=dict(billboard=BV[m]["bb verse"], rolling_stone=BV[m]["rs verse"]), v118_builds=dict(bridge=BV[m]["build bridge"], verse=BV[m]["build verse"]),
                run1_bridge={s: both_modes(s, "Bridge", m) for s in SONGS}, run1_verse={s: both_modes(s, "Verse 1", m) for s in SONGS}) for m in BV}
r436["highest note: the bridge's top less verse 1's and chorus 1's (semitones, median)"] = {s: (float(np.median([a for a, b in TOPS[s]])), float(np.nanmedian([b for a, b in TOPS[s]]))) for s in SONGS if TOPS[s]}
r436["note"] = "the kept tables carry no bridge-over-verse top; the builds' is printed alone"
R["436: the bridge beside kept bridges"] = r436
# 432, 441, 442: the melody over the chord and the bass, by section
Q = T123["the melody over chord and bass, by window: kept quartiles (441, 442)"]; F2 = T123["findings"]["2. the melody over the chord and the bass (first verse and chorus)"]
r441 = {}
for m in ("downbeat_chord_tone", "downbeat_on_root", "downbeat_on_third", "melody_a_step_above_a_chord_tone", "over_bass_second_or_seventh", "chord_tones", "melody_on_root", "melody_on_third", "melody_on_fifth"):
    r441[m] = dict(billboard=F2.get(m, {}).get("billboard"), rolling_stone=F2.get(m, {}).get("rolling_stone"), v118_builds=F2.get(m, {}).get("builds"),
                   kept_quartiles={sec: (Q[sec][m]["q25"], Q[sec][m]["median"], Q[sec][m]["q75"], round(Q[sec][m]["mean"], 3)) for sec in Q if m in Q[sec]},
                   run1={s: dict(verse=both_modes(s, "Verse 1", m, OUTER), chorus=both_modes(s, "Chorus 1", m, OUTER)) for s in SONGS})
r441["paper's aims (readings only for now)"] = dict(downbeat_chord_tone=0.72, downbeat_on_root=0.24, downbeat_on_third=0.26, melody_a_step_above_a_chord_tone=0.24, over_bass_second_or_seventh=0.19,
                                                    chorus_not_below_verse=["downbeat_chord_tone (432)", "downbeat_on_third (441)"])
r441["chorus not below verse"] = {s: dict(downbeat_chord_tone=(r441["downbeat_chord_tone"]["run1"][s]["chorus"] or 0) >= (r441["downbeat_chord_tone"]["run1"][s]["verse"] or 0),
                                          downbeat_on_third=(r441["downbeat_on_third"]["run1"][s]["chorus"] or 0) >= (r441["downbeat_on_third"]["run1"][s]["verse"] or 0)) for s in SONGS}
R["432, 441, 442: the melody over the chord and the bass (first verse and chorus; the chart's chords as triads, the bass on the root)"] = r441
# 443: outer-voice motion, pooled over the windows
F3 = T123["findings"]["3. outer-voice motion, pooled over windows"]
def motion(c): return {"chord-to-chord pairs": c["pairs"], "bass stays": round(c["bass_stays"] / max(1, c["pairs"]), 3), "parallel fifths or octaves, of bass moves": round(c["parallel_perfect"] / max(1, c["bass_moves"]), 3),
                       "bass by step or third: contrary": round(c["contrary"] / max(1, c["clear"]), 3), "similar": round(c["similar"] / max(1, c["clear"]), 3), "melody holds": round(c["oblique"] / max(1, c["clear"]), 3),
                       "contrary of the two moving": round(c["contrary"] / max(1, c["contrary"] + c["similar"]), 3)}
R["443: melody against bass, pooled (printed; no rule or aim)"] = dict(billboard=F3["bb"], rolling_stone=F3["rs"], v118_builds=F3["build"], run1={s: motion(CNT[(s, "main")] + CNT[(s, "ctl")]) for s in SONGS})
# 437: the chorus's returns beside the first (and verse 2 beside verse 1)
LW = T122["the later window beside the first"]; KEYS = {"Verse 2 beside Verse 1": "verse 2 beside verse 1", "Chorus 2 beside Chorus 1": "chorus 2 beside chorus 1", "Last Chorus beside Chorus 1": "chorus last beside chorus 1"}
r437 = {}
for k, kk in KEYS.items():
    r437[k] = dict(billboard=LW[kk]["bb"], rolling_stone=LW[kk]["rs"], v118_builds=LW[kk]["build"], run1={})
    for s in SONGS:
        X = PAIRS[(s, k)]
        if not X: continue
        r437[k]["run1"][s] = {c: round(float(np.nanmean([x[c] for x in X])), 3) for c in ("bars_same_rhythm", "onsets_shared", "pitch_kept", "notes_ratio")} | {"pairs": len(X), "bars all the same rhythm": round(float(np.mean([x["bars_same_rhythm"] == 1 for x in X])), 3)}
R["437: the later windows beside the first (pair, means; kept: mean, 25th, 75th)"] = r437
# 430: song 45's hand edits (Q16 A) read measure by measure with v121's provisional judge (not the judge of record)
PJ = T121["provisional judge (not the judge of record)"]; PM = PJ["measures"]; PMU, PSD, PW, PF = map(np.array, (PJ["mean"], PJ["sd"], PJ["weight"], PJ["fill_missing_with"]))
sys.argv = ["x", "1", "main"]; P45 = importlib.import_module("melody_v124_p45")
F = pickle.load(open("/home/claude/p49/melody_final.pkl", "rb")); pick = F["pick"]; ed = {e["line"]: e for e in pick["hand_edits"]}
after = [dict(n) for n in pick["notes"]]
before = [dict(n) for n in after if n["line"] not in ed] + [dict(on=o, p=p, dur=d, line=k, sec=k.rsplit(":", 1)[0]) for k, e in ed.items() for o, p, d in e["before"]]
before.sort(key=lambda n: n["on"])
def feats36(notes, sec):
    N = P45.win_N(notes, P45.BAR0[sec]); f = dict(P45.feats(N, P45.mton()) or {}); c = cand(sorted(N)) or {}; f.update({k: c[k] for k in ns_["SIX"] if k in c})
    x = np.array([f.get(m, np.nan) if f.get(m) is not None else np.nan for m in PM], float); return np.where(np.isfinite(x), x, PF)
r430 = {}
for sec in ("Chorus 1", "Verse 2"):
    xb, xa = feats36(before, sec), feats36(after, sec); pb, pa = PW * (xb - PMU) / PSD, PW * (xa - PMU) / PSD; d = pa - pb; o = np.argsort(d)
    r430[sec] = dict(judge_drawn=round(float(PJ["intercept"] + pb.sum()), 3), judge_edited=round(float(PJ["intercept"] + pa.sum()), 3),
                     moved_most_down=[(PM[j], round(float(xb[j]), 3), round(float(xa[j]), 3), round(float(d[j]), 2)) for j in o[:6] if d[j] < 0],
                     moved_most_up=[(PM[j], round(float(xb[j]), 3), round(float(xa[j]), 3), round(float(d[j]), 2)) for j in o[::-1][:6] if d[j] > 0])
r430["note"] = ("the pick of record 10c3fce99da2 (songs/p49) before and after the writer's edits; points are weight x z on v121's provisional judge (36 measures), "
                "edited less drawn; the judge reads the build-likeness side as positive. Window 141 prints, on the 36: drawn 1.02, edited 0.30.")
R["430: the writer's edit, read measure by measure (song 45, Q16 A)"] = r430
json.dump(R, open(OUT, "w"), indent=1, default=str)
print(json.dumps({k: (v if k.startswith("430") else "...") for k, v in R.items()}, indent=1, default=str)[:3000])
