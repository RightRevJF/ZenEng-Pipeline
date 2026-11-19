"""The song's key, read from the record (lyric58.song.json), for every document script: the key's name, note spellings by scale degree,
LilyPond and MusicXML names, and Nashville numbers. Nothing here assumes C. Major keys only (the song's mode)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_R = json.load(open(os.path.join(HERE, "lyric58.song.json")))
TONIC = _R["key"]["key"]                       # e.g. "A"
TPC = _R["key"]["tonic_midi"] % 12
KEYSTR = f"{TONIC} major"
LETTERS = "CDEFGAB"; NAT = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MAJOR = [0, 2, 4, 5, 7, 9, 11]
# a chromatic note by its distance from the tonic: (scale degree, alteration): b2, b3, #4, b6, b7 (one going a semitone to the next note is spelled by _spell_dir)
CHROM = {1: (1, -1), 3: (2, -1), 6: (3, +1), 8: (5, -1), 10: (6, -1)}
def _deg_alt(rel):
    rel %= 12
    if rel in MAJOR: return MAJOR.index(rel), 0
    return CHROM[rel]
def letter_acc(pc):
    """(letter, accidental in semitones) for a pitch class, spelled in the key."""
    d, a = _deg_alt(pc - TPC); L = LETTERS[(LETTERS.index(TONIC[0]) + d) % 7]
    acc = (pc - NAT[L]) % 12; acc = acc - 12 if acc > 6 else acc
    return L, acc
def name(pc, uni=True):
    L, a = letter_acc(pc); s = {"#": "♯", "b": "♭"} if uni else {"#": "#", "b": "b"}
    return L + (s["#"] * a if a > 0 else s["b"] * (-a))
NM = [name(pc) for pc in range(12)]               # note names, as a musician reads them in this key
def lily(pc):
    L, a = letter_acc(pc); return L.lower() + ("is" * a if a > 0 else "es" * (-a))
SP = {pc: lily(pc) for pc in range(12)}
LILY_KEY = f"\\key {lily(TPC)} \\major"
def root_pc(root):
    """a chord root as written ('F#', 'Bb', 'C♯') to its pitch class."""
    m = re.match(r"([A-G])([#b♯♭]*)", root); n = NAT[m.group(1)]
    for c in m.group(2): n += 1 if c in "#♯" else -1
    return n % 12
def lily_root(root): return root[0].lower() + "".join("is" if c in "#♯" else "es" for c in root[1:])      # as the chord is written
NUM = {0: "1", 2: "2", 4: "3", 5: "4", 7: "5", 9: "6", 11: "7", 10: "♭7", 3: "♭3", 8: "♭6", 1: "♭2", 6: "♯4"}
def number(root): return NUM[(root_pc(root) - TPC) % 12]
def split_chord(ch):
    m = re.match(r"([A-G][#b♯♭]?)(.*)", ch); return m.group(1), m.group(2)
def nashville(ch):
    """a chord name to its number in the key: 'F#m' in A is '6m'; a slash chord keeps its bass as a number."""
    if "/" in ch:
        a, b = ch.split("/", 1); return nashville(a) + "/" + number(b)
    r, q = split_chord(ch); return number(r) + q
DIATONIC = [(0, ""), (2, "m"), (4, "m"), (5, ""), (7, ""), (9, "m")]
def numbers_line():
    """'A major: 1 = A, 2m = Bm, ...' for the chart's footnote."""
    return f"{KEYSTR}: " + ", ".join(f"{NUM[r]}{q} = {name((TPC + r) % 12)}{q}" for r, q in DIATONIC)
def _spell_dir(p, nxt=None):
    """(letter, accidental) for a note: in the key; a chromatic note a semitone from the next note takes the letter next to that note's letter
    (up into it: the letter below, as D♯ to E or E♯ to F♯; down into it: the letter above, as B♭ to A or C to B)."""
    pc = p % 12
    if (pc - TPC) % 12 in MAJOR or nxt is None or abs(nxt - p) != 1: return letter_acc(pc)
    Lt, _ = letter_acc(nxt % 12); L = LETTERS[(LETTERS.index(Lt) + (-1 if nxt > p else 1)) % 7]
    acc = (pc - NAT[L]) % 12; acc = acc - 12 if acc > 6 else acc
    return L, acc
def lily_dir(p, nxt=None):
    L, a = _spell_dir(p, nxt); return L.lower() + ("is" * a if a > 0 else "es" * (-a))
def lily_octave(p, nxt=None):
    """the LilyPond octave marks, from the written letter's own octave (B♯3 sounds as C4; C♭4 as B3)."""
    L, a = _spell_dir(p, nxt); o = (p - a) // 12 - 4; return "'" * o if o > 0 else "," * (-o)
def name_dir(p, nxt=None):
    s = lily_dir(p, nxt); return s[0].upper() + s[1:].replace("is", "♯").replace("es", "♭")
CAPO = _R["key"].get("capo")                     # e.g. "capo 2, A shapes", or None
def capo_fret(): return int(re.match(r"capo (\d+)", CAPO).group(1)) if CAPO else 0
def shape(ch):
    """the open shape a guitarist fingers for a chord with the capo on: B with capo 2 is an A shape. Spelled as in the shapes' key."""
    if not CAPO: return ch
    k = capo_fret(); SH = re.search(r", (\S+) shapes", CAPO).group(1); spc = (TPC - k) % 12
    def one(c):
        r, q = split_chord(c); rel = (root_pc(r) - TPC) % 12; pc = (spc + rel) % 12
        d, a = _deg_alt(rel); L = LETTERS[(LETTERS.index(SH[0]) + d) % 7]; acc = (pc - NAT[L]) % 12; acc = acc - 12 if acc > 6 else acc
        return L + ("#" * acc if acc > 0 else "b" * (-acc)) + q
    return "/".join(one(x) for x in ch.split("/"))
def capo_line(chords):
    """'Capo 2, A shapes: B is played as A, C♯m as Bm, ...' for the chords the song uses."""
    if not CAPO: return ""
    seen = []
    for c in chords:
        if c not in seen: seen.append(c)
    return f"{CAPO[0].upper() + CAPO[1:]}: " + ", ".join(f"{c} as {shape(c)}" for c in seen).replace("#", "♯")
