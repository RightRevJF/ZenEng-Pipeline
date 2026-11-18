"""824 (749.49): writes the keys of stage4_results.json that the held-out test does not: chromatic_setting, required_bVII, key_choice_song52, song52_written, prototype,
and (822, 823) how written songs end and how far they leave the key, by mode. Run after chord_writer.py and write_song.py.
    python3 lib/luthier/stage4_extras.py"""
import sys, json, random, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import chord_writer as C
path = os.path.join(HERE, "stage4_results.json"); R = json.load(open(path)); ex = {}
for c in (0, 0.5, 1, 2, 4):
    W = C.Writer("major", chromatic=c); rng = random.Random(3); v = [W.section(rng, k, 8) for k in ("verse", "chorus") * 150]
    ex[str(c)] = dict(out=round(st.mean(sum(1 / len(t) for t in b for x in t if x not in C.IN["major"]) / len(b) for b in v), 3), any=round(sum(any(x not in C.IN["major"] for t in b for x in t) for b in v) / len(v), 3))
W = C.Writer("major"); form3 = [("Verse 1", "verse", 8), ("Chorus 1", "chorus", 8), ("Bridge", "bridge", 8)]
req = sum(any("bVII" in t for bb in W.song(form3, seed=s, require="bVII").values() for t in bb) for s in range(40))
r = json.load(open(os.path.join(HERE, "..", "..", "songs", "p62", "spec52.run.json"))); ps = [n["p"] for n in r["pick"]["notes"]]; low, high = min(ps) - 62, max(ps) - 62
keys = {v: [(d["key"], d["lowest"], d["highest"], d["capo"]) for d in C.choose_key(low, high, v, "guitar")[:3]] for v in ("alto", "tenor", "baritone", "soprano")}
form = [("Verse 1", "verse", 8), ("Chorus 1", "chorus", 8), ("Verse 2", "verse", 8), ("Chorus 2", "chorus", 8), ("Bridge", "bridge", 8), ("Chorus 3", "chorus", 10)]; ends = {}
for mode in ("major", "minor"):
    W = C.Writer(mode); outs = []; home = home1 = 0; tonic = "I" if mode == "major" else "i"; q = lambda v: [round(sorted(v)[int(len(v) * x)], 3) for x in (0.25, 0.5, 0.75)]
    for sd in range(200):
        pl = W.song(form, seed=sd); bars = [t for b in pl.values() for t in b]; outs.append(sum(1 / len(t) for t in bars for x in t if x not in C.IN[mode]) / len(bars)); home += pl["Chorus 3"][-1][-1] == tonic; home1 += pl["Chorus 1"][-1][-1] == tonic
    ends[mode] = {"share of bars from outside the key, quartiles: kept": q(W.kept_out), "written": q(outs), "a 10-bar last chorus ends on the tonic, in 100": home / 2, "kept songs end on the tonic, in 100": round(100 * W.songend[tonic] / sum(W.songend.values())),
                  "the first chorus ends on the tonic, in 100": home1 / 2, "kept choruses, in 100": round(100 * W.kindend["chorus"][tonic] / sum(W.kindend["chorus"].values()))}
spell = {t: [C.name(x, t) for x in (("i", "bIII", "iv", "V", "bVI", "bVII") if t.endswith("m") else ("I", "IV", "V", "vi", "bVII", "II"))] for t in ("G#m", "Ebm", "Bbm", "C#m", "F#", "Db", "E")}
R.update(chromatic_setting=ex, required_bVII=[req, 40], key_choice_song52=dict(low=low, high=high, guitar=keys), endings_and_colour=ends, spelling=spell,
         prototype=json.load(open(os.path.join(HERE, "stage4_prototype_heldout.json"))),
         song52_written=[{k: o[k] for k in ("chord_seed", "chord_charge", "survivors", "charge", "chords", "chord_readings") if k in o} | {"chosen": o.get("chosen", False)} for o in json.load(open(os.path.join(HERE, "..", "..", "songs", "p62", "spec52.written_chords.json")))])
json.dump(json.loads(json.dumps(R, default=str)), open(path, "w"), indent=1); print(json.dumps(ends, indent=1)); print(spell)
