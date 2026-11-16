"""Song 54: the offline-research checks (section 2b of the songwrite skill; findings 749.4 to 749.23) read on the record.
  surprise (749.18, 749.20): melody, chord and rhythm surprise from models trained on all 21,998 Hooktheory clips (CC BY-NC-SA via
      Sheet Sage), against the corpus medians kept in studies/surprise and studies/rhythm; stress and syncopation (749.4-749.7, 749.15)
  intensity (749.17): the band's energy by section from the demo (9.12's reader): where the top falls, the release, each return higher
  the breath (749.19): where it falls and the note she re-enters on
  perception (749.21): Module 9.14's low intervals in each chordal part's own voicing; the band over the sung line (and within a second);
      phrases in seconds
  two channels (749.22): chord changes inside sections; the sung line's rests and length variety
  chromatic (749.23): chords outside the key"""
import json, gzip, pickle, sys, collections
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import surprise_hooktheory as SH, surprise_rhythm as RR
REC = pickle.load(open("/home/claude/p64/song_record.pkl", "rb")); DEMO = pickle.load(open("/home/claude/p64/out/demo_report.pkl", "rb"))
S_MED = json.load(open("/home/claude/zeneng-pipeline/studies/surprise/surprise_our_songs.json"))["reference"]
R_MED = json.load(open("/home/claude/zeneng-pipeline/studies/rhythm/rhythm_our_songs.json"))["medians"]
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/surprise")
import importlib.util
spec = importlib.util.spec_from_file_location("sos", "/home/claude/shape/surprise_our_songs.py"); SOS = importlib.util.module_from_spec(spec); spec.loader.exec_module(SOS)
lead = sorted(REC["lead"], key=lambda n: n["on"]); TON = 7
out = {}
D = json.load(gzip.open(SH.SRC)); sm, sc, sr = [], [], []
for c in D.values():
    mm, cc = SH.tokens(c)
    if len(mm) >= 12 and len(cc) >= 4: sm.append(mm); sc.append(cc)
    a = RR.analyse(c)
    if a: sr.append(a["toks"])
MM = SH.VOM(84).fit(sm); CM = SH.VOM(108).fit(sc); RM = SH.VOM(256).fit(sr)
mt = SOS.mel_tokens([n["engine_midi"] for n in lead], TON)
ch = SOS.dedupe([SOS.chord_token(c, TON) for c in REC["chords2"]])
mi, mh = SH.score(MM, mt); ci, chh = SH.score(CM, ch)
clip = {"annotations": {"meters": [{"beats_per_bar": 4, "beat_unit": 4}], "melody": [dict(onset=n["on"] / 12, offset=(n["on"] + n["dur"]) / 12) for n in lead], "num_beats": int(np.ceil((lead[-1]["on"] + lead[-1]["dur"]) / 12))}}
ra = RR.analyse(clip); ri = SH.score(RM, ra["toks"])[0]
z = lambda x: (np.array(x) - np.mean(x)) / (np.std(x) + 1e-9)
out["surprise"] = dict(melody_ic=float(np.mean(mi)), melody_median=S_MED["mel_ic_median"], chord_ic=float(np.mean(ci)), chord_median=S_MED["ch_ic_median"],
                       rhythm_ic=float(np.mean(ri)), rhythm_median=R_MED["rhy_ic_mean"], cheung_melody=float(-np.mean(z(mi) * z(mh))),
                       sync_per_note=ra["sync_per_note"], sync_median=R_MED["sync_per_note"], rest_share=ra["rest_share"], rest_median=R_MED["rest_share"],
                       length_variety=ra["length_variety"], variety_median=R_MED["length_variety"], density=ra["density"], density_median=R_MED["density"])
on_beat = [n for n in lead if n["stress"] and n["first"]]
out["stress"] = dict(stressed=len(on_beat), on_a_beat=float(np.mean([n["on"] % 12 == 0 for n in on_beat])), on_1_or_3=float(np.mean([n["on"] % 24 == 0 for n in on_beat])),
                     unstressed_on_1_or_3=float(np.mean([n["on"] % 24 == 0 for n in lead if not n["stress"] and n["first"]])))
