import os
# ---- v124 Run 1 (exec'd inside readings_v124.py's loop over the runs, after the v119 block: D, Al, st, r, v, P, M, nts, pct, spread, OLD, BASE are in scope) ----
# 405: 389's runs read on the lines drawable without runs; the others counted apart
cat_n = collections.Counter(); cat_r = collections.Counter()
for b in Al:
    ns_ = nts(b); dr_ = (b["meta"].get("drawable405") or {})
    for s_ in P.SUNG:
        sn_ = [n for n in ns_ if n["sec"] == s_]; S_ = {n["on"] for n in sn_}; bd_ = P.SEC_BAND[s_]; seen_ = set()
        for n in sorted(sn_, key=lambda n: n["on"]):
            t_ = n["on"]
            if t_ in seen_ or t_ % 6 != 3: continue
            seen_.add(t_); c_ = "drawable" if dr_.get(n["line"]) is True else "no room or fell back" if n["line"] in dr_ else "not drawn by the rhythm (copy, return, design)"
            cat_n[(bd_, c_)] += 1; cat_r[(bd_, c_)] += (t_ - 3) in S_ and (t_ + 3) in S_
rr_ = D["rerun"].get("run_rates389") or {}
b405 = {}
for bd_ in sorted({k_[0] for k_ in cat_n}):
    b405[bd_] = dict(kept=(rr_.get("kept") or {}).get(bd_), rate=(rr_.get("rate") or {}).get(bd_),
                     **{c_: (cat_n[(bd_, c_)], round(cat_r[(bd_, c_)] / max(1, cat_n[(bd_, c_)]), 3)) for c_ in ("drawable", "no room or fell back", "not drawn by the rhythm (copy, return, design)")})
lines405 = {k_: v_ for k_, v_ in st.items() if k_.startswith("405")}
rd45_ = D["deaths"].get("rhythm: no placement", 0)
h405 = all(abs(x_["drawable"][1] - x_["kept"]) <= 0.10 for x_ in b405.values() if x_["drawable"][0] >= 200 and x_["kept"] is not None)
if SONG_ == "45": h405 = bool(h405 and abs(rd45_ - 0) <= 2 * max(1.0, spread(rd45_, 0)))
r["405"] = dict(by_band=b405, lines=lines405, rhythm_deaths=rd45_, rhythm_deaths_before=(OLD[v]["deaths"].get("rhythm: no placement", 0) if v in OLD else None), held=bool(h405))
r["389"]["held"] = r["405"]["held"]; r["389"]["read_on"] = "drawable lines (405)"
# 428: empty bars printed, not aimed; 378's slot share beside them
ebm = wmean("empty_bars")
r["428"] = dict(empty_bars=round(ebm, 3) if ebm is not None else None, cocopops=EVM["empty_bars"]["cocopops"], bimmuda=EVM["empty_bars"]["bimmuda"],
                slot_share_378=r["391"]["median_share_by_notes_drawn"], redraws=st.get("424: redrawn to leave the slot's last bar empty", 0), knob=(D["rerun"].get("knobs424") or {}).get("eb424"), held="printed")
r424_ = r["424"]["aims"]; r424_["empty_bars"]["agreed"] = False; r424_["empty_bars"]["note"] = "printed (428)"
r["424"]["held"] = bool(all(x_["held"] for m_, x_ in r424_.items() if x_["agreed"] and m_ != "empty_bars"))
# 409: where the window's last note comes from, and the tonic share by source
def rule_end(sec_, i_): return any(not P.end_ok(sec_, i_, p_) for p_ in range(36, 90))
src409 = collections.Counter(); ton409 = collections.Counter()
for b in Al:
    ns_ = nts(b); car_ = b["meta"].get("carriers") or {}
    for s_ in ("Verse 1", "Chorus 1"):
        a_ = P.BAR0[s_] * BAR; W_ = [n for n in ns_ if a_ <= n["on"] < a_ + 8 * BAR]
        if not W_: continue
        n = max(W_, key=lambda n: n["on"]); sec_, i_ = n["line"].rsplit(":", 1); i_ = int(i_); kd_ = str(kind_of(b, n["line"]))
        ln_ = [m for m in ns_ if m["line"] == n["line"]]; is_last = n["on"] == max(m["on"] for m in ln_)
        if sec_ != s_: c_ = "the next section's pickup"
        elif kd_ == "design": c_ = "a design"
        elif not kd_.startswith("fresh"): c_ = "a copy or return"
        elif is_last and rule_end(sec_, i_): c_ = "an ending rule"
        elif any(x_ and x_[0] and tuple(x_[0]) == (sec_, i_) and n["p"] == x_[1] for x_ in car_.values()): c_ = "a carried extreme (329)"
        else: c_ = "the walk"
        src409[(s_, c_)] += 1; ton409[(s_, c_)] += (n["p"] - ETON) % 12 == 0
