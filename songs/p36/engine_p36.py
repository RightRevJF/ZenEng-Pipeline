"""Song 25, "Through Its Breaking" (v64 port; 6/8 in two at dotted-q = 54, two bars a line = 12 eighth slots, span 10). Earlier: Song 24 (3/4). Earlier: Song 23, "What Holds" (4/4 at q = 104, span 10). Earlier: Song 22, "The Seam" (4/4 at q = 80, span 12). Earlier: Song 21, "Make Do" (v64 port; 4/4 at q = 72, span 14). Earlier: Song 20, "Black 5000" (v63 port; 4/4 at q = 144, four bars a line = 16 quarter slots, span 14; v63 compounds). Earlier: Song 19, "Where Words Fail" (v62 port; 4/4 at q = 72, two bars a line, span 14 syllables). Earlier: Song 18, "The Taste of You" (v60 port). Earlier: Song 17, "Bring the Color Back" (v60 port; 12/8). Earlier: Song 16, "Gometapamazitter" (v59 port of song 15's scorer, 4/4 only here). v59 in this port: the exemption covers the
possessive and the plural (fix 1); Rule V1 read on the couplet, the line before a turn exempt (fix 4); the aside role (fix 8);
the v58 span rule as a death in the room (a line over 9 syllables in two bars of 4/4 at q = 112 takes four bars).
Earlier header: Song 15, "A Century in the Carpet" (v58 port; meter-general placement: 4/4 (16 eighths a two-bar line, beats every 2,
strong 0/4/8/12), 7/8 as 2+2+3 (the run's template -- v58 ships no 7/8, a finding: 14 eighths a two-bar line, beats 0/2/4 and
7/9/11, all strong), 6/8 (12, beats 0/3/6/9). Earlier header: Song 14, "Brother Harold" (v58 port; built on song 13's scorer). v58 in this port: the compound metre (12/8: one bar = 12 eighth
slots, beats 0/3/6/9 -- the same slot grid as two bars of 6/8), the four stress rules (28.12 v58 = song 13's F-a..F-d), the writer's
phrases exempt from the word filters (fix 5), Rule V1 switched ON for verse lines (picture_rule; the run's reading, flagged in the
correction note), the never-say lists as deaths.
Old header: Song 13, "Does Not Know My Name" (v55). Ported from song 11's scorer. Changes, logged:
 (1) 6/8 placement. Module 28/29.4's template is 4/4 only (16 eighths, strong 0/4/8/12) and 9-R's feel column has no
     compound row -- a v55 finding. The run's patch: a line spans 2 bars of 6/8 = 12 eighth slots, strong slots = the
     dotted-quarter beats 0/3/6/9; the walk goes in eighths, a stressed syllable that would land off the beat after an
     unstressed one moves to the next beat (gap <= 2 eighths), an optional long-short (quarter-eighth) on stressed
     syllables; pickups 0-3 (as 4/4). Anticipation credit (10.19) one eighth before an empty beat, as in 4/4.
 (2) Register: narrative throughout (writer, Q10 B): dial 0.6, two distinctive words, rare floor 2.75, rhyme-word floor
     4.0; the hook's rhyme floor 4.25 (Table H).
 (3) No never-say list was asked at intake (the run did not ask it; logged as a process miss) -- empty."""
import sys, re, json, hashlib, csv
sys.path.insert(0, "/home/claude/carol"); sys.path.insert(0, "/home/claude/pop")
import popsearch                                   # loads the lexicon overrides and the sung -ear rhyme
from popsearch import OPEN
from lyricsearch import syllables, words, zipf, rhyme_kind, FUNCTION, WEAK_END, OVERRIDE

