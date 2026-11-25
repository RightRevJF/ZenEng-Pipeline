"""The two readings on the builds (PREDICTION.md). The record's fitted spec is run again, a thousand builds.
    python3 studies/the_draw/read_builds.py songs/p65/lyric55   -> builds_lyric55.json"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [os.path.normpath(os.path.join(HERE, "..", "..", "lib", "luthier")), os.path.normpath(os.path.join(HERE, "..", "..", "tables", "metre_atlas"))]
import song_from_lyric as SL, metre_engine as M, word_weight as WW
stem = sys.argv[1]; L = json.load(open(stem + ".json")); rec = json.load(open(stem + ".song.json")); N = 1000
def engine(octave, peak):
    spec = json.loads(json.dumps(rec["spec"])); spec["no_leap_past_an_octave"] = octave
    if not peak: spec["target"].pop("peak", None)
    E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    return E, spec
def living(E):
    rng = random.Random(L.get("seed", 1))
    for _ in range(N):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        yield sorted(E.as_sung(c["notes"]), key=lambda n: n["on"])
def leaps(E, sung):
    top = max(n["p"] for n in sung); by = collections.defaultdict(list); out = []
    for n in sung: by[(n["sec"], n["line"])].append(n)
    for (sec, i), ln in by.items():
        iv = [b["p"] - a["p"] for a, b in zip(ln, ln[1:])]
        for j, d in enumerate(iv):
            if abs(d) <= 12: continue
            far = ln[j + 1] if d > 0 else ln[j]                                   # the higher note of the leap
            pair = any(abs(iv[q]) > 12 and iv[q] * d < 0 for q in (j - 2, j - 1, j + 1, j + 2) if 0 <= q < len(iv))
            out.append(dict(kind=E.KIND.get(sec), how=E.HOW.get((sec, i), ["fresh"])[0], where="first" if j == 0 else "last" if j == len(iv) - 1 else "between", pair=pair, up=d > 0,
                            far_stress=bool(far.get("stress")), far_dur=far["dur"], far_top=far["p"] == top))
    return out
out = dict(song=os.path.basename(stem), A={}, B={})
for name, peak in (("as it is", True), ("the plant taken out", False)):
    E, _ = engine(False, peak); rows = []; nb = 0; withleap = 0; notes = 0; ranges = []
    for sung in living(E):
        nb += 1; lp = leaps(E, sung); withleap += bool(lp); rows += lp; notes += len(sung); ranges.append(max(n["p"] for n in sung) - min(n["p"] for n in sung))
    n = max(1, len(rows)); sh = lambda f: round(sum(1 for r in rows if f(r)) / n, 3)
    out["A"][name] = dict(living=nb, builds_with_a_leap=round(withleap / max(1, nb), 3), leaps=len(rows), per_1000_notes=round(1000 * len(rows) / max(1, notes), 2), median_range=sorted(ranges)[len(ranges) // 2] if ranges else None,
        far_note_is_the_builds_top_in_a_chorus=sh(lambda r: r["far_top"] and r["kind"] == "Chorus"), far_note_is_the_builds_top=sh(lambda r: r["far_top"]), in_a_pair=sh(lambda r: r["pair"]), far_note_stressed=sh(lambda r: r["far_stress"]),
        by_part=dict(collections.Counter(r["kind"] for r in rows)), by_how=dict(collections.Counter(r["how"] for r in rows)), by_place=dict(collections.Counter(r["where"] for r in rows)), far_median_length=sorted(r["far_dur"] for r in rows)[len(rows) // 2] if rows else None)
# B: title lines, the spec as it is
E, spec = engine(rec["spec"].get("no_leap_past_an_octave"), True); hooks = [h.rsplit(":", 1) for h in spec.get("hooks", ())]; cases = []; lines = 0; builds_any = 0; nb = 0; LEN = collections.defaultdict(list)
for sung in living(E):
    nb += 1; anyc = False
    for sec, i in hooks:
        ln = [n for n in sung if n["sec"] == sec and n["line"] == int(i) and n.get("melisma") != "second"]
        if len(ln) < 2: continue
        lines += 1; tr = WW.tier([(n["text"], n["stress"]) for n in ln])
        for n, t in zip(ln, tr): LEN[("stressed", "weak", "function word")[2 - t if t else 2] if t != 1 else "weak"].append(n["dur"])
        top = max(ln, key=lambda n: n["dur"]); k = ln.index(top)
        if top.get("stress") or not any(n["text"] != ln[-1]["text"] for n in ln[k:]): continue
        gaps = [b["on"] - a["on"] for a, b in zip(ln, ln[1:])]; st = [n["dur"] for n in ln if n["stress"]]
        cases.append(dict(kind="function word" if tr[k] == 0 else "weak syllable of a longer word", first=k == 0, how=E.HOW.get((sec, int(i)), ["fresh"])[0], before_widest_gap=k < len(gaps) and gaps[k] == max(gaps),
                          longest_stressed_short_by=top["dur"] - max(st) if st else None, dur=top["dur"])); anyc = True
    builds_any += anyc
n = max(1, len(cases)); sh = lambda f: round(sum(1 for r in cases if f(r)) / n, 3)
out["B"] = dict(living=nb, title_lines=lines, cases=len(cases), cases_in_100_title_lines=round(100 * len(cases) / max(1, lines), 1), builds_with_a_case=round(builds_any / max(1, nb), 3),
    function_word=sh(lambda r: r["kind"] == "function word"), first_note_of_the_line=sh(lambda r: r["first"]), line_is_a_copy=sh(lambda r: r["how"] == "copy"), before_the_widest_gap=sh(lambda r: r["before_widest_gap"]),
    longest_stressed_shorter_by_3=sh(lambda r: r["longest_stressed_short_by"] is not None and r["longest_stressed_short_by"] <= 3), by_6=sh(lambda r: r["longest_stressed_short_by"] is not None and 3 < r["longest_stressed_short_by"] <= 6), by_more=sh(lambda r: r["longest_stressed_short_by"] is not None and r["longest_stressed_short_by"] > 6),
    by_how=dict(collections.Counter(r["how"] for r in cases)), hooks_how=dict(collections.Counter(E.HOW.get((s, int(i)), ["fresh"])[0] for s, i in hooks)), mean_length_by_kind={k: round(sum(v) / len(v), 1) for k, v in LEN.items()})
json.dump(out, open(os.path.join(HERE, f"builds_{os.path.basename(stem)}.json"), "w"), indent=1); print(json.dumps(out))
