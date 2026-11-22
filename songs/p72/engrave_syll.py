"""Song 62: the sung syllable under each note (shared by the engraving and the MusicXML): a word's notes take its syllables (pyphen, with a list of
corrections); a note with no word continues the syllable before (a melisma)."""
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
        j = i
        while j < len(mel) and mel[j]["text"] == w and (j == i or mel[j]["line"] == mel[i]["line"]): j += 1
        ss = syll(w, j - i)
        for x, s_ in enumerate(ss): out.append(s_ + ("-" if x < len(ss) - 1 else ""))
        i = j
    return out
