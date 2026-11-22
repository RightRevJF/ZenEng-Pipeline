"""Song 62, the design copy: the engine writes the tune over chords set by hand where the design says, with one design gate.
  Chords (Roman numerals on the tonic; the engine's draft kept for the refrain):
    verses: a walk down that sounds like a loop and never repeats a three-chord run inside the section:
      I | I | vi | vi | IV | I | ii | V  then  I | I | vi | vi | IV | iii | ii | vi   (the bass walks C B A G F E D G / C B A G F E D A; set in build62.py)
      verse 3 ends on V instead of vi, into the last refrain
    bridge: IV | iii | ii | V | vi | iii | iv | iv   (iv, the borrowed minor, the one departure, under 'for now')
    last refrain: the refrain's chords, its last two bars turned so the title line lands on I for the first time
  Gate 4 (with gate 3 alone the judge's pick chanted, refrain lines on one note, lift 0): the refrain's median at least two semitones over the verse's. LIFT_GATE=0 turns it off.
  Gate 3 (the scorecard: the design's first tune was less plain than 85 of 100 kept tunes): the tune's surprise, bits an interval, at or under the kept median
  (749.18: the sung line on the audience's side). SURPRISE_GATE=0 turns it off, for the record of the earlier pick.
  Gate 2 (added after the first pick zigzagged an octave and a fifth across 'a nod across' and 'remembered'): no leap past an octave inside a line.
  Gate (the writer's answer to question 2): the refrain sung in fewer, longer notes: its notes' mean length at least RATIO times the verses'.
    LUTHIER_VERSE_CLOSER=off PYTHONHASHSEED=0 python3 design62.py [builds] [drafts]  -> run_d/lyric62_d.song.json"""
import sys, os, json, shutil
ROOT = "/home/claude/zeneng-pipeline"; sys.path[:0] = [os.path.join(ROOT, "lib", "luthier")]
import song_from_lyric as SL, chord_writer as C, metre_engine as M
RATIO = float(os.environ.get("REFRAIN_RATIO", "1.3"))
import page_gate as PG; PGT = PG.table()
LIFT_MIN = None if os.environ.get("LIFT_GATE", "1") == "0" else 2
SURPRISE_MAX = None if os.environ.get("SURPRISE_GATE", "1") == "0" else PGT["percentiles_10_25_50_75_90"]["surprise"][2]   # the kept median, bits an interval
V12 = [("I",), ("I",), ("vi",), ("vi",), ("IV",), ("I",), ("ii",), ("V",), ("I",), ("I",), ("vi",), ("vi",), ("IV",), ("iii",), ("ii",), ("vi",)]
V3 = V12[:15] + [("V",)]
BRIDGE = [("IV",), ("iii",), ("ii",), ("V",), ("vi",), ("iii",), ("iv",), ("iv",)]
_song = C.Writer.song
def song(self, form, seed=0, require=None):
    pl = _song(self, form, seed, require)
    for n in list(pl):
        if n in ("Verse 1", "Verse 2"): pl[n] = list(V12[:len(pl[n])])
        elif n == "Verse 3": pl[n] = list(V3[:len(pl[n])])
        elif n == "Bridge": pl[n] = list(BRIDGE[:len(pl[n])])
    last = [n for n in pl if n.startswith("Chorus")]
    if last:
        c1 = pl[last[0]]; c3 = list(c1); c3[-2:] = [("IV", "V"), ("I",)]
        for n in last[1:]:
            if n.startswith("Chorus 3"): pl[n] = c3
    return pl
C.Writer.song = song
_gates = M.Engine.gates
def gates(self, c):
    e = _gates(self, c)
    if e: return e
    v = [n["dur"] for n in c["notes"] if self.KIND.get(n["sec"]) == "Verse"]; ch = [n["dur"] for n in c["notes"] if self.KIND.get(n["sec"]) == "Chorus"]
    if v and ch and sum(ch) / len(ch) < RATIO * sum(v) / len(v): return "design: the refrain in fewer, longer notes"
    sung = sorted((getattr(self, "as_sung", None) or (lambda x: x))(c["notes"]), key=lambda n: n["on"])
    if any(a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["p"] - a["p"]) > 12 for a, b in zip(sung, sung[1:])): return "design: no leap past an octave inside a line"
    if LIFT_MIN is not None:
        import statistics as _st
        v_ = [n["p"] for n in c["notes"] if self.KIND.get(n["sec"]) == "Verse"]; c_ = [n["p"] for n in c["notes"] if self.KIND.get(n["sec"]) == "Chorus"]
        if v_ and c_ and _st.median(c_) - _st.median(v_) < LIFT_MIN: return "design: the refrain lifts at least two semitones over the verse"
    if SURPRISE_MAX is not None:
        p_ = [n["p"] for n in sung if n.get("melisma") != "second"]
        if PG.surprise(PG.ivs([int(x) for x in p_]), PGT["_C"]) > SURPRISE_MAX: return "design: melody surprise above the kept median (749.18)"
    return None
M.Engine.gates = gates
if __name__ == "__main__":
    os.makedirs("run_d", exist_ok=True); shutil.copy("lyric62.json", "run_d/lyric62_d.json")
    L = json.load(open("run_d/lyric62_d.json")); N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000; K = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    rec = SL.write(L, N, K); out = "run_d/lyric62_d.song.json"; json.dump(rec, open(out, "w"), indent=1, default=float)
    if "error" in rec: print(rec["error"], rec.get("deaths"), rec.get("flags")); sys.exit(1)
    SL.BD.midi(rec, out.replace(".json", ".mid")); m = rec["melody"]
    print(f"key {rec['key']['key']} ({rec['key']['lowest']}-{rec['key']['highest']}); chord draft {rec['chord_pick']['draft']}")
    print(f"melody: {m['survivors']} of {m['made']} survive; pick {m['pick']} charge {m['charge']}; deaths {m['deaths']}")
    for n, k, nb in rec["form"]: print(f"  {n}: " + " | ".join(rec["chords"][n]))
    print("judge 7:", {k: v for k, v in (rec.get("judge7") or {}).items() if k in ("pick_distance", "kept_middle_half", "builds", "pass_the_gate")})
    print("checks:", rec["checks"]); print("flags:", rec["flags"])
