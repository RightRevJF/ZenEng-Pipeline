"""Song 62: the record for the arrangement and the demo, from an engine record (song.json).
  python3 build62.py <song.json> <label> [--design]
--design (the designed copy) applies, logged in intake.py:
  the verse bass walks down by step under the designed chords (C B A G F E D, then G or A, in the key of the song);
  hand fixes: each refrain line that opened on a high unstressed note falling a sixth or more now opens a scale step under its second note;
  're-MEM-bered' in the title line, the long note moved onto 'MEM'; 'today' on the tonic; 'for NOW' in the bridge, the long note moved from 'for' to 'now'.
Arrangement (the writer's settings, chamber pop): the engine's piano part and bass (piano left hand) throughout, its drums and harmony voice left out;
the cello enters in the bridge and stays; the full quartet in the last refrain, the violins only where the voice rests (749.21: nothing above the
sung note while it sounds); in the outro the piano and first violin play the title line's tune once, unsung.
Writes out/<label>/record.json and out/<label>/<title> - demo.{mid,mp3}."""
import json, sys, os, subprocess, copy, collections
import mido
SRC, LABEL = sys.argv[1], sys.argv[2]; DESIGN = "--design" in sys.argv
R = json.load(open(SRC)); B = R["bar"]; BT = B // 4; T0 = R["key"]["tonic_midi"] % 12
OUT = f"out/{LABEL}"; os.makedirs(OUT, exist_ok=True)
start = {}; o = 0
for n, k, b in R["form"]: start[n] = (o, b); o += b * B
END = o
mel = sorted(copy.deepcopy(R["melody"]["notes"]), key=lambda n: n["on"]); fixes = []
def line(sec, i): return [n for n in mel if n["sec"] == sec and n["line"] == i]
if DESIGN:
    t = [n for n in line("Chorus 3", 3) if n["text"] == "remembered"]
    if len(t) == 3 and t[0]["dur"] > t[1]["dur"] and t[0]["dur"] > t[2]["dur"]:
        a, b_, c = t; s0 = a["on"]; tot = b_["on"] + b_["dur"] - s0
        a["dur"] = BT; b_["on"] = s0 + BT; b_["dur"] = tot - BT; fixes.append("title line: 're' one beat, 'MEM' held to where 'bered' begins")
    elif len(t) == 3 and t[2]["dur"] > t[1]["dur"]:
        a, b_, c = t; d1, d2 = b_["dur"], c["dur"]; b_["dur"] = d2; c["on"] = b_["on"] + d2; c["dur"] = d1; fixes.append("title line: the long note moved from 'bered' to 'MEM'")
    td = [n for n in line("Chorus 3", 3) if n["text"] == "today"]
    if td and (td[-1]["midi"] - R["key"]["tonic_midi"]) % 12 != 0:
        tn = R["key"]["tonic_midi"]; cand = [p for p in range(td[-1]["midi"] - 6, td[-1]["midi"] + 7) if (p - tn) % 12 == 0][0]
        fixes.append(f"title line: 'today' lands on the tonic ({td[-1]['midi']} to {cand}), the first full close of the song"); td[-1]["midi"] = cand
    f = [n for n in line("Bridge", 3) if n["text"] in ("for", "now")]
    if len(f) == 2 and f[0]["dur"] > f[1]["dur"]:
        a, b_ = f; tot = b_["on"] + b_["dur"] - a["on"]; a["dur"] = BT; b_["on"] = a["on"] + BT; b_["dur"] = tot - BT; fixes.append("bridge: 'for' one beat, 'now' held")
if DESIGN:                                                                                   # the writer's answer: refrain lines start low, so the reach lands on the strong word
    SC = [(R["key"]["tonic_midi"] + d) % 12 for d in (0, 2, 4, 5, 7, 9, 11)]
    for sec in [n for n, k, b in R["form"] if k == "chorus"]:
        for i in sorted({n["line"] for n in mel if n["sec"] == sec}):
            ln = line(sec, i)
            if len(ln) >= 2 and not ln[0]["stress"] and ln[0]["midi"] - ln[1]["midi"] >= 6:
                q = ln[1]["midi"] - 1
                while q % 12 not in SC: q -= 1
                fixes.append(f"{sec} line {i + 1}: the opening '{ln[0]['text']}' from {ln[0]['midi']} to {q}, a step under '{ln[1]['text']}'"); ln[0]["midi"] = q