pass   # no lexicon overrides (song 19)   # Q11 A; sternum one reading   # v54 fix 5 asks these at intake; each has one reading -- the run's readings, logged, not asked
CONC = {}
with open("/home/claude/pop/data/Concreteness_ratings_Brysbaert_et_al_BRM.txt") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        CONC[r["Word"].lower()] = float(r["Conc.M"])
def conc(w):
    w = w.lower().strip("'")
    for c in (w, w.rstrip("s"), w[:-2] if w.endswith("es") else w, w.replace("'s", "")):
        if c in CONC: return CONC[c]
    return None

# Song 8, "All of It Was You" (W/T, v47). The intake's objects stand where Pole A stood; they and the title's words are exempt
# from every word filter (v47 fixes 1.4 / 2.5).
import sys as _s; _s.path.insert(0, "/home/claude/p36")
import intake as _I
for _w, _p in getattr(_I, 'LEXICON', {}).items(): OVERRIDE[_w] = [_p]     # the writer's readings (v54/v60)
POLE_A = set(_I.OBJECTS)
EXEMPT = set(_I.OBJECTS) | {w.lower() for w in _I.TITLE.split()} | set(_I.WRITER_PHRASES) | set(_I.WRITER_WORDS)
PICT = set(_I.OBJECTS) | {w.lower() for w in _I.TITLE.split()}   # what counts as a picture for Rule V1 (objects, title, names)
POLE_B = set()
def exempt(w):
    """v59 fix 1: an exempt word's possessive ('s, s') and plural (s, es, ies) are exempt too"""
    w = w.lower().replace("’", "'")
    forms = {w, w.replace("'s", ""), w.rstrip("'"), w[:-1] if w.endswith("s") else w, w[:-2] if w.endswith("es") else w,
             (w[:-3] + "y") if w.endswith("ies") else w}
    return any(f in EXEMPT for f in forms)
def forms_in(w, S):
    w = w.lower().replace("’", "'")
    forms = {w, w.replace("'s", ""), w.rstrip("'"), w[:-1] if w.endswith("s") else w, w[:-2] if w.endswith("es") else w,
             (w[:-3] + "y") if w.endswith("ies") else w}
    return any(f in S for f in forms)
# Q9 (the run's own answer): never the word love, or any word for it; nothing sweet-talked; no stage-folk diction
Q9_BAN = list(_I.NEVER_SAY) + list(_I.NEVER_PHRASES)
STOCK = popsearch.STOCK + ["can't stop", "won't stop", "don't stop", "here we go", "come alive", "feel alive",
                           "one more time", "all the way", "like there's no", "we own the", "set it off",
                           "out of control", "hold your breath", "count of three", "heart beating", "beat of my heart"]
DIAL = 0.6   # (narrative; old note:) v53 register table, pop row (P, A): dial 0.3, one distinctive word, rare floor 3.0, rhyme-word floor 4.25 (hook 4.25)
DLIM = 2
GENERAL = {"all", "never", "always", "forever", "every", "everybody", "everyone", "nobody", "everything", "nothing"}

def parallel(line, mate):
    if not mate: return 0.0
    a, b = words(line), words(mate)
    p = 0.4 if a[0] == b[0] else 0.0
    fa = [w if w in FUNCTION else "_" for w in a]; fb = [w if w in FUNCTION else "_" for w in b]
    p += 0.3 if fa == fb else 0.0
    p += 0.3 if len(syllables(line)) == len(syllables(mate)) else 0.0
    return min(1.0, p)

