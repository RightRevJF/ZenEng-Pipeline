"""A run with the v47 proposals (proposed_v47.py), and the readings each flag is judged by. Refuses the hold-outs (songs 59, 50, 63).
    python3 lib/luthier/proposed_v47_trial.py <lyric.json> [builds] [--all | --octave --region --title-stress --no-blue --loop-less] [--vary-returns]
Writes <lyric>.v47.song.json beside the lyric and prints: survivors and deaths, the pick's region readings (and whether it is inside), its title line,
blue notes, verse chord repetition, and (with --vary-returns) the changes made to returning sections."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import proposed_v47 as P
f = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 1000; a = set(sys.argv[2:])
if os.path.basename(f).split(".")[0] in P.HOLDOUTS: raise SystemExit(f"{f} is a hold-out: not run")
allf = "--all" in a
P.apply(octave=allf or "--octave" in a, region=allf or "--region" in a, title_stress=allf or "--title-stress" in a, no_blue=allf or "--no-blue" in a, loop_less=allf or "--loop-less" in a)
import song_from_lyric as SL
L = json.load(open(f)); rec = SL.write(L, N, 12)
if "error" in rec: print(rec["error"], rec.get("deaths")); sys.exit(1)
ch = []
if "--vary-returns" in a: ch = P.vary_returns(rec); rec.setdefault("flags", []).append(f"v47 (749.167): {len(ch)} held notes lifted in returning sections")
out = f.replace(".json", ".v47.song.json"); json.dump(rec, open(out, "w"), indent=1, default=float)
m = rec["melody"]; sung = [n["midi"] for n in sorted(m["notes"], key=lambda n: n["on"]) if n.get("text")]; r = P.region_read(sung)
def rep(sec):
    seq = []
    for bar in rec["roman"][sec]:
        for x in bar.split():
            if not seq or seq[-1] != x: seq.append(x)
    seen = set(); k = 0
    for i in range(len(seq) - 2): g = tuple(seq[i:i + 3]); k += g in seen; seen.add(g)
    return round(k / max(1, len(seq) - 2), 3)
verse = next((n for n, k, b in rec["form"] if k == "verse"), None)
print(json.dumps(dict(song=rec["title"], key=rec["key"]["key"], survivors=f"{m['survivors']} of {m['made']}", deaths=m["deaths"], pick=m["pick"],
                      region={k: round(v, 3) if v is not None else None for k, v in r.items()}, in_region=P.in_region(r),
                      verse_chord_repetition=rep(verse) if verse else None, blue_song=rec["spec"].get("degrees", {}).get("blue_song"),
                      words_fit=rec["checks"].get(next(k for k in rec["checks"] if k.startswith("the words' fit"))), judge7=(rec.get("judge7") or {}).get("pick_distance"),
                      vary_returns=ch, flags=rec["flags"]), indent=1))
