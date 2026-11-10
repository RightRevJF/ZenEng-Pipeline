"""The First Wood -- the demo: MP3, General MIDI and GarageBand MIDI from the song record. Choir aahs for the four voices (the tune
a little forward), church organ for the manuals and the pedal; a church's reverb; lightly humanized. The voices are wordless in
General MIDI: the words are lyric events in the MIDI files and in the scores. Stems: the choir against the organ where both sound
(the standing rule: at least +3 dB)."""
import pickle, subprocess, os, sys, collections
import numpy as np, mido
from scipy.io import wavfile
REC = pickle.load(open("/home/claude/p35/song_record.pkl", "rb")); EV = REC["events"]
OUT = "/home/claude/p35/out"; os.makedirs(OUT, exist_ok=True); BASE = f"{OUT}/The First Wood - demo"
TPQ = 480; T12 = TPQ // 12
rng = np.random.default_rng(35)
PARTS = ["S", "A", "T", "B", "Organ RH", "Organ LH", "Pedal", "Organ 4ft"]
CH = {"S": 0, "A": 1, "T": 2, "B": 3, "Organ RH": 4, "Organ LH": 5, "Pedal": 6, "Organ 4ft": 7}
PROG = {"S": 52, "A": 52, "T": 52, "B": 52, "Organ RH": 19, "Organ LH": 19, "Pedal": 19, "Organ 4ft": 19}
PAN = {"S": 50, "A": 40, "T": 84, "B": 76, "Organ RH": 64, "Organ LH": 64, "Pedal": 64, "Organ 4ft": 64}
NAMES = {"S": "Soprano", "A": "Alto", "T": "Tenor", "B": "Bass", "Organ RH": "Organ right hand", "Organ LH": "Organ left hand", "Pedal": "Organ pedal", "Organ 4ft": "Organ 4ft (stanza 4)"}
VOX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
ORG = int(sys.argv[2]) if len(sys.argv) > 2 else 80
tracks = collections.defaultdict(list)
for e in EV:
    p = e["part"]; t0 = e["abs12"] * T12 + (int(rng.integers(-6, 7)) if p in ("S", "A", "T", "B") else 0)
    t1 = (e["abs12"] + e["dur"]) * T12 - 18
    v = e["vel"] + (VOX if p in ("S", "A", "T", "B") else 0) + (6 if p == "S" else 0)
    tracks[p].append((max(0, t0), 1, ("on", e["pitch"], max(1, min(127, v)))))
    tracks[p].append((max(t0 + 20, t1), 0, ("off", e["pitch"], 0)))
    if e.get("first") and e.get("word"): tracks[p].append((max(0, t0), 2, ("lyric", e["word"])))

def write(path, gm=True, only=None):
    mf = mido.MidiFile(ticks_per_beat=TPQ); t0 = mido.MidiTrack(); mf.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name="The First Wood", time=0))
    t0.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(REC["qbpm"]), time=0))
    t0.append(mido.MetaMessage("time_signature", numerator=3, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    t0.append(mido.MetaMessage("key_signature", key="F", time=0))
    now = 0
    for name, b0, b1 in REC["sections"]:
        t = b0 * 36 * T12; t0.append(mido.MetaMessage("marker", text=name, time=t - now)); now = t
    for p in PARTS:
        if only is not None and p not in only: continue
        ch = CH[p]; tr = mido.MidiTrack(); mf.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=NAMES[p], time=0))
        if gm: tr.append(mido.Message("program_change", program=PROG[p], channel=ch, time=0))
        tr.append(mido.Message("control_change", control=10, value=PAN[p], channel=ch, time=0))
        tr.append(mido.Message("control_change", control=7, value=127 if p in ("S", "A", "T", "B") else ORG, channel=ch, time=0))
        tr.append(mido.Message("control_change", control=91, value=90, channel=ch, time=0))
        now = 0
        for t, pri, e in sorted(tracks[p], key=lambda x: (x[0], x[1])):
            dt = t - now; now = t
            if e[0] == "on": tr.append(mido.Message("note_on", channel=ch, note=e[1], velocity=e[2], time=dt))
            elif e[0] == "off": tr.append(mido.Message("note_off", channel=ch, note=e[1], velocity=0, time=dt))
            else: tr.append(mido.MetaMessage("lyrics", text=e[1].encode("ascii", "ignore").decode(), time=dt))
    mf.save(path); return path
SF = "/usr/share/sounds/sf2/FluidR3_GM.sf2"; SR = 44100
def render(mid, wav):
    subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", str(SR), "-F", wav, SF, mid], check=True, capture_output=True)
    sr, x = wavfile.read(wav); os.remove(wav); return x.astype(np.float64)

if __name__ == "__main__":
    gm = write(f"{BASE} (General MIDI).mid"); write(f"{BASE} (GarageBand).mid", gm=False)
    a = write(f"{OUT}/_v.mid", only=["S", "A", "T", "B"]); b = write(f"{OUT}/_o.mid", only=["Organ RH", "Organ LH", "Pedal", "Organ 4ft"])
    xv, xo = render(a, f"{OUT}/_v.wav"), render(b, f"{OUT}/_o.wav"); os.remove(a); os.remove(b)
    n = min(len(xv), len(xo)); xv, xo = xv[:n].mean(1), xo[:n].mean(1)
    mask = np.zeros(n, bool); spb = 60 / REC["qbpm"]
    for name, b0, b1 in REC["sections"]:
        if name in ("Stanza 1", "Stanza 2", "Stanza 4"): mask[int(b0 * 3 * spb * SR):int(b1 * 3 * spb * SR)] = True
    diff = 20 * np.log10(np.sqrt(np.mean(xv[mask] ** 2)) / np.sqrt(np.mean(xo[mask] ** 2)))
    print(f"stems: the choir {diff:+.1f} dB over the organ where both sound (>= +3 dB); voices +{VOX}, organ CC7 {ORG}")
    if "--check" in sys.argv: sys.exit(0)
    y = render(gm, f"{BASE}.wav")
    end = int((REC["seconds"] + 3.0) * SR); y = y[:end]
    fade = int(SR * 2.5); y[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    y = y / (np.abs(y).max() + 1e-9) * 0.89
    wavfile.write(f"{BASE}.wav", SR, (y * 32767).astype(np.int16))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{BASE}.wav", "-af", "volume=4dB,alimiter=limit=0.89:level=disabled", "-b:a", "224k", f"{BASE}.mp3"], check=True)
    os.remove(f"{BASE}.wav"); L = len(y) / SR
    print("wrote", f"{BASE}.mp3", f"{int(L // 60)}:{L % 60:04.1f}")
    pickle.dump(dict(stems_db=float(diff), vox=VOX, org=ORG, length=L), open(f"{OUT}/demo_report.pkl", "wb"))
