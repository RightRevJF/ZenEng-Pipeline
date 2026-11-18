import sys, json, collections, numpy as np
sys.path.insert(0, "/home/claude/zeneng/corpus/nine"); import common as C
d = C.G.d; out = {}; lift = []; reg = collections.defaultdict(list); ret = []; rest = []; top = []; lens = []
def kind(s):
    s = str(s).lower()
    return "chorus" if "chorus" in s or "refrain" in s else "verse" if "verse" in s else "bridge" if "bridge" in s else "pre" if "pre" in s else None
for s, g in d.groupby("song", sort=False):
    if str(s) not in C.PT.SONGS: continue
    g = g.sort_values("abs_beat")
    if len(g) < 150: continue
    t = np.round((g.bar.values * 4.0 + g.beat.values) * 12).astype(int); p = g.pitch.values.astype(int); du = np.round(g.dur.values * 12).astype(int); k = [kind(x) for x in g.section.values]; key = int(g.key_pc.iloc[0])
    rel = lambda q: ((q - key) % 12) + 12 * ((q - key) // 12)      # semitones above the tonic's octave
    base = int(np.median(p)); ton = min((key + 12 * o for o in range(2, 8)), key=lambda x: abs(x - (np.percentile(p, 5))))      # the tonic nearest the song's floor
    by = collections.defaultdict(list)
    for q, kk in zip(p, k):
        if kk: by[kk].append(q)
    if by["verse"] and by["chorus"] and len(by["verse"]) > 20 and len(by["chorus"]) > 20:
        lift.append(float(np.median(by["chorus"]) - np.median(by["verse"]))); top.append(float(np.percentile(by["chorus"], 95) - np.percentile(by["verse"], 95)))
    for kk, v in by.items():
        if len(v) > 20: reg[kk].append([float(np.percentile(v, 5) - ton), float(np.median(v) - ton), float(np.percentile(v, 95) - ton)])
    # sections as runs
    runs = []; 
    for i in range(len(t)):
        if not runs or runs[-1][0] != g.section.values[i] or t[i] - runs[-1][2][-1] > 96 * 2: runs.append([g.section.values[i], k[i], [t[i]], [p[i]], [du[i]]])
        else: runs[-1][2].append(t[i]); runs[-1][3].append(p[i]); runs[-1][4].append(du[i])
    # returns: later chorus against the first, bar by bar from each one's first bar
    ch = [r for r in runs if r[1] == "chorus" and len(r[2]) >= 12]
    def bars(r):
        b0 = r[2][0] // 48; B = collections.defaultdict(list)
        for tt, pp in zip(r[2], r[3]): B[tt // 48 - b0].append((tt % 48, pp))
        return B
    if len(ch) >= 2:
        A = bars(ch[0])
        for r in ch[1:]:
            Bb0 = bars(r); best = None
            for off in (-1, 0, 1):                                                           # a pickup in one and not the other moves the bars by one: the best of three alignments
                Bb = {i + off: v for i, v in Bb0.items()}; n = min(max(A) + 1, max(Bb) + 1); idx = [i for i in range(n) if A.get(i) or Bb.get(i)]
                if len(idx) < 4: continue
                same = sum(A.get(i) == Bb.get(i) for i in idx) / len(idx); rh = sum([x for x, _ in A.get(i, [])] == [x for x, _ in Bb.get(i, [])] for i in idx) / len(idx)
                if best is None or same > best[0]: best = (same, rh)
            if best is None: continue
            same, rh = best
            na = [pp for i in idx for _, pp in A.get(i, [])]; nb = [pp for i in idx for _, pp in Bb.get(i, [])]
            ret.append(dict(same=same, rhythm=rh, exact=same == 1.0))
    # rest share inside sung sections: from a run's first onset to its last note's end, the share with no note sounding
    for r in runs:
        if r[1] in ("verse", "chorus") and len(r[2]) >= 12:
            span = r[2][-1] + r[4][-1] - r[2][0]; sung = sum(min(dd, (r[2][i + 1] - r[2][i]) if i + 1 < len(r[2]) else dd) for i, dd in enumerate(r[4])); rest.append(1 - sung / max(1, span)); lens.append(len(r[2]) / (span / 48))
q = lambda v: [round(float(x), 2) for x in np.percentile(v, (10, 25, 50, 75, 90))]
out["chorus median over verse median, semitones (10, 25, 50, 75, 90)"] = q(lift); out["songs"] = len(lift); out["share with no lift (0 or less)"] = round(float(np.mean(np.array(lift) <= 0)), 3); out["share with a lift of 2 or more"] = round(float(np.mean(np.array(lift) >= 2)), 3)
out["chorus top over verse top (95th percentiles)"] = q(top)
out["register above the tonic nearest the song's floor: 5th percentile, median, 95th (medians over songs)"] = {k: [round(float(np.median([x[i] for x in v])), 1) for i in range(3)] + [len(v)] for k, v in reg.items()}
out["register quartiles"] = {k: {nm: [round(float(x), 1) for x in np.percentile([y[i] for y in v], (25, 50, 75))] for i, nm in enumerate(("floor", "centre", "top"))} for k, v in reg.items()}
out["later chorus against the first: share of bars the same (10, 25, 50, 75, 90)"] = q([r["same"] for r in ret]); out["the same in rhythm"] = q([r["rhythm"] for r in ret]); out["returns"] = len(ret); out["note for note"] = round(float(np.mean([r["exact"] for r in ret])), 3)
out["rest share inside a sung section (10, 25, 50, 75, 90)"] = q(rest); out["notes a bar inside a sung section"] = q(lens)
json.dump(dict(source="CoCoPops Billboard, the kept songs with a verse and a chorus", songs=len(lift), lifts=sorted(lift), tops=sorted(top), registers=out["register quartiles"], note="semitones; registers are above the tonic nearest the song's floor (5th percentile): floor = a section's 5th percentile, centre = its median, top = its 95th; quartiles over songs",
     returns={"note for note": out["note for note"], "bars the same, median": out["later chorus against the first: share of bars the same (10, 25, 50, 75, 90)"][2]}, rest_share=out["rest share inside a sung section (10, 25, 50, 75, 90)"]), open("/home/claude/rightrevjf/zeneng-pipeline/tables/register_plan.json", "w"), indent=1)
json.dump(out, open("kept6a.json", "w"), indent=1); print(json.dumps(out, indent=1))
