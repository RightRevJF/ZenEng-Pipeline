"""Module 11.11 demo for 'Everything That Moves' (song 60; funk-disco, in the record's key, q = 116, 4/4), adapted from demo_p65.py. Guide voice: a tenor sax
at pitch for the baritone; the harmony voice on a soft choir. Every part read from the song record and humanized here (pink-noise velocity and timing, v43; the
drums kept on the grid). General MIDI and the MP3 (no GarageBand MIDI; a full score)."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo60 as KI
import pickle, subprocess, os, sys
import numpy as np, mido
from scipy.io import wavfile
REC = pickle.load(open("/home/claude/p70/" + os.environ.get("SONG60_PKL", "song_record.pkl"), "rb"))
OUT = "/home/claude/p70/" + os.environ.get("SONG60_OUT", "out"); os.makedirs(OUT, exist_ok=True)
BASE = f"{OUT}/{REC['file_title']} - demo"
T = 480; TW = T // 12
BARS = REC["bars"]; lead = REC["lead"]
def tk(e): return int(round(e * TW))
SEC_AT = [0.0]
for x in BARS: SEC_AT.append(SEC_AT[-1] + x["len"] / 12 * 60 / x["qbpm"])
def secs(e): b = min(len(BARS) - 1, e // 48); return SEC_AT[b] + (e - b * 48) / 12 * 60 / BARS[b]["qbpm"]
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
KEYS = ["him", "her", "harm", "drums", "bass", "guitar", "lead", "horns"]
DEV = {k: Dev(i * 17 + 3, tim=1) for i, k in enumerate(KEYS)}
VOX_GAIN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].lstrip("-").isdigit() else 30
BAND_VOL = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 80
CH = dict(him=0, her=7, harm=1, drums=9, bass=2, guitar=3, lead=4, horns=5)
PROG = dict(him=66, her=65, harm=53, drums=0, bass=33, guitar=28, lead=61, horns=61)      # funk-disco: a muted clean rhythm guitar, finger bass, a brass section for the break and the stabs
PAN = dict(him=64, her=64, harm=80, drums=64, bass=64, guitar=40, lead=88, horns=88)
REVERB = dict(him=45, her=45, harm=60, drums=30, bass=10, guitar=30, lead=50, horns=50)
NAMES = dict(him="Voice (guide, tenor sax)", her="Voice 2", harm="Harmony voice (choir)", drums="Drums", bass="Bass", guitar="Rhythm guitar", lead="Horns (break)", horns="Horns")
tracks = {}
def note(key, t0, t1, p, v):
    v = max(1, min(127, int(v))); tr = NAMES[key]; ch = CH[key]
    tracks.setdefault(tr, []).append((max(0, t0), 1, ("on", ch, p, v)))
    tracks[tr].append((max(t0 + 5, t1), 0, ("off", ch, p, 0)))
def meta(key, t, text): tracks.setdefault(NAMES[key], []).append((t, 2, ("meta", "lyrics", dict(text=text))))
VBASE = {s: int(56 + 24 * REC["level"][s]) for s in REC["level"]}
for src, lead_ in ((lead, True), (REC["harm"], False)):
    for n in src:
        key = n["singer"] if n["singer"] in ("him", "her") else "harm"
        dv, dt = DEV[key](); v = VBASE[n["sec"]] + (VOX_GAIN if lead_ else VOX_GAIN - 10) + dv
        t0 = tk(n["on"]) + 3 + dt
        note(key, t0, tk(n["on"] + n["dur"] * 0.93), n["midi"], v)
        if lead_ and n["first"]: meta(key, t0, n["text"])
def play(key, evs):
    for e in evs:
        dv, dt = DEV[key]()
        if key == "drums": dt = 0
        ln = e["dur"] * (0.97 if key == "bass" else 0.9)
        for j, p in enumerate(e["p"]): note(key, tk(e["on"]) + dt, tk(e["on"] + ln), p, e["vel"] + dv - j)
for key, evs in REC["parts"].items(): play(key, evs)
def write(path, gm=True, only=None):
    mf = mido.MidiFile(ticks_per_beat=T)
    t0 = mido.MidiTrack(); mf.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name=REC["title"], time=0))
    evs = [(0, 2, mido.MetaMessage("key_signature", key=KI.TONIC, time=0))]
    q0 = None
    for x in BARS:                                                                           # the tempo plan (A), bar by bar
        if x["qbpm"] != q0: evs.append((tk(x["start"]), 0, mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(x["qbpm"]), time=0))); q0 = x["qbpm"]
    prev = None
    for x in BARS:
        if x["meter"] != prev:
            num, den = map(int, x["meter"].split("/"))
            evs.append((tk(x["start"]), 1, mido.MetaMessage("time_signature", numerator=num, denominator=den, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)))
            prev = x["meter"]
    for s, nb, st, mets, mv in REC["plan"]: evs.append((tk(st), 3, mido.MetaMessage("marker", text=f"{s}", time=0)))
    now = 0
    for t, pri, m in sorted(evs, key=lambda x: (x[0], x[1])):
        m.time = t - now; now = t; t0.append(m)
    seen = set()
    for key, name in NAMES.items():
        if name in seen: continue
        seen.add(name)
        if only is not None and name not in only: continue
        if name not in tracks: continue
        tr = mido.MidiTrack(); mf.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name, time=0))
        if gm and key == "drums": tr.append(mido.Message("program_change", program=0, channel=9, time=0))    # the standard kit
        if gm and key != "drums": tr.append(mido.Message("program_change", program=PROG[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=10, value=PAN[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=7, value=127 if key in ("him", "her") else BAND_VOL, channel=CH[key], time=0))
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
def stems_check():
    VOXN = {NAMES["him"], NAMES["her"]}
    a = write(f"{OUT}/stem_vox.mid", only=VOXN); b = write(f"{OUT}/stem_band.mid", only=set(NAMES.values()) - VOXN - {NAMES["harm"]})
    sr, xv = render(a, f"{OUT}/stem_vox.wav"); _, xb = render(b, f"{OUT}/stem_band.wav")
    n = min(len(xv), len(xb)); xv, xb = xv[:n].mean(1), xb[:n].mean(1)
    mask = np.zeros(n, bool)
    for nn in lead:
        i0 = int(secs(nn["on"]) * sr); i1 = int(secs(nn["on"] + nn["dur"]) * sr); mask[i0:min(n, i1)] = True
    rv = 20 * np.log10(np.sqrt(np.mean(xv[mask] ** 2)) + 1e-9); rb = 20 * np.log10(np.sqrt(np.mean(xb[mask] ** 2)) + 1e-9)
    for f in ("stem_vox.mid", "stem_band.mid", "stem_vox.wav", "stem_band.wav"): os.remove(f"{OUT}/{f}")
    return rv - rb
if __name__ == "__main__":
    diff = stems_check()
    print(f"stems: lead {diff:+.1f} dB over the band (v43 rule: >= +3 dB); vocal gain {VOX_GAIN}, band CC7 {BAND_VOL}")
    if "--check" in sys.argv: sys.exit(0)
    gm = write(f"{BASE} (General MIDI).mid", gm=True)
    wav = f"{BASE}.wav"
    sr, y = render(gm, wav)
    end = int(mido.MidiFile(gm).length * sr) + int(4.0 * sr); y = y[:end]
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
            if tr in (NAMES["him"], NAMES["her"], NAMES["harm"]): continue
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
    for s, nb, st, mets, mv in REC["plan"]:
        L = sum(48 if m == "4/4" else 42 if m == "7/8" else 60 for m in mets)
        a, z = tk(st), tk(st + L); q = (z - a) // 4
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
