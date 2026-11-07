"""By-hand Module 28 lyric search (ZenEng v39, 27.10 sec. 8 / Table H).

The app's scorer is not reachable from this session, so this file implements
Table H's filters, rejection and ranking with public stand-ins:
  stress and phonemes  -> CMU Pronouncing Dictionary (pronouncing)
  familiarity (Zipf)   -> wordfreq
  concreteness         -> a small hand lexicon (approximation; flagged)
  cliche table         -> not available; a hand list of stock hymn/pop phrases
"""
import re, json, hashlib, sys
import pronouncing
from wordfreq import zipf_frequency

FUNCTION = set("""a an the and or but nor for so yet to of in on at by from with into onto upon
over under through among as than that this these those who whom whose which what when where
how why if then is are was were be been being am do does did have has had will would shall should
can could may might must i me my mine we us our ours you your yours he him his she her hers it its
they them their theirs all no not each every some any one both such own there here now o oh
""".split())
# Hymnody's elisions (Module 11.19) plus sung forms used in this hymn.
OVERRIDE = {
    "our": ["AW1 R"], "hour": ["AW1 R"], "prayer": ["P R EH1 R"], "fire": ["F AY1 R"],
    "every": ["EH1 V R IY0"],                      # ev'ry, as hymnals count it
    "emmanuel": ["EH0 M AE1 N Y UW0 EH2 L"],       # sung with a full final vowel, -EL
    "alleluia": ["AE2 L EH0 L UW1 Y AA0"],
    "mary's": ["M EH1 R IY0 Z"], "gladness": ["G L AE1 D N AH0 S"],
}
REDUCED = {"AH0", "IH0", "ER0", "UH0"}
OPEN = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "OW", "OY"}
CONCRETE = set("""light night manger hand hands mother star stable land road roads door doors bread fish
saw shavings bone bones flesh face child sons daughters wood tree cross nails hill hillside sky earth
field fields shepherds lamb straw breath dark darkness dawn morning sun fire water feet tears blood
table cup stone tomb world house street streets city cradle finger fingers arms skin dust lamp
candle snow winter field hearth roof bell bells song voice mountain sea shore window gate bed
""".split())
CASE = set("""light night manger hand hands mother star stable land road roads door bread flesh bone
face child cross tree wood finger morning dark darkness mary jesus christ lamb world poor dust
""".split())
STOCK = ["set us free", "born to die", "king of kings", "light of the world", "prince of peace",
         "joy to the world", "glory to god", "silent night", "holy night", "go tell it",
         "amazing grace", "love came down", "o come let us", "christ the lord", "with us to dwell",
         "forevermore", "hark the herald", "on the mountain", "our hearts", "fill our hearts"]
WEAK_END = FUNCTION - {"you", "me", "i", "us", "we", "him", "her", "them", "here", "there",
                        "now", "all", "own", "mine", "yours", "ours"}

def words(line):
    return re.findall(r"[a-z']+", line.lower().replace("’", "'"))

def phones(w):
    if w in OVERRIDE: return OVERRIDE[w][0]
    p = pronouncing.phones_for_word(w)
    if not p and w.endswith("'s"): p = pronouncing.phones_for_word(w[:-2])
    if not p: raise KeyError(w)
    return p[0]

def syllables(line):
    """[(word, vowel_phone, stressed, is_function)] one entry per sung syllable."""
    out = []
    for w in words(line):
        vs = [ph for ph in phones(w).split() if ph[-1].isdigit()]
        mono = len(vs) == 1
        for v in vs:
            if mono:
                st = w not in FUNCTION
            else:
                st = v[-1] in "12"
            out.append((w, v, st, w in FUNCTION))
    return out

LITURGICAL = {"mary", "mary's", "jesus", "christ", "emmanuel", "alleluia", "god", "manger",
              "bethlehem", "joseph's", "calvary"}   # carol vocabulary: names, never 'archaic'
def zipf(w):
    if w.endswith("'s") or w.endswith("s'"):
        w = w[:-2] if w.endswith("'s") else w[:-1]
    if w in LITURGICAL:
        return max(zipf_frequency(w, "en"), 3.0)   # proper names: not 'archaic'
    return zipf_frequency(w, "en")

def all_phones(w):
    return OVERRIDE.get(w) or pronouncing.phones_for_word(w) or [phones(w)]

def rhyme_kind(a, b):
    if a == b: return 0.0
    strip = lambda s: re.sub(r"\d", "", s)
    for pa in all_phones(a):
        for pb in all_phones(b):
            if strip(pronouncing.rhyming_part(pa)) == strip(pronouncing.rhyming_part(pb)): return 1.0
    ra = pronouncing.rhyming_part(phones(a)); rb = pronouncing.rhyming_part(phones(b))
    va = strip(ra).split()[0]; vb = strip(rb).split()[0]
    if va == vb and ra.split()[-1][:1] == rb.split()[-1][:1]: return 0.8   # family
    if va == vb: return 0.5                                                 # assonance
    return 0.0

