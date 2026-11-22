"""749.146: how often a kept verse line takes one bar, by its syllables and the tempo. See PREDICTION.md and RESULT.md.
The lines are the transcribers' lyric lines, as studies/metre/lines_cocopops.py reads them from the CoCoPops scores (a line starts at a capital letter or after two beats of silence);
that script writes cocopops_lines.json, which is not committed. python3 studies/lever_range/study.py path/to/cocopops_lines.json -> result.json
(A first run read the kept corpus's own line index instead, which marks longer phrases, not lyric lines; its figures were wrong and are not kept.)"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); L = [l for l in json.load(open(sys.argv[1])) if l["slot_beats"] and 0 < l["slot_beats"] <= 32]
band = lambda b: "fast (bar under 1.8 s)" if b < 1.8 else "slow (bar 2.6 s or more)" if b >= 2.6 else "middle"; one = lambda G: round(float(np.mean([l["slot_beats"] / 4 <= 1.05 for l in G])), 3) if G else None
out = dict(lines=len(L), songs=len({l["song"] for l in L}), note="a line's slot = its first onset to the next line's first onset; one bar or less = slot <= 1.05 bars, as studies/metre", verse={}, chorus={})
for role in ("verse", "chorus"):
    for n in range(3, 13):
        G = [l for l in L if l["role"] == role and l["syl"] == n]
        out[role][str(n)] = dict(lines=len(G), one_bar_or_less=one(G), median_slot_bars=round(float(np.median([l["slot_beats"] / 4 for l in G])), 2),
                                 by_tempo={b: dict(lines=sum(band(l["barsec"]) == b for l in G), one_bar_or_less=one([l for l in G if band(l["barsec"]) == b])) for b in ("fast (bar under 1.8 s)", "middle", "slow (bar 2.6 s or more)")})
v = out["verse"]; out["rule"] = dict(eight_syllable_verse_lines_in_one_bar=v["8"]["one_bar_or_less"], range_by_the_rule=[n for n in range(3, 13) if v[str(n)]["one_bar_or_less"] >= v["8"]["one_bar_or_less"]],
                                     by_tempo={b: dict(eight=v["8"]["by_tempo"][b]["one_bar_or_less"], range=[n for n in range(3, 13) if v[str(n)]["by_tempo"][b]["lines"] >= 15 and v[str(n)]["by_tempo"][b]["one_bar_or_less"] >= v["8"]["by_tempo"][b]["one_bar_or_less"]]) for b in v["8"]["by_tempo"]})
print(json.dumps(out["rule"], indent=1)); json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
