"""Module 11.11 demo for 'The Seam' (V/N/P; prog rock, a duet; 130 bars, 6:12). 4/4 at q = 80 (the instrumental 7/8, 2+2+3, at
the same pulse); one tick line in eighths (240 ticks an eighth).
Her verses (E minor)   half-time: kick on 1, snare on 3; clean guitar arpeggios; Rhodes; the synth pad (her instrument) under it.
His verses (F minor)   the same groove a half step up; the bass moving more; a muted guitar instead of arpeggios.
Choruses (C major)     full time, open: overdriven guitar chords, the pad and Rhodes up, ride; both voices, his a third or sixth below.
Instrumental (7/8)     48 bars, a marked BUILD: synth lead (the line, Module 27.21) with pad and keys; the bass from the second quarter,
                       the drums from the third, everything in the last; velocities ramp 0.7 -> 1.05.
Last chorus            everything; WE on C5 (her) over his A4.   Ending  him alone over pad and piano; the last chord F major.
Guide voices: the v43 reed fallback -- HER on oboe, HIM on clarinet (two singers, two guide tracks, v58)."""
import pickle, subprocess, os, collections, sys, random
import numpy as np, mido
from scipy.io import wavfile
REC = pickle.load(open("/home/claude/p22/song_record.pkl", "rb"))
OUT = "/home/claude/p22/out"; os.makedirs(OUT, exist_ok=True); BASE = f"{OUT}/The Seam - demo"
T = 480; E8 = 240
BARS = REC["bars"]; PLAN = REC["plan"]; lead = REC["lead"]; HARM = REC["harm"]; NB = REC["nbars"]; GTR = REC["gtr"]
def tk(e): return int(round(e * E8))
ROOT = {"Em": 4, "C": 0, "Am": 9, "G": 7, "F": 5, "Fm": 5, "Db": 1, "Bbm": 10}
TONES = {"Em": [4, 7, 11], "C": [0, 4, 7], "Am": [9, 0, 4], "G": [7, 11, 2], "F": [5, 9, 0], "Fm": [5, 8, 0], "Db": [1, 5, 8], "Bbm": [10, 1, 5]}
def pink(n, alpha=0.75, scale=1.0, seed=0):
    beta = 2 * alpha - 1; r = np.random.default_rng(seed)
    f = np.fft.rfftfreq(n); amp = np.zeros_like(f); amp[1:] = f[1:] ** (-beta / 2)
    x = np.fft.irfft(amp * np.exp(2j * np.pi * r.random(len(f))), n)
    return (x - x.mean()) / (x.std() + 1e-9) * scale
class Dev:
    def __init__(self, seed, vel=3, tim=2):
        self.v = pink(8192, scale=vel, seed=seed); self.t = pink(8192, scale=tim, seed=seed + 99); self.i = 0
    def __call__(self):
        i = self.i % 8192; self.i += 1
        return int(max(-4, min(4, round(self.v[i])))), int(max(-4, min(4, round(self.t[i]))))
KEYS = ["voc", "voc2", "lead", "keys", "gtr", "bass", "pad", "drums"]
DEV = {k: Dev(i * 17 + 3) for i, k in enumerate(KEYS)}
VOX_GAIN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].lstrip("-").isdigit() else 12
BAND_VOL = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 92
CH = dict(voc=0, voc2=6, lead=1, keys=2, gtr=3, bass=4, pad=5, drums=9)
PROG = dict(voc=68, voc2=71, lead=81, keys=4, gtr=29, bass=34, pad=90, drums=0)
PAN = dict(voc=58, voc2=70, lead=76, keys=46, gtr=30, bass=64, pad=64, drums=64)
REVERB = dict(voc=60, voc2=60, lead=80, keys=60, gtr=50, bass=15, pad=110, drums=45)
NAMES = dict(voc="Guide vocal HER (oboe - reed fallback)", voc2="Guide vocal HIM (clarinet - reed fallback)", lead="Instrumental lead - synth lead",
             keys="Rhodes", gtr="Guitar", bass="Bass", pad="Synth pad", drums="Drums")
tracks = collections.OrderedDict()
def note(key, t0, t1, p, v):
    v = max(1, min(127, int(v))); tr = NAMES[key]; ch = CH[key]
    tracks.setdefault(tr, []).append((max(0, t0), 1, ("on", ch, p, v)))
    tracks[tr].append((max(t0 + 5, t1), 0, ("off", ch, p, 0)))
def meta(key, t, text): tracks.setdefault(NAMES[key], []).append((t, 2, ("meta", "lyrics", dict(text=text))))
def voicing(ch, lo=52, n=4):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in TONES[ch]: out.append(p)
        p += 1
    return out
