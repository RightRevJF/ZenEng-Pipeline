"""Run 08 shared code, frozen by the chair before any outcome is joined.

THE NEW DATA: ChoCo, the Chord Corpus (de Berardinis, Meroño-Peñuela, Poltronieri & Presutti 2023; Zenodo 7706751, v1.0.0;
github.com/smashub/choco), the iReal Pro partitions (forum 33,840 charts; playlists 2,048) and the Wikifonia partition (6,114 lead
sheets with chords). Parsed by /home/claude/scripts/parse_choco.py (copied here as parse_choco.py) into
$DL/choco/charts_run08.json: per chart id, part, title, artists (iReal: usually the composer, "Surname First"; Wikifonia: composers),
genre (iReal), written key, chords [time, dur, root_pc, 12-bit bitmap relative to root, bass_pc]. NO ChoCo chart has ever been joined
to an outcome by this research or the maintainer.

SONGS. A chart is matched to a Discogs-VI 20240701 clique (the maintainer's cliques_versions.py reduction, unchanged, in
$SHAPE/discogs_cliques.json) when (1) the clique's title (nrm of its most common cleaned track title) equals one of the chart's
title variants (variants(): raw; (...) and [...] removed; cut at " - " and at two spaces; a trailing ", The"/", A"/", An" moved to the
front; a trailing count " 1".." 9" removed; all under nrm()), and (2) some name token of the chart's artists string (split on
spaces, hyphens, commas, "&", "/", "and"; nrm(); length >= 4; not a STOP token) occurs inside nrm() of one of the clique's writers
(WRITER match) or inside one of its performers (PERFORMER match). Among several candidate cliques: writer matches before performer
matches, then most artist sets, then first by id. The matched token is the chart's COMPOSER key (person_key(): the matched writer's or performer's whole name, nrm).
A SONG is a clique. Its charts' measures are averaged unweighted (the number of charts is never a control). Its composer is the most
common composer key over its charts (ties: alphabetical). Its genre is the coarse genre (GENRE_MAP) most common over its charts.
Excluded before anything is read of the outcome:
  - charts whose artists string is a STOP_ARTIST (Composer Unknown, Traditional, be2sharp ARR:, Charts Practice, Exercise, ...);
  - charts with fewer than 8 chords;
  - SEEN cliques: every clique in the pack's hooktheory_covers_discogs.json and hooktheory_fresh_covers_discogs.json and in the
    research's lakh_songs_discogs_run07.json (clique ids only are read from those files);
  - HOLD-OUT: any clique whose title equals a McGill chart's title (raw or clean, nrm) and whose performers include that chart's
    artist (nrm), from studies/harmony/billboard_sections.json, the same keys as run 07's _mcgill_keys();
The design is WITHIN COMPOSER: composers with at least two songs.
Possible overlap: run 07's 3,436 Lakh single-song-artist songs (719 matched) are not in any committed table, so they cannot be
excluded by clique; any ChoCo song that is one of them is re-spent (stated in DATA.md).

THE OUTCOME (post-commit only, guarded): per clique, covers = n_artist_sets - 1; y_cov = log(1 + n_artist_sets) standardised over the
analysed songs; first_year (the clique's earliest dated release) in 10-year bins (unknown its own bin) as the era control. For the
timeline test, each artist set's earliest year from $SHAPE/discogs_versions.jsonl.

GUARD: every outcome loader refuses unless the calling folder's PREDICTION.md AND this file are committed and unmodified.
Credit: ChoCo (CC BY 4.0 for the corpus; iReal Pro charts are user contributions, Wikifonia lead sheets were CC-licensed),
Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024; CC BY-SA 4.0).
"""
import json, os, re, gzip, hashlib, subprocess, collections, math
import numpy as np

REPO = "/home/claude/zeneng-pipeline"
DL = "/home/claude/dl"
SHAPE = "/home/claude/shape"
HERE = os.path.dirname(os.path.abspath(__file__))

def nrm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))