if DESIGN and "--vary-refrain" in sys.argv:                                                   # the second refrain varies a little: lines 2 to 4 each lift their longest held note a scale step onto a chord tone (as 839 would)
    SC2 = [(R["key"]["tonic_midi"] + d) % 12 for d in (0, 2, 4, 5, 7, 9, 11)]
    s2, nb2 = start["Chorus 2"]
    def tones_at(t):
        bar_ = (t - s2) // B; ch = R["roman"]["Chorus 2"][bar_].split(); c_ = ch[0] if len(ch) == 1 or (t - s2) % B < B // 2 else ch[1]
        return set(R["chord_tones"][c_]) if c_ in R.get("chord_tones", {}) else set()
    for i in range(1, 4):
        ln = line("Chorus 2", i); held = [n for n in ln if n["dur"] >= BT]
        if not held: continue
        n = max(held, key=lambda n: (n["stress"], n["dur"])); k_ = ln.index(n)
        for q in range(n["midi"] + 1, n["midi"] + 5):
            if q % 12 in SC2 and q % 12 in tones_at(n["on"]) and (k_ == 0 or abs(q - ln[k_ - 1]["midi"]) <= 7) and (k_ == len(ln) - 1 or abs(ln[k_ + 1]["midi"] - q) <= 7):
                fixes.append(f"second refrain line {i + 1}: '{n['text']}' lifted from {n['midi']} to {q}"); n["midi"] = q; break