# ---- the voices ----
VBASE = {"Verse 1": 64, "Verse 3": 66, "Verse 2": 64, "Verse 4": 66, "Chorus 1": 74, "Chorus 2": 76, "Chorus 3": 80, "Ending": 66}
for n in lead:
    key = "voc" if n["singer"] == "her" else "voc2"
    dv, dt = DEV[key](); v = VBASE[n["sec"]] + VOX_GAIN + dv + (6 if n["midi"] >= 67 else 0)
    t0 = tk(n["on"]) + 5 + dt; note(key, t0, tk(n["on"] + n["dur"] * 0.94), n["midi"], v); meta(key, t0, n["syl"][0])
for n in HARM:
    dv, dt = DEV["voc2"](); note("voc2", tk(n["on"]) + 7 + dt, tk(n["on"] + n["dur"] * 0.94), n["midi"], VBASE[n["sec"]] + VOX_GAIN - 4 + dv)
# ---- the instrumental lead (27.21) ----
inst = [b for b in BARS if b["sec"] == "Instrumental"]; i0, i1 = inst[0]["start"], inst[-1]["start"] + inst[-1]["len"]
for n in GTR:
    dv, dt = DEV["lead"](); g = (0.7 + 0.35 * (n["on"] - i0) / (i1 - i0)) if n["sec"] == "Instrumental" else 0.85
    note("lead", tk(n["on"]) + dt, tk(n["on"] + n["dur"] * 0.96), n["midi"], int(96 * g) + dv)
# ---- band, bar by bar ----
rng = random.Random(22)
for bi, b in enumerate(BARS):
    sec, ch, st, ln, met = b["sec"], b["chord"], b["start"], b["len"], b["meter"]; t = tk(st)
    first = bi == 0 or BARS[bi - 1]["sec"] != sec
    k_in = bi - [x for x in range(NB) if BARS[x]["sec"] == sec][0]
    nb_sec = sum(1 for x in BARS if x["sec"] == sec)
    bld = b.get("build"); quarter = (4 * k_in) // nb_sec if bld else 3; g = (0.7 + 0.35 * k_in / max(1, nb_sec - 1)) if bld else 1.0
    def dn(p, e, v, l=0.4):
        dv, dt = DEV["drums"](); note("drums", t + tk(e) + dt, t + tk(e + l), p, int(v * g) + dv)
    r = 28 + ((ROOT[ch] - 28) % 12)
    cho = sec.startswith("Chorus"); verse = sec.startswith("Verse"); her = sec in ("Verse 1", "Verse 3", "Intro")
    end_last = sec == "Outro" and k_in == nb_sec - 1
    [note("pad", t + 10, t + tk(ln) - 10, p, int((44 + (8 if cho else 0) + (6 if bld else 0)) * g)) for p in voicing(ch, 60, 3)]
    if end_last:
        [note("keys", t + 15 * k, t + tk(7.9), p, 56) for k, p in enumerate(voicing(ch, 53, 5))]; note("bass", t, t + tk(7.8), r, 66); dn(49, 0, 70, 8); continue
    # keys: Rhodes chords
    for e in ([0, 3] if met == "4/4" else [0, 4]):
        dv, dt = DEV["keys"](); [note("keys", t + tk(e) + dt + 6 * k, t + tk(e + 2.6), p, int((50 + (6 if cho else 0)) * g) - 2 * k + dv) for k, p in enumerate(voicing(ch, 55, 4))]
    if sec in ("Intro", "Interlude", "Outro") and not (sec == "Intro" and k_in >= 4): continue
    if sec == "Ending":
        dv, dt = DEV["bass"](); note("bass", t + dt, t + tk(7.6), r, 62 + dv); continue
    # bass
    if not bld or quarter >= 1:
        if met == "7/8":
            for e, l in ((0, 1.8), (2, 1.8), (4, 0.9), (5, 0.9), (6, 0.9)):
                dv, dt = DEV["bass"](); note("bass", t + tk(e) + dt, t + tk(e + l), r if e != 5 else r + 7, int(80 * g) + dv)
        elif verse:
            dv, dt = DEV["bass"](); note("bass", t + dt, t + tk(3.6), r, 74 + dv); note("bass", t + tk(4) + dt, t + tk(5.6), r, 66 + dv)
            if not her: note("bass", t + tk(6) + dt, t + tk(7.6), r + 7, 64 + dv)
        else:
            for e in range(0, 8, 2):
                dv, dt = DEV["bass"](); note("bass", t + tk(e) + dt, t + tk(e + 1.8), r, (82 if e == 0 else 72) + dv)
    # guitar
    if verse and her:
        vo = voicing(ch, 55, 5); pat = [0, 2, 4, 3, 1, 3, 4, 2]
        for e, i in enumerate(pat):
            dv, dt = DEV["gtr"](); note("gtr", t + tk(e) + dt, t + tk(e + 1.6), vo[i], 44 + dv)
    elif verse:
        for e in range(0, 8, 2):
            dv, dt = DEV["gtr"](); note("gtr", t + tk(e) + dt, t + tk(e + 0.4), r + 24, 46 + dv)
    elif cho or (bld and quarter >= 3):
        pw = [r + 12, r + 19, r + 24]
        for e in (range(8) if met == "4/4" else range(7)):
            dv, dt = DEV["gtr"](); [note("gtr", t + tk(e) + dt, t + tk(e + 0.85), p, int(62 * g) + dv) for p in pw]
    # drums
    if met == "7/8":
        if quarter >= 2:
            dn(36, 0, 86); dn(36, 4, 80); dn(38, 2, 84); dn(38, 5, 80); [dn(42 if quarter == 2 else 51, e, 44 if e in (0, 2, 4) else 32) for e in range(7)]
            if k_in == nb_sec - 1: [dn([50, 48, 47, 45][i], 3 + i, 84, 0.4) for i in range(4)]
    elif verse:
        dn(36, 0, 74); dn(38, 4, 72); [dn(42, e, 36 if e % 2 == 0 else 28) for e in range(8)]
    elif cho:
        dn(36, 0, 88); dn(36, 3, 72); dn(36, 4, 84); dn(38, 2, 88); dn(38, 6, 90); [dn(51, e, 46 if e % 2 == 0 else 34) for e in range(8)]
        if first: dn(49, 0, 100, 4)
        if sec == "Chorus 3" and k_in == nb_sec - 1: dn(49, 0, 108, 8); dn(57, 0, 96, 8)
    elif sec == "Intro":
        dn(36, 0, 70); dn(38, 4, 66); [dn(42, e, 32) for e in (0, 2, 4, 6)]
