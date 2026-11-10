"""The First Wood -- the readings v76-v88 print for every song, from the record and the pick: outer voices (135), repetition (146),
text setting (149), rhythm (158), declamation and schemas (161, 162), harmony (173) with pull and distance (175); and the class's
numbers beside each, from the tables file. Saved for the test report and the consistency check."""
import pickle, json, collections, sys, re
import numpy as np
sys.path[:0] = ["/home/claude/p35", "/home/claude/carol", "/home/claude/pop"]
import melody_p35 as M
REC = pickle.load(open("/home/claude/p35/song_record.pkl", "rb")); T = M.T
PICK = pickle.load(open("/home/claude/p35/melody_result.pkl", "rb"))["alive"][0]
notes = PICK["notes"]; harm = PICK["harm"]; V = REC["voices"]
out = collections.OrderedDict()
# 135 outer voices (tune and bass)
out["outer_voices"] = {k: round(v, 3) if isinstance(v, float) else v for k, v in M.outer(notes, harm).items()}
out["outer_voices_class_median"] = T["outer_voices"]["hymns"]["median"]
# 146 repetition
rep = M.repetition(notes); legs = M.sequences(notes)
out["repetition"] = dict(rep, sequences=legs)
out["repetition_class_median"] = {k: T["repetition"]["hymns"]["median"][k] for k in ("rhythm_recurs", "exact", "transposed", "distinct_rhythms", "rhythms_for_80pct")}
# 158 rhythm reading
ons = [n["on"] for n in notes]; durs = [n["dur"] for n in notes]
iois = [b - a for a, b in zip(ons, ons[1:] + [24 * 36])]
pos = [o % 36 for o in ons]
cnt = lambda xs, f: sum(1 for x in xs if f(x)) / len(xs)
npvi = 100 * np.mean([abs(a - b) / ((a + b) / 2) for a, b in zip(iois, iois[1:])])
out["rhythm"] = dict(on_downbeat=round(cnt(pos, lambda p: p == 0), 3), on_other_beats=round(cnt(pos, lambda p: p in (12, 24)), 3),
                     on_eighth_offbeat=round(cnt(pos, lambda p: p % 12 == 6), 3), pushed=0.0, ioi_eighth=round(cnt(iois, lambda d: d == 6), 3),
                     ioi_quarter=round(cnt(iois, lambda d: d == 12), 3), ioi_half=round(cnt(iois, lambda d: d == 24), 3), ioi_longer=round(cnt(iois, lambda d: d > 24), 3),
                     npvi=round(float(npvi), 1), onsets_per_bar=round(len(notes) / 24, 2), notes_per_second=round(len(notes) / (24 * 3 * 60 / 92), 2),
                     bar_rhythms_in_class_vocabulary=round(sum(1 for b, r in M.bar_rhythms(notes).items() if tuple(r) in set(M.VOCAB)) / 24, 3))
out["rhythm_class_median"] = {k: T["rhythm_by_class"]["hymns"]["median"][k] for k in ("on_downbeat", "on_other_beats", "on_eighth_offbeat", "pushed", "ioi_eighth", "ioi_quarter", "ioi_half", "npvi", "onsets_per_bar")}
# 161, 162 declamation
dec = M.declamation(PICK)
sch = collections.Counter(r["schema"] for r in dec)
out["declamation"] = dict(lines=len(dec), last_stress_on_downbeat=round(sum(r["last_strong"] for r in dec) / len(dec), 3),
                          starts_before_downbeat=round(sum(r["starts_before_downbeat"] for r in dec) / len(dec), 3),
                          span_bars=dict(collections.Counter(r["span"] for r in dec)), schemas=sch.most_common(8))
# 149 text setting (stanza 1's words; the tune is the same in every stanza)
st = M.WORDS[0]; first = {}; groups = collections.defaultdict(list)
for n in notes: groups[(n["line"], n["syl"])].append(n)
init_s, later_s, init_d, later_d = [], [], [], []
def strength(t): p = t % 36; return 1.0 if p == 0 else (0.5 if p % 12 == 0 else 0.25)
for ln in M.LINES:
    sy = st[ln]
    for j, x in enumerate(sy):
        g = groups[(ln, j)]; d = sum(n["dur"] for n in g); s = strength(g[0]["on"])
        initial = j == 0 or sy[j - 1][0] != x[0]
        (init_s if initial else later_s).append(s); (init_d if initial else later_d).append(d)
