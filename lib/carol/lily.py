"""LilyPond writing with the standing protocol:
  - every voice in \\relative c' (the chain's octave marks computed, never guessed)
  - Python relative-pitch trace (resolve() from prev = 60) BEFORE writing: the written chain must
    reproduce the intended pitches exactly
  - AFTER compiling: LilyPond's own MIDI of a verification score is read back and compared note
    for note (that MIDI is a check file, not a deliverable)
"""
import subprocess, os, re

LETTERS = "cdefgab"
NAT = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
# spelling in D major / with the chromatic notes this hymn uses
SPELL = {0: ("c", ""), 1: ("c", "is"), 2: ("d", ""), 3: ("d", "is"), 4: ("e", ""), 5: ("f", ""),
         6: ("f", "is"), 7: ("g", ""), 8: ("g", "is"), 9: ("a", ""), 10: ("b", "es"), 11: ("b", "")}

def spell(midi):
    letter, acc = SPELL[midi % 12]
    octave = (midi - NAT[letter] - {"is": 1, "es": -1, "": 0}[acc]) // 12 - 1   # scientific octave
    return letter, acc, octave

def resolve(prev_letter, prev_oct, letter, marks):
    """LilyPond relative rule: the new note goes to the octave that puts it within a fourth
    (3 staff steps) of the previous note, then octave marks shift it."""
    p = LETTERS.index(prev_letter) + 7 * prev_oct
    best = None
    for o in range(prev_oct - 2, prev_oct + 3):
        q = LETTERS.index(letter) + 7 * o
        if abs(q - p) <= 3: best = o; break
    return best + marks

def relative_chain(midis, start=60):
    """octave marks for each pitch in \\relative c' starting from c' (= C4, MIDI 60)"""
    pl, po = "c", 4
    out = []
    for m in midis:
        l, a, o = spell(m)
        base = resolve(pl, po, l, 0)
        marks = o - base
        out.append((l, a, marks, o))
        pl, po = l, o
    return out

def trace(chain, intended):
    """re-resolve the written chain from prev = 60 and compare with the intended pitches"""
    pl, po = "c", 4
    for (l, a, marks, _), m in zip(chain, intended):
        o = resolve(pl, po, l, marks)
        got = NAT[l] + {"is": 1, "es": -1, "": 0}[a] + 12 * (o + 1)
        if got != m:
            raise AssertionError(f"relative trace failed: {l}{a}{marks} -> {got}, intended {m}")
        pl, po = l, o
    return True

DUR = {0.5: "8", 1.0: "4", 1.5: "4.", 2.0: "2", 3.0: "2.", 4.0: "1"}

def notes_to_ly(notes, slurs=None, extra=None):
    """notes: list of (midi, dur_beats); slurs: list of (start_idx, end_idx); extra: {idx: str}"""
    midis = [n[0] for n in notes]
    chain = relative_chain(midis)
    trace(chain, midis)
    starts = {s for s, e in (slurs or [])}; ends = {e for s, e in (slurs or [])}
    toks = []
    for i, ((m, d), (l, a, marks, o)) in enumerate(zip(notes, chain)):
        mk = "'" * marks if marks > 0 else "," * (-marks)
        t = f"{l}{a}{mk}{DUR[d]}"
        if extra and i in extra: t += extra[i]
        if i in starts: t += "("
        if i in ends: t += ")"
        toks.append(t)
    return " ".join(toks), chain

def compile_ly(src, outbase, fmt="pdf", png_res=None, cwd="/home/claude/carol/out"):
    os.makedirs(cwd, exist_ok=True)
    path = os.path.join(cwd, outbase + ".ly")
    open(path, "w").write(src)
    args = ["lilypond", "-dno-point-and-click", "-o", os.path.join(cwd, outbase)]
    if fmt == "png":
        args[1:1] = ["--png", f"-dresolution={png_res or 160}"]
    r = subprocess.run(args + [path], capture_output=True, text=True, cwd=cwd)
    errs = [l for l in r.stderr.splitlines() if "error" in l.lower()]
    if r.returncode != 0 or errs:
        raise RuntimeError("lilypond failed:\n" + r.stderr[-3000:])
    warns = [l for l in r.stderr.splitlines() if "warning" in l.lower()]
    return path, warns

def midi_readback(midi_path):
    import mido
    mf = mido.MidiFile(midi_path)
    tracks = []
    for tr in mf.tracks:
        ns = [m.note for m in tr if m.type == "note_on" and m.velocity > 0]
        if ns: tracks.append(ns)
    return tracks