by409 = {f"{s_}: {c_}": (src409[(s_, c_)], round(ton409[(s_, c_)] / src409[(s_, c_)], 3)) for s_, c_ in sorted(src409)}
walked = sum(v_ for (s_, c_), v_ in src409.items() if c_ == "the walk") / max(1, sum(src409.values()))
ltm = wmean("last_note_tonic"); lo409, hi409 = sorted((EVM["last_note_tonic"]["cocopops"], EVM["last_note_tonic"]["bimmuda"]))
ok409 = lo409 <= ltm <= hi409 or min(abs(ltm - lo409), abs(ltm - hi409)) <= 0.2 * sd_of("last_note_tonic")
r["409"] = dict(last_note_tonic=round(ltm, 4), collections=(lo409, hi409), by_source=by409, walked_share=round(walked, 3), knob=(D["rerun"].get("knobs424") or {}).get("lt424"),
                weighted={k_: v_ for k_, v_ in st.items() if k_.startswith("409")},
                held=(bool(ok409) if walked >= 0.5 else f"n/a: endings designed (walked {walked:.0%} of windows); on the tonic {ltm:.1%}"))
# 412: 398 on drawn notes only; 267's deaths; the cause found (450) read in the diagnostic run
d267 = D["deaths"].get("returns related (267)", 0); b267 = BASE[v]["deaths"].get("returns related (267)", 0) if v in BASE else None; o267 = OLD[v]["deaths"].get("returns related (267)", 0) if v in OLD else None
dg_ = f"{PRE}_main_diag450.pkl"
d450 = pickle.load(open(dg_, "rb"))["deaths"].get("returns related (267)", 0) if (v == "main" and os.path.exists(dg_)) else None
r["412"] = dict(deaths267=d267, v119=o267, v118=b267, diag450=d450, knobs398=D["rerun"].get("knobs398_400"), lift_fails=r.get("377", {}).get("lift_fails"),
                held=(bool(abs(d267 - b267) <= 2 * max(1.0, spread(d267, b267)) and (r["377"].get("lift_fails") or 0) < 0.05) if (SONG_ == "45" and b267 is not None) else "reading (song 45's test)"))
# 413: the unit returns on the free units, the losses counted
r["413"] = dict(free_units=r["390"]["free_units"], losses={k_: v_ for k_, v_ in st.items() if k_.startswith("413") or k_.startswith("361: unit return given up") or k_.startswith("361: unit bars copied")},
                held=r["390"]["held"])
# 414: spans given up
r["414"] = dict(given_up=r["391"]["given_up"], given_up_share=r["391"]["given_up_share"], drawn_to_a_span=r["391"]["drawn_to_a_span"], widened=r["391"]["widened"],
                median_share_by_notes_drawn=r["391"]["median_share_by_notes_drawn"], density={k_: v_ for k_, v_ in st.items() if k_.startswith("414")}, held=bool(r["391"]["given_up_share"] < 0.05))
