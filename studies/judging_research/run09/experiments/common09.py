"""Run 09 shared code. The design (which songs) is built from clique titles, writers and performers only; the outcome is guarded.

NEW SONGS. ChoCo v1.0.0 (Zenodo 7706751; CC BY 4.0) charts that no session has ever joined to an outcome:
  (a) the partitions run 08 never parsed (parse09.py -> $DL/choco/charts_run09.json): Band-in-a-Box internet corpus, the Real Book
      (Band-in-a-Box files), and charts transcribed from one recording (Isophonics, uspop2002, rock corpus, Robbie Williams, JAAH, Weimar);
  (b) run 08's iReal Pro and Wikifonia charts that matched NO clique by title plus name (run 08's "542 title-only" remainder and any
      others the rule below finds), from $DL/choco/charts_run08.json (run 08's parse_choco.py, re-run unchanged this pass:
      42,002 charts, 41,206 with 8 or more chords, as in run 08).
THE MATCH (frozen before any outcome; run 08's two rules, unchanged):
  1. NAME MATCH (charts whose meta gives a performer or composer): run 08 build_design: a title variant equals the clique title and a
     name token (length >= 4, not a stop word) occurs in one of the clique's writers (writer match) or performers (performer match);
     among candidates writer before performer, then most artist sets (the pack's tie rule; n_artist_sets is read ONLY to break ties and
     is never stored), then the smaller id. For Weimar the composers string is tried first, then the performers.
  2. TITLE-ONLY (no names, or names that matched nothing): run 08 posthoc08.title_only_rows: the raw title (brackets removed, cut at
     " - ") has at least two words and the union over its variants() hits exactly ONE clique title.
  Excluded before anything is read: charts with fewer than 8 chords; run 08's iReal/Wikifonia charts whose names are a stop artist or
  empty (run 08's rule for those partitions); new-partition charts whose given name is a stop artist (an empty name is allowed there,
  since those partitions give no names); every SEEN
  clique (the pack's Hooktheory and fresh tables, run 07's Lakh table, run 08's 8,640 ChoCo songs); the McGill hold-out (clique title
  and a performer equal to a McGill chart's, and, for title-only matches, any clique whose title equals a McGill title); run 08 design
  charts (they matched already).
SONG = clique; its measures are the unweighted mean over its charts. A song's PROVENANCE: "recording" if all its charts are transcribed
  from recordings, "chart" if none are, "both" otherwise. Its COMPOSER key: the name-matched person_key when a name match exists, else
  nrm(the clique's first listed writer) (Discogs-VI writers, stored alphabetically), else "solo:<clique>" (a singleton).
  Its GENRE (coarse, from the partition; no outcome): "jazz" (real-book, jaah, weimar, iReal swing/ballad/latin/blues/waltz), "pop"
  (isophonics, uspop2002, rock-corpus, robbie-williams, iReal pop/funk/even8/country/folk/gospel), "biab" (Band-in-a-Box internet
  corpus), "wikifonia", "other"; the most common over its charts (ties alphabetical).
THE OUTCOME (post-commit only, guarded): as run 08: covers = n_artist_sets - 1; y_cov = standardised log(1 + n_artist_sets) over the
  analysed songs; first_year in 10-year bins (unknown its own bin).
Credit: ChoCo (CC BY 4.0; iReal Pro and Band-in-a-Box charts are user contributions; Isophonics, uspop2002, rock corpus, Robbie Williams,
JAAH, Weimar Jazz Database annotations as credited in ChoCo); Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024; CC BY-SA 4.0).
"""
import json, os, re, sys, math, collections, subprocess, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/claude/zeneng-pipeline"
sys.path.insert(0, os.path.join(REPO, "studies/judging_research/run08/experiments"))
import common as C8   # run 08's frozen helpers: nrm, variants, tokens, ordered_tokens, person_key, STOP_ARTIST, genre_of, models
DL, SHAPE = C8.DL, C8.SHAPE
nrm = C8.nrm
REC_PARTS = {"isophonics", "uspop2002", "rock-corpus", "robbie-williams", "jaah", "weimar"}
JAZZ8 = {"swing", "ballad", "latin", "blues", "waltz"}
POP8 = {"pop", "funk", "even8", "country", "folk", "gospel"}

