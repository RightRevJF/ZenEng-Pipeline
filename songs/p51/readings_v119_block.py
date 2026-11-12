# ---- v119 (exec'd inside readings_v119.py's loop over the runs: D, Al, st, r, v, P, M, nts, pct, spread are in scope) ----
FAM_ = json.load(open("/home/claude/p51/tables/zeneng_v119_families.json")); KT119 = FAM_["kept targets (398-401)"]
SONG_ = MOD.split("_p")[-1]
def wmean(m_, which=("v", "c")):
    x_ = [b["read"][w][m_] for b in Al for w in which if b["read"][w] and b["read"][w].get(m_) is not None and np.isfinite(b["read"][w][m_])]
    return float(np.mean(x_)) if x_ else None
def wmed(m_, which=("v", "c")):
    x_ = [b["read"][w][m_] for b in Al for w in which if b["read"][w] and b["read"][w].get(m_) is not None and np.isfinite(b["read"][w][m_])]
    return float(np.median(x_)) if x_ else None
def kind_of(b, line):
    sec_, i_ = line.rsplit(":", 1); return (b.get("kinds") or {}).get((sec_, int(i_)), "?")
# 384: the generators patched by whole statements (gen_v119.py asserts each match), each patched path run once in a smoke run
import os as _os
sm_ = f"/home/claude/p51/melody_v119_p{SONG_}_main_smoke3.pkl"
if _os.path.exists(sm_):
    S3 = pickle.load(open(sm_, "rb"))["stats"]
    paths_ = {"unit return": sum(v_ for k_, v_ in S3.items() if k_.startswith("361: lines drawn on a returning unit")), "refit (327/360)": sum(v_ for k_, v_ in S3.items() if k_.startswith(("327", "360: bars fitted again and kept"))),
              "span widened or given up (378, 391)": S3.get("391: span widened to the kept 5th-95th", 0) + S3.get("378: span given up (nothing fitted inside it)", 0),
              "386 move": S3.get("386: notes moved off a semitone from a chord's outside tone", 0), "389 fallback": sum(v_ for k_, v_ in S3.items() if k_.startswith("389")),
              "394": sum(v_ for k_, v_ in S3.items() if k_.startswith("394")), "424": sum(v_ for k_, v_ in S3.items() if k_.startswith("424")),
              "390": sum(v_ for k_, v_ in S3.items() if k_.startswith("390"))}
    need_ = ("unit return", "span widened or given up (378, 391)", "394", "389 fallback")     # 399 and 401 withdrawn (421)
    r["384"] = dict(patches="every patch matched exactly once in each file (gen_v119.py)", smoke_paths=paths_, held=bool(all(paths_[k_] > 0 for k_ in need_)))
else: r["384"] = dict(patches="every patch matched exactly once in each file (gen_v119.py)", smoke_paths="no smoke run on file", held="reading")
# 385: 349's target a share of all the build's notes
osm = wmean("outside_scale"); osk = 0.045 if getattr(P, "MTON", None) is not None else 0.071
r["385"] = dict(outside_scale=round(osm, 4), kept=osk, cost=r["344"]["cost"], placed=st.get("349: notes placed outside the scale", 0), wanting=st.get("349: places wanting", 0),
                passing=st.get("358: chromatic passing notes placed", 0), held=bool(abs(osm - osk) <= 0.02))
# 386: no sung note on a beat or a beat long a semitone from a chord's own outside tone, in drawn, returning or copied lines
r["386"] = dict(clashes=r["375"]["semitone_from_a_raised_tone"], notes_read=r["375"]["notes_read"], where=r["375"]["where"],
                moved={k_: v_ for k_, v_ in st.items() if k_.startswith("386")}, read_by_267="before the moves (Q1 A)", held=bool(r["375"]["semitone_from_a_raised_tone"] == 0))
r["375"]["held"] = bool(r["375"]["semitone_from_a_raised_third"] == 0)                     # 385 retires 375's places-wanting test (the target is now a share of all notes)
# 387: the stop is a reading
kn_ = {k_: round(D["line_knobs"].get(k_, 1.0), 3) for k_ in ("s16", "g8", "g4", "glong")}
r["387"] = dict(stop=D["rerun"].get("stop356") or "did not fire", knobs=kn_, held=bool(not D["rerun"].get("stop356") or any(abs(x_ - 1.0) > 1e-6 for x_ in kn_.values())))
r["388"] = dict(note="the two side runs on song 40 (step 2): see the report", held="printed")
# 389: the run rate by band; falls back before it dies
bnd = collections.Counter(); brn = collections.Counter()
for b in Al:
    ns_ = nts(b)
    for s_ in P.SUNG:
        ons_ = sorted({n["on"] for n in ns_ if n["sec"] == s_}); S_ = set(ons_); bd_ = P.SEC_BAND[s_]
        for t_ in ons_:
            if t_ % 6 == 3: bnd[bd_] += 1; brn[bd_] += (t_ - 3) in S_ and (t_ + 3) in S_
