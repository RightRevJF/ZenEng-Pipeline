"""Swallowed Up -- the song's record: every event of every part, from the frozen riffs, the placed voice and the searched solo.
Every document is written from this record. 9.12's energy is read here, from the events as written (fix 141), with each layer
summed by its loudness (fix 142), on 9-M.5's section terms; the breakdown is marked as the peak though its feel is lowest (9-M.6)."""
import pickle, hashlib, json, collections, sys
sys.path[:0] = ["/home/claude/p34"]
import riffs_p34 as R, lyric as L
RF = pickle.load(open("/home/claude/p34/riffs_frozen.pkl", "rb"))
VO = pickle.load(open("/home/claude/p34/voice.pkl", "rb"))
SO = pickle.load(open("/home/claude/p34/solo_result.pkl", "rb"))
assert VO["riffs_sha"] == RF["sha"] == SO["rerun"]["riffs_sha"]          # the voice and the solo were placed on the frozen riff
PICK = SO["alive"][0]
BARS = R.BARS; NB = len(BARS)
def t_of(b, s): return R.slot_s(b, s)
def dur_s(b, s, d):
    """seconds for d sixteenths from (b, s), across a bar line if need be."""
    a = R.slot_s(b, s); bb, ss = b + (s + d) // 16, (s + d) % 16
    return (R.slot_s(bb, ss) if bb < NB else R.SECONDS) - a

ev = []
def add(part, b, s, d, p, vel, **kw):
    ev.append(dict(part=part, bar=b, slot=s, dur=d, pitch=p, vel=vel, t=round(t_of(b, s), 4), ts=round(dur_s(b, s, d), 4), **kw))

# rhythm guitars 1 and 2 (the same riff, left and right), bass an octave below in the same rhythm
for e in RF["gtr"]:
    b = e["bar"]
    for g in R.gtr_plays(b):
        for p in e["pitches"]: add(g, b, e["slot"], e["dur"], p, 92 if e["pm"] else 104, pm=e["pm"], riff=e["riff"])
    if R.bass_plays(b): add("Bass", b, e["slot"], e["dur"], min(e["pitches"]) - 12, 100 if e["pm"] else 108, pm=e["pm"], riff=e["riff"])
