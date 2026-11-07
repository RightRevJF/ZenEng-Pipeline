"""Module 28 lyric search for a 4/4 pop line, with the rhythm each line implies (Module 29.4).
Template: a line spans 2 bars of 4/4 = 16 eighth slots; strong slots = beats 1 and 3 (0, 4, 8, 12).
The walk: eighths throughout; a stressed syllable that would land off the beat right after an
unstressed one takes the beat instead; pickups of 0-3 eighths are tried; the placement with the most
stressed syllables on strong beats wins. Then Table H's filters and the 28.4 ranking."""
import sys, re, json, hashlib
sys.path.insert(0, "/home/claude/carol")
from lyricsearch import syllables, words, zipf, rhyme_kind, FUNCTION, WEAK_END, CONCRETE, phones, OVERRIDE
OVERRIDE.update({"tonight": ["T AH0 N AY1 T"], "wristband": ["R IH1 S T B AE2 N D"], "gonna": ["G AA1 N AH0"],
                 "y'all": ["Y AO1 L"], "ooh": ["UW1"], "oh": ["OW1"], "hey": ["HH EY1"], "doorman": ["D AO1 R M AE2 N"],
                 "subwoofer": ["S AH1 B W UH2 F ER0"], "group": ["G R UW1 P"], "playlist": ["P L EY1 L IH2 S T"],
                 "selfie": ["S EH1 L F IY0"], "rideshare": ["R AY1 D SH EH2 R"], "streetlights": ["S T R IY1 T L AY2 T S"]})
STRONG = {0, 4, 8, 12}
# CMU spells the sung "-ear" vowel two ways (near N IH1 R, here HH IY1 R); in singing they are one rhyme.
import lyricsearch as _ls, pronouncing as _pr
_rp = _pr.rhyming_part
_pr.rhyming_part = lambda p: re.sub(r"\bIH(\d) R\b", r"IY\1 R", _rp(p))
OPEN = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "OW", "OY"}
STOCK = ["tonight's gonna be", "good night", "paint the town", "live it up", "fill up my cup", "raise your glass",
         "hands up in the air", "put your hands up", "like there's no tomorrow", "dance the night away",
         "all night long", "turn it up", "let's get it started", "the night is young", "just begun",
         "on the dance floor", "party rock", "feel the beat", "up all night", "light it up", "we found love"]

def walk(syl, pickup):
    slots = []; pos = -pickup; prev_st = True
    for w, v, st, fn in syl:
        if st and pos % 2 == 1 and not prev_st: pos += 1
        slots.append(pos); pos += 1; prev_st = st
    return slots

def place(line, nslots=16):
    syl = syllables(line)
    best = None
    for pk in range(0, 4):
        sl = walk(syl, pk)
        if sl[-1] > nslots - 1: continue
        on_strong = [(s, x) for s, x in zip(sl, syl) if s in STRONG]
        hits = sum(1 for s, x in on_strong if x[2])
        antic = sum(1 for s, x in zip(sl, syl) if x[2] and (s + 1) in STRONG and (s + 1) not in sl)
        sc = hits + 0.5 * antic
        if best is None or sc > best[0]: best = (sc, pk, sl, on_strong, antic)
    return syl, best