rr_ = D["rerun"].get("run_rates389") or {}
byb = {bd_: dict(onsets=bnd[bd_], in_runs=round(brn[bd_] / max(1, bnd[bd_]), 3), kept=(rr_.get("kept") or {}).get(bd_), rate=(rr_.get("rate") or {}).get(bd_)) for bd_ in sorted(bnd)}
rdth = D["deaths"].get("rhythm: no placement", 0); rold = OLD[v]["deaths"].get("rhythm: no placement", 0) if v in OLD else None
V116_RHY = {"45": 0}                                                                      # song 45's v116 runs (songs/p49): no rhythm-placement deaths
base_ = V116_RHY.get(SONG_, rold)
r["389"] = dict(by_band=byb, rhythm_deaths=rdth, v118=rold, v116=V116_RHY.get(SONG_), fallbacks={k_: v_ for k_, v_ in st.items() if k_.startswith("389") or k_.startswith("366: fallback")},
                join_deaths=sum(v_ for k_, v_ in D["deaths"].items() if k_.startswith("join")),
                held=bool(all(abs(x_["in_runs"] - x_["kept"]) <= 0.10 for x_ in byb.values() if x_["onsets"] >= 200 and x_["kept"] is not None)
                          and (base_ is None or abs(rdth - base_) <= 2 * max(1.0, spread(rdth, base_)))))
# 390: unit returns read on the units free to draw
KUR_ = {1: ("unit2_returns", 0.172), 2: ("unit3_returns", 0.315), 3: ("unit4_to_unit2", 0.188)}
free_ = {}; given_n = collections.Counter(); tot_n = collections.Counter()
for j_, (m_, kp_) in KUR_.items():
    vals_ = []
    for b in Al:
        g_ = (b["meta"].get("ur_given") or {})
        for w, kd_ in (("v", "Verse"), ("c", "Chorus")):
            f_ = b["read"][w]
            if not f_ or f_.get(m_) is None or not np.isfinite(f_[m_]): continue
            tot_n[j_] += 1
            if (g_.get(kd_) or {}).get(j_) or (g_.get(kd_) or {}).get(str(j_)): given_n[j_] += 1; continue
            vals_.append(f_[m_])
    free_[m_] = dict(free_mean=round(float(np.mean(vals_)), 3) if vals_ else None, kept=kp_, free_share=round(1 - given_n[j_] / max(1, tot_n[j_]), 3))
r["390"] = dict(free_units=free_, rates=D["rerun"].get("unit_return_rates371"), plan_given={k_: v_ for k_, v_ in st.items() if k_.startswith("390")},
                held=bool(all(x_["free_mean"] is None or abs(x_["free_mean"] - x_["kept"]) <= 0.10 for x_ in free_.values())))
r["371"]["held"] = r["390"]["held"]; r["371"]["free_units"] = free_
# 391: 378 read on drawn lines; spans widened before they are given up
def spans_drawn(b):
    byl = collections.OrderedDict()
    for n in sorted(nts(b), key=lambda n: n["on"]): byl.setdefault(n["line"], []).append(n)
    out = []
    for sec_ in P.SUNG:
        for j in range(len(P.LINES[sec_]) - 1):
            a_, b_ = byl.get(f"{sec_}:{j}"), byl.get(f"{sec_}:{j + 1}")
            if not a_ or not b_: continue
            if not str(kind_of(b, f"{sec_}:{j}")).startswith("fresh"): continue
            slot_ = b_[0]["on"] - a_[0]["on"]
            if slot_ <= 0: continue
            out.append((len(a_), len({n["syl"] for n in a_}), (a_[-1]["on"] + a_[-1]["dur"] - a_[0]["on"]) / slot_, slot_))
    return out