STOP = {"the", "and", "with", "from", "feat", "featuring", "composer", "unknown", "traditional", "arr", "arranged", "music",
        "words", "lyrics", "jr", "sr", "van", "von", "der", "del", "de", "la", "le", "los", "das", "dos", "band", "trad", "anon",
        "anonymous", "various", "public", "domain", "charts", "practice", "exercise", "flinner"}
STOP_ARTIST = {"composerunknown", "traditional", "be2sharparr", "chartspractice", "exercise", "unknown", "trad", "anonymous",
               "anon", "publicdomain", "various", "variousartists", ""}

def variants(t):
    t = t or ""; out = {t}
    a = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", t); out.add(a)
    for s in list(out):
        out.add(s.split(" - ")[0]); out.add(re.split(r"\s{2,}", s.strip())[0]); out.add(s.split("-")[0])
    for s in list(out):
        m = re.match(r"^(.*),\s*(the|a|an)\s*$", s.strip(), re.I)
        if m: out.add(m.group(2) + " " + m.group(1))
    for s in list(out):
        out.add(re.sub(r"\s+[1-9]$", "", s.strip()))
    for s in list(out):
        m = re.match(r"^(.*),\s*(the|a|an)\s*$", s.strip(), re.I)
        if m: out.add(m.group(2) + " " + m.group(1))
    return {nrm(s) for s in out if len(nrm(s)) >= 2}

def tokens(a):
    return sorted({nrm(x) for x in re.split(r"[\s\-,&/;]+|\band\b", a or "") if len(nrm(x)) >= 4 and nrm(x) not in STOP})

def ordered_tokens(a):
    seen = []; 
    for x in re.split(r"[\s\-,&/;]+|\band\b", a or ""):
        t = nrm(x)
        if len(t) >= 4 and t not in STOP and t not in seen: seen.append(t)
    return seen

def person_key(otoks, names):
    """the COMPOSER key: the chart's tokens in the order written; the first token found inside some name decides; among the names
    holding it, the one holding most of the chart's tokens, then alphabetical. Returns nrm(that name) or None."""
    for t in otoks:
        hit = [n for n in names if t in n]
        if hit:
            return sorted(hit, key=lambda n: (-sum(u in n for u in otoks), n))[0]
    return None

GENRE_MAP = [("swing", "swing"), ("bebop", "swing"), ("ballad", "ballad"), ("bossa", "latin"), ("samba", "latin"),
             ("latin", "latin"), ("choro", "latin"), ("bolero", "latin"), ("salsa", "latin"), ("tango", "latin"), ("cha", "latin"),
             ("mambo", "latin"), ("baiao", "latin"), ("baião", "latin"), ("frevo", "latin"), ("afro", "latin"),
             ("bluegrass", "folk"), ("fiddle", "folk"), ("folk", "folk"), ("celtic", "folk"), ("reel", "folk"), ("jig", "folk"),
             ("country", "country"), ("worship", "gospel"), ("gospel", "gospel"), ("hymn", "gospel"), ("christian", "gospel"),
             ("blues", "blues"), ("waltz", "waltz"), ("funk", "funk"), ("soul", "funk"), ("r&b", "funk"), ("rnb", "funk"),
             ("disco", "funk"), ("rock", "pop"), ("pop", "pop"), ("reggae", "pop"), ("even", "even8"), ("straight", "even8"),
             ("shuffle", "blues"), ("march", "other"), ("polka", "other")]
def genre_of(c):
    if c["part"] == "wikifonia": return "wikifonia"
    g = (c.get("genre") or "").lower()
    for k, v in GENRE_MAP:
        if k in g: return v
    return "other"

def committed_clean(path):
    r = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", path], capture_output=True, text=True).stdout.strip()
    t = subprocess.run(["git", "-C", REPO, "ls-files", "--error-unmatch", path], capture_output=True, text=True).returncode
    return r == "" and t == 0

