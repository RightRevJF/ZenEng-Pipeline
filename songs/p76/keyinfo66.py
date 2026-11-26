"""The song's key, read from the record (lyric66_d.hand.song.json), for every document script: the key's name, note spellings, LilyPond and
MusicXML names, and Nashville numbers. A minor key (the writer's A minor): natural minor spellings, with the raised notes the chords use spelled
sharp (G♯, the leading tone; D♯ and C♯, from the descent's E/D♯ and A/C♯; F♯). Numbers count from the minor tonic: 1m, 4m, 5, ♭3, ♭6, ♭7."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
_R = json.load(open(os.path.join(HERE, "lyric66_d.hand.song.json")))
TONIC = _R["key"]["key"].rstrip("m")             # "A"
TPC = _R["key"]["tonic_midi"] % 12
KEYSTR = f"{TONIC} minor"
LETTERS = "CDEFGAB"; NAT = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MINOR = [0, 2, 3, 5, 7, 8, 10]
CHROM = {1: (1, -1), 4: (2, +1), 6: (3, +1), 9: (5, +1), 11: (6, +1)}      # b2, #3, #4, #6, #7 (scale degree index, alteration)
def _deg_alt(rel):
    rel %= 12
    if rel in MINOR: return MINOR.index(rel), 0
    return CHROM[rel]
def letter_acc(pc):
    d, a = _deg_alt(pc - TPC); L = LETTERS[(LETTERS.index(TONIC[0]) + d) % 7]
    acc = (pc - NAT[L]) % 12; acc = acc - 12 if acc > 6 else acc
    return L, acc
def name(pc, uni=True):
    L, a = letter_acc(pc); s = {"#": "♯", "b": "♭"} if uni else {"#": "#", "b": "b"}
    return L + (s["#"] * a if a > 0 else s["b"] * (-a))
NM = [name(pc) for pc in range(12)]
def lily(pc):
    L, a = letter_acc(pc); return L.lower() + ("is" * a if a > 0 else "es" * (-a))
SP = {pc: lily(pc) for pc in range(12)}
LILY_KEY = f"\\key {lily(TPC)} \\minor"
def root_pc(root):
    m = re.match(r"([A-G])([#b♯♭]*)", root); n = NAT[m.group(1)]
    for c in m.group(2): n += 1 if c in "#♯" else -1
    return n % 12
def lily_root(root): return root[0].lower() + "".join("is" if c in "#♯" else "es" for c in root[1:])
NUM = {0: "1", 2: "2", 3: "♭3", 4: "3", 5: "4", 7: "5", 8: "♭6", 9: "6", 10: "♭7", 11: "7", 1: "♭2", 6: "♯4"}
def number(root): return NUM[(root_pc(root) - TPC) % 12]
def split_chord(ch):
    m = re.match(r"([A-G][#b♯♭]?)(.*)", ch); return m.group(1), m.group(2)
def nashville(ch):
    if "/" in ch:
        a, b = ch.split("/", 1); return nashville(a) + "/" + number(b)
    r, q = split_chord(ch); return number(r) + q
DIATONIC = [(0, "m"), (3, ""), (5, "m"), (7, ""), (8, ""), (10, "")]
def numbers_line():
    return f"{KEYSTR}: " + ", ".join(f"{NUM[r]}{q} = {name((TPC + r) % 12)}{q}" for r, q in DIATONIC)
def _spell_dir(p, nxt=None): return letter_acc(p % 12)
def lily_dir(p, nxt=None):
    L, a = _spell_dir(p, nxt); return L.lower() + ("is" * a if a > 0 else "es" * (-a))
def lily_octave(p, nxt=None):
    L, a = _spell_dir(p, nxt); o = (p - a) // 12 - 4; return "'" * o if o > 0 else "," * (-o)
def name_dir(p, nxt=None):
    s = lily_dir(p, nxt); return s[0].upper() + s[1:].replace("is", "♯").replace("es", "♭")
def pitch_name(p): return f"{name(p % 12)}{(p - letter_acc(p % 12)[1]) // 12 - 1}"
CAPO = _R["key"].get("capo")
def shape(ch): return ch
def capo_line(chords): return ""