mel = [k for k, g in groups.items() if len(g) > 1]
phr_end_mel = [k for k in mel if k[1] == M.NSYL[k[0]] - 1]
fin = []
for ln in M.LINES:
    ds = [sum(n["dur"] for n in groups[(ln, j)]) for j in range(M.NSYL[ln])]
    fin.append(ds[-1] / np.median(ds))
summit = [n for n in notes if n["p"] == M.SUMMIT][0]
out["text_setting"] = dict(initial_strength=round(float(np.mean(init_s)), 3), later_strength=round(float(np.mean(later_s)), 3),
                           dur_ratio_initial_over_later=round(float(np.mean(init_d) / np.mean(later_d)), 3), melisma_rate=round(len(mel) / sum(M.NSYL.values()), 3),
                           melismas_at_phrase_end=len(phr_end_mel), final_lengthening_median=round(float(np.median(fin)), 2),
                           phrase_starts_off_downbeat=round(sum(1 for ln in M.LINES if [n for n in notes if n["line"] == ln][0]["on"] % 36 != 0) / 6, 3),
                           summit=dict(word=st["R1"][summit["syl"]][0], vowel=st["R1"][summit["syl"]][1], dur=summit["dur"], first_reached_at=round(notes.index(summit) / len(notes), 2)))
# 173 harmony reading; 175 pull and distance
chs = [v["chord"] for v in V]
before_tonic = collections.Counter(a for a, b in zip(chs, chs[1:]) if b == "I" and a != "I")
root = lambda c: M.root_of(c)
motion = collections.Counter()
for a, b in zip(chs, chs[1:]):
    d = (root(b) - root(a)) % 12
    motion["fall fifth" if d == 5 else "rise fifth" if d == 7 else "step" if d in (1, 2, 10, 11) else "third" if d in (3, 4, 8, 9) else "same"] += 1
tonic_time = sum(v["end"] - v["on"] for v in V if v["chord"] in ("I", "I64")) / sum(v["end"] - v["on"] for v in V)
nct = 0; nct_step = 0
for i, n in enumerate(notes):
    h = [x for x in harm if x["on"] <= n["on"] < x["end"]][0]
    if n["p"] % 12 not in M.tones_of(h["chord"]):
        nct += 1; nxt = notes[i + 1]["p"] if i + 1 < len(notes) else None
        if nxt is not None and abs(nxt - n["p"]) <= 2: nct_step += 1
PULL = {"V": 0.80, "V7": 0.80, "vii": 0.77, "IV": 0.31, "vi": 0.13, "ii": 0.12, "iii": 0.04, "I": 0.0, "I64": 0.0}     # Table CO, classical (Mozart)
DIST = {"I": 0, "I64": 0, "V": 5, "V7": 5, "IV": 5, "iii": 7, "vi": 7, "ii": 8, "vii": 8}                             # Lerdahl, from the tonic
out["harmony"] = dict(chords=len(chs), distinct=len(set(chs)), chords_per_bar=round(len(chs) / 24, 2), tonic_time=round(tonic_time, 3),
                      sevenths=round(sum(1 for c in chs if c == "V7") / len(chs), 3), inverted=round(sum(1 for v in V if v["bass"] % 12 != root(v["chord"])) / len(V), 3),
                      before_the_tonic=dict(before_tonic), root_motion=dict(motion), nonchord_notes=nct, nonchord_resolving_by_step=(round(nct_step / nct, 3) if nct else None),
                      pull_mean=round(float(np.mean([PULL[c] for c in chs])), 3), distance_mean_from_tonic=round(float(np.mean([DIST[c] for c in chs])), 2))
out["harmony_class_median"] = {k: T["harmony_by_class"]["bach_chorales"]["median"][k] for k in ("distinct", "tonic_time", "sevenths", "inverted", "chords_per_bar")}
out["harmony_class_before_tonic"] = T["harmony_by_class"]["bach_chorales"]["before_the_tonic"][:4]
out["bands"] = dict(pitch_bits=PICK["meas"]["pitch_bits"], pitch_band=[M.PBAND["p05"], M.PBAND["p95"]], rhythm_bits=PICK["meas"]["rhythm_bits"], rhythm_band=[M.RBAND["p05"], M.RBAND["p95"]])
pickle.dump(out, open("/home/claude/p35/readings.pkl", "wb"))
if __name__ == "__main__":
    for k, v in out.items(): print(k, json.dumps(v, default=str)[:600])