spd = [x for b in Al for x in spans_drawn(b)]
KSP_ = {"3-5": (0.429, 0.75), "6-8": (0.531, 0.80), "9-12": (0.656, 0.875), "13+": (0.783, 0.938)}
def grp2(nn): return "3-5" if nn <= 5 else "6-8" if nn <= 8 else "9-12" if nn <= 12 else "13+"
medd = {g_: round(float(np.median([x[2] for x in spd if grp2(x[0]) == g_])), 3) for g_ in KSP_ if sum(1 for x in spd if grp2(x[0]) == g_) >= 30}
fulld = [x for x in spd if x[1] * 6 >= 0.5 * x[3]]; underd = float(np.mean([x[2] < 0.5 for x in fulld])) if fulld else 0.0
dts = st.get("378: lines drawn to a span", 0); gup = st.get("378: span given up (nothing fitted inside it)", 0)
r["391"] = dict(median_share_by_notes_drawn=medd, lines_drawn=len(spd), under_half_of_full=round(underd, 3), widened=st.get("391: span widened to the kept 5th-95th", 0),
                drawn_to_a_span=dts, given_up=gup, given_up_share=round(gup / max(1, dts + gup), 3), all_lines=r["378"]["median_share_by_notes"],
                held=bool(all(KSP_[g_][0] <= x_ <= KSP_[g_][1] for g_, x_ in medd.items()) and gup / max(1, dts + gup) < 0.05))
r["378"]["held"] = r["391"]["held"]
# 392: the chorus floor for drawn notes (song 45)
r["392"] = (dict(lift_fails=r["377"].get("lift_fails"), drawn=r["377"].get("drawn_minus_verse"), pinned=r["377"].get("pinned_minus_verse"), held=r["377"]["held"])
            if "lift_fails" in r["377"] else dict(note="no pinned notes in this song", held="n/a"))
# 393: verse 2's share on the lines with verse 1's syllable count
if "313" in r:
    r["393"] = dict(equal_lines=r["313"]["equal_lines"], share_equal=r["313"]["share"], share_other=r["313"]["share_other_lines"], share_all=r["313"]["share_all_lines"],
                    held=("n/a (no verse 2 line has verse 1's syllable count)" if not r["313"]["equal_lines"] else bool(abs(r["313"]["share"][1] - 0.5) <= 0.10) if v == "main" else "main run only"))
    for k_ in ("338", "351", "360", "370"):
        if k_ in r and v == "main" and isinstance(r["393"]["held"], bool): r[k_]["held"] = r["393"]["held"] if k_ != "351" else bool(r["393"]["held"] and r["351"].get("share_given_up", 0) < 0.10)
else: r["393"] = dict(note="no verse 2", held="n/a")
# 394: memory breaks
def mem_b(Dx): return sum(1 for b in Dx["all"] if (b["info"].get("limits7") or {}).get("memory", 1.0) is not None and (b["info"].get("limits7") or {}).get("memory", 1.0) < 0.12)
mn_ = mem_b(D); mo_ = mem_b(OLD[v]) if v in OLD else None
r["394"] = dict(memory_breaks=mn_, v118=mo_, stats={k_: v_ for k_, v_ in st.items() if k_.startswith("394")},
                v114=r.get("368", {}).get("v114"), held=(r["368"]["held"] if "368" in r else "reading"))
if "368" in r: r["368"]["memory_breaks_now"] = mn_; r["368"]["held"] = bool(abs(mn_ - r["368"]["v114"]) <= 2 * spread(mn_, r["368"]["v114"]))
if "368" in r: r["394"]["held"] = r["368"]["held"]
# 395: 311 and 324 read in the section's own key where the record lifts it
r["395"] = dict(lifted=sorted(LIFTED) or "none", last_section=LASTSEC, last_chorus_tonic=r["311"]["last_chorus_tonic"], tonic_endings=r["324"]["tonic_endings"],
                held=(r["311"]["held"] and r["324"]["held"] is not False) if LIFTED else "n/a (no lift)")
# 398: chord tones at the kept rates
ctm, ctb, ctd, rsm = wmed("chord_tones"), wmed("chord_tones_on_beat"), wmed("chord_tones_on_downbeat"), wmean("non_chord_resolved_by_step")
r["398"] = dict(chord_tones=round(ctm, 3), on_beat=round(ctb, 3), on_downbeat=round(ctd, 3) if ctd is not None else None, resolved_by_step=round(rsm, 3),
                kept=dict(chord_tones=0.639, on_beat=0.669, on_downbeat=0.722, resolved_by_step=0.501), knobs=D["rerun"].get("knobs398_400"),
                held=bool(0.54 <= ctm <= 0.76 and 0.56 <= ctb <= 0.80 and abs(rsm - 0.50) <= 0.10))
