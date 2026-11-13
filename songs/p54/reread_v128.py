"""v128 Run 3 (481: every song on its own tonic, song 43 on A natural minor): Windows 141-143 read again on each run of this session, as Window 145 and 147 read them (zeneng_v125_port_reread.json's code, the
first 400 complete builds of each main run (RR_MODE=ctl: control), the chord at the note (v128: the half-bar chart where the run has one), each song on its own tonic), beside Billboard and
Rolling Stone, and each run against the run before it: which readings moved toward the kept songs and which away.
Usage: python3 reread_v127.py OUT.json name=prefix [name=prefix ...]   (prefix: .../melody_vNNN; the song and _main.pkl are added)"""
import sys, json, pickle, collections, re, os
MODE8 = os.environ.get("RR_MODE", "main")                                                # 485: the control runs read the same way
import numpy as np, pandas as pd
OUT = sys.argv[1]; RUNS = [a.split("=", 1) for a in sys.argv[2:]]
T = "/home/claude/p54/tables"
T121 = json.load(open(f"{T}/zeneng_v121_blind_spots.json")); T122 = json.load(open(f"{T}/zeneng_v122_whole_song.json")); T123 = json.load(open(f"{T}/zeneng_v123_bass_at_the_chord.json"))
T125 = json.load(open(f"{T}/zeneng_v125_port_reread.json")); T127 = json.load(open(f"{T}/zeneng_v127_run1.json"))
ns_ = {"np": np, "collections": collections}
exec(next(v for k, v in T121.items() if k.startswith("code: cand")), ns_)
for src, names in ((T122["code"], ("om", "pair")), (T123["code"], ("sgn", "bmove", "outer"))):
    for name in names: exec(re.search(rf"^def {name}\(.*?(?=^\S)", src, re.S | re.M).group(0), ns_)
SIX = ["equal_gap_run_max", "gap_same_as_before", "gap_entropy", "most_onsets_in_a_beat", "phrase_starts_same_place", "zigzag_of_three"]
ns_.update(SIX=SIX, MAJ={0, 2, 4, 5, 7, 9, 11}, MIN={0, 2, 3, 5, 7, 8, 10}); om, pair, outer = ns_["om"], ns_["pair"], ns_["outer"]
HARM = ["chord_tones", "chord_tones_on_beat", "chord_tones_off_beat", "chord_tones_on_downbeat"]
FE = T122["measures (agreed by both collections, and the chord tones)"]                      # the 27 (23 agreed and the chord tones)
NAME = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def rm(c): c = c.split("/")[0]; r = NAME[c[0]] + (1 if "#" in c[:2] else -1 if (len(c) > 1 and c[1] == "b") else 0); return r % 12, ("m" in c[1:3] and "maj" not in c)
def pcs(c): r, m = rm(c); return frozenset({r, (r + (3 if m else 4)) % 12, (r + 7) % 12})
def eng(c):
    r, m = rm(c); b = ((rm(c.split("/")[1])[0] - r) % 12) if "/" in c else 0   # 440: a chord over its third or fifth
    return (r, frozenset((0, 3 if m else 4, 7)), b, False)
SECS = {"Verse 1": ("verse", "1"), "Verse 2": ("verse", "2"), "Chorus 1": ("chorus", "1"), "Bridge": ("bridge", "1")}; TON = {"40": 2, "42": 10, "43": 9, "44": 3, "45": 7}; MINOR8 = {"43"}   # v128 481: song 43 on A, natural minor
if os.environ.get("RR_SONGS"): TON = {k: v for k, v in TON.items() if k in os.environ["RR_SONGS"].split(",")}   # Part 2: songs 40, 42 and 43 only
KS = T122["kept figures by section (both collections pooled)"]
FV = T127["reread"]["first verse and chorus: every measure"]; FO = T127["reread"]["the melody over chord and bass"]
def kept_of(tab, m):
    r = tab[m]; sd = (r["run1"] - r["billboard"]) / r["run1_sd_from_each"][0] if r["run1_sd_from_each"][0] else None
    return r["billboard"], r["rolling_stone"], sd
