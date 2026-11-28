"""What a seed fixes that moves K6: the song's melisma share (848), drawn once from the seed and the title among 4/4's kept quartiles. Part 1: for seeds 1 to 12 of each lyric, the share drawn, beside the six-mark share of RESULT_260_counts.json. Part 2: on builds of two seeds of one lyric, rhythm again within sections on the notes as made and as sung. python3 studies/other_metres/count_melisma_share.py -> prints JSON. A count; no note is changed."""
import os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, count_after_251 as CA, pool_count as PC
from scipy.stats import spearmanr
SL = PC.SL
def drawn(seed, title): return random.Random(f"melisma {seed} {title}").choices([SL.ORN["song_q"][0], SL.ORN["song_median"], SL.ORN["song_q"][1]], [0.25, 0.5, 0.25])[0]
def made_and_sung(lyr, rec, builds=300):
    L = json.load(open(lyr)); R = json.load(open(rec)); E, sp = CA.engine(L, R); phr = sum(sum(v) for v in sp["slots"].values()); six = PC.marks_for(sp.get("table"), True); rng = random.Random(L.get("seed", 1)); a = []; b = []; mel = []
    for _ in range(builds):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        sung = E.as_sung(c["notes"]); a.append(PC.figs(E, c["notes"], phr, True)["rhythm_again"]); b.append(PC.figs(E, sung, phr, True)["rhythm_again"]); mel.append(sum(1 for x in sung if x.get("melisma") == "second") / len(sung))
    lo = six["rhythm_again"][0]
    return dict(living_builds=len(a), the_share_drawn_in_100_syllables=drawn(L.get("seed", 1), L["title"]), second_notes_of_melismas_share_of_notes=round(float(np.mean(mel)), 3), rhythm_again_within_sections_median=dict(notes_as_made=round(float(np.median(a)), 3), as_sung=round(float(np.median(b)), 3)), meeting_the_rhythm_line_in_100=dict(notes_as_made=round(100 * float(np.mean([x >= lo for x in a])), 1), as_sung=round(100 * float(np.mean([x >= lo for x in b])), 1)))
if __name__ == "__main__":
    S = sys.argv[1]; runs = json.load(open(os.path.join(HERE, "RESULT_260_counts.json")))["count_b"]["runs"]; out = dict(the_three_shares_and_their_chances=dict(shares=[SL.ORN["song_q"][0], SL.ORN["song_median"], SL.ORN["song_q"][1]], chances=[0.25, 0.5, 0.25], whose="the kept 4/4 songs' quartiles (848)"), by_lyric={})
    for n, title in ((55, "Your Yard Man"), (49, "The World Is Asking")):
        sh = [drawn(s, title) for s in range(1, 13)]; w = [runs[f"{n}_{s}"]["m"]["six"] for s in range(1, 13)]; wo = [runs[f"{n}_{s}"]["n"]["six"] for s in range(1, 13)]
        out["by_lyric"][str(n)] = dict(by_seed=[dict(seed=s, share_drawn=sh[s - 1], six_marks_without_749_259=wo[s - 1], with_it=w[s - 1]) for s in range(1, 13)], rank_correlation_of_the_share_with_the_six_marks=dict(with_749_259=round(float(spearmanr(sh, w)[0]), 2), without=round(float(spearmanr(sh, wo)[0]), 2)),
                                       six_marks_with_749_259_by_share={str(v): [b_ for a_, b_ in zip(sh, w) if a_ == v] for v in sorted(set(sh))})
    out["made_and_sung"] = {f"song 49's words, seed {s}": made_and_sung(f"{S}/m/49_s{s}/lyric49.json", f"{S}/m/49_s{s}/lyric49.song.json") for s in (10, 11)}
    out["made_and_sung"]["song 55's words, seed 10"] = made_and_sung(f"{S}/m/55_s10/lyric55.json", f"{S}/m/55_s10/lyric55.song.json")
    print(json.dumps(out, indent=1))