def coarse_genre(c):
    p = c["part"]
    if p in ("real-book", "jaah", "weimar"): return "jazz"
    if p in ("isophonics", "uspop2002", "rock-corpus", "robbie-williams"): return "pop"
    if p == "biab-internet-corpus": return "biab"
    if p == "wikifonia": return "wikifonia"
    g = C8.genre_of(c)
    return "jazz" if g in JAZZ8 else "pop" if g in POP8 else "other"

def committed_clean(path): return C8.committed_clean(path)

def guard(folder):
    p = os.path.join(folder, "PREDICTION.md")
    if not (os.path.exists(p) and committed_clean(p) and committed_clean(os.path.abspath(__file__))):
        raise SystemExit("GUARD: PREDICTION.md and common09.py must be committed and unmodified before any outcome is joined")
    pushed = subprocess.run(["git", "-C", REPO, "branch", "-r", "--contains", "HEAD"], capture_output=True, text=True).stdout
    if "origin/judging-research" not in pushed:
        raise SystemExit("GUARD: the predictions commit must be pushed to origin/judging-research first")

def _seen_cliques():
    s = C8._seen_cliques()
    D = json.load(open(os.path.join(REPO, "studies/judging_research/data/choco_songs_discogs_run08.json")))
    s |= {v["clique"] for v in D["songs"]}           # clique ids only are read from this file
    return s

def _run08_design_charts():
    D = json.load(open(os.path.join(REPO, "studies/judging_research/data/choco_songs_discogs_run08.json")))
    return {k for v in D["songs"] for k in v["charts"]}

def load_charts():
    A = json.load(open(os.path.join(DL, "choco", "charts_run09.json")))
    for c in A: c.setdefault("source", "chart")
    B = json.load(open(os.path.join(DL, "choco", "charts_run08.json")))
    used = _run08_design_charts()
    for c in B:
        c["source"] = "chart"; c["names_kind"] = "composer" if c["artists"] else ""; c["composers"] = ""; c["timebase"] = "beats"
    B = [c for c in B if c["id"] not in used]
    return A + B