rows, orow, wins = [], [], {}
for ver, pre in RUNS:
    for s, ton in TON.items():
        P = pickle.load(open(f"{pre}_p{s}_{MODE8}.pkl", "rb")); st = {}; i = 0
        for name, kind, nb in P["form"]: st[name] = (i, nb); i += nb
        for bi, c in enumerate([c for c in P["every"] if not c.get("partial")][:400]):
            for name, (sec, k) in SECS.items():
                if name not in st or st[name][1] < 8: continue
                b0 = st[name][0]; raw = sorted(((t[0] - b0 * 48) / 12, t[2], (P["chords2"][t[0] // 24] if P.get("chords2") else P["chords"][t[0] // 48])) for t in c["notes"] if b0 * 48 <= t[0] < (b0 + 8) * 48 and t[3] == name)
                m = om([(t, p, pcs(ch)) for t, p, ch in raw], ton, s in MINOR8)
                if m: rows.append(dict(m, ver=ver, song=s, build=bi, sec=sec, k=k)); wins[(ver, s, bi, sec, k)] = [(t, p) for t, p, ch in raw]
                if k == "1" and sec in ("verse", "chorus"):
                    o = outer([(t, p, eng(ch)) for t, p, ch in raw])
                    if o: orow.append(dict(o[0], ver=ver, song=s, build=bi, sec=sec))
A = pd.DataFrame(rows); O = pd.DataFrame(orow); S = lambda D, s, k: D[(D.sec == s) & (D.k == k)]; first = lambda D: D[(D.k == "1") & D.sec.isin(("verse", "chorus"))]
out = {"about": __doc__.split("Usage")[0].strip(), "runs": [v for v, _ in RUNS], "builds read (each run, song)": 400}
def block(tab, D, ms):
    o = {}
    for m in ms:
        if m not in tab or m not in D: continue
        bb, rs, sd = kept_of(tab, m); r = dict(billboard=bb, rolling_stone=rs, kept_sd=round(sd, 4) if sd else None)
        for v, _ in RUNS:
            e = D[D.ver == v]; r[v] = round(float(e[m].mean()), 4); r[v + "_by_song"] = [round(float(e[e.song == s][m].mean()), 4) for s in TON]
            r[v + "_sd_from_kept"] = round(float((e[m].mean() - (bb + rs) / 2) / sd), 2) if sd else None
        o[m] = r
    return o
out["first verse and chorus"] = block(FV, first(A), list(FV))
out["the melody over chord and bass"] = block(FO, O, list(FO))
out["chorus first beat on the third (billboard 0.247, rolling stone 0.294)"] = {v: round(float(O[(O.ver == v) & (O.sec == "chorus")].downbeat_on_third.mean()), 4) for v, _ in RUNS}
out["chorus first beat on the third, by song"] = {v: [round(float(O[(O.ver == v) & (O.sec == "chorus") & (O.song == s)].downbeat_on_third.mean()), 4) for s in TON] for v, _ in RUNS}
v2 = {}
for v, _ in RUNS:
    D = A[A.ver == v].assign(bid=lambda d: d.song + "_" + d.build.astype(str)); a, b = S(D, "verse", "1").set_index("bid"), S(D, "verse", "2").set_index("bid"); ix = a.index.intersection(b.index)
    dd = {m: round(float((b.loc[ix, m] - a.loc[ix, m]).mean() / KS["verse 1"][m]["sd"]), 2) for m in FE}
    bysong = {}
    for s in TON:
        jx = [x for x in ix if x.startswith(s + "_")]
        bysong[s] = int(sum(abs((b.loc[jx, m] - a.loc[jx, m]).mean() / KS["verse 1"][m]["sd"]) < .15 for m in FE)) if jx else None
    pk = pd.DataFrame([pair(wins[(v, s, bi, "verse", "1")], N) for (vv, s, bi, sec, k), N in wins.items() if vv == v and sec == "verse" and k == "2" and (vv, s, bi, "verse", "1") in wins])
    v2[v] = {"pairs": len(ix), "measures under 0.15 kept sd, of 27": int(sum(abs(x) < .15 for x in dd.values())), "by song (of 27)": bysong, "every measure (kept sd)": dd,
             "chord tones on the beat, verse 1 / verse 2 (by song)": {s: [round(float(a.loc[[x for x in ix if x.startswith(s + "_")], "chord_tones_on_beat"].mean()), 3), round(float(b.loc[[x for x in ix if x.startswith(s + "_")], "chord_tones_on_beat"].mean()), 3)] for s in TON},
             "chord tones on the beat, verse 1 / verse 2 (pooled)": [round(float(a.loc[ix, "chord_tones_on_beat"].mean()), 3), round(float(b.loc[ix, "chord_tones_on_beat"].mean()), 3)],
             "verse 1 / verse 2 / kept verse 2": {m: [round(float(a.loc[ix, m].mean()), 3), round(float(b.loc[ix, m].mean()), 3), round(KS["verse 2"][m]["mean"], 3)] for m in ("chord_tones_on_beat", "chord_tones", "repeat", "step", "equal_gap_run_max", "gap_eighth")},
             "pair (bars the same rhythm, onsets shared, pitch kept, notes ratio)": [round(float(pk[c].mean()), 3) for c in ("bars_same_rhythm", "onsets_shared", "pitch_kept", "notes_ratio")] if len(pk) else None}
out["the second verse less the first, paired by build (434's test: under 0.15 kept sd on 20 of 27; kept: Billboard 23, Rolling Stone 23)"] = v2
KD = T125["findings"]["at the builds' own density: kept mean, builds' mean, difference in kept sd"]
def band(npb): return "3.5 to 4.5 notes a bar" if npb < 4.5 else "4.5 to 5.5 notes a bar" if npb < 5.5 else "5.5 to 9 notes a bar"
dens = {}
for v, _ in RUNS:
    D = first(A[A.ver == v]).assign(b=lambda d: d.notes_per_bar.map(band)); o = {}
    for bd, x in D.groupby("b"):
        o[bd] = {m: [KD[bd][m][0], round(float(x[m].mean()), 3)] for m in ("equal_gap_run_max", "gap_same_as_before", "zigzag_of_three", "gap_eighth", "turns_per_move", "range")} | {"windows": len(x)}
    dens[v] = o
out["at the windows' own density (kept, run)"] = dens
# toward or away from the kept songs, each run against the one before (first verse and chorus, the melody over the chord, the pair)
mv = {}
for (v0, _), (v1, _) in zip(RUNS, RUNS[1:]):
    tw, aw, same = [], [], []
    for grp in ("first verse and chorus", "the melody over chord and bass"):
        for m, r in out[grp].items():
            k = (r["billboard"] + r["rolling_stone"]) / 2; sd = r["kept_sd"] or 1.0; d0, d1 = abs(r[v0] - k) / sd, abs(r[v1] - k) / sd
            (tw if d1 < d0 - 0.02 else aw if d1 > d0 + 0.02 else same).append((m, round(d0, 2), round(d1, 2)))
    a0, a1 = v2[v0]["every measure (kept sd)"], v2[v1]["every measure (kept sd)"]
    for m in FE:
        (tw if abs(a1[m]) < abs(a0[m]) - 0.02 else aw if abs(a1[m]) > abs(a0[m]) + 0.02 else same).append(("verse 2 less verse 1: " + m, abs(a0[m]), abs(a1[m])))
    mv[f"{v1} against {v0}"] = {"toward kept (measure, sd from kept before, after)": tw, "away": aw, "within 0.02 sd": [x[0] for x in same]}
out["moved toward kept, or away"] = mv
json.dump(out, open(OUT, "w"), indent=1, default=str)
for v in v2: print(v, v2[v]["measures under 0.15 kept sd, of 27"], v2[v]["chord tones on the beat, verse 1 / verse 2 (pooled)"], v2[v]["pair (bars the same rhythm, onsets shared, pitch kept, notes ratio)"])
for k, x in mv.items(): print(k, "toward", len(x["toward kept (measure, sd from kept before, after)"]), "away", len(x["away"]))
