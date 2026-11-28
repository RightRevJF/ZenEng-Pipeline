"""Folk replication, notes side only. Reads the four printed collections that ship inside music21
(O'Neill's 1850, Ryan's Mammoth, Aird's Airs, the Essen folk-song collection) and writes, per tune,
its titles, metre, length, range, pitch-class entropy and every part of the page gate
(lib/luthier/page_gate.py, imported unchanged). No outcome is read here.

python3 studies/folk_replication/measures.py -> studies/folk_replication/measures.json.gz
"""
import os, re, sys, json, gzip, glob, warnings, hashlib
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "lib", "luthier"))
import page_gate                                   # unchanged; read only
import music21
from music21 import converter, harmony
CORPUS = os.path.join(os.path.dirname(music21.__file__), "corpus")
COLLECTIONS = [("oneills", "oneills1850"), ("ryans", "ryansMammoth"), ("airds", "airdsAirs"), ("essen", "essenFolksong")]

def pc_entropy(p, d):
    """bits; the pitch-class distribution weighted by each note's time to the next (as the withdrawn study's code defined it)"""
    h = np.bincount(np.asarray(p, int) % 12, np.asarray(d, float), 12); h = h[h > 0]; q = h / h.sum()
    return float(-(q * np.log2(q)).sum())

def split_tunes(text):
    """ABC text -> list of tune texts, each starting at X:"""
    out, cur = [], None
    for line in text.splitlines():
        if re.match(r"^\s*X\s*:", line):
            if cur: out.append("\n".join(cur))
            cur = [line]
        elif cur is not None: cur.append(line)
    if cur: out.append("\n".join(cur))
    return out

def header(t, field):
    return [m.group(1).strip() for m in re.finditer(r"^\s*%s\s*:(.*)$" % field, t, re.M)]

NOTE = re.compile(r"(\^\^|__|\^|_|=)?([A-Ga-g])([,']*)")
def carry_accidentals(tune_text):
    """ABC: an accidental holds for the same note (letter and octave) to the end of its bar. music21 10.5 does not
    carry it, so write it out on every later note of that bar that has none of its own."""
    out = []
    for line in tune_text.splitlines():
        if re.match(r"^\s*[A-Za-z]\s*:", line) or line.lstrip().startswith("%"):
            out.append(line); continue
        res, i, n = [], 0, len(line)
        while i < n:
            ch = line[i]
            if ch == "%": res.append(line[i:]); break
            if ch in "\"!+":                                   # chord symbols, annotations and decorations
                j = line.find(ch, i + 1); j = n - 1 if j < 0 else j; res.append(line[i:j + 1]); i = j + 1; continue
            if ch == "[" and i + 2 < n and line[i + 1].isalpha() and line[i + 2] == ":":   # inline field
                j = line.find("]", i); j = n - 1 if j < 0 else j; res.append(line[i:j + 1]); i = j + 1; continue
            if ch == "|":
                CARRY.clear(); res.append(ch); i += 1; continue
            m = NOTE.match(line, i)
            if m:
                acc, letter, octv = m.group(1), m.group(2), m.group(3)
                key = (letter, octv)
                if acc: CARRY[key] = acc
                elif key in CARRY: acc = CARRY[key]
                res.append((acc or "") + letter + octv); i = m.end(); continue
            res.append(ch); i += 1
        out.append("".join(res))
    CARRY.clear()
    return "\n".join(out)
CARRY = {}

def notes_of(tune_text):
    s = converter.parse(carry_accidentals(tune_text), format="abc")
    if hasattr(s, "scores"): s = s.scores[0] if len(s.scores) else s
    fl = s.flatten().stripTies()
    on, p, dur = [], [], []
    for n in fl.notesAndRests:
        if n.isRest or isinstance(n, harmony.Harmony): continue
        if n.duration.isGrace or n.quarterLength == 0: continue
        if n.isChord: m = max(x.midi for x in n.pitches)
        else: m = n.pitch.midi
        on.append(float(n.offset)); p.append(int(m)); dur.append(float(n.quarterLength))
    if len(p) < 2: return None
    order = np.argsort(on, kind="stable"); on = np.array(on)[order]; p = np.array(p)[order]; dur = np.array(dur)[order]
    d = np.append(np.diff(on), dur[-1]); d = np.where(d <= 0, dur, d)
    return p, d

def metre_class(m):
    m = (m or "").replace(" ", "")
    if m in ("C", "4/4", "C|", "2/2"): return "4/4" if m in ("C", "4/4") else "2/2"
    if m in ("2/4", "3/4", "6/8", "9/8", "12/8", "3/8", "6/4", "3/2"): return m
    if m in ("", "none", "free"): return "none"
    return "other"

def main():
    rows, failed = [], {}
    for coll, folder in COLLECTIONS:
        files = sorted(glob.glob(os.path.join(CORPUS, folder, "*.abc"))); failed[coll] = 0
        for f in files:
            text = open(f, encoding="latin-1").read()
            for t in split_tunes(text):
                x = (header(t, "X") or ["?"])[0]; titles = [s for s in header(t, "T") if s]; M = (header(t, "M") or [""])[0]
                if not titles: failed[coll] += 1; continue
                try:
                    r = notes_of(t)
                except Exception:
                    r = None
                if r is None: failed[coll] += 1; continue
                p, d = r
                try:
                    g = page_gate.read(p, d)
                except Exception:
                    failed[coll] += 1; continue
                rid = hashlib.md5(("%s|%s|%s" % (coll, os.path.basename(f), x)).encode()).hexdigest()[:12]
                row = dict(id=rid, collection=coll, file=os.path.basename(f), x=x, titles=titles, metre=metre_class(M), metre_raw=M,
                           n_notes=int(len(p)), ln_notes=float(np.log(len(p))), range=float(p.max() - p.min()), pc_entropy=pc_entropy(p, d))
                for k, v in g.items(): row[k] = float(v)
                rows.append(row)
        print(coll, "tunes kept", sum(r["collection"] == coll for r in rows), "not read", failed[coll], flush=True)
    out = os.path.join(HERE, "measures.json.gz")
    with gzip.open(out, "wt") as fh: json.dump(dict(music21=music21.__version__, failed=failed, rows=rows), fh)
    print("tunes", len(rows), "->", out)

if __name__ == "__main__":
    main()
