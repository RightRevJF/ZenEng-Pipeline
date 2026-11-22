"""Song 61, second edition: the writer's hand edits to the engine's pick, logged in intake.py. Reads lyric61.song.json (the engine's record,
untouched) and writes lyric61.hand.song.json, which the document scripts read. Every edit keeps the line's syllables and stays diatonic.
  1. 'Three, and then two' (verse 3 and the last chorus): the engine sang 'three' a quarter beat and held 'and' and 'then' (2.25 and 3.25 beats).
     Now like the knock: 'three' on the downbeat for a beat and a half (its melisma kept), a half-beat breath, 'and then' quick on beat 3,
     'two' on the next downbeat, held to where the engine's 'two' ended. Same pitches.
  2. 'when we were kids' (verse 3): 'were' was held 1.25 beats and 'kids' a half. Now 'were' a half beat and 'kids' held two, and 'kids' lifts
     to G#4 (the third of the key) where the engine kept it on E4: one diatonic change of a line's melody in verse 3."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "lib", "luthier"))
R = json.load(open(os.path.join(HERE, "lyric61.song.json"))); BAR = R["bar"]; B = BAR // 4
N = R["melody"]["notes"]
def line(sec, i): return sorted([n for n in N if n["sec"] == sec and n["line"] == i], key=lambda n: n["on"])
EDITS = []
for sec in ("Verse 3", "Last Chorus"):
    i = 4 if sec == "Verse 3" else 6
    ns = line(sec, i); three, mel, and_, then, two = ns; t0 = three["on"]; end = two["on"] + two["dur"]; nxt_bar = (t0 // BAR + 1) * BAR
    assert [three["text"], mel["text"], and_["text"], then["text"], two["text"]] == ["three", "", "and", "then", "two"], [n["text"] for n in ns]
    before = [(n["text"], n["on"], n["dur"], n["midi"]) for n in ns]
    three["dur"] = B; mel["on"] = t0 + B; mel["dur"] = B // 2
    and_["on"] = t0 + 2 * B; and_["dur"] = B // 2; then["on"] = t0 + 2 * B + B // 2; then["dur"] = B // 2
    two["on"] = nxt_bar; two["dur"] = end - nxt_bar
    EDITS.append(dict(where=f"{sec}, line {i + 1}", before=before, after=[(n["text"], n["on"], n["dur"], n["midi"]) for n in ns]))
ns = line("Verse 3", 3); were, kids = ns[-2], ns[-1]
assert (were["text"], kids["text"]) == ("were", "kids")
before = [(n["text"], n["on"], n["dur"], n["midi"]) for n in (were, kids)]; end = kids["on"] + kids["dur"]
were["dur"] = B // 2; kids["on"] = were["on"] + B // 2; kids["dur"] = 2 * B; kids["midi"] = R["key"]["tonic_midi"] + 4 + 12 * ((kids["midi"] - R["key"]["tonic_midi"]) // 12)
EDITS.append(dict(where="Verse 3, line 4", before=before, after=[(n["text"], n["on"], n["dur"], n["midi"]) for n in (were, kids)]))
N.sort(key=lambda n: n["on"])
for a, b in zip(N, N[1:]): assert a["on"] + a["dur"] <= b["on"], (a, b)
import word_weight as WW_
fit = {k: round(v, 3) for k, v in WW_.fit([n for n in N if n.get("melisma") != "second"], BAR, B, parts=True).items()}
R["hand_edits"] = dict(note="the writer's hand edits (hand61.py), logged in intake.py; the engine's record is lyric61.song.json", edits=EDITS,
                       words_fit_engine=R["judge7"]["pick_words_fit"], words_fit_after=fit)
json.dump(R, open(os.path.join(HERE, "lyric61.hand.song.json"), "w"), indent=1)
if __name__ == "__main__":
    for e in EDITS: print(e["where"], "\n  before", e["before"], "\n  after ", e["after"])
    print("words' fit: engine", R["judge7"]["pick_words_fit"], "after", fit)
