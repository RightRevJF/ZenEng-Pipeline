"""The First Wood -- the song's record: every event of every part. Every document is written from it.
Form: the organ plays the refrain as an introduction (8 bars), then four stanzas of 24 bars, each with its pickup: 104 bars.
Arrangement: stanza 1 in unison (sopranos and altos on the tune, tenors and basses an octave below), the organ in four parts;
stanza 2 in four parts with the organ; stanza 3 in four parts unaccompanied; stanza 4 in four parts, the organ full (the tune
doubled an octave higher in the right hand). The voices sing every syllable together; a chord that changes inside a syllable moves
the lower voices under it. 9.12 is read on the record (141), each layer by its loudness (142); the last stanza must read the top."""
import pickle, sys, collections, hashlib, json, re
sys.path[:0] = ["/home/claude/p35", "/home/claude/carol", "/home/claude/pop"]
import melody_p35 as M, lyric as L
MR = pickle.load(open("/home/claude/p35/melody_result.pkl", "rb")); PICK = MR["alive"][0]
VO = pickle.load(open("/home/claude/p35/voices.pkl", "rb")); assert VO["fp"] == PICK["fp"]
QBPM = 92; BAR = 36; SEC12 = 60 / QBPM / 12
TUNE = PICK["notes"]; VOICES = VO["voices"]
INTRO_FROM = 16                                   # the refrain: tune bars 16-23
NB = 8 + 24 * 4
def song_bar(stanza, b): return 8 + 24 * stanza + b if stanza is not None else b - INTRO_FROM

