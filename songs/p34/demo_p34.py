"""Swallowed Up -- the demo (9-M.9): MP3, General MIDI and GarageBand MIDI, read from the song record.
  Two rhythm guitars apart in timing (about 10 ms) and tuning (+6 cents), hard left and right; palm mutes as short notes; bass on
  the root an octave below; the lead right of centre; the GM power kit. Snare backbeats 115-120, blast snares 125-127 (never every
  stroke at 127); quantised to about 90%; little reverb on the blast passages.
  The harsh voice: in the MIDI files, a placeholder on three keys (low C3, mid G3, high D4) with the words as lyric events; in the MP3,
  a rendered placeholder -- noise and a rough buzz through the vowel's formants (darkened for the growl, bright for the scream).
  Both are DEFAULTS, to be checked by ear. The demo is a reference for pitch, rhythm and form, not for tone.
  Stems: the voice measured against the band where it sounds (the standing rule: at least +3 dB)."""
import pickle, subprocess, os, sys, collections
import numpy as np, mido
from scipy.io import wavfile
from scipy import signal
REC = pickle.load(open("/home/claude/p34/song_record.pkl", "rb"))
OUT = "/home/claude/p34/out"; os.makedirs(OUT, exist_ok=True); BASE = f"{OUT}/Swallowed Up - demo"
TPQ = 480; S16 = TPQ // 4
EV = REC["events"]; BARS = REC["bars"]; NB = REC["nbars"]
def tick(b, s): return (b * 16 + s) * S16
rng = np.random.default_rng(34)
CH = {"Gtr 1": 0, "Gtr 2": 1, "Bass": 2, "Lead": 3, "Voice": 4, "Drums": 9}
PROG = {"Gtr 1": 30, "Gtr 2": 30, "Bass": 34, "Lead": 30, "Voice": 54, "Drums": 16}
PAN = {"Gtr 1": 4, "Gtr 2": 124, "Bass": 64, "Lead": 84, "Voice": 64, "Drums": 64}
NAMES = {"Gtr 1": "Rhythm guitar 1 (left)", "Gtr 2": "Rhythm guitar 2 (right)", "Bass": "Bass", "Lead": "Lead guitar", "Voice": "Harsh voice (placeholder)", "Drums": "Drums"}
BAND_VOL = int(sys.argv[1]) if len(sys.argv) > 1 else 100
tracks = collections.defaultdict(list)
for e in EV:
    p = e["part"]; t0 = tick(e["bar"], e["slot"])
    jit = int(rng.integers(-3, 4)) if p == "Drums" else int(rng.integers(-6, 7))      # about 90% quantised
    if p == "Gtr 2": jit += 16                                                          # the second guitar about 10 ms behind
    t0 = max(0, t0 + jit)
    if p == "Drums": ln = 60
    elif e.get("pm"): ln = int(e["dur"] * S16 * 0.5)                                    # palm mutes short
    else: ln = int(e["dur"] * S16 * (0.97 if e["dur"] >= 8 else 0.9))
    vel = max(1, min(127, e["vel"] + (0 if p == "Drums" else int(rng.integers(-3, 4)))))
    tracks[p].append((t0, 1, ("on", e["pitch"], vel)))
    tracks[p].append((t0 + max(10, ln), 0, ("off", e["pitch"], 0)))
    if p == "Voice": tracks[p].append((t0, 2, ("lyric", e["word"])))
# reverb: little on the blasts
for k, bb in enumerate(BARS):
    if k == 0 or bb["sec"] != BARS[k - 1]["sec"]:
        rv = 8 if "Chorus" in bb["sec"] else (35 if bb["sec"] == "Slowdown" else 20)
        for p in ("Gtr 1", "Gtr 2", "Drums", "Lead"): tracks[p].append((tick(k, 0), 0, ("cc", 91, rv)))

def write(path, gm=True, only=None):
    mf = mido.MidiFile(ticks_per_beat=TPQ); t0 = mido.MidiTrack(); mf.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name="Swallowed Up", time=0))
    meta = []
    for k, bb in enumerate(BARS):
        if k == 0 or bb["q"] != BARS[k - 1]["q"]: meta.append((tick(k, 0), 0, mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bb["q"]), time=0)))
        if k == 0:
            meta.append((0, 1, mido.MetaMessage("time_signature", numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)))
            meta.append((0, 2, mido.MetaMessage("key_signature", key="Bm", time=0)))
        if k == 0 or bb["sec"] != BARS[k - 1]["sec"]: meta.append((tick(k, 0), 3, mido.MetaMessage("marker", text=bb["sec"], time=0)))
    now = 0
    for t, pri, m in sorted(meta, key=lambda x: (x[0], x[1])): m.time = t - now; now = t; t0.append(m)
    for p, name in NAMES.items():
        if only is not None and p not in only: continue
        ch = CH[p]; tr = mido.MidiTrack(); mf.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name, time=0))
        if gm: tr.append(mido.Message("program_change", program=PROG[p], channel=ch, time=0))
        if gm and p == "Gtr 2": tr.append(mido.Message("pitchwheel", pitch=123, channel=ch, time=0))      # +6 cents
        tr.append(mido.Message("control_change", control=10, value=PAN[p], channel=ch, time=0))
        tr.append(mido.Message("control_change", control=7, value=127 if p == "Voice" else BAND_VOL, channel=ch, time=0))
        now = 0
        for t, pri, e in sorted(tracks[p], key=lambda x: (x[0], x[1])):
            dt = t - now; now = t
            if e[0] == "on": tr.append(mido.Message("note_on", channel=ch, note=e[1], velocity=e[2], time=dt))
            elif e[0] == "off": tr.append(mido.Message("note_off", channel=ch, note=e[1], velocity=0, time=dt))
            elif e[0] == "cc": tr.append(mido.Message("control_change", channel=ch, control=e[1], value=e[2], time=dt))
            else: tr.append(mido.MetaMessage("lyrics", text=e[1].encode("ascii", "ignore").decode(), time=dt))
    mf.save(path); return path

