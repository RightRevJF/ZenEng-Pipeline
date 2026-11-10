"""Module 11.11 demo for 'Sadie' (a country-rock anthem; a male baritone lead, a gang, a band; 88 bars, 2:50, 4/4 at q = 124 on eighths;
A major). Kit, picked bass, distorted rhythm guitar, overdriven lead guitar (the riff and the answers), steel-string acoustic, drawbar
organ, the gang (choir aahs, unison and the octave below) -- all read from the song record and humanized here (pink-noise velocity and
timing, v43). Guide voice: trombone (the baritone's register, at pitch). The drop: the record's silence, the kick's heartbeat alone;
9.12 reads it as designed silence (fix 87) and checks it reads below its neighbours (fix 60)."""
import pickle, subprocess, os, collections, sys, random
import numpy as np, mido
from scipy.io import wavfile
REC = pickle.load(open("/home/claude/p33/song_record.pkl", "rb"))
OUT = "/home/claude/p33/out"; os.makedirs(OUT, exist_ok=True); BASE = f"{OUT}/Sadie - demo"
T = 480; E8 = 240          # an eighth (the record's slot)
BARS = REC["bars"]; PLAN = REC["plan"]; lead = REC["lead"]; HARM = REC["harm"]; NB = REC["nbars"]
def tk(e): return int(round(e * E8))
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
KEYS = ["voc", "gang", "drm", "bas", "rhy", "riff", "ac", "org"]
DEV = {k: Dev(i * 17 + 3, tim=1) for i, k in enumerate(KEYS)}
VOX_GAIN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].lstrip("-").isdigit() else 12
BAND_VOL = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 92
CH = dict(voc=0, gang=1, drm=9, bas=2, rhy=3, riff=4, ac=5, org=6)
PROG = dict(voc=57, gang=52, drm=0, bas=34, rhy=30, riff=29, ac=25, org=16)
PAN = dict(voc=64, gang=64, drm=64, bas=64, rhy=30, riff=96, ac=80, org=50)
REVERB = dict(voc=40, gang=70, drm=25, bas=8, rhy=22, riff=40, ac=30, org=50)
NAMES = dict(voc="Guide vocal (trombone)", gang="Gang (choir)", drm="Drums", bas="Bass", rhy="Rhythm guitar", riff="Lead guitar (riff and answers)",
             ac="Acoustic guitar", org="Organ")
tracks = collections.OrderedDict()
def note(key, t0, t1, p, v):
    v = max(1, min(127, int(v))); tr = NAMES[key]; ch = CH[key]
    tracks.setdefault(tr, []).append((max(0, t0), 1, ("on", ch, p, v)))
    tracks[tr].append((max(t0 + 5, t1), 0, ("off", ch, p, 0)))
def ctrl(key, t, kind, val):
    tracks.setdefault(NAMES[key], []).append((max(0, t), 0, ("cc" if kind != "pw" else "pw", CH[key], kind, val)))
def meta(key, t, text): tracks.setdefault(NAMES[key], []).append((t, 2, ("meta", "lyrics", dict(text=text))))
# ---- the voice ----
VBASE = {"Verse 1": 66, "Pre 1": 70, "Chorus 1": 76, "Verse 2": 68, "Pre 2": 72, "Chorus 2": 78, "Bridge": 66, "Drop": 72, "Chorus 3": 80, "Chorus 4": 82}
for n in lead:
    dv, dt = DEV["voc"](); v = VBASE[n["sec"]] + VOX_GAIN + dv + (4 if n["syl"][2] else 0)
    t0 = tk(n["on"]) + 3 + dt
    note("voc", t0, tk(n["on"] + n["dur"] * 0.92), n["midi"], v); meta("voc", t0, n["syl"][0])
def play(key, evs):
    for e in evs:
        dv, dt = DEV[key]()
        if key == "drm": dt = 0
        art = e.get("art", "")
        ln = e["dur"] * (0.97 if art in ("ring", "pad") else (0.55 if art == "palm" else 0.9))
        t0 = tk(e["on"]) + dt
        for j, p in enumerate(e["p"]):
            off = 6 * j if key == "ac" else 0
            note(key, t0 + off, tk(e["on"] + ln), p, e["vel"] + dv - j)