# drums
for e in RF["drums"]: add("Drums", e["bar"], e["slot"], 1, e["note"], e["vel"])
# the lead: the solo (searched), and the last chorus's tremolo an octave and a fourth above the riff (the lead's layer at the top)
b0 = R.SEC_FIRST["Solo"]
for s, d, p in PICK["notes"]: add("Lead", b0 + s // 16, s % 16, d, p, 108, src="solo")
lc = R.SEC_FIRST["Last Chorus"]
for e in RF["gtr"]:
    if lc <= e["bar"] < lc + 8: add("Lead", e["bar"], e["slot"], e["dur"], min(e["pitches"]) + 24, 98, src="last chorus tremolo")
# the voice: no pitch; a stroke at one of three heights (low, mid, high)
HKEY = {"low": 48, "mid": 55, "high": 62}                      # the placeholder keys (9-M.9: three keys; DEFAULT)
for v in VO["voice"]:
    add("Voice", v["bar"], v["slot"], v["dur"], HKEY[v["height"]], 112 if v["stressed"] else 96, word=v["word"], stressed=v["stressed"], family=v["family"],
        height=v["height"], vowel=v["vowel"], vowel_src=v["vowel_src"], sec_line=(v["sec"], v["line"]), j=v["j"], emphatic=v["emphatic"], line_end=v["line_end"])

# overlaps: no two notes of one pitch in one part overlap (trim the earlier)
by = collections.defaultdict(list)
for e in ev:
    if e["part"] != "Drums": by[(e["part"], e["pitch"])].append(e)
for k, es in by.items():
    es.sort(key=lambda e: (e["bar"], e["slot"]))
    for a, b in zip(es, es[1:]):
        if a["t"] + a["ts"] > b["t"] + 1e-6:
            a["ts"] = round(b["t"] - a["t"], 4)
ev.sort(key=lambda e: (e["t"], e["part"], e["pitch"]))

# ---- 9.12 on 9-M.5's terms, from the record (141), layers summed by loudness (142) ----
FEELR = {None: 0, 0.25: 1, 0.5: 2, 1: 3, 2: 4, 4: 5}
RIFFR = {"A": 1, "B": 1, "B'": 1, "C": 3, "D": 2, "E": 2, "F": 2, "G": 2}
def cymr(c):
    if not c: return 0
    if "crash" in c and "eighths" in c: return 3
    if "eighths" in c or "china" in c or "crash" in c: return 2
    return 1
def energy():
    out = collections.OrderedDict()
    for sec, n, q in R.FORM:
        bs = [k for k in range(NB) if BARS[k]["sec"] == sec]
        secs = sum(4 * 60 / BARS[k]["q"] for k in bs)
        es = [e for e in ev if e["bar"] in bs]
        feel = sum(FEELR[RF["feel"][k]["feel"]] for k in bs) / len(bs)
        kick = sum(1 for e in es if e["part"] == "Drums" and e["pitch"] == 36) / secs
        cym = sum(cymr(RF["feel"][k]["cymbal"]) for k in bs) / len(bs)
        riff = sum(RIFFR[BARS[k]["riff"]] for k in bs) / len(bs)
        layers = 0.0
        for part in ("Gtr 1", "Gtr 2", "Bass", "Drums", "Lead", "Voice"):
            pe = [e for e in es if e["part"] == part]
            if not pe: continue
            share = len({e["bar"] for e in pe}) / len(bs)                 # how much of the section the layer covers
            layers += share * max(e["vel"] for e in pe) / 127               # by loudness: a layer adds, never subtracts (142)
        E = 0.30 * feel / 5 + 0.20 * min(1, kick / 10) + 0.15 * cym / 3 + 0.15 * riff / 3 + 0.20 * layers / 6
        out[sec] = dict(E=round(E, 3), feel=round(feel, 2), kick_s=round(kick, 2), cymbal=round(cym, 2), riff=round(riff, 2), layers=round(layers, 2))
    return out
EN = energy()
for v, c in (("Verse 1", "Chorus 1"), ("Verse 2", "Chorus 2"), ("Verse 3", "Chorus 3")): assert EN[c]["E"] > EN[v]["E"], (v, c)
assert EN["Last Chorus"]["E"] == max(x["E"] for x in EN.values()), "the last chorus is the top of the arc (the breakdown, marked as the peak, apart)"

rec = dict(title=L.TITLE, form=R.FORM, nbars=NB, seconds=R.SECONDS, bars=[dict(sec=bb["sec"], i=bb["i"], q=bb["q"], riff=bb["riff"], chords=RF["chords"][k],
           feel=RF["feel"][k]) for k, bb in enumerate(BARS)], events=ev, energy=EN, heaviness=R.heaviness(RF["gtr"], RF["drums"]),
           riffs_sha=RF["sha"], voice_sha=VO["sha"], voice_lines=VO["lines"], voice_lock=VO["lock"], solo=dict(fp=PICK["fp"], meas=PICK["meas"], survivors=SO["survivors"],
           built=SO["made"], deaths=dict(SO["deaths"]), order_fp=SO["order_fp"], rerun=SO["rerun"], top20=SO["top20"]), hand_edits=[],
           peak="Slowdown (the breakdown, bars 121-128)", hkey=HKEY)
rec["fp"] = hashlib.sha1(json.dumps([(e["part"], e["bar"], e["slot"], e["dur"], e["pitch"]) for e in ev]).encode()).hexdigest()[:12]
pickle.dump(rec, open("/home/claude/p34/song_record.pkl", "wb"))
if __name__ == "__main__":
    c = collections.Counter(e["part"] for e in ev)
    print(f"record {rec['fp']}: {len(ev)} events {dict(c)}; {NB} bars, {R.SECONDS:.1f} s")
    for k, v in EN.items(): print(f"  {k:12s} {v}")
