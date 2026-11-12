"""Module 11.11 demo for 'Before It's Done' (song 45; 56 bars, 3:07, q = 72, 4/4, G major, the last chorus and the tag a whole step up in A).
Guide voice: tenor sax (the man's guide); steel-string guitar, fingerpicked (each note rings until its string is played again, as a guitar
does), and the cello from verse 2 -- all read from the song record and humanized here (pink-noise velocity and timing, v43; strums rolled)."""
import pickle, subprocess, os, sys
import numpy as np, mido
from scipy.io import wavfile
REC = pickle.load(open("/home/claude/p49/song_record.pkl", "rb"))
OUT = "/home/claude/p49/out"; os.makedirs(OUT, exist_ok=True); SUF = ""
BASE = f"{OUT}/Before It's Done - demo"
T = 480; TW = T // 12
BARS = REC["bars"]; PLAN = REC["plan"]; lead = REC["lead"]; NB = REC["nbars"]
def swing(e): return e                                                                # straight eighths
def tk(e): return int(round(swing(e) * TW))
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
KEYS = ["voc", "gtr", "vc"]
DEV = {k: Dev(i * 17 + 3, tim=1) for i, k in enumerate(KEYS)}
VOX_GAIN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].lstrip("-").isdigit() else 6
BAND_VOL = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 84
CH = dict(voc=0, gtr=1, vc=2)
PROG = dict(voc=66, gtr=25, vc=42)
PAN = dict(voc=64, gtr=52, vc=80)
REVERB = dict(voc=50, gtr=45, vc=60)
NAMES = dict(voc="Voice - guide (tenor sax)", gtr="Acoustic guitar (fingerpicked)", vc="Cello")
tracks = {}
def note(key, t0, t1, p, v):
    v = max(1, min(127, int(v))); tr = NAMES[key]; ch = CH[key]
    tracks.setdefault(tr, []).append((max(0, t0), 1, ("on", ch, p, v)))
    tracks[tr].append((max(t0 + 5, t1), 0, ("off", ch, p, 0)))
def meta(key, t, text): tracks.setdefault(NAMES[key], []).append((t, 2, ("meta", "lyrics", dict(text=text))))
VBASE = {"Verse 1": 64, "Chorus 1": 72, "Verse 2": 66, "Chorus 2": 74, "Bridge": 64, "Last Chorus": 80, "Tag": 62}
for n in lead:
    key = "voc"
    dv, dt = DEV[key](); v = VBASE[n["sec"]] + VOX_GAIN + dv + (4 if n["midi"] >= 62 else 0)
    t0 = tk(n["on"]) + 3 + dt
    note(key, t0, tk(n["on"] + n["dur"] * 0.93), n["midi"], v)
    if n["first"]: meta(key, t0, n["text"])
def play_gtr(evs):
    """each note rings to its end in the record (its string played again, or the hand leaving the fret); a strum rolled low to high."""
    for e in evs:
        roll = 5 if e.get("art") == "strum" else 0
        order = sorted(range(len(e["p"])), key=lambda j: -e["sf"][j][0])
        for k, j in enumerate(order):
            dv, dt = DEV["gtr"](); note("gtr", tk(e["on"]) + k * roll + dt, tk(e["ring"][j]) - 2, e["p"][j], e["vel"] + dv)
def play(key, evs):
    for e in evs:
        dv, dt = DEV[key]()
        for j, p in enumerate(e["p"]): note(key, tk(e["on"]) + dt, tk(e["on"] + e["dur"]) - 4, p, e["vel"] + dv - j)
