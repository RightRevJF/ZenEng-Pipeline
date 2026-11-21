"""Wood and Cloth (second edition): the demo, from song_record.json. General MIDI: church organ (19) on the organ's three staves,
choir aahs (52) for the four parts, voice oohs (53) for the descant. The plan as the organ score prints it: introduction and stanzas
1-2 full, stanza 3 softer (manuals only), stanza 4 the choir alone, the link swelling, stanza 5 full with the descant; the tempo
broadens over the last two bars and the last chord is held. Track names ASCII; tempo in quarters."""
import json, subprocess, mido
H = "/home/claude/zeneng-pipeline/songs/p12"; OUT = f"{H}/out"
R = json.load(open(f"{H}/song_record.json")); V = R["voices"]; BAR = 36; ST = {int(k): v for k, v in R["stanza_offsets"].items()}; END = R["end"]
ED = R["edition"]; TPQ = 480; T = lambda t: int(t * TPQ / 12)
def vel(voice, t):
    if voice.startswith("org"):
        if ST[3] <= t < ST[4]: return 50
        if t >= R["link"]: return 84 if t >= ST[5] else 64 + int(20 * (t - R["link"]) / (4 * BAR))
        return 72
    if voice == "Desc": return 84
    if ST[3] <= t < ST[4]: return 58
    if ST[4] <= t < R["link"]: return 70
    if t >= ST[5]: return 88
    return 76
CH = {"S": (0, 52), "A": (1, 52), "T": (2, 52), "B": (3, 52), "Desc": (4, 53), "org_rh": (5, 19), "org_lh": (6, 19), "org_ped": (7, 19)}
mf = mido.MidiFile(ticks_per_beat=TPQ)
tempo = mido.MidiTrack(); mf.tracks.append(tempo); tempo.append(mido.MetaMessage("track_name", name="Wood and Cloth", time=0))
tempo.append(mido.MetaMessage("time_signature", numerator=3, denominator=4, time=0))
marks = [(0, 100)] + [(END - 2 * BAR + 12 * i, 100 - 6 * (i + 1)) for i in range(6)]
last = 0
for t, q in marks:
    tempo.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(q), time=T(t) - last)); last = T(t)
for name, (ch, prog) in CH.items():
    tr = mido.MidiTrack(); mf.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name, time=0))
    tr.append(mido.Message("program_change", channel=ch, program=prog, time=0))
    ev = []
    for e in V[name]:
        ps = e["p"] if isinstance(e["p"], list) else [e["p"]]
        d = e["dur"] + (24 if e["on"] + e["dur"] == END else 0)          # the last chord held a little longer (the fermata)
        for p in ps:
            ev.append((T(e["on"]), 1, p, vel(name, e["on"]))); ev.append((T(e["on"] + d) - 8, 0, p, 0))
    ev.sort(key=lambda x: (x[0], x[1])); now = 0
    for t, on, p, v in ev:
        tr.append(mido.Message("note_on" if on else "note_off", channel=ch, note=p, velocity=v, time=t - now)); now = t
mid = f"{OUT}/Wood and Cloth{ED} - demo.mid"; mf.save(mid)
wav = f"/tmp/wac_demo.wav"; mp3 = f"{OUT}/Wood and Cloth{ED} - demo.mp3"
subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-r", "44100", "-F", wav, "/usr/share/sounds/sf2/FluidR3_GM.sf2", mid], check=True, capture_output=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "volume=6dB,alimiter=limit=0.89:level=disabled", "-b:a", "224k", mp3], check=True)
print("demo", round(mf.length, 1), "s")
