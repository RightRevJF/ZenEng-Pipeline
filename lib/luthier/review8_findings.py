import json, sys, collections, numpy as np
sys.path.insert(0, "/home/claude/zeneng-pipeline/lib/luthier"); import word_weight as WW
def lines_of(R):
    L = collections.OrderedDict()
    for n in sorted(R["melody"]["notes"], key=lambda n: n["on"]): L.setdefault((n["sec"], n["line"]), []).append(n)
    return L
def report(path):
    R = json.load(open(path)); L = lines_of(R); BAR = 48 if R["metre"] == "4/4" else (36 if R["metre"] == "6/8" else 48)
    # 749.58 rests between lines in a section
    rests = []; keys = list(L)
    for a, b in zip(keys, keys[1:]):
        if a[0] != b[0]: continue
        la, lb = L[a], L[b]; rests.append(lb[0]["on"] - (la[-1]["on"] + la[-1]["dur"]))
    # 749.59 melismas on function words; 749.64 weak endings
    mel_fn = mel = 0; weak_long = cand = 0; ex = []
    for k, ns in L.items():
        syl = [n for n in ns if n["text"] != ""]; tr = WW.tier([(n["text"], n["stress"]) for n in syl]); tmap = {id(n): t for n, t in zip(syl, tr)}
        cur = None
        for n in ns:
            if n["text"] != "": cur = n
            elif cur is not None: 
                if not getattr(cur, "_m", False): pass
        # group melismas: a syllable followed by '' notes
        for i, n in enumerate(ns):
            if n["text"] != "" and i + 1 < len(ns) and ns[i + 1]["text"] == "":
                mel += 1; mel_fn += tmap[id(n)] == 0
        # line-final word
        if len(syl) >= 2 and syl[-1]["text"] == syl[-2]["text"] and syl[-2]["stress"] and not syl[-1]["stress"]:
            cand += 1
            def sung(n):  # length incl. melisma continuation
                i = ns.index(n); d = n["dur"]; j = i + 1
                while j < len(ns) and ns[j]["text"] == "": d += ns[j]["dur"]; j += 1
                return d
            a, b = sung(syl[-2]), sung(syl[-1])
            if b > a: weak_long += 1; ex.append((syl[-1]["text"], a, b))
    rests = np.array(rests)
    return dict(rests_median=float(np.median(rests)) if len(rests) else None, rests_exactly_quarter=f"{int((rests == 12).sum())}/{len(rests)}", melismas_on_function_words=f"{mel_fn}/{mel}",
                weak_endings_held_longer=f"{weak_long}/{cand}", examples=ex[:6], rest_share_check=next((v for k, v in R["checks"].items() if k.startswith("rest share")), None),
                sixteenth_share=round(float(np.mean([(b["on"] - a["on"]) == 3 for ns in L.values() for a, b in zip(ns, ns[1:])])), 3),
                deaths=R["melody"]["deaths"], survivors=f'{R["melody"]["survivors"]}/{R["melody"]["made"]}', length_s=next((v for k, v in R["checks"].items() if k.startswith("length")), None),
                judge7_pool=R["judge7"]["pool"] if R.get("judge7") else None, gates=R["judge7"].get("gates_passed") if R.get("judge7") else None,
                words_gate=R["judge7"].get("words_gate") if R.get("judge7") else None, band_kept=R["judge7"].get("in_the_kept_middle_half") if R.get("judge7") else None)
for p in sys.argv[1:]: print(p.split("/")[-1], json.dumps(report(p)))
