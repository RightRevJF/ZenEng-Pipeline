"""Module 11.11 demo for 'Make Do' (V/N; dream-pop, 68 bars, 3:47). 4/4 at q = 72, one tick line in eighths (240 ticks an eighth).
Intro / verses   a slow drum machine (kick on 1, a soft rim on 3, quiet eighth hats), a bass that barely moves (whole notes), a clean
                 guitar ringing eighth-note arpeggios in Gmaj7 / Cmaj7 shapes, a pad under it all; the intro's line on the clean lead.
Choruses         the same, opened: the pad louder, the snare on 3 with a long tail, a second guitar holding chord shapes; DO on B3.
Break            12 bars, 'where the light comes in': the instrumental line (Module 27.21) on its own track, the band thinned to pad,
                 bass and hats so the line sits in the gap.
Chorus 3         the last DO on D4; the outro's line rings out over Gmaj7.
Guide vocal: the v43 reed fallback for a baritone (bassoon), at sung pitch (B2-D4).  Instrumental lead -- clean guitar (GM 27), its
own track and stem (11.11, v64)."""
import pickle, subprocess, os, collections, sys, random
import numpy as np, mido
from scipy.io import wavfile
REC = pickle.load(open("/home/claude/p21/song_record.pkl", "rb"))
OUT = "/home/claude/p21/out"; os.makedirs(OUT, exist_ok=True); BASE = f"{OUT}/Make Do - demo"
T = 480; E8 = 240
BARS = REC["bars"]; PLAN = REC["plan"]; lead = REC["lead"]; NB = REC["nbars"]; GTR = REC["gtr"]
def tk(e): return int(round(e * E8))
ROOT = {"Gmaj7": 7, "Cmaj7": 0, "D": 2, "Em7": 4, "Am7": 9, "G": 7}
TONES = {"Gmaj7": [7, 11, 2, 6], "Cmaj7": [0, 4, 7, 11], "D": [2, 6, 9], "Em7": [4, 7, 11, 2], "Am7": [9, 0, 4, 7], "G": [7, 11, 2]}
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
KEYS = ["voc", "lead", "arp", "chords", "bass", "pad", "drums"]
DEV = {k: Dev(i * 17 + 3) for i, k in enumerate(KEYS)}
VOX_GAIN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].lstrip("-").isdigit() else 12
BAND_VOL = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 92
CH = dict(voc=0, lead=1, arp=2, chords=3, bass=4, pad=5, drums=9)
PROG = dict(voc=70, lead=27, arp=27, chords=26, bass=33, pad=89, drums=0)
PAN = dict(voc=64, lead=74, arp=40, chords=88, bass=64, pad=64, drums=64)
REVERB = dict(voc=60, lead=110, arp=110, chords=100, bass=20, pad=120, drums=70)
NAMES = dict(voc="Guide vocal (bassoon -- reed fallback, baritone)", lead="Instrumental lead - clean guitar", arp="Clean guitar (arpeggios)",
             chords="Guitar (held shapes)", bass="Bass", pad="Pad", drums="Drum machine")
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
# ---- vocal ----
VBASE = {"Verse 1": 64, "Verse 2": 66, "Verse 3": 66, "Chorus 1": 72, "Chorus 2": 74, "Chorus 3": 76}
for n in lead:
    dv, dt = DEV["voc"]()
    v = VBASE[n["sec"]] + VOX_GAIN + dv + (6 if n["midi"] >= 59 else 0)
    t0 = tk(n["on"]) + 6 + dt; t1 = tk(n["on"] + n["dur"] * 0.94)
    note("voc", t0, t1, n["midi"], v); meta("voc", t0, n["syl"][0])
# ---- the instrumental lead (27.21) ----
for n in GTR:
    dv, dt = DEV["lead"](); note("lead", tk(n["on"]) + dt, tk(n["on"] + n["dur"] * 0.97), n["midi"], (72 if n["sec"] == "Break" else 62) + dv)
