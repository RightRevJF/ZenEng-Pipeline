"""The title line's choice of rhythm, against the table: for each title line drawn fresh in two bars, the kept two-bar windows offered to it (with the engine's pickups) that pass 840's test, the share of the table's own count the commonest of them takes, and how many it takes to cover half and nine tenths; beside the share of builds the commonest rhythm takes in our draw.
python3 studies/other_metres/count_title_choice.py RECORD.song.json [BUILDS] -> prints JSON. A count."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def table_side(E, sy):
    n = len(sy); lead = next((k for k, x in enumerate(sy) if x[1]), n); W = {}
    for p in sorted({0, min(1, lead), min(2, lead)}):
        for w, c in E.kept_windows(n - p, 2):
            if w[0] != 0 and p > 0: continue
            if E.S.get("no_pickup_windows") and w[0] >= E.BAR - 12 and sum(1 for o in w if o < E.BAR) <= 2: continue
            ons = tuple([-6 * (p - j) for j in range(p)] + list(w)); st = [t for t, x in zip(ons, sy) if x[1]]
            if (not st) or 2 * sum(1 for t in st if E.on_beat(t)) >= len(st): W[ons] = W.get(ons, 0) + c
    tot = sum(W.values()); srt = sorted(W.values(), reverse=True); cum = 0; k50 = k90 = None
    for i, v in enumerate(srt, 1):
        cum += v
        if k50 is None and cum >= 0.5 * tot: k50 = i
        if k90 is None and cum >= 0.9 * tot: k90 = i
    rk = sorted(W.items(), key=lambda x: -x[1]); table_side.rank = {k: (i + 1, round(v / tot, 3)) for i, (k, v) in enumerate(rk)}
    return dict(passing_windows=len(W), their_kept_count=tot, commonest_share_by_kept_count=round(srt[0] / tot, 3) if tot else None, windows_to_cover_half=k50, windows_to_cover_nine_tenths=k90)
def read(record, builds=600, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); hooks = [h for h in sp.get("hooks", ()) if E.HOW.get((h.rsplit(":", 1)[0], int(h.rsplit(":", 1)[1])), ["fresh"])[0] not in ("copy", "again")]; C = {h: collections.Counter() for h in hooks}; rng = random.Random(seed); made = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if err: continue
        made += 1
        for h in hooks: s_, i_ = h.rsplit(":", 1); U = E.line_start(s_, int(i_)); C[h][tuple(sorted(x["on"] - U for x in c["notes"] if x["sec"] == s_ and x["line"] == int(i_)))] += 1
    out = {}
    for h in hooks:
        s_, i_ = h.rsplit(":", 1); sy = E.LINES[s_][int(i_)]; sb = sp["sung_bars"][s_][int(i_)]; srt = sorted(C[h].values(), reverse=True); cum = 0; k50 = k90 = None
        for i, v in enumerate(srt, 1):
            cum += v
            if k50 is None and cum >= 0.5 * made: k50 = i
            if k90 is None and cum >= 0.9 * made: k90 = i
        tb = table_side(E, sy) if sb == 2 else "not a two-bar line"; mine = C[h].most_common(1)[0][0]; rk = table_side.rank.get(mine) if sb == 2 else None
        out[h] = dict(syllables=len(sy), stressed=sum(1 for x in sy if x[1]), sung_bars=sb, table=tb, ours=dict(distinct_rhythms=len(C[h]), commonest_share_of_builds=round(srt[0] / made, 3), rhythms_to_cover_half=k50, rhythms_to_cover_nine_tenths=k90), the_commonest_in_ours_is_the_tables_commonest=(None if sb != 2 else bool(rk and rk[0] == 1)), our_commonest_in_the_table_rank_and_share=(None if sb != 2 else list(rk) if rk else "not among the passing kept windows (a one-bar or weighted rhythm)"))
    return dict(builds=builds, made=made, title_lines=out)
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 600), indent=1))