REG = {r: (0.6, 2, 2.75, 4.25 if r in ("chorus", "hook") else 4.0) for r in ("verse", "pre", "chorus", "bridge", "hook", "aside", "refrain", "tag", "breakdown", "lift", "shout", "refrain")}   # Q7 A: narrative
def norm(t): return " ".join(re.sub(r"[^a-z0-9' ]", " ", t.lower().replace("\u2019", "'")).split())
def score(line, role="verse", mate=None, need_rhyme=None, kernel=None, nslots=12, par_mate=None, prospective=False,
          allow_party=False, couplet=None, before_turn=False, cap=10):
    assert role in _I.ROLES, f"v48 2.2: slot has no valid role ({role})"
    DIAL, DLIM, RARE, RHYME_FLOOR = REG[role]
    low = " ".join(words(line))
    if not allow_party:
        ban = [b for b in Q9_BAN if re.search(r"\b" + re.escape(b) + r"\b", low)]
        if ban: return {"line": line, "dead": f"Q9: never-say word ('{ban[0]}')"}
    try:
        syl, best = place(line, nslots)
    except KeyError as e:
        return {"line": line, "dead": f"lexicon: unknown word {e}"}
    if best is None: return {"line": line, "dead": f"too dense: {len(syl)} syllables in its span ({METER})"}
    if nslots in (12, 16) and len(syl) > cap: return {"line": line, "dead": f"span: {len(syl)} syllables > {cap} in two bars at dotted-q = 54 (v58 span: 4.4 s x 2.1)"}
    sc, pk, sl, on_strong, antic = best
    bad = [x[0] for s, x in on_strong if not x[2] and not x[3]]
    if bad: return {"line": line, "dead": f"unstressed content syllable on a strong beat ({bad[0]})"}
    n_on = len(on_strong)
    agree = (sum(1 for s, x in on_strong if x[2]) + 0.5 * antic) / max(1, n_on + antic)
    if agree < 0.5: return {"line": line, "dead": f"strong-beat agreement {agree:.2f} < 0.5"}
    ws = words(line); content = [w for w in ws if w not in FUNCTION]
    distinct = sorted({w for w in content if zipf(w) < 4.5 and not exempt(w)})   # v59 fix 1
    if len(distinct) > DLIM: return {"line": line, "dead": f"{len(distinct)} distinctive words {distinct} (limit {DLIM})"}
    arch = [w for w in content if lemma_zipf(w) < RARE and w not in NAMES and w not in COMPOUND_HALVES and not exempt(w) and not any(c.startswith(w + ' =') for c in COMPOUND_LOG)]   # v43: compounds exempt from the word filters
    if arch: return {"line": line, "dead": f"rare word '{arch[0]}' (lemma Zipf {lemma_zipf(arch[0]):.2f} < {RARE})"}
    stock = [s for s in STOCK if re.search(r"\b" + re.escape(s) + r"\b", low)]
    if stock and role in ("hook", "chorus", "refrain"): return {"line": line, "dead": f"cliché in a hook line ('{stock[0]}')"}
    cs = [conc(w) for w in content]; cs = [c for c in cs if c is not None]
    writer = any(w in _I.WRITER_PHRASES for w in ws)
    objs = any(w in NAMES or forms_in(w, PICT) for w in ws)   # v58 Rule V1: an object of the intake or a name counts
    pic = lambda l: any(w in NAMES or forms_in(w, PICT) for w in words(l)) or any((conc(w) or 0) >= 4.0 for w in words(l) if w not in FUNCTION)
    coup = bool(couplet) and pic(couplet)          # v59 fix 4: read on the couplet -- a picture in the mate line satisfies it
    if role in ("verse", "verse_b") and not writer and not objs and not before_turn and not coup and not any(c >= 4.0 for c in cs):
        return {"line": line, "dead": "Rule V1: no concrete image (no content word ≥ 4.0 on Brysbaert)"}
    has_act = act(line)
    pass  # v43: the act is a bonus only
    # Rule V4 off for Narrative (v43 accounting rule)
    if kernel and norm(kernel) not in norm(line): return {"line": line, "dead": f"kernel '{norm(kernel)}' dropped"}
    last = ws[-1]
    stressed_mono = len(syllables(last)) == 1
    AUXEND = {"do", "does", "did", "is", "was", "are", "were", "has", "have", "had", "can", "could", "will", "would"}
    if last in DEM or (last == "to" and len(ws) > 1 and ws[-2] in TO_VERBS): pass   # F-b, F-d
    elif last in AUXEND: pass                     # v52 (Table K): an auxiliary standing for its verb is an ending ('what hands do')
    elif last in WEAK_END and not syllables(line)[-1][2] and not (need_rhyme and stressed_mono) and last not in ("up", "out", "down", "on", "in", "off", "here", "there", "now", "again", "home") \
            and not prospective:
        return {"line": line, "dead": f"weak ending ('{last}')"}   # song 27 port: a line-final word the stress rules stress is not a weak ending
    rk = None
    if need_rhyme and mate:
        if last == mate.lower(): return {"line": line, "dead": f"identical rhyme ('{last}' on '{mate}')"}   # v53 certificate
        rk = rhyme_kind(last, mate)
        if rk < need_rhyme: return {"line": line, "dead": f"rhyme with '{mate}' {rk} < {need_rhyme}"}
        rf = RHYME_FLOOR
        if zipf(last) < rf and not exempt(last): return {"line": line, "dead": f"rhyme word '{last}' Zipf {zipf(last):.2f} < {rf}"}
    # ---- ranking, 28.4 weights ----
    fam = sum(zipf(w) for w in ws) / len(ws); famn = max(0, min(1, (fam - 3.0) / 3.5))
    shape = 1.0 if len(distinct) == 1 else 0.6
    if role in ("chorus", "hook", "refrain"):
        address = 1.0 if any(w in POLE_A for w in ws) else 0.5          # third-person story: the chorus holds an object
    else:
        address = 1.0 if any(w in POLE_A for w in ws) else 0.0
    rhyme = (rk if rk is not None else 0.5) * (0.5 if agree < 0.75 else 1.0)
    held = syl[-1]
    vowels = 0.6 * (held[1] not in ("AH0", "IH0", "ER0")) + 0.4 * (re.sub(r"\d", "", held[1]) in OPEN)
    lc = conc(last)
    endw = 1.0 if (lc and lc >= 4.0 and last not in FUNCTION) else (0.7 if last in ("you", "me", "i") else 0.6)
    ending = endw * max(0.5, min(1, zipf(last) / 5.5))
    concs = sum(1 for c in cs if c >= 4.0) / max(1, len(cs)); abss = sum(1 for c in cs if c <= 2.0) / max(1, len(cs))
    ngen = sum(1 for w in ws if w in GENERAL)
    ladder = any(c >= 4.0 for c in cs) and any(c <= 2.5 for w, c in zip([w for w in content if conc(w) is not None], cs)
                                               if w not in FUNCTION)
    imagery = max(0, min(1, 0.4 + (0.4 if ladder else 0.0) + 0.3 * (concs - abss) * DIAL - 0.15 * max(0, ngen - 1)))
    innovation = 0.3 if stock else 0.6
    par = parallel(line, par_mate)
    n = len(syl)
    binding = 0.5 * (1.0 if sound_inside(line) else 0.0) + 0.5 * (1.0 if has_act else 0.0)
    comp = (0.20 * agree + 0.10 * binding + 0.15 * shape + 0.075 * famn + 0.10 * address + 0.10 * rhyme + 0.05 * vowels +
            0.10 * ending + 0.05 * imagery + 0.025 * innovation + 0.05 * par)        # v43: binding 0.10, from fam and innovation
    return {"line": line, "dead": None, "composite": round(comp, 3), "align": round(agree, 2), "nsyl": n,
            "pickup": pk, "slots": sl, "v1": ("couplet" if (role in ("verse", "verse_b") and not objs and not any(c >= 4.0 for c in cs) and couplet) else ""), "distinct": distinct, "rhyme": rk, "imagery": round(imagery, 2), "end": last, "ladder": ladder, "act": has_act, "sound": sound_inside(line)}

