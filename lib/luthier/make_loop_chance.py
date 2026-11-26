"""749.185 (a trial, studies/loop_chance): for each kind and mode, the chance with which a verse or bridge over the kept 75th of chord repetition is drawn again, set so that about 25 in 100 stay over it:
1 less 0.25 over the unpatched writer's own share over the kept 75th (a thousand drafts a kind; seed 749185, not the checks' seed).
    python3 lib/luthier/make_loop_chance.py   -> tables/loop_chance.json"""
import os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import chord_writer as C
if __name__ == "__main__":
    ALL = json.load(open(C.DATA)); out = dict(note="749.185, a trial: chance of drawing again a verse or bridge whose chord repetition is over the kept 75th; share_over is the unpatched writer's, a thousand drafts, seed 749185", chance={}, share_over={})
    for mode in ("major", "minor"):
        songs = [s for s in ALL if s["mode"] == mode]; W = C.Writer(mode, songs); S = C.sections(songs, mode); rng = random.Random(749185)
        for k in ("verse", "bridge"):
            src_ = [b for kk, b, _, _ in S if kk == k]; wrote = []
            for _ in range(1000):
                W.chromatic = C.weight_for(rng.choice(W.kept_out) * W.setting, mode) if W.setting > 0 else 0.0
                r = C.chord_repetition(W.section(rng, k, len(rng.choice(src_))))
                if r is not None: wrote.append(r)
            over = sum(w > W.rep_q75[k] for w in wrote) / len(wrote); out["share_over"][f"{mode} {k}"] = round(over, 3); out["chance"][f"{mode} {k}"] = round(max(0.0, 1 - 0.25 / over), 3) if over > 0 else 0.0
    json.dump(out, open(os.path.join(HERE, "..", "..", "tables", "loop_chance.json"), "w"), indent=1); print(out)
