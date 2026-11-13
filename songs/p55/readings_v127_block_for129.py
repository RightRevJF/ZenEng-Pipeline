# ---- v127 Run 2 (exec'd after the v124 block): the refit judge (470-473), 464, 459; Parts 1-3's own readings are in reread_v127.py ----
from scipy.stats import spearmanr as _sp
ev_ = [c for c in D["every"] if c.get("judge") and "refit_content" in c["judge"]]
rc_ = np.array([c["judge"]["refit_content"] for c in ev_]); oc_ = np.array([c["judge"]["content"] for c in ev_])
r["470"] = dict(complete_builds=len(ev_), refit_content_mean=round(float(rc_.mean()), 3) if len(rc_) else None, survivors_refit_mean=round(float(np.mean([b["judge"]["refit_content"] for b in Al if "refit_content" in b["judge"]])), 3),
                v108_content_mean=round(float(oc_.mean()), 3) if len(oc_) else None, rank_correlation=round(float(_sp(rc_, oc_).correlation), 3) if len(rc_) > 2 else None,
                kept="kept songs' median 1.97, 5th percentile -0.51 (Window 146)", held="printed")
r["471"] = dict(under_kept_5th=round(float(np.mean(rc_ < -0.51)), 3) if len(rc_) else None, floor_deaths_v108=D["deaths"].get("the judge's floor (254; 279)", 0),
                rule="the floor moves to the refit when the share is under a third on every song", held=("floor stays on the v108 judge" if len(rc_) and np.mean(rc_ < -0.51) >= 1 / 3 else "under a third on this song"))
pr_ = D.get("pick_ranks") or {}
r["472"] = dict(pick=D["pick"]["fp"] if D.get("pick") else None, **pr_, same=bool(pr_ and pr_.get("v108_pick") == pr_.get("refit_pick")), held="printed")
r["473"] = dict(note="the judge reads the first eight bars of Verse 1 and Chorus 1 only; verse 2 answers to 434's test", held="n/a")
r["464"] = (dict(deaths267=D["deaths"].get("returns related (267)", 0), v118=(BASE[v]["deaths"].get("returns related (267)", 0) if v in BASE else None),
                 before=(OLD[v]["deaths"].get("returns related (267)", 0) if v in OLD else None),
                 held=bool(D["deaths"].get("returns related (267)", 0) <= (BASE[v]["deaths"].get("returns related (267)", 0) if v in BASE else 33)))
            if SONG_ == "45" else dict(note="song 45 only", held="n/a"))
if SONG_ == "45": r["412"]["held"] = r["464"]["held"]
r["459"] = dict(r["415"], rule="bars whose syllable counts differ by one or less") if "share" in r["415"] else dict(r["415"])
# 456 (amends 424): the last-note test on windows whose last note the walk chose; the rest printed by source
wk_ = {k_: v_ for k_, v_ in r["409"]["by_source"].items() if k_.endswith("the walk")}
nw_ = sum(v_[0] for v_ in wk_.values()); tw_ = sum(v_[0] * v_[1] for v_ in wk_.values()) / max(1, nw_)
lo456, hi456 = r["409"]["collections"]; ok456 = lo456 <= tw_ <= hi456 or min(abs(tw_ - lo456), abs(tw_ - hi456)) <= 0.2 * sd_of("last_note_tonic")
r["456"] = dict(walked_windows=nw_, walked_tonic=round(tw_, 4), collections=(lo456, hi456), by_source=r["409"]["by_source"],
                held=(bool(ok456) if nw_ >= 100 else f"n/a: {nw_} walked windows (under 100)"))