# ---- v42 (Window 59): the concrete act and sound inside the line ----
import spacy
_NLP = spacy.load("en_core_web_sm")
RARE = 2.75
RHYME_FLOOR = 4.0
NAMES = set(); COMPOUND_HALVES = set()
def lemma_zipf(w):
    lem = _NLP(w)[0].lemma_.lower()
    return max(zipf(w), zipf(lem))
from lyricsearch import phones
def act(line):
    doc = _NLP(line.replace("’", "'"))
    noun = any(t.pos_ in ("NOUN", "PROPN") and (conc(t.lemma_.lower()) or conc(t.text.lower()) or 0) >= 4.0 for t in doc)
    verb = any(t.pos_ == "VERB" and (conc(t.lemma_.lower()) or 0) >= 3.0 for t in doc)
    return noun and verb
def sound_inside(line):
    cw = [w for w in words(line) if w not in FUNCTION and len(w) > 2]
    init, vow = [], []
    for w in cw:
        try: p = phones(w).split()
        except Exception: continue
        init.append(p[0] if not re.search(r"\d", p[0]) else None)
        st = [x for x in p if x.endswith("1")]
        vow.append(re.sub(r"\d", "", st[0]) if st else None)
    return any(a and init.count(a) > 1 for a in init) or any(v and vow.count(v) > 1 for v in vow)


