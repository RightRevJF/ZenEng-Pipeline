"""Song 62: the files for an AI singer (ACE Studio or Synthesizer V): the vocal line alone as MIDI, from bar 1 at the song's tempo (so it lines up
with the instruments), each note carrying its syllable as a MIDI lyric; and the lyrics typed the way ACE Studio takes them (whole words; '-' on a
note that holds the syllable before).  python3 voice_for_singer62.py "first edition, corrected" """
import json, sys, re, mido
sys.path.insert(0, "."); import engrave_syll as ES
LABEL = sys.argv[1]; D = f"out/{LABEL}"; R = json.load(open(f"{D}/record.json")); BT = R["bar"] // 4; T = R["title"]
mel = sorted(R["melody"], key=lambda n: n["on"]); sy = ES.syllables(mel)
TPB = 480; tk = lambda e: int(round(e * TPB / BT)); mf = mido.MidiFile(ticks_per_beat=TPB); tr = mido.MidiTrack(); mf.tracks.append(tr)
tr.append(mido.MetaMessage("track_name", name="Voice")); tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(R["bpm"]))); tr.append(mido.MetaMessage("time_signature", numerator=4, denominator=4))
ev = []
for n, s in zip(mel, sy):
    t0, t1 = tk(n["on"]), tk(n["on"] + n["dur"]) - 1
    ev.append((t0, 0, "lyric", (s or "-").replace("’", "'").rstrip("-") if s else "-")); ev.append((t0, 1, "on", n["midi"])); ev.append((t1, 2, "off", n["midi"]))
ev.sort(key=lambda x: (x[0], x[1])); now = 0
for t, _, k, v in ev:
    m = mido.MetaMessage("lyrics", text=v, time=t - now) if k == "lyric" else mido.Message("note_on" if k == "on" else "note_off", note=v, velocity=90 if k == "on" else 0, time=t - now)
    tr.append(m); now = t
mf.save(f"{D}/{T} - voice for ACE Studio.mid")
# the lyrics, line by line, as ACE Studio takes them
by = {}
for n in mel: by.setdefault((n["sec"], n["line"]), []).append(n)
SHOW = {"Chorus 1": "Refrain", "Chorus 2": "Refrain", "Chorus 3": "Last refrain"}
out = [f"{T}: lyrics for ACE Studio", "Type or paste one line at a time onto that line's notes. A dash holds the word before over one more note.", ""]; last = None
for (sec, ln), ns in sorted(by.items(), key=lambda kv: kv[1][0]["on"]):
    if sec != last: out.append(""); out.append(SHOW.get(sec, sec)); last = sec
    toks = []; prev = None
    for n in ns:
        if not n["text"]: toks.append("-")
        elif n["text"] != prev:
            w_ = n["text"]; w_ = {"sunday": "Sunday", "saturday": "Saturday", "december": "December", "i": "I", "dad": "Dad"}.get(w_, w_)
            toks.append(w_[:1].upper() + w_[1:] if not toks else w_); prev = n["text"]
    out.append(" ".join(toks))
open(f"{D}/{T} - lyrics for ACE Studio.txt", "w").write("\n".join(out) + "\n")
print(len(mel), "notes;", sum(1 for s in sy if s is None), "held")
