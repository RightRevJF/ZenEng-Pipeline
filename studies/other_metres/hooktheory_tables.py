"""Popular-song tables in 3/4 and in 6/4 read as 6/8, from the Hooktheory clips (Sheet Sage's release; fetched outside the repo; CC BY-NC-SA 3.0).
python3 studies/other_metres/hooktheory_tables.py -> trial_tables/3-4_pop_sung.json, 6-8_pop_sung.json (the atlas's form), their .rows.json (one song a row) and hooktheory_by_song.json.
A clip is a section someone transcribed (a verse, a chorus), not a whole song; a song's clips are pooled. Songs whose video is in the pack's Discogs join are 'released songs'; the rest (film, game and library tunes among them, and unmatched songs) are set apart."""
import os, sys, json, gzip, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, atlas_build as AB, leadsheet_waltz_figures as LW, make_leadsheet_table as MK
FILT = json.load(open(os.path.join(HERE, "hooktheory_filter.json"))); OUT_ARTISTS = set(FILT["soundtrack_game_library"]) | set(FILT["classical"])
def left_out(h): w = set(h["artist"].split("-")) | set(h["song"].split("-")); return h["artist"] in OUT_ARTISTS or any(set(x.split("-")) <= w for x in FILT["words_in_artist_or_song_slug"])
SRC = "/home/claude/corpus/sheetsage-data/hooktheory/Hooktheory.json.gz"; DISC = json.load(open(os.path.join(ROOT, "studies", "judging_data", "hooktheory_covers_discogs.json")))
def clip_notes(x, unit):
    """notes on the grid of twelfths of a quarter; unit = twelfths a Hooktheory beat is worth (12 in 3/4; 6 where 6/4 is read as 6/8)"""
    ns = []
    for n in x["annotations"].get("melody") or []:
        on = n["onset"] * unit; off = n["offset"] * unit
        if abs(on - round(on)) > 1e-6 or round(on) % 3: return None
        ns.append([int(round(on)), max(1, int(round(off - on))), 60 + 12 * n["octave"] + n["pitch_class"]])
    ns.sort(); return ns if len(ns) >= 8 and all(b[0] > a[0] for a, b in zip(ns, ns[1:])) else None
