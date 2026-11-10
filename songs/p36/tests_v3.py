"""The paper's tests for the fixes ported in version 3, run on the pick, the survivors and the builds. Writes tests_v3.pkl."""
import sys, pickle, numpy as np, collections
sys.argv = [sys.argv[0], "1", "main"]; sys.path[:0] = ["/home/claude/p36"]
import melody_v3_p36 as V
M = V.M; BAR, BEAT = V.BAR, V.BEAT
Mn = pickle.load(open("/home/claude/p36/melody_v3_main.pkl", "rb")); P = Mn["alive"][0]; notes = P["notes"]; S = Mn["alive"]
REC = pickle.load(open("/home/claude/p36/song_record_v3.pkl", "rb"))
T = {}
# 194
def st(w): return [x[1] for x in M.syl(w)]
T["194"] = dict(july=st("July"), radio=st("radio"), microwave=st("microwave"), somewhere=st("somewhere"), anyway_end=st("so I dance anyway")[-3:], anyway_mid=st("anyway the clock")[:3])
# 195: deaths at 181 where construction was used; the 8-bar stock share (bar windows)
T["195"] = dict(deaths_181=Mn["deaths"].get("returns related, on lines (181/195)", 0), stock8_pick=P["read"]["stock8"], stock8_builds_median=float(np.median(Mn["spread"]["stock8"])),
                stock8_builds_mean=float(np.mean(Mn["spread"]["stock8"])))
# 196
T["196"] = dict(two_pitch_pick=P["read"]["two_pitch"], monotony_deaths=Mn["deaths"].get("monotony run (166/196)", 0))
# 197: a leap past a fifth followed by another leap (past a fifth) in any survivor
def leap_leap(ns):
    iv = [b["p"] - a["p"] for a, b in zip(ns, ns[1:]) if a["line"] == b["line"]]
    return sum(1 for x, y in zip(iv, iv[1:]) if abs(x) > 7 and abs(y) > 4)
T["197"] = dict(pick=leap_leap(notes), survivors_with=sum(1 for c in S if leap_leap(c["notes"])), survivors=len(S))
# 198
sp = Mn["spread"]
T["198"] = dict(repeat=float(np.median(sp["iv_repeat"])), step=float(np.median(sp["iv_step"])), larger=float(np.median(sp["iv_larger"])), target=(0.276, 0.426, 0.03))
# 199: the pick's chord-tone share (all notes) and key words
on = {n["on"] for n in notes}
ct_all = sum(n["p"] % 12 in M.CH[M.chord_for(n, on)][1] for n in notes) / len(notes)
T["199"] = dict(chord_all=ct_all, middle_half=(0.536, 0.759), keyword=M.keyword_chord(notes)[0], keyword_deaths=Mn["deaths"].get("key word on a chord tone (134)", 0), keyword_deaths_v1=42)
# 200: flat 3 / flat 7 a semitone from a chord tone or a tritone from the root, in any survivor
def bad200(ns):
    o = {n["on"] for n in ns}; k = 0
    for n in ns:
        if n["p"] % 12 in (6, 1):
            r, tones = M.CH[M.chord_for(n, o)]
            if any(abs((n["p"] - t) % 12) in (1, 11) for t in tones) or (n["p"] - r) % 12 == 6: k += 1
    return k
def tri_root(ns):
    o = {n["on"] for n in ns}; return sum(1 for n in ns if (n["p"] - M.CH[M.chord_for(n, o)][0]) % 12 == 6)
T["200"] = dict(survivors_bad=sum(1 for c in S if bad200(c["notes"])), pick_bad=bad200(notes), tritone_root_pick=tri_root(notes), tritone_root_survivors=sum(1 for c in S if tri_root(c["notes"])))
# 201
med = float(np.median([n["dur"] for n in notes])); last = sorted(notes, key=lambda n: n["on"])[-1]["dur"]
T["201"] = dict(sixteenth=P["read"]["sixteenth"], final_over_median=last / med, third_bar_lines=["Verse 1 line 2", "Verse 1 line 4", "Verse 2 line 2", "Verse 2 line 4", "Chorus line 4", "Chorus line 8", "Bridge line 2"], spans=V.SPANS, nbars=V.NBARS)
# 205: across builds, the share of verse and chorus windows whose opening repeats at once
T["205"] = dict(builds_mean=float(np.mean(sp["repeat_at_once"])), builds_share_any=float(np.mean([x > 0 for x in sp["repeat_at_once"]])), pick=P["read"]["repeat_at_once"],
                pick_plans=P["meta"]["plans"], survivors_aabc=sum(1 for c in S if c["meta"]["plans"]["ChorusHead"][:2] == ["A", "A"]), survivors_total=Mn["survivors"], stored=len(S))
# 206: lengths in any 8-bar span; line-end held lengths; longest over median
ends = collections.Counter(n["dur"] for i, n in enumerate(notes) if i + 1 == len(notes) or notes[i + 1]["line"] != n["line"])
T["206"] = dict(max_lengths_any_span=max(len({n["dur"] for n in notes if b * BAR <= n["on"] < (b + 8) * BAR}) for b in range(V.NBARS - 7) if any(b * BAR <= n["on"] < (b + 8) * BAR for n in notes)),
                line_end_lengths=dict(ends), longest_over_median=max(n["dur"] for n in notes) / med, eighth_share=sum(1 for n in notes if n["dur"] == 6) / len(notes))
# 207
T["207"] = dict(spread=P["read"]["spread"], chart=(1.199, 1.615, 2.119))
# 204: the pick's windows on Table CU's measures, outside the chart middle half
outs = collections.Counter(); W = V.windows(notes)
for s, b0 in W:
    r = V.win_read(notes, b0)
    for k, (q1, q2, q3) in V.CU.items():
        if r[k] < q1 or r[k] > q3: outs[k] += 1
T["204"] = dict(windows=len(W), outside=dict(outs))
# 208
T["208"] = dict(rel_verse=P["read"]["bridge_rel_verse"], rel_chorus=P["read"]["bridge_rel_chorus"], median_minus_verse=P["read"]["bridge_median_minus_verse"], onsets_ratio=P["read"]["bridge_onsets_ratio"])
# 209: the synth never starts a note on a sung onset or while a syllable is being attacked; where it sounds
sung_on = {n["on"] for n in REC["lead"]}
syn = REC["synth"]
T["209"] = dict(statements=len(REC["riff"]["slots"]), notes=len(syn), on_sung_onset=sum(1 for s_ in syn if s_["on"] in sung_on),
                over_sung_onset=sum(1 for s_ in syn for n in REC["lead"] if s_["on"] < n["on"] < s_["on"] + s_["dur"]),
                where=sorted(set(x.split(" ")[0] if x in ("intro", "outro") else x.rsplit(" ", 1)[0] for x in REC["riff"]["slots"])), related=REC["riff"]["related"])
pickle.dump(T, open("/home/claude/p36/tests_v3.pkl", "wb"))
for k, v in T.items(): print(k, v)