play_gtr(REC["gtr"]); play("vc", REC["cello"])
def write(path, gm=True, only=None):
    mf = mido.MidiFile(ticks_per_beat=T)
    t0 = mido.MidiTrack(); mf.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name=REC["title"], time=0))
    evs = [(0, 0, mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(REC["qbpm"]), time=0)),
           (0, 1, mido.MetaMessage("time_signature", numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)),
           (0, 2, mido.MetaMessage("key_signature", key="G", time=0)),
           (tk(REC["plan"][[x[0] for x in REC["plan"]].index("Last Chorus")][2] * 48), 2, mido.MetaMessage("key_signature", key="A", time=0))]
    for s, nb, b0, met in PLAN: evs.append((tk(b0 * 48), 3, mido.MetaMessage("marker", text=s, time=0)))
    now = 0
    for t, pri, m in sorted(evs, key=lambda x: (x[0], x[1])):
        m.time = t - now; now = t; t0.append(m)
    for key, name in NAMES.items():
        if only is not None and name not in only: continue
        if name not in tracks: continue
        tr = mido.MidiTrack(); mf.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name, time=0))
        if gm: tr.append(mido.Message("program_change", program=PROG[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=10, value=PAN[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=7, value=127 if key == "voc" else BAND_VOL, channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=91, value=REVERB.get(key, 40), channel=CH[key], time=0))
        now = 0
        for t, pri, e in sorted(tracks.get(name, []), key=lambda x: (x[0], x[1])):
            dt = t - now; now = t
            if e[0] == "on": tr.append(mido.Message("note_on", channel=e[1], note=e[2], velocity=e[3], time=dt))
            elif e[0] == "off": tr.append(mido.Message("note_off", channel=e[1], note=e[2], velocity=0, time=dt))
            elif e[0] == "prog":
                if gm: tr.append(mido.Message("program_change", channel=e[1], program=e[2], time=dt))
                else: now -= dt
            else: tr.append(mido.MetaMessage(e[1], text=e[2].get("text", "").encode("ascii", "ignore").decode(), time=dt))
    mf.save(path); return path
SF = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
def render(mid, wav):
    subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", "44100", "-F", wav, SF, mid], check=True, capture_output=True)
    sr, x = wavfile.read(wav); return sr, x.astype(np.float64)
def stems_check():
    a = write(f"{OUT}/stem_vox.mid", only={NAMES["voc"]}); b = write(f"{OUT}/stem_band.mid", only=set(NAMES.values()) - {NAMES["voc"]})
    sr, xv = render(a, f"{OUT}/stem_vox.wav"); _, xb = render(b, f"{OUT}/stem_band.wav")
    n = min(len(xv), len(xb)); xv, xb = xv[:n].mean(1), xb[:n].mean(1)
    mask = np.zeros(n, bool)
    for nn in lead:
        i0 = int(swing(nn["on"]) * REC["tw_sec"] * sr); i1 = int(swing(nn["on"] + nn["dur"]) * REC["tw_sec"] * sr); mask[i0:min(n, i1)] = True
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
    end = int(mido.MidiFile(gm).length * sr) + int(2.0 * sr); y = y[:end]
    fade = int(sr * 2.0); y[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    y = y / (np.abs(y).max() + 1e-9) * 0.89
    wavfile.write(wav, sr, (y * 32767).astype(np.int16))
    mp3 = f"{BASE}.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "volume=6dB,alimiter=limit=0.89:level=disabled", "-b:a", "224k", mp3], check=True)
    os.remove(wav)
    print("wrote", mp3, f"{int(len(y)/sr//60)}:{len(y)/sr%60:04.1f}")
    def window(a, z):
        ev, vel, trs = 0.0, [], set()
        for tr, evs in tracks.items():
            if tr == NAMES["voc"]: continue
            ons = sorted(t for (t, p, e) in evs if p == 1 and e[0] == "on" and a <= t < z)
            vel += [e[3] for (t, p, e) in evs if p == 1 and e[0] == "on" and a <= t < z]
            last = None; cnt = 0
            for t in ons:
                if last is None or t - last > 30: cnt += 1
                last = t
            if cnt: trs.add(tr)
            ev += cnt
        return ev, (float(np.mean(vel)) if vel else 0.0), len(trs)
    rows = []
    for s, nb, b0, met in PLAN:
        a, z = tk(b0 * 48), tk((b0 + nb) * 48); q = (z - a) // 4
        whole = window(a, z); first = window(a, a + q); lastq = window(z - q, z)
        rows.append(dict(sec=s, events=whole[0] / nb, vel=whole[1], tracks=whole[2], q1=dict(events=first[0] / max(1, nb / 4), vel=first[1], tracks=first[2]),
                         q4=dict(events=lastq[0] / max(1, nb / 4), vel=lastq[1], tracks=lastq[2]), build=False))
    MIN_SPAN = dict(events=4, vel=16, tracks=3)
    allv = {kk: [r[kk] for r in rows] + [r["q1"][kk] for r in rows] + [r["q4"][kk] for r in rows] for kk in ("events", "vel", "tracks")}
    def nz(kk, v):
        lo_, hi_ = min(allv[kk]), max(allv[kk]); span = max(hi_ - lo_, MIN_SPAN[kk]); return (v - lo_) / span
    for r in rows:
        r["energy"] = float(np.mean([nz(kk, r[kk]) for kk in ("events", "vel", "tracks")]))
        r["start"] = float(np.mean([nz(kk, r["q1"][kk]) for kk in ("events", "vel", "tracks")]))
        r["end"] = float(np.mean([nz(kk, r["q4"][kk]) for kk in ("events", "vel", "tracks")]))
        r["slope"] = r["end"] - r["start"]; r["is_build"] = r["build"] or r["slope"] >= 0.2
        r["energy_read"] = r["end"] if r["is_build"] else r["energy"]
    print("\nModule 9.12 energy arc (band only, floor spans, by event; a build read by where it arrives)")
    for r in rows: print(f"  {r['sec']:12s} {'#' * int(round(r['energy_read'] * 20)):20s} read {r['energy_read']:.2f}  avg {r['energy']:.2f}  start {r['start']:.2f} -> end {r['end']:.2f}{'  BUILD' if r['is_build'] else ''}")
    pickle.dump(dict(energy=rows, stems_db=diff, vox_gain=VOX_GAIN, band_vol=BAND_VOL), open(f"{OUT}/demo_report.pkl", "wb"))