def score(line, role="verse", mate=None, need_rhyme=None, kernel=None, nslots=16):
    try:
        syl, best = place(line, nslots)
    except KeyError as e:
        return {"line": line, "dead": f"lexicon: unknown word {e}"}
    if best is None:
        return {"line": line, "dead": f"too dense: {len(syl)} syllables will not fit two bars"}
    sc, pk, sl, on_strong, antic = best
    bad = [x[0] for s, x in on_strong if not x[2] and not x[3]]
    if bad: return {"line": line, "dead": f"unstressed content syllable on a strong beat ({bad[0]})"}
    n_on = len(on_strong)
    agree = ((sum(1 for s, x in on_strong if x[2]) + 0.5 * antic) / max(1, n_on + antic)) if n_on + antic else 0
    if agree < 0.5: return {"line": line, "dead": f"strong-beat agreement {agree:.2f} < 0.5"}
    # peak note proxy: the first stressed syllable that is not a reduced vowel (27.4); reduced vowel there kills
    ws = words(line); content = [w for w in ws if w not in FUNCTION]
    distinct = sorted({w for w in content if zipf(w) < 4.5})
    if len(distinct) > (1 if role != "verse" else 2):     # verses carry a concrete flash or two (Window 27)
        return {"line": line, "dead": f"{len(distinct)} distinctive words {distinct}"}
    arch = [w for w in content if zipf(w) < 3.0]
    if arch: return {"line": line, "dead": f"rare word {arch[0]} (Zipf {zipf(arch[0]):.2f})"}
    low = " ".join(ws)
    stock = [s for s in STOCK if s in low]
    if stock and role in ("hook", "chorus"): return {"line": line, "dead": f"cliché in a hook line ('{stock[0]}')"}
    if stock: return {"line": line, "dead": f"stock phrase from a famous party song ('{stock[0]}')"}
    if kernel and kernel not in low: return {"line": line, "dead": f"kernel '{kernel}' dropped"}
    last = ws[-1]
    if last in WEAK_END and last not in ("up", "out", "down", "on", "in", "off"):   # particles of phrasal verbs end lines
        return {"line": line, "dead": f"weak ending ({last})"}
    rk = None
    if need_rhyme and mate:
        rk = rhyme_kind(last, mate)
        if rk < need_rhyme: return {"line": line, "dead": f"rhyme with '{mate}' {rk} < {need_rhyme}"}
        if zipf(last) < 4.5: return {"line": line, "dead": f"rhyme word {last} too rare"}
    # ranking (28.4 weights)
    fam = sum(zipf(w) for w in ws) / len(ws); famn = max(0, min(1, (fam - 3.0) / 3.5))
    shape = 1.0 if len(distinct) == 1 else (0.7 if len(distinct) == 2 else 0.5)
    if role in ("chorus", "hook"):
        address = 1.0 if re.search(r"\b(you|your|we|us|our|y'all)\b", low) else 0.0
    else:
        address = 1.0 if any(w in CONCRETE or w in {"chat", "chain", "shoes", "stamp", "car", "mirror", "wristband",
                                                 "streetlights", "line", "block", "door", "doors", "floor", "phone", "phones"} for w in ws) else 0.0
    rhyme = (rk if rk is not None else 0.5) * (0.5 if agree < 0.75 else 1.0)
    held = syl[-1]
    vowels = 0.6 * (held[1] not in ("AH0", "IH0", "ER0")) + 0.4 * (re.sub(r"\d", "", held[1]) in OPEN)
    endw = 1.0 if last in CONCRETE else (0.7 if last in ("you", "me", "i", "us", "up") else 0.6)
    ending = endw * max(0.5, min(1, zipf(last) / 5.5))
    gen = sum(1 for w in ws if w in ("all", "never", "always", "forever", "every", "everybody", "nobody"))
    general = min(1.0, 0.5 + 0.25 * gen)               # Window 34: generalization words are a pop hit marker
    comp = (0.25 * agree + 0.15 * shape + 0.10 * famn + 0.10 * address + 0.10 * rhyme + 0.05 * vowels +
            0.10 * ending + 0.05 * general + 0.10 * (1.0 if len(syl) <= (8 if role != "verse" else 11) else 0.6))
    return {"line": line, "dead": None, "composite": round(comp, 3), "align": round(agree, 2), "nsyl": len(syl),
            "pickup": pk, "slots": sl, "fam": round(fam, 2), "distinct": distinct, "rhyme": rk}

def run(name, cands, role="verse", mate=None, need_rhyme=None, kernel=None, show=4, nslots=16):
    cands = [c.strip() for c in cands.strip().splitlines() if c.strip()]
    res = [score(c, role, mate, need_rhyme, kernel, nslots) for c in cands]
    alive = sorted([r for r in res if not r["dead"]], key=lambda r: -r["composite"])
    dead = [r for r in res if r["dead"]]
    fp = hashlib.sha1(json.dumps([r["line"] for r in alive]).encode()).hexdigest()[:10]
    print(f"\n== {name}: {len(cands)} written, {len(alive)} survive [{fp}]")
    for i, r in enumerate(alive[:show], 1):
        print(f"  {i}. {r['composite']:.3f} {r['line']}  (align {r['align']}, {r['nsyl']} syl, pickup {r['pickup']}, rare {r['distinct']}, rhyme {r['rhyme']})")
    for r in dead: print(f"     x {r['line']} -- {r['dead']}")
    return alive