play("drm", REC["drums"]); play("bas", REC["bass"]); play("rhy", REC["rhy"]); play("riff", REC["riff"]); play("ac", REC["ac"]); play("org", REC["organ"]); play("gang", REC["gang"])
def write(path, gm=True, only=None):
    mf = mido.MidiFile(ticks_per_beat=T)
    t0 = mido.MidiTrack(); mf.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name=REC["title"], time=0))
    ev = []
    for s, nb, b0, met in PLAN:
        st = BARS[b0]["start"]; num, den = met.split("/")
        ev.append((tk(st), 0, mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BARS[b0]["qbpm"]), time=0)))
        ev.append((tk(st), 1, mido.MetaMessage("time_signature", numerator=int(num), denominator=int(den), clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)))
        k = {"A major": "A"}[BARS[b0]["key"]]
        ev.append((tk(st), 2, mido.MetaMessage("key_signature", key=k, time=0)))
        ev.append((tk(st), 3, mido.MetaMessage("marker", text=s, time=0)))
    now = 0
    for t, pri, m in sorted(ev, key=lambda x: (x[0], x[1])):
        m.time = t - now; now = t; t0.append(m)
    for key, name in NAMES.items():
        if only is not None and name not in only: continue
        if name not in tracks: continue
        tr = mido.MidiTrack(); mf.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name, time=0))
        if gm and key != "drm": tr.append(mido.Message("program_change", program=PROG[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=10, value=PAN[key], channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=7, value=127 if key == "voc" else BAND_VOL, channel=CH[key], time=0))
        tr.append(mido.Message("control_change", control=91, value=REVERB.get(key, 40), channel=CH[key], time=0))
        now = 0
        for t, pri, e in sorted(tracks.get(name, []), key=lambda x: (x[0], x[1])):
            dt = t - now; now = t
            if e[0] == "on": tr.append(mido.Message("note_on", channel=e[1], note=e[2], velocity=e[3], time=dt))
            elif e[0] == "off": tr.append(mido.Message("note_off", channel=e[1], note=e[2], velocity=0, time=dt))
            elif e[0] == "cc": tr.append(mido.Message("control_change", channel=e[1], control=e[2], value=max(0, min(127, e[3])), time=dt))
            elif e[0] == "pw": tr.append(mido.Message("pitchwheel", channel=e[1], pitch=e[3], time=dt))
            else: tr.append(mido.MetaMessage(e[1], text=e[2].get("text", "").encode("ascii", "ignore").decode(), time=dt))
    mf.save(path); return path
SF = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
def render(mid, wav):
    subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", "44100", "-F", wav, SF, mid], check=True, capture_output=True)
    sr, x = wavfile.read(wav); return sr, x.astype(np.float64)
def sec_of_tick(tick, mf):
    return mido.tick2second(tick, T, 500000)
def stems_check():
    a = write(f"{OUT}/stem_vox.mid", only={NAMES["voc"]}); b = write(f"{OUT}/stem_band.mid", only=set(NAMES.values()) - {NAMES["voc"]})
    sr, xv = render(a, f"{OUT}/stem_vox.wav"); _, xb = render(b, f"{OUT}/stem_band.wav")
    n = min(len(xv), len(xb)); xv, xb = xv[:n].mean(1), xb[:n].mean(1)
    # the tempo map: seconds at each eighth
    es = 60.0 / REC["qbpm"]["4/4"] / 2; tsec = []; acc = 0.0
    for bb in BARS:
        for _ in range(bb["len"]): tsec.append(acc); acc += es
    tsec.append(acc)
    mask = np.zeros(n, bool)
    for nn in lead:
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
            if tr in (NAMES["voc"], NAMES["gang"]): continue
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
        sil_n = sum(1 for bb in BARS[b0:b0 + nb] if bb.get("silence")); sil = [None] * sil_n
        if sil_n: z = tk(BARS[b0 + nb - sil_n]["start"]); nb = nb - sil_n; q = (z - a) // 4      # fix 87: designed silence out of the reading
        a, z = a - 20, z - 20                         # the humanized timing (+-4 ticks) must not carry a downbeat entry into the section before
        whole = window(a, z); first = window(a, a + q); lastq = window(z - q, z)
        rows.append(dict(sec=s, silent_bars=len(sil), events=whole[0] / nb, vel=whole[1], tracks=whole[2],
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
    # fix 87: a designed silence is left out of the reading -- the drop is read on its first bar alone; fix 60: it must read below its neighbours
    dr_ = next(r for r in rows if r["sec"] == "Drop"); i_ = rows.index(dr_)
    print(f"  drop (designed silence: {dr_['silent_bars']} of 4 bars out of the reading): reads {dr_['energy']:.2f} against {rows[i_-1]['sec']} {rows[i_-1]['energy_read']:.2f} and {rows[i_+1]['sec']} {rows[i_+1]['energy_read']:.2f} -> {'below both' if dr_['energy'] < min(rows[i_-1]['energy_read'], rows[i_+1]['energy_read']) else 'NOT below'}")
    pickle.dump(dict(energy=rows, stems_db=diff, vox_gain=VOX_GAIN, band_vol=BAND_VOL), open(f"{OUT}/demo_report.pkl", "wb"))