# ---- meter-general placement (run's port) ----
METER = "4/4"
BAR = {"5/4": 10, "4/4s": 16, "4/4": 8, "7/8": 7, "6/8": 6, "12/8": 12, "3/4": 6}
BEATS = {"5/4": [0, 2, 4, 6, 8], "4/4s": [0, 2, 4, 6, 8, 10, 12, 14], "4/4": [0, 2, 4, 6], "7/8": [0, 2, 4], "6/8": [0, 3], "12/8": [0, 3, 6, 9], "3/4": [0, 2, 4]}
STRONGB = {"5/4": [0, 6], "4/4s": [0, 8], "4/4": [0, 4], "7/8": [0, 2, 4], "6/8": [0, 3], "12/8": [0, 3, 6, 9], "3/4": [0]}
def grid(meter, nslots):
    bar = BAR[meter]; nb = -(-nslots // bar) + 4
    beats = {b * bar + x for b in range(-1, nb) for x in BEATS[meter]}
    strong = {b * bar + x for b in range(0, nb) for x in STRONGB[meter]}
    return beats, strong
def walk_m(syl, pickup, stretch, beats):
    slots = []; pos = -pickup; prev_st = True
    for i, (w, v, st, fn) in enumerate(syl):
        if st and pos not in beats and not prev_st:
            nxt = min(b for b in beats if b > pos); pos = nxt
        slots.append(pos)
        pos += 2 if (st and stretch and i < len(syl) - 1 and pos in beats and (pos + 2) not in beats or False) else 1
        prev_st = st
    return slots
def place(line, nslots=16):
    syl = syllables(line)
    beats, STRONG = grid(METER, nslots)
    best = None
    for pk in range(0, 4):
        for stretch in (True, False):
            sl = walk_m(syl, pk, stretch, beats)
            if sl[-1] > nslots - 1: continue
            on_strong = [(s, x) for s, x in zip(sl, syl) if s in STRONG]
            if any(not x[2] and not x[3] for s, x in on_strong): continue          # a placement that puts an unstressed content syllable on a beat is not the walk's best
            hits = sum(1 for s, x in on_strong if x[2])
            antic = sum(1 for s, x in zip(sl, syl) if x[2] and (s + 1) in STRONG and (s + 1) not in sl)
            sc = hits + 0.5 * antic + (0.1 if stretch else 0)
            if best is None or sc > best[0]: best = (sc, pk, sl, on_strong, antic)
    return syl, best

# ---- run's stress patches (song 13), each a v55 finding ----
#  F-a  'no one' is a compound pronoun stressed on its first half (NO one); the lexicon tags both halves function words.
#  F-b  a line-final demonstrative standing alone ('more than THIS') is stressed and is not a weak ending; v54 fix 4
#       promoted it only inside a phrase with no stress at all.
#  F-c  the pronoun after 'neither/so + aux' is contrastive and takes the stress ('and neither do I').
#  F-d  'to' standing for its infinitive after a verb ('it doesn't need to', 'you need me to') is the same ellipsis as
#       v52's auxiliary ending ('what hands do') and is not a weak ending.
DEM = {"this", "that", "these", "those"}
TO_VERBS = {"need", "have", "want", "like", "got", "used", "ought", "going", "me", "you", "him", "her", "us", "them"}
import lyricsearch as _lsx
def _patch_syl(fn):
    def syl(line):
        out = fn(line); ws = [x[0] for x in out]
        res = []
        for i, (w, v, st, f) in enumerate(out):
            if w == "no" and i + 1 < len(ws) and ws[i + 1] == "one": st = True
            if i == len(out) - 1 and w in DEM: st = True
            if i == len(out) - 1 and w == "do" and i >= 1 and ws[i - 1] == "make": st = True   # the run's rule (song 21): 'make DO' -- a phrasal verb's last word takes the phrase stress at the line's end
            if i == len(out) - 1 and w in ("i", "you", "we", "he", "she") and i >= 2 and ws[i - 2] in ("neither", "so", "nor"): st = True
            res.append((w, v, st, f))
        return res
    return syl
COMPOUND_LOG = []
def _compound(fn):
    """v63 Table H: a closed compound whose two parts the lexicon knows (>= 3 letters each, neither a function word) is known:
    the parts' phones in order, the first's stress primary, the second's demoted to secondary; the longest known first part wins."""
    def ph(w):
        try: return fn(w)
        except KeyError:
            for k in range(len(w) - 3, 2, -1):
                a, b = w[:k], w[k:]
                if a in FUNCTION or b in FUNCTION: continue
                try: pa, pb = fn(a), fn(b)
                except KeyError: continue
                COMPOUND_LOG.append(f"{w} = {a} + {b}")
                return pa + " " + pb.replace("1", "2")
            raise
    return ph
def install_patches():
    global syllables
    _lsx.phones = _compound(_lsx.phones)
    import phrasestress48 as _ps
    syllables = _patch_syl(_lsx.syllables)
    _lsx.syllables = syllables

LOG = []
MOVES = ["object", "number", "time", "question", "understatement", "body", "list", "you", "contradiction", "swap", "proverb", "plain"]
def run(name, cands, show=5, **kw):
    raw = [c.strip() for c in cands.strip().splitlines() if c.strip()]
    movemap = {}
    cands = []
    for c in raw:
        if ":" in c and c.split(":")[0].strip() in MOVES:
            mv, c = c.split(":", 1); c = c.strip(); movemap[c] = mv.strip()
        cands.append(c)
    res = [score(c, **kw) for c in cands]
    alive = sorted([r for r in res if not r["dead"]], key=lambda r: -r["composite"])
    dead = [r for r in res if r["dead"]]
    fp = hashlib.sha1(json.dumps([r["line"] for r in alive]).encode()).hexdigest()[:10]
    print(f"\n== {name}: {len(cands)} written, {len(alive)} survive [frozen {fp}]")
    for i, r in enumerate(alive[:show], 1):
        print(f"  {i}. {r['composite']:.3f}  [{movemap.get(r['line'], '-')}] {r['line']}  ({r['nsyl']} syl, align {r['align']}{' LADDER' if r['ladder'] else ''}{' ACT' if r['act'] else ''}{' SOUND' if r['sound'] else ''}, rhyme {r['rhyme']})")
    why = {}
    for r in dead: why.setdefault(r["dead"].split("(")[0].split(":")[0].strip(), []).append(r["line"])
    print("     deaths: " + "; ".join(f"{k} {len(v)}" for k, v in why.items()))
    LOG.append({"slot": name, "written": len(cands), "alive": [r["line"] for r in alive], "fp": fp, "moves": movemap,
                "scores": {r["line"]: r["composite"] for r in alive},
                "dead": [(r["line"], r["dead"]) for r in dead]})
    return alive

def save(path):
    json.dump(LOG, open(path, "w"), indent=1)