# ---- band, bar by bar ----
rng = random.Random(21)
for bi, b in enumerate(BARS):
    sec, ch, st, ln = b["sec"], b["chord"], b["start"], b["len"]; t = tk(st)
    first = bi == 0 or BARS[bi - 1]["sec"] != sec
    k_in = bi - [x for x in range(NB) if BARS[x]["sec"] == sec][0]
    nb_sec = sum(1 for x in BARS if x["sec"] == sec)
    def dn(p, e, v, l=0.4):
        dv, dt = DEV["drums"](); note("drums", t + tk(e) + dt, t + tk(e + l), p, v + dv)
    r = 31 + ((ROOT[ch] - 31) % 12)
    cho = sec.startswith("Chorus"); brk = sec == "Break"; last_bar = sec == "Outro" and k_in == nb_sec - 1
    [note("pad", t + 10, t + tk(ln) - 10, p, 40 + (8 if cho else 0) + (6 if brk else 0)) for p in voicing(ch, 60, 4)]
    if last_bar:
        [note("arp", t + 20 * k, t + tk(7.9), p, 54 - 3 * k) for k, p in enumerate(voicing(ch, 52, 5))]; note("bass", t, t + tk(7.8), r, 64); continue
    dv, dt = DEV["bass"](); note("bass", t + dt, t + tk(7.6), r, 70 + (6 if cho else 0) + dv)
    if not brk:                                              # the ringing arpeggios
        vo = voicing(ch, 55, 5); pat = [0, 2, 4, 3, 1, 3, 4, 2]
        for e, i in enumerate(pat):
            dv, dt = DEV["arp"](); note("arp", t + tk(e) + dt, t + tk(e + 2.5), vo[i] + 12 * (e == 2), 46 + dv + (6 if e == 0 else 0) + (4 if cho else 0))
    if cho:
        [note("chords", t + 12, t + tk(7.6), p, 46) for p in voicing(ch, 59, 3)]
    if sec == "Intro" and k_in < 2: continue
    dn(36, 0, 70 + (6 if cho else 0)); dn(37 if not cho else 38, 4, 54 if not cho else 70, 1.5)
    if not brk or True:
        [dn(42, e, (34 if e % 2 == 0 else 26) + (4 if cho else 0)) for e in range(8)]
    if first and cho: dn(57, 0, 64, 6)
    if sec == "Chorus 3" and k_in == 7: dn(49, 0, 74, 8)
def write(path, gm=True, only=None):
    mf = mido.MidiFile(ticks_per_beat=T)
    t0 = mido.MidiTrack(); mf.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name=REC["title"], time=0))
    ev = []
    for s, nb, b0, met in PLAN:
        st = BARS[b0]["start"]; num, den = met.split("/")
        ev.append((tk(st), 0, mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BARS[b0]["qbpm"]), time=0)))
        ev.append((tk(st), 1, mido.MetaMessage("time_signature", numerator=int(num), denominator=int(den), clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0)))
        k = "G"
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
    a = write(f"{OUT}/stem_vox.mid", only={NAMES["voc"]}); b = write(f"{OUT}/stem_band.mid", only=set(NAMES.values()) - {NAMES["voc"]})
    sr, xv = render(a, f"{OUT}/stem_vox.wav"); _, xb = render(b, f"{OUT}/stem_band.wav")
    n = min(len(xv), len(xb)); xv, xb = xv[:n].mean(1), xb[:n].mean(1)
    # the tempo map: seconds at each eighth
    es = REC["eighth_sec"]; tsec = []; acc = 0.0
    for bb in BARS:
        for _ in range(bb["len"]): tsec.append(acc); acc += es[bb["meter"]]
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
            if tr == NAMES["voc"]: continue
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
    print("\nModule 9.12 energy arc (v64: band only, floor spans, by event; a build read by where it arrives)")
    for r in rows: print(f"  {r['sec']:12s} {'#' * int(round(r['energy_read'] * 20)):20s} read {r['energy_read']:.2f}  avg {r['energy']:.2f}  start {r['start']:.2f} -> end {r['end']:.2f}{'  BUILD' if r['is_build'] else ''}")
    pickle.dump(dict(energy=rows, stems_db=diff, vox_gain=VOX_GAIN, band_vol=BAND_VOL), open(f"{OUT}/demo_report.pkl", "wb"))
