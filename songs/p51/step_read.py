"""The readings made between the steps (v119): one main run of a song, read for the fixes ported so far and for the measures that
separate most (Window 139, zeneng_v119_families.json). Usage: python3 step_read.py SONG PKL_PREFIX OUT_JSON"""
import sys, os, pickle, json, collections, importlib
import numpy as np
SONG, PRE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p51", "/home/claude/p40"]
P = importlib.import_module(f"melody_v119_p{SONG}"); M = P.M; BAR, BEAT = P.BAR, P.BEAT
FAM = json.load(open("/home/claude/p51/tables/zeneng_v119_families.json")); KT_ = FAM["kept targets (398-401)"]
D = pickle.load(open(f"{PRE}_main.pkl", "rb")); Al = [b for b in D["all"] if b["read"]["v"] and b["read"]["c"]]; st = D["stats"]
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st_, syl=sy) for o, d, p, s, l, st_, sy in b["notes"]]
r = dict(song=SONG, step=D["rerun"].get("v119_step"), fixes_on=D["rerun"].get("fixes_on"), made=D["made"], survivors=D["survivors"], order=D["order_fp"],
         complete=len(Al), deaths=dict(D["deaths"].most_common()))
def mean_of(m): v = [b["read"][w][m] for b in Al for w in ("v", "c") if b["read"][w].get(m) is not None and np.isfinite(b["read"][w][m])]; return round(float(np.mean(v)), 3) if v else None
def med_of(m): v = [b["read"][w][m] for b in Al for w in ("v", "c") if b["read"][w].get(m) is not None and np.isfinite(b["read"][w][m])]; return round(float(np.median(v)), 3) if v else None
r["measures"] = {m: dict(kept_mean=KT_[m]["kept mean"], kept_quartiles=KT_[m]["kept quartiles"], builds_mean=mean_of(m), builds_median=med_of(m))
                 for m in ("chord_tones", "chord_tones_on_beat", "chord_tones_on_downbeat", "chord_tones_off_beat", "chord_tones_on_long_notes", "non_chord_resolved_by_step",
                           "turns_per_move", "distinct_durations", "first_onset", "fourth_fifth")}
for m, k in (("outside_scale", 0.071), ("gap_quarter", 0.186), ("gap_eighth", 0.465), ("gap_sixteenth", 0.107)):
    r["measures"][m] = dict(kept_mean=k, builds_mean=mean_of(m), builds_median=med_of(m))
# 385, 349, 358
r["385"] = dict(outside_scale=mean_of("outside_scale"), kept=0.045 if getattr(P, "MTON", None) is not None else 0.071, placed=st.get("349: notes placed outside the scale", 0),
                wanting=st.get("349: places wanting", 0), passing=st.get("358: chromatic passing notes placed", 0))