def build(D, want, unit, BL, BEATS, beat, name, metre):
    songs = collections.defaultdict(list); secs = collections.defaultdict(list); off_grid = 0
    filtered = [0]
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != want or "MELODY" not in x["tags"]: continue
        if left_out(x["hooktheory"]): filtered[0] += 1; continue
        ns = clip_notes(x, unit)
        if ns is None: off_grid += 1; continue
        key = (x["hooktheory"]["artist"], x["hooktheory"]["song"]); songs[key].append((ns, (x.get("youtube") or {}).get("id")))
        t = (x.get("alignment") or {}).get("refined") or (x.get("alignment") or {}).get("user")
        if t and len(t["beats"]) > 1: secs[key].append((t["times"][-1] - t["times"][0]) / (t["beats"][-1] - t["beats"][0]) * want[0])
    rows = []; BAR = collections.Counter(); WIN = collections.defaultdict(collections.Counter); IV = collections.Counter(); POS = collections.Counter(); DUR = collections.Counter(); by = []
    for key, clips in sorted(songs.items()):
        allns = []; shift = 0
        for ns, vid in clips:
            b0 = ns[0][0] // BL; ns = [[on - b0 * BL + shift, d, p] for on, d, p in ns]; shift = (ns[-1][0] // BL + 2) * BL; allns += ns      # a song's clips laid end to end, a bar apart
        if len(allns) < 24: continue
        released = any(v in DISC for _, v in clips); r = {**AB.readings(allns, BL, BEATS, beat), **MK.structure(allns, BL)}; f = LW.figs(allns) if BL == 36 else {}; bars = collections.defaultdict(list)
        for on, d, q in allns: bars[on // BL].append((on % BL, d, q)); DUR[d] += 1
        p = [x[2] for x in allns]; row = dict(artist=key[0], song=key[1], released=released, clips=len(clips), notes=len(allns), bars=len(bars), seconds_a_bar=round(float(np.median(secs[key])), 2) if secs[key] else None, range=max(p) - min(p), distinct_pitches=len(set(p)), commonest_pitch=max(collections.Counter(p).values()) / len(p), **{k_: r[k_] for k_ in ("notes a bar", "onsets on the beat", "onsets on the bar's first beat", "bars on a rhythm already sung", "bars on a figure already sung", "distinct rhythms over bars")}); by.append(row)
        rows.append(r)
        for b, v in bars.items():
            BAR[tuple(o for o, d, q in v)] += 1
            for o, d, q in v: POS[o] += 1
            if b + 1 in bars: w = tuple(o for o, d, q in v) + tuple(o + BL for o, d, q in bars[b + 1]); WIN[len(w)][w] += 1
        for a, b in zip(allns, allns[1:]):
            if b[0] - a[0] < 2 * BL: IV[int(max(-12, min(12, b[2] - a[2])))] += 1
    names = sorted(rows[0]); tot = sum(POS.values()); src = f"{len(rows)} songs' Hooktheory clips (soundtrack, game, library and classical sources left out by hooktheory_filter.json) written in {want[0]}/{want[1]}" + (" and read as 6/8" if unit == 6 else "") + " (Sheet Sage's Hooktheory.json.gz; CC BY-NC-SA 3.0; not committed); sections, not whole songs"
    T = dict(metre=metre, source=src, kind="simple triple" if metre == "3/4" else "compound duple", bar=BL, beats=BEATS, beat=beat, found=len(by), tunes=len(rows), readings_quartiles={k: [float(np.percentile([r[k] for r in rows], q)) for q in (25, 50, 75)] for k in names}, bar_rhythms=[[list(k), v] for k, v in BAR.most_common(40)], bars_total=sum(BAR.values()),
             two_bar_windows={str(n): [[list(k), v] for k, v in c.most_common(40)] for n, c in WIN.items()}, intervals={str(k): v for k, v in sorted(IV.items())}, onset_weights={str(k): round(v / tot, 4) for k, v in sorted(POS.items())}, durations={str(k): v for k, v in DUR.most_common(20)}, licence="a trial table; CC BY-NC-SA 3.0 source: non-commercial; counts only")
    D_ = os.path.join(HERE, "trial_tables"); json.dump(T, open(os.path.join(D_, name + ".json"), "w")); json.dump(dict(names=names, rows=[[round(float(r[n]), 5) for n in names] for r in rows], songs=len(rows), source=src), open(os.path.join(D_, name + ".rows.json"), "w"))
    def q(v): return [round(float(z), 3) for z in np.percentile(v, (10, 25, 50, 75, 90))] if len(v) else None
    out = dict(written=f"{want[0]}/{want[1]}", read_as=metre, clips_off_the_grid=off_grid, clips_left_out_by_the_filter=filtered[0], songs=len(by), in_the_discogs_join=sum(b["released"] for b in by), bars_total=T["bars_total"], top_bar_rhythms=[[k, round(v / T["bars_total"], 3)] for k, v in T["bar_rhythms"][:8]])
    for grp, sel in (("all", by), ("in the Discogs join", [b for b in by if b["released"]])):
        out["by song, " + grp] = {k: q([b[k] for b in sel if b[k] is not None]) for k in ("bars", "notes", "seconds_a_bar", "notes a bar", "onsets on the beat", "onsets on the bar's first beat", "range", "distinct_pitches", "commonest_pitch", "bars on a rhythm already sung", "bars on a figure already sung")}
    A, J = out["by song, all"], out["by song, in the Discogs join"]; out["joined_median_inside_the_full_middle_half"] = {k: bool(A[k][1] <= J[k][2] <= A[k][3]) for k in A if A[k] and J[k]}
    out["examples_released"] = [f"{b['artist']}: {b['song']}" for b in sorted((b for b in by if b["released"]), key=lambda b: -b["notes"])[:25]]; return out
if __name__ == "__main__":
    D = json.load(gzip.open(SRC)); out = {"3/4": build(D, (3, 4), 12, 36, [0, 12, 24], 12, "3-4_pop_sung", "3/4"), "6/4 read as 6/8": build(D, (6, 4), 6, 36, [0, 18], 18, "6-8_pop_sung", "6/8")}
    json.dump(out, open(os.path.join(HERE, "hooktheory_by_song.json"), "w"), indent=1)
    for k, o in out.items():
        print(k, {a: o[a] for a in ("songs", "in_the_discogs_join", "clips_left_out_by_the_filter", "clips_off_the_grid", "bars_total")}); print("  joined median inside the full middle half:", o["joined_median_inside_the_full_middle_half"]); print("  bars", o["top_bar_rhythms"])
        for g in ("by song, all", "by song, in the Discogs join"): print("  ", g, json.dumps(o[g]))
        print("  ", o["examples_released"][:14])