# 399: a section opens on its downbeat
def open_db(b, s_):
    t0 = P.BAR0[s_] * BAR; return any(n["on"] == t0 for n in nts(b) if n["sec"] == s_)
FIXR_ = getattr(P, "FIXR", {}) or {}
dsg = {s_: (1.0 if (s_, 0) in FIXR_ else float(np.mean([str(kind_of(b, f"{s_}:0")) == "design" or not str(kind_of(b, f"{s_}:0")).startswith(("fresh", "?")) for b in Al]))) for s_ in ("Verse 1", "Chorus 1")}   # a design places the entry
o399 = {s_: round(float(np.mean([open_db(b, s_) for b in Al])), 3) for s_ in ("Verse 1", "Chorus 1")}
r["399"] = dict(shares=o399, kept=0.69, test=[0.59, 0.79], first_line_not_drawn_free=dsg, stats={k_: v_ for k_, v_ in st.items() if k_.startswith("399")},
                held=bool(all(0.59 <= o399[s_] <= 0.79 or dsg[s_] > 0.5 for s_ in o399)))
# 400: turns per move
tv, tc = wmean("turns_per_move", ("v",)), wmean("turns_per_move", ("c",))
r["400"] = dict(verse=round(tv, 3), chorus=round(tc, 3), kept=0.584, knob=(D["rerun"].get("knobs398_400") or {}).get("turn400"), held=bool(abs(tv - 0.584) <= 0.04 and abs(tc - 0.584) <= 0.04))
# 401: four note lengths
ddm_ = wmed("distinct_durations")
r["401"] = dict(distinct_durations_median=ddm_, kept=4, shortened=st.get("401: a note shortened to the palette", 0), shorter_than_palette=st.get("401: a note shorter than the palette allows (kept as drawn)", 0),
                held=bool(ddm_ == 4))
r["396"] = dict(note="separability by family: sep_v119.py, across the five songs", held="below")
# ---- v120: tests, costs and separation on the 30 agreed measures, against both kept collections pooled (420, 422); 399 and 401 withdrawn (421) ----
SC120 = json.load(open("/home/claude/p51/tables/zeneng_v120_second_collection.json")); A30 = SC120["the 30 agreed measures (420, 422)"]
EVM = {x_["measure"]: x_ for x_ in SC120["every measure: collections' gap in sd, means (CoCoPops, BiMMuDa 1958-1991, builds v118)"]}
BW120 = json.load(open("/home/claude/p51/tables/zeneng_v120_bimmuda_windows.json"))
def pooled(m_): return round((314 * EVM[m_]["cocopops"] + 231 * EVM[m_]["bimmuda"]) / 545, 4)
def sd_of(m_): return abs(EVM[m_]["cocopops"] - EVM[m_]["bimmuda"]) / max(1e-6, abs(EVM[m_]["collections"]))
def both(m_): return dict(cocopops=EVM[m_]["cocopops"], bimmuda=EVM[m_]["bimmuda"], builds=round(wmean(m_), 4) if wmean(m_) is not None else None)
# 340/347 on the agreed 30: a judge fitted on both collections pooled against this run's builds
from sklearn.linear_model import LogisticRegression as _LR
KC_ = np.array([[row_.get(m_, np.nan) for m_ in A30] for row_ in P.KRW], float); KB_ = np.array([[np.nan if x_ is None else x_ for x_ in rw_] for rw_ in BW120["rows"]], float)
K_ = np.vstack([KC_, KB_]); cm_ = np.nanmean(K_, 0); K_ = np.where(np.isfinite(K_), K_, cm_)
B_ = np.array([[f_.get(m_, np.nan) if f_.get(m_) is not None else np.nan for m_ in A30] for b in Al for w in ("v", "c") if (f_ := b["read"][w])], float); B_ = np.where(np.isfinite(B_), B_, cm_)
X_ = np.vstack([K_, B_]); mu2, sd2 = X_.mean(0), X_.std(0) + 1e-9
lr2 = _LR(C=1.0, max_iter=5000, class_weight="balanced").fit((X_ - mu2) / sd2, np.r_[np.ones(len(K_)), np.zeros(len(B_))])
cost2 = lr2.coef_[0] * (K_.mean(0) - B_.mean(0)) / sd2; o2 = np.argsort(-cost2)
r["340"] = dict(gap=round(float(cost2.sum()), 2), measures="the 30 agreed (420)", kept="CoCoPops and BiMMuDa 1958-1991 pooled (545 windows)", window_134=[11.0, 10.4],
                eight=[(A30[j], round(float(cost2[j]), 2), round(float(K_[:, j].mean()), 3), round(float(B_[:, j].mean()), 3)) for j in o2[:8]], held="printed")