def guard(folder):
    p = os.path.join(folder, "PREDICTION.md")
    if not (os.path.exists(p) and committed_clean(p) and committed_clean(os.path.abspath(__file__))):
        raise SystemExit("GUARD: PREDICTION.md and common.py must be committed and unmodified before any outcome is joined")
    pushed = subprocess.run(["git", "-C", REPO, "branch", "-r", "--contains", "HEAD"], capture_output=True, text=True).stdout
    if "origin/judging-research" not in pushed:
        raise SystemExit("GUARD: the predictions commit must be pushed to origin/judging-research first")

# ---------------------------------------------------------------- design (no outcome)
def _seen_cliques():
    s = set()
    for f in ("hooktheory_covers_discogs.json", "hooktheory_fresh_covers_discogs.json"):
        txt = subprocess.run(["git", "-C", REPO, "show", "origin/main:studies/judging_data/" + f], capture_output=True, text=True).stdout
        d = json.loads(txt)
        rows = d.get("songs", d) if isinstance(d, dict) else d
        if isinstance(rows, dict):
            for k, v in rows.items():
                if isinstance(v, dict) and v.get("clique"): s.add(v["clique"])
        else:
            for v in rows:
                if isinstance(v, dict) and v.get("clique"): s.add(v["clique"])
    L = json.load(open(os.path.join(REPO, "studies/judging_research/data/lakh_songs_discogs_run07.json")))
    for v in L["songs"]:
        if v.get("clique"): s.add(v["clique"])
    return s

def _mcgill_keys():
    M = json.load(open(os.path.join(REPO, "studies", "harmony", "billboard_sections.json")))
    def clean(t): return re.sub(r"\([^)]*\)|\[[^\]]*\]", "", t or "").split(" - ")[0].strip()
    return {(nrm(m["artist"]), nrm(m["title"])) for m in M} | {(nrm(m["artist"]), nrm(clean(m["title"]))) for m in M}

def build_design(write=True):
    """matches charts to cliques; writes $DL/choco/design_run08.json (songs: clique id, composer, genre, chart ids, match type).
    Reads only clique titles, writers and performers (no counts, no years)."""
    C = json.load(open(os.path.join(DL, "choco", "charts_run08.json")))
    Q = json.load(open(os.path.join(SHAPE, "discogs_cliques.json")))
    by = collections.defaultdict(list)
    for q in Q:
        by[q["title"]].append((q["id"], [nrm(w) for w in q["writers"]], q["artists"], q["n_artist_sets"]))
    # n_artist_sets is used ONLY to break ties among candidate cliques (the pack's rule); it is never stored in the design.
    seen = _seen_cliques(); mg = _mcgill_keys(); mg_titles = collections.defaultdict(set)
    for a, t in mg: mg_titles[t].add(a)
    charts = {}; nstop = nshort = nseen = nhold = nm = 0
    for c in C:
        if nrm(c["artists"]) in STOP_ARTIST: nstop += 1; continue
        if len(c["chords"]) < 8: nshort += 1; continue
        toks = tokens(c["artists"]); otoks = ordered_tokens(c["artists"]); best = None
        if not toks: nstop += 1; continue
        for v in variants(c["title"]):
            for cid, wr, perf, nset in by.get(v, []):
                kw = person_key(otoks, wr); kp = person_key(otoks, perf)
                if kw: cand = (0, -nset, cid, kw, "writer")
                elif kp: cand = (1, -nset, cid, kp, "performer")
                else: continue
                if best is None or cand[:3] < best[:3]: best = cand
        if best is None: continue
        nm += 1; cid = best[2]
        if cid in seen: nseen += 1; continue
        charts[c["id"]] = dict(clique=cid, composer=best[3], match=best[4], genre=genre_of(c), part=c["part"])
    # hold-out: by clique title and performers
    used = {v["clique"] for v in charts.values()}
    clq = {q["id"]: q for q in Q if q["id"] in used}
    hold = {cid for cid, q in clq.items() if any(a in q["artists"] for a in mg_titles.get(q["title"], ()))}
    for k in [k for k, v in charts.items() if v["clique"] in hold]: del charts[k]; nhold += 1
    songs = collections.defaultdict(list)
    for k, v in charts.items(): songs[v["clique"]].append((k, v))
    S = []
    for cid, L in songs.items():
        comp = sorted(collections.Counter(v["composer"] for _, v in L).items(), key=lambda x: (-x[1], x[0]))[0][0]
        gen = sorted(collections.Counter(v["genre"] for _, v in L).items(), key=lambda x: (-x[1], x[0]))[0][0]
        S.append(dict(clique=cid, composer=comp, genre=gen, charts=sorted(k for k, _ in L),
                      match="writer" if any(v["match"] == "writer" for _, v in L) else "performer",
                      parts=sorted({v["part"] for _, v in L})))
    cnt = collections.Counter(s["composer"] for s in S)
    for s in S: s["within"] = cnt[s["composer"]] >= 2
    info = dict(charts_total=len(C), stop_artist=nstop, short=nshort, matched_charts=nm, seen_charts=nseen, holdout_charts=nhold,
                songs=len(S), within_songs=sum(s["within"] for s in S), composers_within=sum(1 for v in cnt.values() if v >= 2),
                writer_match_songs=sum(s["match"] == "writer" for s in S))
    if write:
        json.dump(dict(info=info, songs=S), open(os.path.join(DL, "choco", "design_run08.json"), "w"))
    return info, S

