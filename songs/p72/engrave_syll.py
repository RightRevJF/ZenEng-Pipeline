"""Song 62: the sung syllable under each note (shared by the engraving and the MusicXML): a word's notes take its syllables (pyphen, with a list of
corrections); a note with no word continues the syllable before (a melisma), also inside a word."""
import re, pyphen
H = pyphen.Pyphen(lang="en_US")
OVR = {w_.replace("-", ""): w_.split("-") for w_ in "a-cross ev-ery re-mem-bered morn-ing morn-ings sat-ur-day fa-ther out-grew noth-ing coun-ter de-cem-ber cof-fee doc-tor mid-night on-ly ser-mon door-way nod-ded clos-et to-mor-row to-mor-row's him-self moth-er moth-er's wid-ow thir-ty de-cide be-fore o-pen go-ing to-day sun-day want-ed did-n't af-ter".split()}
def syll(word, k):
    w = re.sub(r"[^A-Za-z']", "", word); p = list(OVR[w.lower()]) if w.lower() in OVR else (H.inserted(w).split("-") if w else [w])
    while len(p) > k: p[-2:] = [p[-2] + p[-1]]
    while len(p) < k: i_ = max(range(len(p)), key=lambda j: len(p[j])); s_ = p[i_]; c_ = max(1, len(s_) // 2); p[i_:i_ + 1] = [s_[:c_], s_[c_:] or s_[-1:]]
    return p
def syllables(mel):
    out = []; i = 0
    while i < len(mel):
        w = mel[i]["text"]
        if not w: out.append(None); i += 1; continue
        j = i; idx = []
        while j < len(mel) and (mel[j]["text"] == w or (mel[j]["text"] == "" and any(m_["text"] == w and m_["line"] == mel[i]["line"] for m_ in mel[j + 1:j + 3]))) and mel[j]["line"] == mel[i]["line"]:
            idx.append(j); j += 1
        k = sum(1 for x_ in idx if mel[x_]["text"]); ss = iter(syll(w, k)); c_ = 0
        for x_ in idx:
            if not mel[x_]["text"]: out.append(None); continue
            s_ = next(ss); c_ += 1; out.append(s_ + ("-" if c_ < k else ""))
        i = j
    return out
