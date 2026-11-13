"""v128 Run 3 (496): each test's kept pass rate, printed beside it. A kept song (CoCoPops, 314 windows of 170 songs, zeneng_v105_kept_windows.json
with zeneng_v117_kept_songs_and_modes.json's song ids) is read the way the test reads a song: the mean of its own windows (its verse and its
chorus), against the test's band. A test whose band is the engine's own rule, a count of deaths, or a reading has no kept rate and says so.
Usage: python3 kept_pass_v128.py   (writes kept_pass_v129.json)"""
import json, collections
import numpy as np
KW = json.load(open("/home/claude/p40/tables/zeneng_v105_kept_windows.json")); SM = json.load(open("/home/claude/p55/tables/zeneng_v117_kept_songs_and_modes.json"))
MS = KW["measures"]; rows = [dict(zip(MS, r)) for r in KW["rows"]]
by = collections.defaultdict(list)
for s, r in zip(SM["song"], rows): by[s].append(r)
def song_mean(m):
    out = []
    for s, rs in by.items():
        v = [r[m] for r in rs if r.get(m) is not None and np.isfinite(r[m])]
        if v: out.append(float(np.mean(v)))
    return np.array(out)
def rate(m, lo=None, hi=None, fn=None):
    v = song_mean(m)
    if fn is not None: ok = fn(v)
    else: ok = (v >= (lo if lo is not None else -np.inf)) & (v <= (hi if hi is not None else np.inf))
    return round(float(np.mean(ok)), 3), len(v)
def both(m, lo, hi):
    """both windows of the song inside the band (a test read at the median of verse and chorus separately)."""
    ok = []
    for s, rs in by.items():
        v = [r[m] for r in rs if r.get(m) is not None and np.isfinite(r[m])]
        if v: ok.append(all(lo <= x <= hi for x in v))
    return round(float(np.mean(ok)), 3), len(ok)
K = {}
def put(t, how, val=None):
    K[t] = dict(kept_pass=val[0] if val else None, songs=val[1] if val else None, how=how)
put("312", "past_fifth at or under 3.6% in both windows", both("past_fifth", 0, 0.036))
for t in ("344", "349", "358", "385"): put(t, "outside_scale within two points of 7.1% (song mean)", rate("outside_scale", 0.051, 0.091))
for t in ("354", "357", "365", "372"):
    v = [song_mean(m) for m in ("gap_sixteenth", "gap_eighth", "gap_quarter", "gap_longer")]; mu = [float(np.mean(x)) for x in v]
    ok = np.all([np.abs(x - m_) <= 0.05 for x, m_ in zip(v, mu)], axis=0); put(t, "each of the four gap shares within five points of the kept mean (song mean)", (round(float(np.mean(ok)), 3), len(ok)))
put("355", "on_sixteenth within two points of 9.4% (song mean; runs and pushes are not in the kept windows)", rate("on_sixteenth", 0.074, 0.114))
put("398", "chord tones 54-76% and on a beat 56-80% (song mean)", (lambda a, b: (round(float(np.mean((a >= .54) & (a <= .76) & (b >= .56) & (b <= .80))), 3), len(a)))(song_mean("chord_tones"), song_mean("chord_tones_on_beat")))
for t in ("400", "408"): put(t, "turns per move within 0.04 of 0.584 (song mean)", rate("turns_per_move", 0.544, 0.624))
put("401", "four distinct note lengths (song median)", rate("distinct_durations", fn=lambda v: np.round(v) == 4))
put("343", "four distinct note lengths (song median)", rate("distinct_durations", fn=lambda v: np.round(v) == 4))
for t in ("329", "453"): put(t, "range inside the kept middle half, 8-13 (song mean)", rate("range", 8, 13))
put("424", "fourths and fifths between the collections' means or within a fifth of a sd (song mean)", rate("fourth_fifth", 0.066, 0.101))   # 0.080-0.087, a fifth of a sd (0.070) either side
for t in ("409", "456"): put(t, "the window's last note on the tonic 27.7-32.9% or within 0.09 (a song's two windows read 0, 0.5 or 1)", rate("last_note_tonic", 0.187, 0.419))
for t in ("390", "413", "361", "371", "350"): put(t, "unit returns within ten points of the kept rate (a song's windows read 0, 0.5 or 1)", rate("unit3_returns", 0.215, 0.415))
for t in ("310", "322", "330"): put(t, "likeness of bar rhythms inside 0.04-0.23 (song mean of parallel)", rate("parallel", 0.04, 0.23))
for t in ("313", "323", "331", "338", "351", "360", "370", "393", "415", "459"):
    put(t, "verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142)")
for t in ("378", "391", "414"): put(t, "a line's median share of its slot inside the kept middle half by notes: half of kept lines by definition (Window 138's lines are not on this machine)")
put("465", "a drawn line's class: the kept shares are the kept lines' own (a reading of the share, not a song test)")
put("458", "drawn lines' median rate inside the kept 25th-75th: half of kept lines by definition")
put("478", "verse 2's repeats and steps within five points of verse 1's: not computable song by song (no paired kept verses here)")
put("484", "pitch kept 72-79%: the kept collections' figure (no song-by-song figure here)")
put("438", "both shares inside their kept middle halves: half of kept songs on each by definition; the joint share is not in the table (no song rows)")
put("500", "the class shares are the kept lines' own (a reading of shares, not a song test)")
put("501", "drawn lines' median rate inside the kept 25th-75th: half of kept lines by definition")
put("503", "verse 2's chord tones on the beat within five points of verse 1's: not computable song by song (no paired kept verses here)")
put("441", "first-beat root within six points of 24%, third within six of 26% (no song-level kept table here)")
for t in ("311", "314", "315", "317", "319", "320", "321", "324", "325", "326", "332", "333", "335", "352", "353", "362", "363", "367", "369", "373", "374", "375", "376", "377",
          "379", "380", "381", "382", "383", "384", "386", "387", "392", "395", "417", "419", "464", "412", "470", "471", "472", "473", "476", "477", "491", "494", "440", "502", "505", "508", "513", "519", "520", "356", "368", "394", "389", "405", "490"):
    put(t, "a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate")
for t in ("316", "318", "327", "328", "334", "336", "337", "340", "342", "388", "396", "428", "486", "489", "504", "399", "341", "345", "346", "347", "348", "366", "359"):
    if t not in K: put(t, "a reading, a cost, or a share read on builds (no song-level kept test)")
K["about"] = __doc__.split("Usage")[0].strip()
json.dump(K, open("/home/claude/p55/kept_pass_v129.json", "w"), indent=1)
for t, v in K.items():
    if t != "about" and v["kept_pass"] is not None: print(t, v["kept_pass"], v["songs"], v["how"])