# 375 and 386: notes on a beat or a beat long a semitone from a chord's own outside tone, by the kind of line
CH_ = P.CHORD; viol = 0; seen = 0; vk = collections.Counter()
for b in Al:
    for n in nts(b):
        if n["on"] % BEAT and n["dur"] < 12: continue
        ch_ = CH_[n["on"] // BAR]; tones_ = M.CH[ch_][1]; out_ = [t_ for t_ in tones_ if t_ not in M.SCALE]
        if out_:
            seen += 1; bad = any((n["p"] - t_) % 12 in (1, 11) for t_ in out_) and n["p"] % 12 not in tones_; viol += bad
            if bad:
                kd_ = b["kinds"].get(tuple(n["line"].rsplit(":", 1)[:1]) + (int(n["line"].rsplit(":", 1)[1]),), "?") if isinstance(b.get("kinds"), dict) else "?"
                vk[str(kd_)] += 1
r["386"] = dict(notes_read=seen, clashes=viol, by_line=dict(vk), moved={k: v for k, v in st.items() if k.startswith("386")})
r["387"] = dict(stop=D["rerun"].get("stop356"), knobs={k: round(v, 3) for k, v in D["line_knobs"].items() if k in ("s16", "g8", "g4", "glong", "run", "on16")})
# 389: runs among sixteenth-position onsets, by the band of the section; pushes
bands = D["rerun"].get("section_bands372"); rr = D["rerun"].get("run_rates389", {}); nb = collections.Counter(); rb = collections.Counter(); n6 = r6 = p6 = 0
for b in Al:
    ns = nts(b)
    for s_ in P.SUNG:
        ons = sorted({n["on"] for n in ns if n["sec"] == s_}); S_ = set(ons); bd = P.SEC_BAND[s_]
        for t in ons:
            if t % 6 == 3: nb[bd] += 1; rb[bd] += (t - 3) in S_ and (t + 3) in S_
    for s_ in ("Verse 1", "Chorus 1"):
        ons = sorted({n["on"] for n in ns if P.BAR0[s_] * BAR <= n["on"] < (P.BAR0[s_] + 8) * BAR}); S_ = set(ons)
        for t in ons:
            if t % 6 == 3: n6 += 1; r6 += (t - 3) in S_ and (t + 3) in S_; p6 += (t + 3) not in S_
r["389"] = dict(by_band={bd: dict(onsets=nb[bd], in_runs=round(rb[bd] / max(1, nb[bd]), 3), kept=(rr.get("kept") or {}).get(bd), rate=(rr.get("rate") or {}).get(bd)) for bd in sorted(nb)},
                pushed=round(p6 / max(1, n6), 3), in_runs_windows=round(r6 / max(1, n6), 3),
                rhythm_deaths=D["deaths"].get("rhythm: no placement", 0), join_deaths=sum(v for k, v in D["deaths"].items() if k.startswith("join")),
                fallbacks={k: v for k, v in st.items() if k.startswith("389") or k.startswith("366: fallback")}, may_run=st.get("366: lines drawn that may run", 0), may_not=st.get("366: lines drawn that may not run", 0))
W = D["would"]
r["394"] = dict(memory_breaks=W.get("limit broken: memory", 0), surprisal_breaks=W.get("limit broken: surprisal", 0), rhythm_band_breaks=W.get("limit broken: rhythm band", 0),
                stats={k: v for k, v in st.items() if k.startswith("394")})
# 399: a sung note on the downbeat of the section's first bar (begun there, or reached after a pickup)
def on_first_beat(ns, s_):
    t0 = P.BAR0[s_] * BAR
    return any(n["on"] == t0 for n in ns if n["sec"] == s_)                              # the window's first onset on the downbeat (kept 69%)
r["399"] = {s_: round(float(np.mean([on_first_beat(nts(b), s_) for b in Al])), 3) for s_ in ("Verse 1", "Chorus 1")} | dict(kept=0.69, test=(0.59, 0.79),
           stats={k: v for k, v in st.items() if k.startswith("399")})
r["401"] = dict(distinct_durations_median=med_of("distinct_durations"), kept=4, stats={k: v for k, v in st.items() if k.startswith("401") or k.startswith("343")})
r["398"] = dict(chord_tones=med_of("chord_tones"), on_beat=med_of("chord_tones_on_beat"), on_downbeat=med_of("chord_tones_on_downbeat"), resolved_by_step=mean_of("non_chord_resolved_by_step"),
                knobs={k: round(v, 3) for k, v in D["line_knobs"].items() if k.startswith("ct398") or k in ("res398",)}, stats={k: v for k, v in st.items() if k.startswith("398")})
vt = [b["read"]["v"]["turns_per_move"] for b in Al if b["read"]["v"].get("turns_per_move") is not None]; ct = [b["read"]["c"]["turns_per_move"] for b in Al if b["read"]["c"].get("turns_per_move") is not None]
r["400"] = dict(verse=round(float(np.mean(vt)), 3), chorus=round(float(np.mean(ct)), 3), kept=0.58, knob=round(D["line_knobs"].get("turn400", 1.0), 3))
json.dump(r, open(OUT, "w"), indent=1, default=str)
print(json.dumps({k: r[k] for k in ("song", "step", "made", "survivors", "order")}), "| outside", r["385"]["outside_scale"], "| clashes", r["386"]["clashes"], "| rhythm deaths", r["389"]["rhythm_deaths"],
      "| memory", r["394"]["memory_breaks"], "| 399", r["399"]["Verse 1"], r["399"]["Chorus 1"], "| dd", r["401"]["distinct_durations_median"])