def load_design(within=True):
    D = json.load(open(os.path.join(DL, "choco", "design_run08.json")))
    S = [s for s in D["songs"] if s["within"]] if within else D["songs"]
    return D["info"], S

def charts_by_id():
    return {c["id"]: c for c in json.load(open(os.path.join(DL, "choco", "charts_run08.json")))}

def halves(name):
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % 2

# ---------------------------------------------------------------- outcome (guarded)
def load_outcomes(songs, folder):
    guard(folder)
    need = {s["clique"] for s in songs}; out = {}
    for q in json.load(open(os.path.join(SHAPE, "discogs_cliques.json"))):
        if q["id"] in need:
            out[q["id"]] = dict(n_sets=q["n_artist_sets"], versions=q["versions"], first_year=q["first_year"])
    for s in songs:
        o = out[s["clique"]]; s["n_sets"] = o["n_sets"]; s["covers"] = o["n_sets"] - 1; s["first_year"] = o["first_year"]
        s["ln_sets"] = math.log(1 + o["n_sets"])
    v = np.array([s["ln_sets"] for s in songs]); m, sd = v.mean(), v.std()
    for s in songs: s["y_cov"] = (s["ln_sets"] - m) / sd
    return songs

def load_timelines(songs, folder):
    """per song: sorted list of earliest years of each artist set (None dropped)."""
    guard(folder)
    need = {s["clique"] for s in songs}; T = {}
    with open(os.path.join(SHAPE, "discogs_versions.jsonl")) as f:
        for line in f:
            if '"id": "C-' not in line[:20]: continue
            d = json.loads(line)
            if d["id"] in need: T[d["id"]] = sorted(y for _, y, _ in d["sets"] if y is not None)
    for s in songs: s["years"] = T.get(s["clique"], [])
    return songs