def build_design09(write=True):
    charts = load_charts()
    Q = json.load(open(os.path.join(SHAPE, "discogs_cliques.json")))
    by = collections.defaultdict(list); qid = {}
    for q in Q:
        by[q["title"]].append((q["id"], [nrm(w) for w in q["writers"]], q["artists"], q["n_artist_sets"]))
        qid[q["id"]] = (q["title"], q["artists"], q["writers"])
    seen = _seen_cliques(); mg = C8._mcgill_keys(); mgt = collections.defaultdict(set)
    for a, t in mg: mgt[t].add(a)
    stats = collections.Counter(); M = {}
    for c in charts:
        if len(c["chords"]) < 8: stats["short"] += 1; continue
        if c["part"] in ("ireal-forum", "ireal-playlists", "wikifonia") and nrm(c["artists"]) in C8.STOP_ARTIST:
            stats["stop_artist_run08_rule"] += 1; continue     # run 08's rule for its own partitions (stop or empty names)
        if c["artists"] and nrm(c["artists"]) in C8.STOP_ARTIST and not c.get("composers"):
            stats["stop_artist"] += 1; continue
        vs = C8.variants(c["title"]); best = None
        names = [x for x in (c.get("composers", ""), c["artists"]) if x and nrm(x) not in C8.STOP_ARTIST]
        for nm_ in names:
            otoks = C8.ordered_tokens(nm_)
            if not otoks: continue
            for v in vs:
                for cid, wr, perf, nset in by.get(v, []):
                    kw = C8.person_key(otoks, wr); kp = C8.person_key(otoks, perf)
                    if kw: cand = (0, -nset, cid, kw, "writer")
                    elif kp: cand = (1, -nset, cid, kp, "performer")
                    else: continue
                    if best is None or cand[:3] < best[:3]: best = cand
            if best is not None: break
        if best is not None:
            cid, comp, how = best[2], best[3], best[4]
        else:
            raw = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", c["title"]).split(" - ")[0]
            if len(raw.split()) < 2: stats["title_one_word"] += 1; continue
            cands = {cid for v in vs for cid, _, _, _ in by.get(v, [])}
            if len(cands) != 1: stats["title_not_unique" if cands else "no_match"] += 1; continue
            cid = cands.pop(); how = "title"; comp = None
            if any(v in mgt for v in vs): stats["holdout_title"] += 1; continue
        if cid in seen: stats["seen"] += 1; continue
        t, perf, wr = qid[cid]
        if any(a in perf for a in mgt.get(t, ())): stats["holdout"] += 1; continue
        if comp is None:
            comp = nrm(wr[0]) if wr else "solo:" + cid
        M[c["id"]] = dict(clique=cid, composer=comp, match=how, part=c["part"], source=c["source"], genre=coarse_genre(c))
        stats["kept_" + how] += 1
    songs = collections.defaultdict(list)
    for k, v in M.items(): songs[v["clique"]].append((k, v))
    S = []
    for cid, L in songs.items():
        named = [v for _, v in L if v["match"] != "title"]
        pool = named if named else [v for _, v in L]
        comp = sorted(collections.Counter(v["composer"] for v in pool).items(), key=lambda x: (-x[1], x[0]))[0][0]
        gen = sorted(collections.Counter(v["genre"] for _, v in L).items(), key=lambda x: (-x[1], x[0]))[0][0]
        srcs = {v["source"] for _, v in L}
        S.append(dict(clique=cid, composer=comp, genre=gen, charts=sorted(k for k, _ in L),
                      match="name" if named else "title", parts=sorted({v["part"] for _, v in L}),
                      provenance="both" if len(srcs) > 1 else srcs.pop()))
    cnt = collections.Counter(s["composer"] for s in S)
    for s in S: s["within"] = cnt[s["composer"]] >= 2
    info = dict(charts_considered=len(charts), **stats, songs=len(S), within_songs=sum(s["within"] for s in S),
                by_provenance=dict(collections.Counter(s["provenance"] for s in S)), by_genre=dict(collections.Counter(s["genre"] for s in S)),
                by_match=dict(collections.Counter(s["match"] for s in S)),
                by_part=dict(collections.Counter(p for s in S for p in s["parts"])))
    if write: json.dump(dict(info=info, songs=S), open(os.path.join(DL, "choco", "design_run09.json"), "w"))
    return info, S

def load_design():
    D = json.load(open(os.path.join(DL, "choco", "design_run09.json"))); return D["info"], D["songs"]

def load_outcomes(songs, folder):
    guard(folder)
    need = {s["clique"] for s in songs}; out = {}
    for q in json.load(open(os.path.join(SHAPE, "discogs_cliques.json"))):
        if q["id"] in need: out[q["id"]] = dict(n_sets=q["n_artist_sets"], first_year=q["first_year"])
    for s in songs:
        o = out[s["clique"]]; s["n_sets"] = o["n_sets"]; s["covers"] = o["n_sets"] - 1; s["first_year"] = o["first_year"]
        s["ln_sets"] = math.log(1 + o["n_sets"])
    v = np.array([s["ln_sets"] for s in songs]); m, sd = v.mean(), v.std()
    for s in songs: s["y_cov"] = (s["ln_sets"] - m) / sd
    return songs

halves = C8.halves; ols_fe = C8.ols_fe; zs = C8.zs; dummies = C8.dummies; decade_bins = C8.decade_bins; verdict = C8.verdict

if __name__ == "__main__":
    info, S = build_design09()
    print(json.dumps(info, indent=1))
