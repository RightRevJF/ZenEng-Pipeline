"""749.111, third trial outside the engine: the peak planted in the chorus. See PREDICTION3.md. python3 studies/plant_the_peak/trial3.py [N] -> trial3.json"""
import sys, os, json, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", ".."); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier")); N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
sys.path[:0] = [os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import kept_corpus as KC, metre_engine as M, soundness as S
top = lambda p: float((np.asarray(p) == max(p)).mean()); KS = list(KC.kept_songs()); K10, K90 = (float(x) for x in np.percentile([top(k["p"]) for k in KS], (10, 90)))
def kind(x): x = str(x).lower(); return "Chorus" if ("chorus" in x or "refrain" in x) else "Bridge" if "bridge" in x else "Verse" if "verse" in x else None
out = dict(kept_share_on_top_10th_90th=[round(K10, 4), round(K90, 4)])
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("60", "songs/p70/lyric60.v41.song.json"), ("59", "songs/p69/lyric59.song.json")):
    R = json.load(open(os.path.join(ROOT, path))); spec = R["spec"]; tg = spec["target"]; aim = float(tg["from_its_words"]["range"]); where = "Chorus"; res = {}
    for form in ("as built", "redrawn", "moved"):
        S2 = json.loads(json.dumps(spec)); reg = S2["registers"]; floor = min(reg[x][1] for x in ("Verse", "Chorus")); E0 = M.Engine(S2); P = int(min(floor + round(aim), max(reg[x][2] for x in ("Verse", "Chorus", "Bridge"))))
        while P % 12 not in E0.SCALE: P -= 1
        if form != "as built":
            under = P - 2
            while under % 12 not in E0.SCALE: under -= 1
            reg["Chorus"][2] = P; reg["Chorus"][0] = min(reg["Chorus"][0], P - 3)
            for x in ("Verse", "Bridge"): reg[x][2] = min(reg[x][2], under); reg[x][0] = min(reg[x][0], reg[x][2] - 2)
        E = M.Engine(S2); orig = E.pitches; state = dict(done=False, planted=0)
        def draw(rng, ons, U, sec, i, prev, avoid=None, end_off=None, E=E, orig=orig, state=state, form=form, P=P, where=where):
            key = f"{sec}:{i}"; base = list(E.reg(sec, i)); had = E.S["registers"].get(key)
            if form != "as built" and not state["done"] and E.KIND.get(sec) == where:
                state["done"] = True; E.S["registers"][key] = [P - 3, base[1], P]; ps = None
                for _ in range(60 if form == "redrawn" else 1):
                    ps = orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off)
                    if ps and max(ps) == P and any(p == P and E.LINES[sec][i][j][1] for j, p in enumerate(ps)): state["planted"] += 1; break
                else:
                    if form == "moved" and ps:                                                       # the line moved whole, by scale steps, until its highest stressed note is the peak
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
        E.pitches = draw; rng = random.Random(3); sp, sh, wf, made = [], [], [], 0
        for _ in range(N):
            state["done"] = False; c, err = E.build(rng); made += 1
            if err or E.gates(c): continue
            p = [n["p"] for n in c["notes"]]; sp.append(max(p) - min(p)); sh.append(top(p))
            wf.append(S.record_row(dict(melody=dict(notes=[dict(n, midi=n["p"]) for n in sorted(c["notes"], key=lambda n: n["on"])]), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}))["the words' fit, whole"])
        res[form] = dict(builds=len(sp), of=made, peak=P, planted_share=round(state["planted"] / max(made, 1), 2), span_quartiles=[float(x) for x in np.percentile(sp, (25, 50, 75))], span_within_2_of_the_asking=round(float(np.mean(np.abs(np.array(sp) - aim) <= 2)), 2),
                         share_on_top_inside_kept_10th_90th=round(float(np.mean((np.array(sh) >= K10) & (np.array(sh) <= K90))), 2), words_fit=round(float(np.median(wf)), 3))
        print(tag, form, res[form], flush=True)
    out[tag] = dict(asked_range=round(aim, 1), forms=res)
T4 = ("55", "54", "58", "60"); out["checks"] = {}
for f in ("redrawn", "moved"):
    ok = lambda t_: [out[t_]["forms"][f]["span_within_2_of_the_asking"] >= 0.5, out[t_]["forms"][f]["share_on_top_inside_kept_10th_90th"] >= 0.8, out[t_]["forms"][f]["builds"] >= 0.7 * out[t_]["forms"]["as built"]["builds"], out[t_]["forms"][f]["words_fit"] >= out[t_]["forms"]["as built"]["words_fit"] - 0.02]
    cnt = [sum(ok(t_)[i] for t_ in T4) for i in range(4)]; out["checks"][f] = dict(songs_meeting_each_check_of_4=dict(zip(["1 range follows the words", "2 the peak is a peak", "3 builds survive", "4 the words still sit"], cnt)), passes=bool(all(c >= 3 for c in cnt)), builds_inside_the_range=round(float(np.mean([out[t_]["forms"][f]["span_within_2_of_the_asking"] for t_ in T4])), 2))
    print(f, out["checks"][f])
json.dump(out, open(os.path.join(HERE, "trial3.json"), "w"), indent=1)
