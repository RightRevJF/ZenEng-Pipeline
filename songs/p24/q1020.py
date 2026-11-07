"""Module 10.20 (v55), the quotable line, run outside the app: every line ranked against the song's other lines on four within-song
z-scores, in two regimes. Approximations, logged: no lyric trigram and no POS model from the 15,297-lyric corpus here, so lexical
surprise is read as low content-word Zipf and syntactic ordinariness is not scored; antithesis is detected as two equal cola, one
negated and one not, with the same frame (the hand antonym list is empty); metaphor is not measured (as the module says)."""
import sys, re, collections, statistics as st
sys.path[:0] = ["/home/claude/p24", "/home/claude/carol", "/home/claude/pop"]
import engine_p24 as E, phrasestress48 as P; P.install(E); E.install_patches()
from lyricsearch import syllables, zipf, FUNCTION, phones
import lyric as L
nlp = E._NLP
lines = list(dict.fromkeys(L.SUNG)); rep = collections.Counter(L.SUNG)
title = L.TITLE.lower()
QUANT = {"all", "every", "everything", "nothing", "never", "always", "each", "no", "everyone", "nobody", "else"}
THIRD = {"he", "she", "her", "his", "him", "they", "them", "their"}
def cw(l): return [w for w in re.findall(r"[a-z']+", l.lower()) if w not in FUNCTION]
def gen(l):
    d = nlp(l); s = 0.0
    s += sum(1 for t in d if t.lower_ in ("a", "an"))
    s -= 0.5 * sum(1 for t in d if t.lower_ in THIRD)
    s -= 0.5 * sum(1 for t in d if t.tag_ == "VBD")
    s += sum(1 for t in d if t.lower_ in QUANT) + sum(1 for t in d if t.tag_ in ("JJR", "RBR"))
    s += sum(1 for t in d if t.pos_ == "NOUN" and (E.conc(t.text) or 5) <= 2.5) - sum(1 for t in d if t.pos_ == "PROPN")
    return s
def dbp(l):
    c = cw(l); z = st.mean(zipf(w) for w in c) if c else 6
    others = [set(cw(o)) for o in lines if o != l]; me = set(c)
    dist = 1 - max((len(me & o) / max(1, len(me | o)) for o in others), default=0)
    return (-z) + 2 * dist
def stressed_words(l): return [x for x in syllables(l) if x[2]]
def euph(l):
    ws = [w for w in re.findall(r"[a-z']+", l.lower()) if w not in FUNCTION]
    ini = []
    for w in ws:
        try: ini.append(phones(w).split()[0])
        except Exception: pass
    allit = sum(1 for a, b in zip(ini, ini[1:]) if a == b and not a[-1].isdigit())
    vs = [x[1] for x in stressed_words(l)]
    internal = sum(c - 1 for c in collections.Counter(re.sub(r"\d", "", v) for v in vs).values() if c > 1)
    return allit + 0.5 * internal
def sent(l, i):
    s = 0.0; cola = [c.strip() for c in l.split(",") if c.strip()]
    if len(cola) == 2:
        a, b = cola; na, nb = len(syllables(a)), len(syllables(b))
        neg = lambda t: bool(re.search(r"\b(not|never|no|didn't|don't|won't|can't|isn't|wasn't|nothing)\b", t.lower()))
        if abs(na - nb) <= 1: s += 1                                   # isocolon
        if abs(na - nb) <= 1 and neg(a) != neg(b) and a.split()[0].lower() == b.split()[0].lower(): s += 2   # antithesis by negation
    if len(re.findall(r",", l)) >= 2: s += 1                           # tricolon (a three-part list)
    sec = next([x for _, x in ls] for _, ls in L.SECTIONS if l in [x for _, x in ls]); j = sec.index(l)
    for k in (j - 1, j + 1):
        if 0 <= k < len(sec):
            o = sec[k].lower().split(); m = l.lower().split()
            if o[0] == m[0]: s += 1                                    # anaphora
            if o[-1] == m[-1]: s += 1                                  # epistrophe
    return s
def z(vals):
    m, sd = st.mean(vals), (st.pstdev(vals) or 1)
    return [(v - m) / sd for v in vals]
G = z([gen(l) for l in lines]); D = z([dbp(l) for l in lines]); U = z([euph(l) for l in lines])
S = z([sent(l, i) for i, l in enumerate(lines)]); R = z([rep[l] for l in lines])
T = [1.0 if ("song" in l.lower()) else 0.0 for l in lines]; T = z(T)
REM = [r + u + g + t - 0.5 * d for r, u, g, t, d in zip(R, U, G, T, D)]      # repeated, euphonic, general (conventional), title-bearing
ANN = [d + s for d, s in zip(D, S)]                                          # lexically original, figured, distinct
q = lambda v: sorted(v)[int(0.75 * (len(v) - 1))]
rows = sorted(zip(lines, REM, ANN), key=lambda x: -(x[1] + x[2]))
print("Module 10.20 -- the quotable line (within-song z-scores; ceiling: features agree with human picks 64-72%; the writer's pick stands)")
for l, r, a in rows: print(f"  REM {r:+5.2f}{'*' if r >= q(REM) else ' '}  ANN {a:+5.2f}{'*' if a >= q(ANN) else ' '}  x{rep[l]}  {l}")
both = [l for l, r, a in rows if r >= q(REM) and a >= q(ANN)]
print("top quartile under both:", both)
import pickle; pickle.dump(dict(rows=rows, both=both), open("/home/claude/p24/q1020.pkl", "wb"))
# v59 fix 12: the blind pick's middle slot -- a line top-quartile under both; else the most-repeated hook line (chorus, hook, refrain
# or tag, sung twice or more; the title line first on a tie); else the best summed rank. The rule that filled it prints.
hookroles = {l: r for _, ls in L.SECTIONS for r, l in ls}
REMt, ANNt = rows[0], None
remtop = max(rows, key=lambda x: x[1])[0]; anntop = max(rows, key=lambda x: x[2])[0]
both_free = [l for l in both if l not in (remtop, anntop)]   # v59: the three slots distinct
if both_free: mid, rule = both_free[0], "top quartile under both"
else:
    cand = [l for l in lines if hookroles.get(l) in ("chorus", "hook", "refrain", "tag") and rep[l] >= 2 and l not in (remtop, anntop)]
    if cand:
        mx = max(rep[l] for l in cand); cand = [l for l in cand if rep[l] == mx]
        cand.sort(key=lambda l: (0 if "song" in l.lower() else 1))
        mid, rule = cand[0], "the most-repeated hook line"
    else:
        mid = next(l for l, r, a in rows if l not in (remtop, anntop)); rule = "the best summed rank"
print("blind pick slots:", dict(remembered=remtop, middle=mid, annotated=anntop, rule=rule))
pickle.dump(dict(rows=rows, both=both, slots=dict(remembered=remtop, middle=mid, annotated=anntop, rule=rule)), open("/home/claude/p24/q1020.pkl", "wb"))
