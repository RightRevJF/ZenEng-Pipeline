"""After the result (a description, not a test): what a piled verse is made of. Each record's fitted spec, a thousand builds. -> describe.json"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
out = {}
for name, stem in (("50", "songs/p60/lyric50"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); spec = rec["spec"]; E = M.Engine(json.loads(json.dumps(spec)))
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); mu = spec["registers"]["Verse"][0]; deg = collections.Counter(); off = []; rep = []; dist = []; sh = []; nline = collections.Counter(E.HOW.get(k, ["fresh"])[0] for k in E.KEYS if CP.kind(k[0]) == "Verse"); syl = [len(E.LINES[s][i]) for s, i in E.KEYS if CP.kind(s) == "Verse"]; inline = []
    for _ in range(1000):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        v = [n for n in sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]) if CP.kind(n["sec"]) == "Verse"]; ps = [n["p"] for n in v]; p0, cnt = collections.Counter(ps).most_common(1)[0]
        deg[(p0 - 0) % 12] += 1; off.append(p0 - mu); sh.append(cnt / len(ps)); dist.append(len(set(ps)))
        same = [a["p"] == b["p"] for a, b in zip(v, v[1:]) if a["sec"] == b["sec"] and a["line"] == b["line"]]; rep.append(sum(same) / max(1, len(same)))
    n = len(sh); out[name] = dict(living=n, verse_lines_by_how=dict(nline), middle_syllables_a_verse_line=st.median(syl), middle_share_on_the_commonest_pitch=round(st.median(sh), 3), middle_share_of_repeated_notes_inside_verse_lines=round(st.median(rep), 3), middle_number_of_different_pitches_in_the_verses=st.median(dist),
        the_commonest_pitch_less_the_verse_centre_quartiles=[sorted(off)[int(q * (n - 1))] for q in (.25, .5, .75)], commonest_pitch_class_top3={str(k): round(c / n, 2) for k, c in deg.most_common(3)}, repeat_asked=spec["target"]["readings"]["repeated notes"], repeat_weight=spec["target"]["moves"]["repeat"])
    print(name, json.dumps(out[name]), flush=True)
json.dump(out, open(os.path.join(HERE, "describe.json"), "w"), indent=1)