def write(path, gm=True, only=None):
    mf = mido.MidiFile(ticks_per_beat=T)
    t0 = mido.MidiTrack(); mf.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name=REC["title"], time=0))
    ev = []
    for s, nb, b0, met in PLAN:
        st = BARS[b0]["start"]; num, den = met.split("/")
        ev.append((tk(st), 0, mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BARS[b0]["qbpm"]), time=0)))
        ev.append((tk(st), 1, mido.MetaMessage("time_signature", numerator=int(num), denominator=int(den), clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)))
        k = {"E minor": "Em", "F minor": "Fm", "C major": "C"}[BARS[b0]["key"]]
        ev.append((tk(st), 2, mido.MetaMessage("key_signature", key=k, time=0)))
        ev.append((tk(st), 3, mido.MetaMessage("marker", text=s, time=0)))
    now = 0
    for t, pri, m in sorted(ev, key=lambda x: (x[0], x[1])):
        m.time = t - now; now = t; t0.append(m)
    for key, name in NAMES.items():
        if only is not None and name not in only: continue
        if name not in tracks: continue
        tr = mido.MidiTrack(); mf.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name, time=0))
        if gm and key != "drums": tr.append(mido.Message("program_change", program=PROG[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=10, value=PAN[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=7, value=127 if key == "voc" else BAND_VOL, channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=91, value=REVERB.get(key, 40), channel=CH[key], time=0))
        now = 0
        for t, pri, e in sorted(tracks.get(name, []), key=lambda x: (x[0], x[1])):
            dt = t - now; now = t
            if e[0] == "on": tr.append(mido.Message("note_on", channel=e[1], note=e[2], velocity=e[3], time=dt))
            elif e[0] == "off": tr.append(mido.Message("note_off", channel=e[1], note=e[2], velocity=0, time=dt))
            else: tr.append(mido.MetaMessage(e[1], text=e[2].get("text", "").encode("ascii", "ignore").decode(), time=dt))
    mf.save(path); return path
SF = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
def render(mid, wav):
    subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", "44100", "-F", wav, SF, mid], check=True, capture_output=True)
    sr, x = wavfile.read(wav); return sr, x.astype(np.float64)
def sec_of_tick(tick, mf):
    return mido.tick2second(tick, T, 500000)
def stems_check():
    a = write(f"{OUT}/stem_vox.mid", only={NAMES["voc"], NAMES["voc2"]}); b = write(f"{OUT}/stem_band.mid", only=set(NAMES.values()) - {NAMES["voc"], NAMES["voc2"]})
    sr, xv = render(a, f"{OUT}/stem_vox.wav"); _, xb = render(b, f"{OUT}/stem_band.wav")
    n = min(len(xv), len(xb)); xv, xb = xv[:n].mean(1), xb[:n].mean(1)
    # the tempo map: seconds at each eighth
    es = REC["eighth_sec"]; tsec = []; acc = 0.0
    for bb in BARS:
        for _ in range(bb["len"]): tsec.append(acc); acc += es[bb["meter"]]
    tsec.append(acc)
    mask = np.zeros(n, bool)
    for nn in lead + HARM:
        i0 = int(tsec[nn["on"]] * sr); i1 = int(tsec[min(len(tsec) - 1, nn["on"] + nn["dur"])] * sr); mask[i0:min(n, i1)] = True
    rv = 20 * np.log10(np.sqrt(np.mean(xv[mask] ** 2)) + 1e-9); rb = 20 * np.log10(np.sqrt(np.mean(xb[mask] ** 2)) + 1e-9)
    for f in ("stem_vox.mid", "stem_band.mid", "stem_vox.wav", "stem_band.wav"): os.remove(f"{OUT}/{f}")
    return rv - rb
if __name__ == "__main__":
    diff = stems_check()
    print(f"stems: lead {diff:+.1f} dB over the band (v43 rule: >= +3 dB); vocal gain {VOX_GAIN}, band CC7 {BAND_VOL}")
    if "--check" in sys.argv: sys.exit(0)
    gm = write(f"{BASE} (General MIDI).mid", gm=True); gb = write(f"{BASE} (GarageBand).mid", gm=False)
    wav = f"{BASE}.wav"
    sr, y = render(gm, wav)
    end = int(mido.MidiFile(gm).length * sr) + int(1.5 * sr); y = y[:end]
    fade = int(sr * 3.5); y[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    y = y / (np.abs(y).max() + 1e-9) * 0.89
    wavfile.write(wav, sr, (y * 32767).astype(np.int16))
    mp3 = f"{BASE}.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "volume=6dB,alimiter=limit=0.89:level=disabled", "-b:a", "224k", mp3], check=True)
    os.remove(wav)
    print("wrote", mp3, f"{int(len(y)/sr//60)}:{len(y)/sr%60:04.1f}")
    def window(a, z):
        ev, vel, trs = 0.0, [], set()
        for tr, evs in tracks.items():
            if tr in (NAMES["voc"], NAMES["voc2"]): continue
            ons = sorted(t for (t, p, e) in evs if p == 1 and a <= t < z)
            vel += [e[3] for (t, p, e) in evs if p == 1 and a <= t < z]
            last = None; cnt = 0
            for t in ons:
                if last is None or t - last > 30: cnt += 1
                last = t
            if cnt: trs.add(tr)
            ev += cnt
        return ev, (float(np.mean(vel)) if vel else 0.0), len(trs)
    rows = []
    for s, nb, b0, met in PLAN:
        a, z = tk(BARS[b0]["start"]), tk(BARS[b0 + nb - 1]["start"] + BARS[b0 + nb - 1]["len"])
        q = (z - a) // 4
        whole = window(a, z); first = window(a, a + q); lastq = window(z - q, z)
        rows.append(dict(sec=s, events=whole[0] / nb, vel=whole[1], tracks=whole[2],
                         q1=dict(events=first[0] / max(1, nb / 4), vel=first[1], tracks=first[2]),
                         q4=dict(events=lastq[0] / max(1, nb / 4), vel=lastq[1], tracks=lastq[2]), build=BARS[b0].get("build", False)))
    MIN_SPAN = dict(events=4, vel=16, tracks=3)          # 9.12 (v64): a flat arc reads flat
    allv = {kk: [r[kk] for r in rows] + [r["q1"][kk] for r in rows] + [r["q4"][kk] for r in rows] for kk in ("events", "vel", "tracks")}
    def nz(kk, v):
        lo_, hi_ = min(allv[kk]), max(allv[kk]); span = max(hi_ - lo_, MIN_SPAN[kk]); return (v - lo_) / span
    for r in rows:
        r["energy"] = float(np.mean([nz(kk, r[kk]) for kk in ("events", "vel", "tracks")]))
        r["start"] = float(np.mean([nz(kk, r["q1"][kk]) for kk in ("events", "vel", "tracks")]))
        r["end"] = float(np.mean([nz(kk, r["q4"][kk]) for kk in ("events", "vel", "tracks")]))
        r["slope"] = r["end"] - r["start"]
        r["is_build"] = r["build"] or r["slope"] >= 0.2
        r["energy_read"] = r["end"] if r["is_build"] else r["energy"]
    print("\nModule 9.12 energy arc (v64: band only (the instrumental lead counted), floor spans, by event; a build read by where it arrives)")
    for r in rows: print(f"  {r['sec']:12s} {'#' * int(round(r['energy_read'] * 20)):20s} read {r['energy_read']:.2f}  avg {r['energy']:.2f}  start {r['start']:.2f} -> end {r['end']:.2f}{'  BUILD' if r['is_build'] else ''}")
    pickle.dump(dict(energy=rows, stems_db=diff, vox_gain=VOX_GAIN, band_vol=BAND_VOL), open(f"{OUT}/demo_report.pkl", "wb"))
