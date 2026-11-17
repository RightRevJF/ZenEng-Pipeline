"""chords_p67.py: song 57's chord plan, written by the chord writer (writers/chords.py) with no hand choice: McGill Billboard major-mode
sections, 1965-1979 weighted, E major, the bVII required somewhere (the key question's answer, A). Each section kind is drawn once;
repeats keep their chords, as kept songs do: verse 3 (16 bars) is the verse's 8 bars twice; the last chorus (14 bars) is the chorus's
12 with its last two bars again under the repeated 'Thank God' line; the ending (2 bars) is drawn as an outro ending on I.
Writes chords_p67.json (per-bar chords, the writer's report)."""
import sys, json
sys.path.insert(0, "/home/claude/zeneng-pipeline")
from writers.chords import write_song, to_bars
SEED = 20261117 + 467
BASE = [("Intro", "intro", 4), ("Verse", "verse", 8), ("Chorus", "chorus", 12), ("Bridge", "bridge", 14), ("Jam", "solo", 32), ("Outro", "outro", 8)]
plan, rep = write_song(BASE, mode="major", tonic="E", era=(1965, 1979), require={"bVII"}, seed=SEED)
P = dict(plan)
P["Verse 3"] = plan["Verse"] * 2
P["Last Chorus"] = plan["Chorus"] + plan["Chorus"][-2:]
P["Outro"], P["Ending"] = plan["Outro"][:6], plan["Outro"][6:]
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 8), ("Chorus 1", "Chorus", 12), ("Verse 2", "Verse", 8), ("Chorus 2", "Chorus", 12),
        ("Bridge", "Bridge", 14), ("Jam", "Jam", 32), ("Verse 3", "Verse 3", 16), ("Last Chorus", "Last Chorus", 14), ("Outro", "Outro", 6), ("Ending", "Ending", 2)]
for nm, k, nb in FORM: assert len(P[k]) == nb, (nm, len(P[k]), nb)
json.dump(dict(form=FORM, plan={k: [list(b) for b in v] for k, v in P.items()}, report=rep), open("chords_p67.json", "w"), indent=1)
if __name__ == "__main__":
    for k in ["Intro", "Verse", "Chorus", "Bridge", "Jam", "Outro", "Ending"]:
        print(f"{k:8}", " | ".join(" ".join(b) for b in P[k]))
        r = rep["sections"].get(k, {})
        if r: print("        ", "score", r["score"], "flags", r["flags"], {m: round(v, 2) for m, v in r["readings"].items()})