# 415: verse 2's share on the bars where the verses carry the same count of syllable onsets
if "Verse 2" in P.SUNG:
    def sh415(b):
        ns_ = nts(b); a_, c_, sa_, sc_ = collections.defaultdict(set), collections.defaultdict(set), collections.Counter(), collections.Counter(); seen_ = set()
        for n in ns_:
            if n["sec"] not in ("Verse 1", "Verse 2"): continue
            k_ = n["on"] // BAR - P.BAR0[n["sec"]]; (a_ if n["sec"] == "Verse 2" else c_)[k_].add(n["on"] % BAR)
            if (n["line"], n["syl"]) not in seen_: seen_.add((n["line"], n["syl"])); (sa_ if n["sec"] == "Verse 2" else sc_)[k_] += 1
        keep_ = [k_ for k_ in a_ if k_ in c_ and abs(sa_[k_] - sc_[k_]) <= 1]   # 459: counts within one
        return (sum(1 for k_ in keep_ if len(a_[k_] ^ c_[k_]) <= 1) / len(keep_) if keep_ else None, len(keep_) / max(1, len(a_)))
    X415 = [sh415(b) for b in Al]; sh_ = [x_[0] for x_ in X415 if x_[0] is not None]; rd_ = [x_[1] for x_ in X415]
    r["415"] = dict(share=pct(sh_) if sh_ else None, bars_read=pct(rd_), builds_with_no_bar=sum(1 for x_ in X415 if x_[0] is None), rate=D["rerun"].get("rate293"),
                    held=(bool(np.median(rd_) >= 0.5 and sh_ and abs(np.median(sh_) - 0.5) <= 0.10) if v == "main" else bool(np.median(rd_) >= 0.5)))
    for k_ in ("313", "331", "393"):
        if k_ in r: r[k_]["held"] = r["415"]["held"]; r[k_]["read_on"] = "bars of equal syllables (415)"
else: r["415"] = dict(note="no verse 2", held="n/a")
# 417: 311 reads the last chorus where one exists; a designed tag apart
LC_ = "Last Chorus" if (P.KIND.get(LASTSEC) == "Tag" and "Last Chorus" in P.SUNG) else LASTSEC   # 417: a designed tag is read apart
EN_ = []; TG_ = []
for b in Al:
    lc_ = [n for n in nts(b) if n["sec"] == LC_]
    if lc_: EN_.append(((lc_[-1]["p"] + LIFT_(LC_)) - (ETON + LIFT_(LC_))) % 12 == 0)
    if LASTSEC != LC_:
        tg_ = [n for n in nts(b) if n["sec"] == LASTSEC]
        if tg_: TG_.append((tg_[-1]["p"] - ETON) % 12)
r["311"]["last_chorus_tonic"] = round(float(np.mean(EN_)), 4); r["311"]["section_read"] = LC_; r["311"]["held"] = bool(np.mean(EN_) == 1.0 and r["311"]["misses"] == 0)
r["417"] = dict(section_read=LC_, last_chorus_tonic=r["311"]["last_chorus_tonic"], tag=(LASTSEC, dict(collections.Counter(TG_).most_common(4))) if TG_ else "no tag", held=r["311"]["held"])
r["395"]["last_chorus_tonic"] = r["311"]["last_chorus_tonic"]; r["395"]["last_section"] = LC_; r["395"]["held"] = (r["311"]["held"] and r["324"]["held"] is not False) if LIFTED else "n/a (no lift)"
# 419: 375 and 386's clash read on the chord at the note (M.chord_for), and the notes with no move printed
v419 = 0; s419 = 0; ex419 = []; k419 = collections.Counter()
for b in Al:
    ns_ = nts(b); on_ = {n["on"] for n in ns_}
    for n in ns_:
        if n["on"] % BEAT and n["dur"] < 12: continue
        ch_ = M.chord_for(n, on_); tones_ = M.CH[ch_][1]; out_ = [t_ for t_ in tones_ if t_ not in M.SCALE]
        if not out_: continue
        s419 += 1
        if any((n["p"] - t_) % 12 in (1, 11) for t_ in out_) and n["p"] % 12 not in tones_:
            v419 += 1; k419[str(kind_of(b, n["line"]))] += 1
            if len(ex419) < 8: ex419.append((n["line"], n["on"], n["p"], ch_, str(kind_of(b, n["line"]))))
r["419"] = dict(notes_read=s419, clashes=v419, by_kind=dict(k419), examples=ex419, bar_chord_reading=r["375"]["semitone_from_a_raised_tone"], held=bool(v419 == 0))
r["386"]["held"] = r["419"]["held"]; r["386"]["clashes_at_the_note"] = v419
r["384"]["smoke"] = "smoke/ (40 builds a song, every patched path; 415's path read on the calibration rounds)"