# intensity (749.17) from the demo's energy reader
rows = DEMO["energy"]; plan = REC["plan"]; tot = REC["nbars"]
pos = {}; b = 0
for s, nb, st, mets, mv in plan: pos[s] = ((b + nb / 2) / tot, b / tot, (b + nb) / tot); b += nb
top = max(rows, key=lambda r: r["energy_read"]); after = [r for r in rows if pos[r["sec"]][1] > pos[top["sec"]][1]]
ch_rows = [r for r in rows if r["sec"].startswith("Chorus")]
out["intensity"] = dict(top=top["sec"], top_place=(round(pos[top["sec"]][1], 3), round(pos[top["sec"]][2], 3)), release=[(r["sec"], round(r["energy_read"], 2)) for r in after],
                        choruses=[(r["sec"], round(r["energy_read"], 2)) for r in ch_rows], each_return_higher=all(a["energy_read"] < b_["energy_read"] for a, b_ in zip(ch_rows, ch_rows[1:])),
                        each_chorus_over_its_verse=all(next(r for r in rows if r["sec"] == f"Chorus {k}")["energy_read"] > next(r for r in rows if r["sec"] == f"Verse {k}")["energy_read"] for k in range(1, 5)))
# the breath (749.19)
br = REC["breath"]; her0 = next(n for n in lead if n["singer"] == "her")
out["breath"] = dict(bar=br["bar"] + 1, place=round(br["at"] / REC["end"], 3), her_first=(her0["midi"], her0["text"], REC["bars"][her0["on"] // 48]["chord"]), silence_beats=(her0["on"] - br["at"]) / 12)
# perception (749.21)
LOW = {1: 60, 2: 60, 3: 53, 4: 53, 5: 46, 6: 47, 7: 34, 8: 41, 9: 41, 10: 41, 11: 41}
P_ = REC["parts"]; CHORDAL = ("acoustic", "piano", "steel", "tele")
viol = collections.Counter(); ex = []
for k in CHORDAL:
    for e in P_.get(k, []):
        ps = sorted(set(e["p"]))
        for a, b_ in zip(ps, ps[1:]):
            iv = b_ - a
            if 0 < iv < 12 and a < LOW[iv]: viol[k] += 1; ex.append((k, e["on"] // 48 + 1, a, b_))
def sounding(t, names):
    return [q for n in names for e in P_.get(n, []) if e["on"] <= t < e["on"] + e["dur"] for q in e["p"]]
BAND = ("acoustic", "tele", "fiddle", "steel", "piano")
above = within = 0
for n in lead:
    acc = sounding(n["on"], BAND)
    if any(q > n["midi"] for q in acc): above += 1
    if any(q != n["midi"] and (q - n["midi"]) % 12 and abs(q - n["midi"]) <= 2 for q in acc): within += 1
ab_by = {w: float(np.mean([any(q > n["midi"] for q in sounding(n["on"], BAND)) for n in lead if n["singer"] == w])) for w in ("him", "her")}
phr = []; cur = [lead[0]]
for a, b_ in zip(lead, lead[1:]):
    if b_["on"] - (a["on"] + a["dur"]) >= 12 or a["singer"] != b_["singer"]: phr.append(cur); cur = [b_]
    else: cur.append(b_)
phr.append(cur); secs = [((L[-1]["on"] + L[-1]["dur"]) - L[0]["on"]) / 12 * 60 / REC["qbpm"] for L in phr]
out["perception"] = dict(low_interval_violations=dict(viol), low_examples=ex[:6], band_above_tune=above / len(lead), band_above_by_singer=ab_by, band_within_second=within / len(lead),
                         phrases=len(secs), phrase_median_s=float(np.median(secs)), phrase_range_s=(round(min(secs), 1), round(max(secs), 1)), phrases_over_6s=int(sum(s > 6 for s in secs)), phrases_over_8s=int(sum(s > 8 for s in secs)))
# two channels (749.22) and chromatic harmony (749.23)
cps = {}
for s, nb, st, mets, mv in plan:
    b0 = st // 48; H = REC["chords2"][2 * b0: 2 * (b0 + nb)]; cps[s] = round(sum(1 for x, y in zip(H, H[1:]) if x != y) / nb, 2)
key_pcs = {7, 9, 11, 0, 2, 4, 6}
def chord_pcs(c):
    import re
    m = re.match(r"([A-G])([#b]?)(m?)", c); r = (PC[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0)) % 12
    return {r, (r + (3 if m.group(3) else 4)) % 12, (r + 7) % 12}
outside = sorted({c for c in REC["chords2"] if not chord_pcs(c.split("/")[0]) <= key_pcs})
out["channels"] = dict(chord_changes_per_bar=cps, distinct_chords=sorted(set(REC["chords2"])), chromatic_chords=outside, chromatic_share=0.0 if not outside else None)
json.dump(out, open("/home/claude/p64/research_p64.json", "w"), indent=1, default=str)
for k, v in out.items(): print(k, json.dumps(v, default=str)[:700])
