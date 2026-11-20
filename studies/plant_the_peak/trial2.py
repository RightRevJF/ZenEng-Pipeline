"""749.111, second trial outside the engine: the peak placed more surely. See PREDICTION2.md. python3 studies/plant_the_peak/trial2.py [N] -> trial2.json"""
import sys, os, json, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", ".."); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier")); N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
import kept_corpus as KC, metre_engine as M
top = lambda p: float((np.asarray(p) == max(p)).mean()); KS = list(KC.kept_songs()); K10, K90 = (float(x) for x in np.percentile([top(k["p"]) for k in KS], (10, 90)))
def kind(x): x = str(x).lower(); return "Chorus" if ("chorus" in x or "refrain" in x) else "Bridge" if "bridge" in x else "Verse" if "verse" in x else None
out = dict(kept_share_on_top_10th_90th=[round(K10, 4), round(K90, 4)])
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("59", "songs/p69/lyric59.song.json")):
    R = json.load(open(os.path.join(ROOT, path))); spec = R["spec"]; tg = spec["target"]; aim = float(tg["readings"]["range"]); k = next(k for k in KS if k["song"] == tg["kept_song"])
    i0 = int(np.argmax(np.asarray(k["p"]) == max(k["p"]))); where = kind(k["sec"][i0]) or "Chorus"; res = {}
    for form in ("as built", "A60", "C"):
        S = json.loads(json.dumps(spec)); reg = S["registers"]; floor = min(reg[x][1] for x in ("Verse", "Chorus")); P = int(floor + aim)
        E0 = M.Engine(S)
        while P % 12 not in E0.SCALE: P -= 1
        if form != "as built":
            for x in ("Verse", "Chorus", "Bridge"): reg[x][2] = P; reg[x][0] = min(reg[x][0], P - 2)
        E = M.Engine(S); orig = E.pitches; state = dict(done=False, planted=0)
        def draw(rng, ons, U, sec, i, prev, avoid=None, end_off=None, E=E, orig=orig, state=state, form=form, P=P, where=where):
            key = f"{sec}:{i}"; base = list(E.reg(sec, i)); had = E.S["registers"].get(key)
            if form != "as built" and not state["done"] and E.KIND.get(sec) == where:
                state["done"] = True; E.S["registers"][key] = [P - 3, base[1], P]; ps = None
                for _ in range(60 if form == "A60" else 1):
                    ps = orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off)
                    if ps and max(ps) == P and any(p == P and E.LINES[sec][i][j][1] for j, p in enumerate(ps)): state["planted"] += 1; break
                else:
                    if form == "C" and ps:                                                       # the line moved whole, by scale steps, until its highest stressed note is the peak
                        sc = [q for q in range(base[1] - 12, P + 13) if q % 12 in E.SCALE]; st = [p for j, p in enumerate(ps) if E.LINES[sec][i][j][1]] or ps
                        ix = lambda q: min(range(len(sc)), key=lambda z: abs(sc[z] - q)); k = ix(P) - ix(max(st)); ps2 = [sc[min(len(sc) - 1, max(0, ix(p) + k))] for p in ps]
                        if max(ps2) == P and min(ps2) >= base[1]: ps = ps2; state["planted"] += 1
                if had is None: E.S["registers"].pop(key, None)
                else: E.S["registers"][key] = had
                return ps
            if False:
                E.S["registers"][key] = [min(base[0], P - 4), base[1], P - 2]; ps = orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off)
                if had is None: E.S["registers"].pop(key, None)
                else: E.S["registers"][key] = had
                return ps
            return orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off)
        E.pitches = draw; rng = random.Random(3); sp, sh, made = [], [], 0
        for _ in range(N):
            state["done"] = False; c, err = E.build(rng); made += 1
            if err or E.gates(c): continue
            p = [n["p"] for n in c["notes"]]; sp.append(max(p) - min(p)); sh.append(top(p))
        res[form] = dict(builds=len(sp), of=made, peak=P, planted_share=round(state["planted"] / max(made, 1), 2), span_quartiles=[float(x) for x in np.percentile(sp, (25, 50, 75))] if sp else None,
                         span_within_2_of_aim=round(float(np.mean(np.abs(np.array(sp) - aim) <= 2)), 2) if sp else None, share_on_top_quartiles=[round(float(x), 3) for x in np.percentile(sh, (25, 50, 75))] if sp else None,
                         share_on_top_inside_kept_10th_90th=round(float(np.mean((np.array(sh) >= K10) & (np.array(sh) <= K90))), 2) if sp else None)
        res[form]["passes"] = bool(sp and res[form]["span_within_2_of_aim"] >= 0.5 and res[form]["share_on_top_inside_kept_10th_90th"] >= 0.9)
        print(tag, form, res[form], flush=True)
    out[tag] = dict(aims_at=tg["kept_song"], aim_range=aim, kept_song_first_reaches_its_top_in=where, forms=res)
json.dump(out, open(os.path.join(HERE, "trial2.json"), "w"), indent=1)