bass = [dict(on=e["on"], dur=e["dur"], p=e["midi"]) for e in R["bass"]]
if DESIGN:
    walk1 = [0, -1, -3, -5, -7, -8, -10, -5]; walk2 = [0, -1, -3, -5, -7, -8, -10, -3]; top = 36 + ((T0 - 36) % 12) if (36 + ((T0 - 36) % 12)) >= 36 else 48
    top = 36 + (T0 % 12) if 36 + (T0 % 12) <= 41 else 24 + (T0 % 12)
    for sec in ("Verse 1", "Verse 2", "Verse 3"):
        s, nb = start[sec]; bass = [e for e in bass if not (s <= e["on"] < s + nb * B)]
        steps = walk1 + (walk2[:7] + ([-5] if sec == "Verse 3" else [-3]))
        for i in range(nb):
            p = top + steps[i % 16] if i < 16 else top
            bass.append(dict(on=s + i * B, dur=B * 3 // 4, p=p)); bass.append(dict(on=s + i * B + 3 * BT, dur=BT, p=p + 12 if i % 4 == 3 else p))
    bass.sort(key=lambda e: e["on"])
piano = [dict(on=e["on"], dur=e["dur"], p=list(e["p"]), vel=e.get("vel", 66)) for e in R["parts"]["chords"]]
def sec_at(t):
    for n, (s, nb) in start.items():
        if s <= t < s + nb * B: return n
    return "Outro"
def sung_low(t0, t1): ps = [n["midi"] for n in mel if t0 <= n["on"] < t1]; return min(ps) if ps else None
def roman_at(t):
    n = sec_at(t); s, nb = start[n]; bar = (t - s) // B; rn = R["roman"][n][bar] if n in R["roman"] and bar < len(R["roman"][n]) else "I"
    return rn if isinstance(rn, str) else rn[0]
TONES = R["chord_tones"] if "chord_tones" in R else {}
cello, viola, vln2, vln1 = [], [], [], []
for n in ("Bridge", "Verse 3", "Chorus 3", "Outro"):
    if n == "Verse 3": continue
    s, nb = start[n]
    for i in range(nb):
        t = s + i * B; bs = [e["p"] for e in bass if t <= e["on"] < t + B]
        if not bs: continue
        p = bs[0]
        while p < 36: p += 12
        cello.append(dict(on=t, dur=B, p=p))
        if n in ("Chorus 3", "Outro"):
            lo = sung_low(t, t + B) or 99; v = p + 7
            while v + 12 < lo - 2 and v + 12 <= 57: v += 12
            if v < lo - 1 and v >= 48: viola.append(dict(on=t, dur=B, p=v))
# violins answer in the last refrain's rests: the line's last three sung pitches an octave up, a beat each, where a rest of two beats or more follows
c3 = [n for n in mel if n["sec"] == "Chorus 3"]
by = collections.defaultdict(list)
for n in c3: by[n["line"]].append(n)
for i, ns in sorted(by.items()):
    end = ns[-1]["on"] + ns[-1]["dur"]; nxt = min([m["on"] for m in mel if m["on"] >= end] or [END])
    k = (nxt - end) // BT
    for j, m in enumerate(ns[-3:][:k]): vln1.append(dict(on=end + j * BT, dur=BT, p=m["midi"] + 12))
    if k >= 2: vln2.append(dict(on=end, dur=min(nxt - end, 4 * BT), p=ns[-1]["midi"] + 7))
# outro: the title line's tune once, unsung (piano right hand and first violin)
tl = [n for n in mel if n["sec"] == "Chorus 3" and n["line"] == 3]; so, nbo = start["Outro"]
if tl:
    sh = so + BT - tl[0]["on"]
    for m in tl:
        if m["on"] + sh + m["dur"] <= END: vln1.append(dict(on=m["on"] + sh, dur=m["dur"], p=m["midi"] + 12)); piano.append(dict(on=m["on"] + sh, dur=m["dur"], p=[m["midi"] + 12], vel=58))
piano = [e for e in piano if not (so <= e["on"] < END and any(so <= v["on"] for v in vln1) and e["vel"] != 58 and e["on"] >= so + BT)] + [dict(on=so + BT, dur=nbo * B - BT, p=[60 + T0 if 60 + T0 < 66 else 48 + T0, 64 + T0 if 64 + T0 < 70 else 52 + T0], vel=50)]
rec = dict(title=R["title"], label=LABEL, design=DESIGN, fixes=fixes, key=R["key"], bpm=R["bpm"], bar=B, form=R["form"], chords=R["chords"], roman=R["roman"],
           melody=mel, parts=dict(piano=piano, bass=bass, cello=cello, viola=viola, violin2=vln2, violin1=vln1), source=SRC, pick=R["melody"]["pick"])
# checks
def sounding(part, t): return [e for e in part if e["on"] <= t < e["on"] + e["dur"]]
strs = cello + viola + vln2 + vln1
above = sum(1 for n in mel if any((e["p"] if isinstance(e["p"], int) else max(e["p"])) > n["midi"] for e in sounding(strs, n["on"])))
rec["checks"] = dict(strings_above_a_sung_note_share=round(above / len(mel), 4), strings_notes=len(strs), cello_from_bar=(start["Bridge"][0] // B + 1), fixes=fixes)
json.dump(rec, open(f"{OUT}/record.json", "w"), indent=1)
# MIDI and the demo
TPB = 480; tk = lambda e: int(round(e * TPB / BT)); mid = mido.MidiFile(ticks_per_beat=TPB)
meta = mido.MidiTrack(); mid.tracks.append(meta); meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(R["bpm"]))); meta.append(mido.MetaMessage("time_signature", numerator=4, denominator=4))
def track(name, ch, prog, evs, vel):
    tr = mido.MidiTrack(); mid.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name)); tr.append(mido.Message("program_change", channel=ch, program=prog))
    ev = []
    for e in evs:
        ps = e["p"] if isinstance(e["p"], list) else [e["p"]]
        for p in ps: ev.append((tk(e["on"]), 1, p, e.get("vel", vel))); ev.append((tk(e["on"] + e["dur"]) - 1, 0, p, 0))
    ev.sort(key=lambda x: (x[0], x[1])); now = 0
    for t, on, p, v in ev: tr.append(mido.Message("note_on" if on else "note_off", channel=ch, note=p, velocity=v, time=t - now)); now = t
track("Voice (guide)", 0, 71, [dict(on=n["on"], dur=n["dur"], p=n["midi"]) for n in mel], 104)
track("Piano", 1, 0, piano, 64); track("Piano LH", 2, 0, [dict(e, vel=60) for e in bass], 60)
track("Violin I", 3, 40, vln1, 62); track("Violin II", 4, 40, vln2, 52); track("Viola", 5, 41, viola, 52); track("Cello", 6, 42, cello, 58)
title = f"{R['title']} ({LABEL})"; mp = f"{OUT}/{title} - demo.mid"; mid.save(mp)
wav = f"{OUT}/demo.wav"; subprocess.run(["fluidsynth", "-ni", "-g", "0.7", "-r", "44100", "-F", wav, "/usr/share/sounds/sf2/FluidR3_GM.sf2", mp], check=True, capture_output=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-b:a", "192k", f"{OUT}/{title} - demo.mp3"], check=True); os.remove(wav)
print(LABEL, rec["checks"], f"{END // B} bars, {round(END / BT * 60 / R['bpm'])} s")