worst2 = [(A30[j], round(float(cost2[j]), 2)) for j in o2 if cost2[j] > 0.5]
r["347"] = dict(over_half_a_point=worst2, gap=r["340"]["gap"], held=bool(not worst2))
# tests on measures the collections disagree on become readings, printed with both collections' means (420); harmony apart (422)
DIS = SC120["measures to print only (420)"]
for k_, ms_ in (("341", ("pushed", "on_sixteenth")), ("348", ("pushed", "on_sixteenth")), ("355", ("pushed", "on_sixteenth")), ("366", ("pushed", "on_sixteenth")),
                ("343", ("distinct_durations",)), ("344", ("outside_scale",)), ("349", ("outside_scale",)), ("358", ("outside_scale",)), ("385", ("outside_scale",)),
                ("346", ("on_offbeat_eighth",)), ("356", ("distinct_durations",))):
    if k_ in r: r[k_]["held"] = "reading (420)"; r[k_]["both_collections"] = {m_: both(m_) for m_ in ms_}
for k_ in ("345", "398"):
    if k_ in r: r[k_]["held"] = "printed apart (422: harmony, CoCoPops alone)"
# the gap shares: read on the sixteenth and the eighth only (the quarter and longer are among the disagreed)
gm16, gm8 = wmean("gap_sixteenth"), wmean("gap_eighth")
for k_ in ("354", "357", "365", "372"):
    if k_ in r and isinstance(r[k_].get("kept"), dict):
        kk_ = list(r[k_]["kept"].values()); r[k_]["agreed_two"] = dict(gap_sixteenth=(round(gm16, 3), kk_[0]), gap_eighth=(round(gm8, 3), kk_[1]))
        ok_ = abs(gm16 - kk_[0]) <= 0.05 and abs(gm8 - kk_[1]) <= 0.05
        r[k_]["held"] = bool(ok_ and (all(x_ == 1.0 for d_ in r["365"]["knobs249"].values() for x_ in d_.values()) if k_ == "365" else True))
# unit returns and turns per move against both collections pooled
for j_, (m_, _kp) in KUR_.items(): r["390"]["free_units"][m_]["kept_pooled"] = pooled(m_)
r["390"]["held"] = bool(all(x_["free_mean"] is None or abs(x_["free_mean"] - x_["kept_pooled"]) <= 0.10 for x_ in r["390"]["free_units"].values()))
r["371"]["held"] = r["390"]["held"]
r["400"]["kept_pooled"] = pooled("turns_per_move"); r["400"]["held"] = bool(abs(tv - pooled("turns_per_move")) <= 0.04 and abs(tc - pooled("turns_per_move")) <= 0.04)
r["399"] = dict(note="withdrawn by v120 (421); printed: " + str(o399) + " beside both collections (first onset: CoCoPops 0.37 beats, BiMMuDa 1.36)", held="withdrawn (421)")
r["401"] = dict(note=f"withdrawn by v120 (421); 343 a reading: distinct lengths {ddm_} at the median (CoCoPops 4.0, BiMMuDa 4.7)", held="withdrawn (421)")
# 424: each aim's builds' mean between the two collections' means or within a fifth of a standard deviation of the nearer
r424 = {}
for m_ in ("fourth_fifth", "last_note_tonic", "empty_bars", "outside_scale"):
    bm_ = wmean(m_); lo_, hi_ = sorted((EVM[m_]["cocopops"], EVM[m_]["bimmuda"]))
    ok_ = lo_ <= bm_ <= hi_ or min(abs(bm_ - lo_), abs(bm_ - hi_)) <= 0.2 * sd_of(m_)
    r424[m_] = dict(builds=round(bm_, 4), cocopops=EVM[m_]["cocopops"], bimmuda=EVM[m_]["bimmuda"], fifth_sd=round(0.2 * sd_of(m_), 4), held=bool(ok_), agreed=m_ in A30)
r["424"] = dict(aims=r424, knobs=D["rerun"].get("knobs424"), kept_pooled=D["rerun"].get("kept424"), stats={k_: v_ for k_, v_ in st.items() if k_.startswith("424")},
                held=bool(all(x_["held"] for m_, x_ in r424.items() if x_["agreed"])))