def score_line(line, tmpl, mate=None, role="verse"):
    """tmpl: dict(nsyl, strong=[idx], held=[idx], peak=idx, rhyme='perfect'|'any'|None)."""
    cert = []
    try:
        syl = syllables(line)
    except KeyError as e:
        return {"line": line, "dead": f"lexicon: unknown word {e}"}
    if len(syl) != tmpl["nsyl"]:
        return {"line": line, "dead": f"syllables {len(syl)} != {tmpl['nsyl']}"}
    strong = tmpl["strong"]
    bad = [syl[i][0] for i in strong if not syl[i][2] and not syl[i][3]]
    if bad:
        return {"line": line, "dead": f"unstressed content syllable on strong beat ({bad[0]})"}
    agree = sum(1 for i in strong if syl[i][2]) / len(strong)
    if agree < 0.5:
        return {"line": line, "dead": f"strong-beat agreement {agree:.2f} < 0.5"}
    pk = syl[tmpl["peak"]]
    if pk[1] in REDUCED:
        return {"line": line, "dead": f"reduced vowel on peak ({pk[0]} {pk[1]})"}
    ws = words(line)
    content = [w for w in ws if w not in FUNCTION]
    distinct = [w for w in content if zipf(w) < 4.5]
    if len(set(distinct)) > 1:
        return {"line": line, "dead": f"{len(set(distinct))} distinctive words {sorted(set(distinct))} > 1"}
    arch = [w for w in content if zipf(w) < 3.0]
    if arch:
        return {"line": line, "dead": f"archaic/rare word {arch[0]} (Zipf {zipf(arch[0]):.2f} < 3.0)"}
    low = " ".join(ws)
    stock = [s for s in STOCK if s in low]
    if stock and role == "hook":
        return {"line": line, "dead": f"cliche in hook line ('{stock[0]}')"}
    last = ws[-1]
    if tmpl.get("convergence") and not re.search(r"(AA|AE|AH|AO|AW|AY|EH|OW|OY|IY|UW|EY|ER)\d?( [LR])?$", phones(last)):
        return {"line": line, "dead": f"Rule C2: convergence word '{last}' ends on a closed consonant"}
    predicate_over = last == "over" and len(ws) > 1 and ws[-2] in ("is", "are", "was", "were")
    if last in WEAK_END and not predicate_over:
        return {"line": line, "dead": f"weak line ending ({last})"}
    rk = None
    if tmpl.get("rhyme") and mate:
        rk = rhyme_kind(last, mate)
        need = 1.0 if tmpl["rhyme"] == "perfect" else 0.5
        if rk < need:
            return {"line": line, "dead": f"rhyme with '{mate}' {rk} < {need}"}
        if zipf(last) < 4.5:
            return {"line": line, "dead": f"rhyme word {last} Zipf {zipf(last):.2f} < 4.5"}
    # ---- rank (28.4 weights) ----
    fam = sum(zipf(w) for w in ws) / len(ws)
    famn = max(0, min(1, (fam - 3.0) / 3.5))
    shape = 1.0 if len(set(distinct)) == 1 else 0.5
    if role in ("chorus", "hook"):
        address = 1.0 if re.search(r"\b(to|for|with|before|praise|thank|thanks|bless|adore|love|see|know|follow|serve|worship|hail) you\b", low) else 0.0
    else:
        address = 1.0 if any(w in CASE for w in ws) else 0.0
    rhyme = (rk if rk is not None else 0.5) * (0.5 if agree < 0.75 else 1.0)
    held = [syl[i] for i in tmpl["held"]]
    no_red = 1.0 if not any(h[1] in REDUCED for h in held) else 0.0
    open_share = sum(1 for h in held if re.sub(r"\d", "", h[1]) in OPEN) / len(held)
    vowels = 0.6 * no_red + 0.4 * open_share
    endw = 1.0 if last in CONCRETE else (0.7 if last in ("you", "me", "i") else 0.6)
    ending = endw * max(0.5, min(1, zipf(last) / 5.5))
    conc = sum(1 for w in content if w in CONCRETE) / max(1, len(content))
    gen = sum(1 for w in ws if w in ("all", "never", "always", "forever", "every"))
    imagery = max(0, 0.5 + 0.5 * conc - 0.15 * max(0, gen - 1))
    innovation = 0.3 if stock else 0.6
    par = 0.0
    if mate and tmpl.get("mate_line"):
        m = words(tmpl["mate_line"])
        if m and ws[0] == m[0]: par += 0.4
        if [w for w in ws if w in FUNCTION][:3] == [w for w in m if w in FUNCTION][:3]: par += 0.3
        par += 0.3
    comp = (0.25 * agree + 0.15 * shape + 0.10 * famn + 0.10 * address + 0.10 * rhyme +
            0.05 * vowels + 0.10 * ending + 0.05 * imagery + 0.05 * innovation + 0.05 * par)
    return {"line": line, "dead": None, "composite": round(comp, 3), "align": round(agree, 2),
            "fam": round(fam, 2), "distinct": sorted(set(distinct)), "vowels": round(vowels, 2),
            "open_held": round(open_share, 2), "ending": round(ending, 2), "rhyme": rk,
            "stock": stock}

def T(nsyl, peak, rhyme=None, mate_line=None, convergence=False):
    strong = list(range(0, nsyl, 2))
    return {"nsyl": nsyl, "strong": strong, "held": strong, "peak": peak, "rhyme": rhyme,
            "mate_line": mate_line, "convergence": convergence}

def run(slot, cands, tmpl, mate=None, role="verse", show=5):
    res = [score_line(c, tmpl, mate, role) for c in cands]
    alive = sorted([r for r in res if not r["dead"]], key=lambda r: -r["composite"])
    dead = [r for r in res if r["dead"]]
    fp = hashlib.sha1(json.dumps([r["line"] for r in alive]).encode()).hexdigest()[:10]
    print(f"\n== {slot}: {len(cands)} written, {len(alive)} survive, {len(dead)} die  [fingerprint {fp}]")
    for i, r in enumerate(alive[:show], 1):
        print(f"  {i}. {r['composite']:.3f}  {r['line']}   (align {r['align']}, Zipf {r['fam']}, "
              f"distinct {r['distinct']}, held-open {r['open_held']}, rhyme {r['rhyme']})")
    for r in dead:
        print(f"     x {r['line']}  -- {r['dead']}")
    return alive, dead