# ---------------------------------------------------------------- models
def decade_bins(songs, key="first_year"):
    lab = [("u" if s.get(key) is None else str(min(max(s[key], 1900), 2020) // 10 * 10)) for s in songs]
    return lab

def dummies(labels, drop_first=True):
    u = sorted(set(labels)); u = u[1:] if drop_first else u
    return np.array([[1.0 if l == k else 0.0 for k in u] for l in labels]).reshape(len(labels), len(u))

def within(X, g):
    X = np.asarray(X, float).copy(); g = np.asarray(g)
    for k in np.unique(g):
        i = g == k; X[i] -= X[i].mean(0)
    return X

def ols_fe(y, X, g):
    """within-group OLS of y on X (group = composer), CR1 SEs clustered by group. Returns b, se, p for every column, N, G."""
    from scipy import stats
    y = np.asarray(y, float); X = np.asarray(X, float); g = np.asarray(g)
    Xw = within(X, g); yw = within(y[:, None], g)[:, 0]
    keep = np.abs(Xw).sum(0) > 1e-12; Xw = Xw[:, keep]
    XtX = np.linalg.pinv(Xw.T @ Xw); b = XtX @ Xw.T @ yw; e = yw - Xw @ b
    G = len(np.unique(g)); N, K = Xw.shape
    meat = np.zeros((K, K))
    for k in np.unique(g):
        i = g == k; s = Xw[i].T @ e[i]; meat += np.outer(s, s)
    V = XtX @ meat @ XtX * (G / (G - 1)) * ((N - 1) / (N - K - G))
    se = np.sqrt(np.diag(V)); p = 2 * stats.t.sf(np.abs(b / se), G - 1)
    bb = np.full(len(keep), np.nan); ss = bb.copy(); pp = bb.copy(); bb[keep] = b; ss[keep] = se; pp[keep] = p
    return bb, ss, pp, N, G

def zs(v):
    v = np.asarray(v, float); return (v - np.nanmean(v)) / np.nanstd(v)

def design_matrix(songs, meas, extra=()):
    cols = [zs([s[meas] for s in songs])] + [zs([s[e] for s in songs]) for e in extra]
    X = np.column_stack(cols)
    D = np.column_stack([dummies([s["genre"] for s in songs]), dummies(decade_bins(songs))])
    return np.column_stack([X, D]) if D.size else X

def fake_power(songs, meas, extra, beta, alpha, sign=+1, draws=300, comp_share=0.3, seed=11):
    """fake outcomes on the real design: y = composer effect (variance comp_share) + beta * z(meas) + noise (rest), standardised;
    first_year unknown before the outcome, so the decade dummies are left out of the fake fit. Power = share of draws with p < alpha
    and the estimate's sign = sign. Also the share of draws in which the range-kill would fire (prediction outside the 95% range)."""
    rng = np.random.default_rng(seed); g = np.array([s["composer"] for s in songs])
    X = np.column_stack([zs([s[meas] for s in songs])] + [zs([s[e] for s in songs]) for e in extra] + [dummies([s["genre"] for s in songs])])
    ok = ~np.isnan(X).any(1); X, g2 = X[ok], g[ok]; z = X[:, 0]
    ug, inv = np.unique(g2, return_inverse=True); hits = 0; kills = 0; ses = []
    for d in range(draws):
        u = rng.normal(0, math.sqrt(comp_share), len(ug))[inv]
        y = u + beta * z + rng.normal(0, math.sqrt(max(1 - comp_share - beta ** 2, 0.05)), len(z))
        b, se, p, N, G = ols_fe(y, X, g2)
        hits += (p[0] < alpha) and (np.sign(b[0]) == sign); kills += abs(beta - b[0]) > 1.96 * se[0]; ses.append(se[0])
    return dict(power=hits / draws, kill_rate_if_true=kills / draws, se_fake=float(np.median(ses)), N=int(ok.sum()),
                G=int(len(ug)), comp_share=comp_share, draws=draws)

def verdict(b, se, p, pred, alpha, halves_b, second_b, power, floor=0.2):
    sign = np.sign(pred); counted = power >= floor
    inside = abs(pred - b) <= 1.96 * se
    passed = counted and p < alpha and np.sign(b) == sign and all(np.sign(h) == sign for h in halves_b) and np.sign(second_b) == sign
    if not counted: v = "estimate (under the power floor): passes nothing, kills nothing"
    elif passed: v = "PASS"
    elif not inside: v = "KILLED (the prediction lies outside the 95% range)"
    else: v = "unsettled (no pass; the prediction lies inside the 95% range)"
    return dict(counted=bool(counted), passed=bool(passed), prediction_inside_95=bool(inside), verdict=v)
