"""What real 4/4 songs do above the bar (lines_cocopops.py -> cocopops_lines.json): the bar's length in seconds; a line's slot in bars and
in seconds against its syllables, by tempo; syllables a second; where lines start in the section's four-bar groups; one-bar lines; and the
longest rest inside a line. Middle halves are quartiles across lines unless noted."""
import json, numpy as np, collections
L = [l for l in json.load(open("cocopops_lines.json")) if l["slot_beats"] and 0 < l["slot_beats"] <= 32]
songs = collections.defaultdict(list)
for l in L: songs[l["song"]].append(l)
q = lambda v, p: round(float(np.percentile(v, p)), 2)
R = {}
bs = [s[0]["barsec"] for s in songs.values() if s[0]["barsec"]]
R["bar_seconds"] = dict(songs=len(bs), median=q(bs, 50), q1=q(bs, 25), q3=q(bs, 75), share_over_2_6s=round(float(np.mean(np.array(bs) >= 2.6)), 3))
print("bar seconds:", R["bar_seconds"])
T = [l for l in L if l["barsec"]]
def tempo_band(b): return "fast (bar under 1.8 s)" if b < 1.8 else ("slow (bar 2.6 s or more)" if b >= 2.6 else "middle")
R["by_tempo"] = {}
for band in ("fast (bar under 1.8 s)", "middle", "slow (bar 2.6 s or more)"):
    S = [l for l in T if tempo_band(l["barsec"]) == band]
    row = {"lines": len(S), "songs": len({l["song"] for l in S})}
    for lo, hi, tag in ((3, 5, "3-5 syl"), (6, 8, "6-8 syl"), (9, 99, "9+ syl")):
        G = [l for l in S if lo <= l["syl"] <= hi]
        if not G: continue
        bars = np.array([l["slot_beats"] / 4 for l in G]); secs = np.array([l["slot_beats"] / 4 * l["barsec"] for l in G])
        row[tag] = dict(n=len(G), median_slot_bars=q(bars, 50), one_bar_or_less=round(float(np.mean(bars <= 1.05)), 2), two_bars=round(float(np.mean((bars > 1.05) & (bars <= 2.05))), 2),
                        four_plus=round(float(np.mean(bars > 3.05)), 2), median_slot_seconds=q(secs, 50))
    sps = [l["syl"] / (l["span_beats"] / 4 * l["barsec"]) for l in S if l["span_beats"] > 0 and l["syl"] >= 3]
    row["syllables_per_second_sung"] = dict(median=q(sps, 50), q1=q(sps, 25), q3=q(sps, 75))
    R["by_tempo"][band] = row
    print(band, json.dumps(row))
# hypermetric placement: the bar (from the section's start) a line belongs to, in sections of 8 or 16 bars
H = [l for l in L if l["sec_len"] in (8, 16) and l["bar_in_sec"] is not None and 0 <= l["bar_in_sec"] < l["sec_len"]]
c4 = collections.Counter(l["bar_in_sec"] % 4 for l in H); n = sum(c4.values())
R["line_start_hyperbeat"] = {f"bar {k + 1} of 4": round(c4[k] / n, 3) for k in range(4)}
R["line_start_hyperbeat"]["lines"] = n
print("line starts by bar of four-bar group:", R["line_start_hyperbeat"])
R["pickup_share"] = {r: round(float(np.mean([l["pickup"] for l in L if l["role"] == r])), 3) for r in ("verse", "pre-chorus", "chorus", "bridge")}
print("pickups:", R["pickup_share"])
# one-bar lines
O = [l for l in L if l["slot_beats"] <= 4.05]
sy = np.array([l["syl"] for l in O]); sp = np.array([l["span_beats"] for l in O])
R["one_bar_lines"] = dict(lines=len(O), share_of_lines=round(len(O) / len(L), 3), syllables_median=q(sy, 50), syllables_q90=q(sy, 90),
                         share_7_plus=round(float(np.mean(sy >= 7)), 3),
                         span_beats_by_syllables={str(k): dict(n=int(np.sum(sy == k)), median=q(sp[sy == k], 50), q10=q(sp[sy == k], 10), q90=q(sp[sy == k], 90)) for k in range(3, 9) if np.sum(sy == k) >= 20})
print("one-bar lines:", json.dumps(R["one_bar_lines"]))
# the longest rest inside a line, by syllables and slot
R["inner_rest_q90_beats"] = {}
for lo, hi, tag in ((3, 5, "3-5"), (6, 8, "6-8"), (9, 99, "9+")):
    for sl, stag in (((0, 4.05), "1 bar"), ((4.05, 8.05), "2 bars"), ((8.05, 16.05), "3-4 bars")):
        G = [l["max_inner_rest"] for l in L if lo <= l["syl"] <= hi and sl[0] < l["slot_beats"] <= sl[1]]
        if len(G) >= 30: R["inner_rest_q90_beats"][f"{tag} syl, {stag}"] = dict(n=len(G), median=q(G, 50), q90=q(G, 90), share_3_beats_plus=round(float(np.mean(np.array(G) >= 3)), 3))
print("inner rests:", json.dumps(R["inner_rest_q90_beats"]))
# odd-length sections
secs = collections.Counter(); odd = 0; tot = 0
seen = set()
for l in L:
    key = (l["song"], l["role"], l["sec_len"], l["bar_in_sec"] is not None)
for s, ls in songs.items():
    lens = {(l["role"], l["sec_len"]) for l in ls if l["sec_len"]}
    for r, n in lens:
        if r in ("verse", "chorus", "pre-chorus", "bridge"): tot += 1; odd += (n % 4 != 0)
R["sections_not_multiple_of_4"] = dict(share=round(odd / tot, 3), sections=tot)
print("odd sections:", R["sections_not_multiple_of_4"])
json.dump(R, open("metre_results.json", "w"), indent=1)
