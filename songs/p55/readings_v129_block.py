# ---- v129 (exec'd after the v128 block): 500-505, 508, 513, 519, 520 and the range beside each song's design ----
SL9 = dict(P.SL465) if hasattr(P, "SL465") else {}
def slot_key9(nb_): return next(k_ for k_, s_ in P.SL465 if nb_ * 4 <= k_)
cls9 = collections.defaultdict(collections.Counter); ob9 = collections.defaultdict(list)
for b in [b for b in D["every"] if not b.get("partial")][:400]:
    Lm = collections.OrderedDict()
    for t in sorted(b["notes"]): Lm.setdefault(t[4], []).append(t)
    ks_ = list(Lm)
    for a_, c_ in zip(ks_, ks_[1:]):
        A_, B_ = Lm[a_], Lm[c_]
        if len(A_) < 3 or A_[0][3] != B_[0][3]: continue
        sec_, i_ = a_.rsplit(":", 1); nb_ = P.slot_len(sec_, int(i_))
        cls9[(nb8(len(A_)), nb_)][min(3, B_[0][0] // 48 - A_[-1][0] // 48)] += 1
        sp9 = (A_[-1][0] - A_[0][0]) / 12
        if sp9 > 0: ob9[nb8(len(A_))].append((len(A_) - 1) / sp9)
NBK9 = ("3 to 5", "6 to 8", "9 to 12", "13 and over"); NIDX = {k_: j_ for j_, k_ in enumerate(NBK9)}
r500 = {}
for (b_, nb_), cn_ in sorted(cls9.items(), key=lambda kv: (NIDX[kv[0][0]], kv[0][1])):
    tot_ = sum(cn_.values())
    if tot_ < 100: continue
    sn_ = K465[b_][KCL]; sn_ = [sn_[x] for x in ("0", "1", "2", "3 or more")]; ss_ = dict(P.SL465)[slot_key9(nb_)]
    kc_ = [a * s / max(1e-9, p) for a, s, p in zip(sn_, ss_, P.PALL465)]; z_ = sum(kc_); kc_ = [x / z_ for x in kc_]
    r500[f"{b_} notes, {nb_}-bar slot"] = dict(lines=tot_, classes=[round(cn_[j] / tot_, 3) for j in range(4)], kept=[round(x, 3) for x in kc_])
oor9 = {k_: v_ for k_, v_ in st.items() if k_.startswith("500: class")}
far9 = max((max(abs(a - c) for a, c in zip(x_["classes"], x_["kept"])) for x_ in r500.values() if x_["lines"] >= 200), default=None)
r["500"] = dict(by_notes_and_slot=r500, out_of_reach=dict(sorted(oor9.items(), key=lambda kv: -kv[1])[:8]), out_of_reach_total=sum(oor9.values()),
                given_up=st.get("465: class given up for a line", 0), drawn=sum(v_ for k_, v_ in st.items() if k_.startswith("465: class ") and k_.endswith(" drawn")), widest_gap=far9,
                held=bool(far9 is not None and far9 <= 0.10 and st.get("465: class given up for a line", 0) / max(1, sum(v_ for k_, v_ in st.items() if k_.startswith("465: class ") and k_.endswith(" drawn"))) < 0.05))
r501 = {}
for b_ in NBK9:
    if len(ob9[b_]) < 20: continue
    q_ = dict(P.OB501)[{"3 to 5": 5, "6 to 8": 8, "9 to 12": 12, "13 and over": 999}[b_]]
    r501[b_] = dict(lines=len(ob9[b_]), onsets_a_beat=pct(ob9[b_], (25, 50, 75)), kept=q_[1:4])
r["501"] = dict(by_notes=r501, inside=st.get("501: line inside the kept onsets a beat", 0), redrawn=st.get("501: outside the kept onsets a beat, redrawn", 0), given_up=st.get("501: onsets a beat given up for a line", 0),
                held=bool(r501 and all(x_["kept"][0] <= x_["onsets_a_beat"][1] <= x_["kept"][2] for x_ in r501.values() if x_["lines"] >= 200)))
dd9 = sum(v_ for k_, v_ in D["deaths"].items() if k_.startswith("design"))
r["502"] = dict(design_deaths=dd9, survivors=D["survivors"], held=bool(dd9 < 50)) if SONG_ == "45" else dict(note="song 45 only", held="n/a")
c1_, c2_ = [], []
if "Verse 2" in P.SUNG:
    for b in [b for b in D["every"] if not b.get("partial")][:400]:
        ns_ = nts(b); f1_, f2_ = P.win_feats(ns_, P.BAR0["Verse 1"]), P.win_feats(ns_, P.BAR0["Verse 2"])
        if f1_ and f2_ and np.isfinite(f1_.get("chord_tones_on_beat", np.nan)) and np.isfinite(f2_.get("chord_tones_on_beat", np.nan)): c1_.append(f1_["chord_tones_on_beat"]); c2_.append(f2_["chord_tones_on_beat"])
k9 = D["rerun"].get("knobs129") or {}
r["503"] = (dict(verse1=round(float(np.mean(c1_)), 3), verse2=round(float(np.mean(c2_)), 3), knob=k9.get("ctb503"), held=bool(abs(np.mean(c2_) - np.mean(c1_)) <= 0.05)) if c1_ else dict(note="no second verse", held="n/a"))
r["504"] = dict(notes_to_syllables=k9.get("mel504"), knobs=(D["rerun"].get("knobs128") or {}).get("b489"), held="read in the reread, by density band")
r["505"] = dict(rates_389=k9.get("runr"), run_weights=(D["rerun"].get("knobs128") or {}).get("r490"), drawable_runs={b_: (x_["kept"], x_["drawable"]) for b_, x_ in r["405"]["by_band"].items()}, held=r["405"]["held"])
r["508"] = dict(joins_before_a_copy=D["deaths"].get("join: no held end and breath before the copy (212)", 0), joins_before_a_line=D["deaths"].get("join: no held end and breath before the line (212)", 0),
                fitted_to_the_designed_line=st.get("508: fitted to the breath of the designed line before", 0), align=D["deaths"].get("align: the words do not fit the returning tune", 0), held="printed")
c438 = D["rerun"].get("chart438")
r["513"] = (dict(reverted=c438.get("reverted513"), inversions=[x_[2] for x_ in c438.get("inversions", [])], held=r["440"]["held"]) if c438 else dict(note="the song's own chart (Run 3 left it there)", held="n/a"))
rc9 = np.array([c["judge"]["refit_content"] for c in D["every"] if c.get("judge") and "refit_content" in c["judge"]])
r["519"] = dict(table="zeneng_v129_judge.json", content_mean=round(float(rc9.mean()), 3), under_kept_song_5th=round(float(np.mean(rc9 < -0.723)), 3), kept="kept songs' mean over their windows: 5th -0.723, 25th 0.49, median 1.419",
                floor="stays on the v108 judge (under -0.72 on every song is not under a third)", held="printed")
lk9 = D.get("line_knobs") or {}; kn9 = D["rerun"].get("knobs127") or {}
r["520"] = dict(knob_408_in_run=("sh408" in lk9) or ("sh408" in kn9), knob_455_in_run=("s16_by_band" in kn9), held=bool("sh408" not in lk9 and "sh408" not in kn9 and "s16_by_band" not in kn9))
DES9 = {"40": "no designed range (the song's register and 329's carriers)", "42": "no designed range", "43": "no designed range ('blue movie' falls from the chorus's top)",
        "44": "the verse sings 6.3 semitones by its design (intake)", "45": "the chorus over the verse by Q14 A's three: the range is its lift's"}
rv9 = [b["read"]["v"]["range"] for b in Al if b["read"]["v"] and b["read"]["v"].get("range") is not None]; rcc9 = [b["read"]["c"]["range"] for b in Al if b["read"]["c"] and b["read"]["c"].get("range") is not None]
r["520"]["range"] = dict(verse=round(float(np.mean(rv9)), 2) if rv9 else None, chorus=round(float(np.mean(rcc9)), 2) if rcc9 else None, kept=10.9, design=DES9.get(SONG_, ""), held="printed (520: not aimed)")
