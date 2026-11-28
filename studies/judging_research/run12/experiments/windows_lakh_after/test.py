"""windows_lakh_after (run 12, AFTER SEEING RESULTS): does chord repetition's link to covers sit in the LATE window on other songs?
Written after the Hooktheory WINDOWS estimate showed ch_rep: beta_E +0.06, beta_L -0.18, Delta -0.24 (analytic SE 0.072; its
bootstrap failed). Lakh whole songs (run 07's within-artist set): SEEN for y_foreign and eight chord measures (run 07) and for the
bass coupling (run 11), never for cover TIMING. A pass is a lead needing songs not yet used, never a finding.

Steps (python3 test.py run; refuses unless PREDICTION.md, this file, common12.py and harness12.py are committed, unmodified, pushed):
 1. Notes side: common12.lakh_rows() (near-duplicate files counted once), measures ch_rep (run 07's MIDI chord repetition) and REP_L.
 2. Outcome: each song's Discogs-VI clique from data/lakh_songs_discogs_run07.json; the clique's versions read from Discogs-VI
    20240701 main.zip (/home/claude/dl/discogs/main.zip, streamed, by cliques_versions.py's reduction: per performing-artist set,
    the year of its earliest track release); t0 = the clique's earliest year (as cliques_versions.py's first_year).
 3. Covers and windows by fitness.py's cover rule via common12.window_counts (own sets share a normalised name with the Lakh
    artist = the song key's artist part); N_E = ages 0-3, N_L = ages 8+; exposures from the frozen fit (common12.exposure).
 4. Songs with t0 <= 2005, artists with 2+ such songs. Per window: FE Poisson (common12.pois_fe) of N_w on z(measure), the Lakh
    controls (LAKH_BASE + LAKH_SKEPTIC, z) and five-year t0 dummies, offset log exposure. Delta = beta_L - beta_E, analytic joint
    cluster sandwich SE (as harness12.windows_fit). Halves by md5(artist) mod 2.
"""
import os, sys, json, re, math, zipfile, hashlib, collections, subprocess
import numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE); sys.path.insert(0, EXP)
import common12 as C
ZIP = "/home/claude/dl/discogs/main.zip"
ALPHA = 0.05 / 4; PRED = -0.12
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))

def guard():
    for p in (os.path.join(HERE, "PREDICTION.md"), os.path.join(HERE, "test.py"), os.path.join(EXP, "common12.py"), os.path.join(EXP, "harness12.py")):
        if not C._pushed_clean(p): raise SystemExit(f"REFUSED: {p} not committed/pushed: outcome NOT joined")

def versions_for(cliques):
    z = zipfile.ZipFile(ZIP); out = {}
    name = [n for n in z.namelist() if n.endswith(".jsonl")][0]
    with z.open(name) as f:
        for line in f:
            d = json.loads(line)
            if d["clique_id"] not in cliques: continue
            per = {}; years = []
            for v in d["versions"]:
                for t in v["tracks"]:
                    a = tuple(sorted(norm(x) for x in (t.get("track_artist_names") or t.get("release_artist_names") or [])))
                    y = re.match(r"(\d{4})", t.get("released") or ""); yy = int(y.group(1)) if y and 1890 <= int(y.group(1)) <= 2025 else None
                    if yy is not None: years.append(yy)
                    if a:
                        p = per.setdefault(a, None)
                        if yy is not None: per[a] = yy if p is None else min(p, yy)
            out[d["clique_id"]] = dict(first_year=min(years) if years else None, versions=[[list(a), y, []] for a, y in per.items()])
    return out, name

def ctrl(R):
    cols = [C._z([r[c] for r in R]) for c in C.LAKH_BASE + C.LAKH_SKEPTIC]
    b = [str(r["t0"] // 5 * 5) for r in R]; lv = sorted(set(b))
    return np.column_stack(cols + [np.array([float(x == l) for x in b]) for l in lv[1:]])

def wfit(M, m):
    g = [r["artist"] for r in M]; X = np.column_stack([C._z([r[m] for r in M]), ctrl(M)]); res = {}
    for w in ("E", "L"): res[w] = C.pois_fe([r["N_" + w] for r in M], X, np.log([r["X_" + w] for r in M]), g)
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; G = len(codes)
    def full(o): S = np.zeros((G, o["S"].shape[1])); S[o["groups_kept"]] = o["S"]; return S
    cov = (G / (G - 1)) * (res["L"]["Hi"] @ full(res["L"]).T @ full(res["E"]) @ res["E"]["Hi"])[0, 0]
    bE, bL = float(res["E"]["b"][0]), float(res["L"]["b"][0]); vE, vL = float(res["E"]["V"][0, 0]), float(res["L"]["V"][0, 0])
    d = bL - bE; se = math.sqrt(max(vL + vE - 2 * cov, 1e-12))
    return dict(delta=d, se=se, p=float(2 * stats.norm.sf(abs(d / se))), lo=d - 1.96 * se, hi=d + 1.96 * se, beta_E=bE, se_E=math.sqrt(vE),
                beta_L=bL, se_L=math.sqrt(vL), n=len(M), artists=G, covers_E=float(sum(r["N_E"] for r in M)), covers_L=float(sum(r["N_L"] for r in M)))

def main():
    guard()
    R = [r for r in C.lakh_rows()]
    T = {s["key"]: s for s in json.load(open(C.LAKH_TABLE))["songs"]}
    cq = {r["key"]: T[r["key"]].get("clique") for r in R if r["key"] in T}
    need = {c for c in cq.values() if c}
    V, member = versions_for(need); P = C.fit_summary(); noown = 0
    for r in R:
        r["t0"] = None; c = cq.get(r["key"])
        if not c or c not in V or V[c]["first_year"] is None: continue
        t0 = int(V[c]["first_year"]); w = C.window_counts(V[c]["versions"], r["artist"], t0)
        if w is None: noown += 1; continue
        r.update(t0=t0, N_E=float(w["N_E"]), N_L=float(w["N_L"]), N_all=float(w["N_all"]),
                 X_E=C.exposure(t0, C.EARLY[0], C.EARLY[1], P), X_L=C.exposure(t0, C.LATE_FROM, None, P))
    base = [r for r in R if r["t0"] is not None and r["t0"] <= 2005 and all(np.isfinite(r.get(k, np.nan)) for k in ["ch_rep", "REP_L"] + C.LAKH_BASE + C.LAKH_SKEPTIC)]
    S = C.within_artist(base)
    out = dict(info=dict(lakh_rows=len(R), with_clique=len(need), cliques_found=len(V), no_own_set=noown, test_rows=len(S), zip_member=member,
                         zip_sha256_head=hashlib.sha256(open(ZIP, "rb").read(1 << 20)).hexdigest()), alpha=ALPHA, prediction=PRED)
    m = wfit(S, "ch_rep"); hv = [wfit(C.within_artist([r for r in S if r["half"] == h]), "ch_rep") for h in (0, 1)]
    passed = m["delta"] < 0 and m["p"] < ALPHA and all(h["delta"] < 0 for h in hv)
    killed = not (m["lo"] <= PRED <= m["hi"])
    out["ch_rep"] = dict(main=m, halves=hv, verdict="passed (a lead: after seeing results)" if passed else ("killed" if killed else "unsettled"))
    out["readings"] = dict(REP_L=wfit(S, "REP_L"), ch_rep_1970_plus=wfit(C.within_artist([r for r in S if r["t0"] >= 1970]), "ch_rep"))
    json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float))

if __name__ == "__main__":
    if sys.argv[1:] == ["run"]: main()