ev = []
def add(part, abs12, dur, p, vel, **kw):
    ev.append(dict(part=part, bar=abs12 // BAR, slot=abs12 % BAR, abs12=abs12, dur=dur, pitch=p, vel=vel, t=round(abs12 * SEC12, 4), ts=round(dur * SEC12, 4), **kw))

def chord_at(t):
    return [v for v in VOICES if v["on"] <= t < v["end"]][0]

def place(stanza):
    """the tune and the three lower voices for one stanza (None = the organ's introduction), in absolute twelfths."""
    if stanza is None:
        notes = [n for n in TUNE if n["line"] in ("R1", "R2")]; off = -INTRO_FROM * BAR
    else:
        notes = TUNE; off = (8 + 24 * stanza) * BAR
    last = stanza == 3
    out = {"S": [], "A": [], "T": [], "B": []}
    # the onsets: every syllable, and every chord change inside a syllable
    sylon = sorted({n["on"] for n in notes if not any(m["line"] == n["line"] and m["syl"] == n["syl"] and m["on"] < n["on"] for m in notes)})
    chon = sorted({v["on"] for v in VOICES if notes[0]["on"] <= v["on"] <= notes[-1]["on"]})
    ons = sorted(set(sylon) | set(chon))
    ends = {}
    for n in notes:
        ends[n["on"]] = n
    tune_end = {}
    for i, n in enumerate(notes):
        e = n["on"] + n["dur"]
        if last and i == len(notes) - 1: e = 24 * BAR               # the last chord fills its bar
        out["S"].append(dict(on=n["on"], end=e, p=n["p"], line=n["line"], syl=n["syl"], first=n["on"] in sylon))
    def syl_end(t):
        n = M.sounding(notes, t)
        if n is None: return None
        g = [m for m in notes if m["line"] == n["line"] and m["syl"] == n["syl"]]
        e = max(m["on"] + m["dur"] for m in g)
        return 24 * BAR if (last and g[-1] is notes[-1]) else e
    for k, t in enumerate(ons):
        n = M.sounding(notes, t)
        if n is None: continue
        nxt = ons[k + 1] if k + 1 < len(ons) else None
        se = syl_end(t)
        # a lower voice lasts until the next onset, or until its syllable ends (a line's end before a rest)
        e = min(nxt, se) if nxt is not None else se
        if last and k == len(ons) - 1: e = 24 * BAR
        h = chord_at(t)
        is_syl = t in sylon
        sy = next((m for m in notes if m["on"] <= t < m["on"] + m["dur"]), None)
        for part, key in (("A", "alto"), ("T", "tenor"), ("B", "bass")):
            out[part].append(dict(on=t, end=e, p=h[key], line=sy["line"], syl=sy["syl"], first=is_syl, chord=h["chord"]))
    # merge a lower voice's repeated pitch inside one syllable (a held chord under a slurred tune) into one note
    for part in ("A", "T", "B"):
        merged = []
        for x in out[part]:
            if merged and not x["first"] and merged[-1]["p"] == x["p"] and merged[-1]["end"] == x["on"]: merged[-1]["end"] = x["end"]
            else: merged.append(dict(x))
        out[part] = merged
    return out, off

ARR = {None: "organ", 0: "unison", 1: "harmony", 2: "a cappella", 3: "full"}
for stanza in (None, 0, 1, 2, 3):
    parts, off = place(stanza)
    mode = ARR[stanza]
    words = M.WORDS[stanza] if stanza is not None else None
    if mode != "organ":
        for part in ("S", "A", "T", "B"):
            src = parts["S"] if mode == "unison" else parts[part]
            for x in src:
                p = x["p"] if not (mode == "unison" and part in ("T", "B")) else x["p"] - 12
                syl = words[x["line"]][x["syl"]] if x["first"] else None
                add(part, off + x["on"], x["end"] - x["on"], p, 84 if part == "S" else 76, stanza=stanza + 1, line=x["line"], syl_i=x["syl"], first=x["first"],
                    word=(syl[0] if syl else None), stressed=(syl[2] if syl else None))
    if mode in ("organ", "unison", "harmony", "full"):
        vel = {"organ": 74, "unison": 72, "harmony": 74, "full": 86}[mode]
        for x in parts["S"]: add("Organ RH", off + x["on"], x["end"] - x["on"], x["p"], vel, stanza=(stanza + 1 if stanza is not None else 0), role="S")
        for x in parts["A"]: add("Organ RH", off + x["on"], x["end"] - x["on"], x["p"], vel - 4, stanza=(stanza + 1 if stanza is not None else 0), role="A")
        for x in parts["T"]: add("Organ LH", off + x["on"], x["end"] - x["on"], x["p"], vel - 4, stanza=(stanza + 1 if stanza is not None else 0))
        for x in parts["B"]: add("Pedal", off + x["on"], x["end"] - x["on"], x["p"] - 12 if x["p"] >= 48 else x["p"], vel, stanza=(stanza + 1 if stanza is not None else 0))
        if mode == "full":
            for x in parts["S"]: add("Organ 4ft", off + x["on"], x["end"] - x["on"], x["p"] + 12, vel - 6, stanza=4, octave=True)
# the stanza joins: the last chord of a stanza stops where the next stanza's pickup begins (no overlaps in a part and pitch)
by = collections.defaultdict(list)
for e in ev: by[(e["part"], e["pitch"])].append(e)
for k, es in by.items():
    es.sort(key=lambda e: e["abs12"])
    for a, b in zip(es, es[1:]):
        if a["abs12"] + a["dur"] > b["abs12"]: a["dur"] = b["abs12"] - a["abs12"]; a["ts"] = round(a["dur"] * SEC12, 4)
for part in ("S", "A", "T", "B"):
    es = sorted([e for e in ev if e["part"] == part], key=lambda e: e["abs12"])
    for a, b in zip(es, es[1:]):
        if a["abs12"] + a["dur"] > b["abs12"]: a["dur"] = b["abs12"] - a["abs12"]; a["ts"] = round(a["dur"] * SEC12, 4)
ev = [e for e in ev if e["dur"] > 0]
ev.sort(key=lambda e: (e["abs12"], e["part"], e["pitch"]))
TOTAL = NB * BAR; SECONDS = TOTAL * SEC12

# ---- 9.12 from the record (141), layers by loudness (142) ----
SECS = [("Introduction", 0, 8)] + [(f"Stanza {i + 1}", 8 + 24 * i, 8 + 24 * (i + 1)) for i in range(4)]
def energy():
    out = collections.OrderedDict()
    for name, b0, b1 in SECS:
        es = [e for e in ev if b0 <= e["bar"] < b1]; secs = (b1 - b0) * BAR * SEC12
        ons = len({(e["abs12"], e["pitch"]) for e in es}) / secs                       # struck notes, a unison counted once (by event, v77)
        layers = 0.0
        for part in ("S", "A", "T", "B", "Organ RH", "Organ LH", "Pedal", "Organ 4ft"):
            pe = [e for e in es if e["part"] == part]
            if pe: layers += (len({e["bar"] for e in pe}) / (b1 - b0)) * max(e["vel"] for e in pe) / 127
        distinct = len({(e["abs12"], e["pitch"] % 12) for e in es}) / max(1, len({e["abs12"] for e in es}))
        voices = len({e["pitch"] for e in es if e["part"] in ("S", "A", "T", "B")})
        E = 0.4 * min(1, ons / 20) + 0.4 * layers / 7 + 0.2 * min(1, distinct / 3)
        out[name] = dict(E=round(E, 3), onsets_s=round(ons, 2), layers=round(layers, 2), parts_per_onset=round(distinct, 2))
    return out
EN = energy()
assert EN["Stanza 4"]["E"] == max(v["E"] for v in EN.values()), EN

rec = dict(title=L.TITLE, qbpm=QBPM, nbars=NB, seconds=SECONDS, events=ev, sections=SECS, arrangement={k if k is None else k + 1: v for k, v in ARR.items()},
           energy=EN, tune=TUNE, voices=VOICES, fp=PICK["fp"], meas=PICK["meas"], plan=PICK["plan"], search=dict(made=MR["made"], survivors=MR["survivors"],
           deaths=dict(MR["deaths"]), would=dict(MR["would"]), order_fp=MR["order_fp"], rerun=MR["rerun"], top20=MR["top20"]), hand_edits=[])
rec["record_fp"] = hashlib.sha1(json.dumps([(e["part"], e["abs12"], e["dur"], e["pitch"]) for e in ev]).encode()).hexdigest()[:12]
pickle.dump(rec, open("/home/claude/p35/song_record.pkl", "wb"))
if __name__ == "__main__":
    c = collections.Counter(e["part"] for e in ev)
    print(f"record {rec['record_fp']}: {len(ev)} events {dict(c)}; {NB} bars, {SECONDS:.1f} s")
    for k, v in EN.items(): print(f"  {k:13s} {v}")
