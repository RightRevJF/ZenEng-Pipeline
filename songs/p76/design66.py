"""Song 66 (They Did the Right Thing), the design copy: the writer's key, A minor, for a tenor.
The engine draws the tune against a written tonic and only then chooses the key. Its own run (lyric66.song.json) put the tonic at the
bottom of the tune (2 to 19 semitones over it), which sits a tenor in D minor; in A minor that tune is either B2 to E4 or B3 to E5.
The writer chose A minor (intake LOG). So one design gate: a build lives only if the whole tune fits a tenor (C3 to A4, chord_writer.VOICES)
over an A3 tonic, that is from 9 under the written tonic to 12 over it; and the key is A minor on A3 (MIDI 57).
Everything else is the engine as it is (v52, no switch on).
    PYTHONHASHSEED=0 python3 design66.py [builds] [drafts]  -> run_d/lyric66_d.song.json"""
import sys, os, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [os.path.join(ROOT, "lib", "luthier")]
import song_from_lyric as SL, chord_writer as C, metre_engine as M
TONIC = 57; LO, HI = C.VOICES["tenor"]; DOWN, UP = LO - TONIC, HI - TONIC          # -9 and +12 over the written tonic (60)
_gates = M.Engine.gates
def gates(self, c):
    e = _gates(self, c)
    if e: return e
    ps = [n["p"] - 60 for n in c["notes"]]
    if min(ps) < DOWN or max(ps) > UP: return "design: the tune inside a tenor over an A3 tonic (the writer's A minor)"
    return None
M.Engine.gates = gates
_ck = C.choose_key
def choose_key(low, high, voice="tenor", lead="guitar", mode="major", centre=None):
    ks = [k for k in _ck(low, high, voice, lead, mode, centre) if k["key"] == "Am" and k["tonic_midi"] == TONIC]
    return ks
C.choose_key = choose_key; SL.C.choose_key = choose_key
if __name__ == "__main__":
    os.chdir(HERE); os.makedirs("run_d", exist_ok=True); shutil.copy("lyric66.json", "run_d/lyric66_d.json")
    L = json.load(open("run_d/lyric66_d.json")); N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000; K = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    rec = SL.write(L, N, K); out = "run_d/lyric66_d.song.json"; json.dump(rec, open(out, "w"), indent=1, default=float)
    if "error" in rec: print(rec["error"], rec.get("deaths"), rec.get("flags")); sys.exit(1)
    SL.BD.midi(rec, out.replace(".json", ".mid")); m = rec["melody"]
    print(f"key {rec['key']['key']} ({rec['key']['lowest']}-{rec['key']['highest']}); chord draft {rec['chord_pick']['draft']}")
    print(f"melody: {m['survivors']} of {m['made']} survive; pick {m['pick']} charge {m['charge']}; deaths {m['deaths']}")
    for n, k, nb in rec["form"]: print(f"  {n}: " + " | ".join(rec["chords"][n]))
    print("judge 7:", {k: v for k, v in (rec.get("judge7") or {}).items() if k in ("pick_distance", "kept_middle_half", "builds", "pass_the_gate", "pool")})
    print("checks:", rec["checks"]); print("flags:", rec["flags"])