SF = "/usr/share/sounds/sf2/FluidR3_GM.sf2"; SR = 44100
def render(mid, wav):
    subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", str(SR), "-F", wav, SF, mid], check=True, capture_output=True)
    sr, x = wavfile.read(wav); os.remove(wav); return x.astype(np.float64)

# ---- the rendered harsh-voice placeholder ----
FORM = {"IY": (270, 2290, 3010), "IH": (390, 1990, 2550), "EH": (530, 1840, 2480), "AE": (660, 1720, 2410), "AA": (730, 1090, 2440),
        "AO": (570, 840, 2410), "UH": (440, 1020, 2240), "UW": (300, 870, 2240), "AH": (640, 1190, 2390), "ER": (490, 1350, 1690),
        "OW": (500, 900, 2400), "EY": (480, 1900, 2500), "AY": (700, 1200, 2500), "AW": (700, 1000, 2400), "OY": (550, 900, 2400)}
SRC = {"low": (72, 0.55, 0.88), "mid": (150, 0.45, 1.0), "high": (330, 0.70, 1.0)}       # f0, noise share, formant scale
def harsh(e, n):
    f0, nz, fs = SRC[e["height"]]
    t = np.arange(n) / SR
    jit = np.cumsum(rng.normal(0, 0.9, n)) / 400.0
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.06 * np.sin(2 * np.pi * 23 * t) + jit * 0.02)) / SR
    buzz = signal.sawtooth(ph) + 0.6 * signal.sawtooth(ph / 2)                        # a subharmonic for the growl's roughness
    src = (1 - nz) * buzz + nz * rng.normal(0, 1, n)
    y = np.zeros(n)
    for k, F in enumerate(FORM.get(e["vowel"], FORM["AH"])):
        b, a = signal.iirpeak(min(F * fs, SR / 2 - 100), 6.0 + 2 * k, fs=SR); y += signal.lfilter(b, a, src) / (1 + k)
    att = min(n, int(0.012 * SR)); rel = min(n, int(0.06 * SR))
    env = np.ones(n); env[:att] = np.linspace(0, 1, att); env[-rel:] *= np.linspace(1, 0, rel)
    y = np.tanh(2.5 * y / (np.abs(y).max() + 1e-9)) * env
    return y * (1.0 if e["stressed"] else 0.72)
def voice_track(total):
    y = np.zeros(total)
    for e in EV:
        if e["part"] != "Voice": continue
        i0 = int(e["t"] * SR); n = max(200, int(e["ts"] * 0.92 * SR))
        if i0 + n > total: n = total - i0
        y[i0:i0 + n] += harsh(e, n)
    return y

if __name__ == "__main__":
    gm = write(f"{BASE} (General MIDI).mid", gm=True); gb = write(f"{BASE} (GarageBand).mid", gm=False)
    band_mid = write(f"{OUT}/_band.mid", gm=True, only=[p for p in NAMES if p != "Voice"])
    xb = render(band_mid, f"{OUT}/_band.wav"); os.remove(band_mid)
    total = len(xb); v = voice_track(total)
    mask = np.zeros(total, bool)
    for e in EV:
        if e["part"] == "Voice": mask[int(e["t"] * SR):int((e["t"] + e["ts"]) * SR)] = True
    band_mono = xb.mean(1)
    rb = np.sqrt(np.mean(band_mono[mask] ** 2)); rv = np.sqrt(np.mean(v[mask] ** 2))
    TARGET = 4.0
    g = rb / rv * 10 ** (TARGET / 20); v *= g
    diff = 20 * np.log10(np.sqrt(np.mean(v[mask] ** 2)) / rb)
    y = xb + v[:, None] * np.array([1.0, 1.0])
    end = int((REC["seconds"] + 2.5) * SR); y = y[:end]
    fade = int(SR * 2.5); y[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    y = y / (np.abs(y).max() + 1e-9) * 0.89
    wav = f"{BASE}.wav"; wavfile.write(wav, SR, (y * 32767).astype(np.int16))
    mp3 = f"{BASE}.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "volume=5dB,alimiter=limit=0.89:level=disabled", "-b:a", "224k", mp3], check=True)
    os.remove(wav)
    L = len(y) / SR
    print(f"stems: the voice {diff:+.1f} dB over the band where it sounds (>= +3 dB); band CC7 {BAND_VOL}")
    print("wrote", mp3, f"{int(L // 60)}:{L % 60:04.1f}")
    # the snare's velocities as the demo plays them (9-M.9)
    sn = [e for e in EV if e["part"] == "Drums" and e["pitch"] == 38]
    blast = [e["vel"] for e in sn if "Chorus" in BARS[e["bar"]]["sec"]]; back = [e["vel"] for e in sn if "Chorus" not in BARS[e["bar"]]["sec"]]
    print(f"snare: backbeats {min(back)}-{max(back)}, blasts {min(blast)}-{max(blast)} ({sum(1 for x in blast if x == 127)} of {len(blast)} at 127)")
    pickle.dump(dict(stems_db=float(diff), band_vol=BAND_VOL, length=L, snare_back=(min(back), max(back)), snare_blast=(min(blast), max(blast)),
                     blast_at_127=sum(1 for x in blast if x == 127) / len(blast)), open(f"{OUT}/demo_report.pkl", "wb"))
