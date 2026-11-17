"""Sung syllables from MusicXML scores with lyrics attached to notes (PDMX on Zenodo, CC BY 4.0; OpenEWLD on GitHub, public-domain lead
sheets): for the first part that carries lyrics, voice 1, every sung note with its first-verse syllable, bar, position in the bar
(quarters; a short first bar is treated as a pickup and right-aligned), length (ties merged), pitch, and the time signature.
Output matches parse_words.py's note dicts, so words_test.annotate and the measures there can read it."""
import zipfile, re, io
import xml.etree.ElementTree as ET
STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def load_xml(path):
    if path.endswith(".mxl"):
        z = zipfile.ZipFile(path)
        name = None
        try:
            c = ET.fromstring(z.read("META-INF/container.xml"))
            rf = c.find(".//rootfile"); name = rf.get("full-path") if rf is not None else None
        except (KeyError, ET.ParseError): pass
        if not name or name not in z.namelist(): name = next(n for n in z.namelist() if n.endswith((".xml", ".musicxml")) and not n.startswith("META-INF"))
        return ET.fromstring(z.read(name))
    return ET.parse(path).getroot()
def strip_ns(root):
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag: el.tag = el.tag.split("}", 1)[1]
    return root
def part_notes(part):
    out = []; div = 1; beats, btype = 4, 4; first = True
    for mi, meas in enumerate(part.findall("measure")):
        pos = 0; notes = []; mlen = 0
        for el in meas:
            if el.tag == "attributes":
                d = el.find("divisions")
                if d is not None: div = int(float(d.text))
                t = el.find("time")
                if t is not None and t.find("beats") is not None:
                    try: beats, btype = int(t.find("beats").text), int(t.find("beat-type").text)
                    except ValueError: pass
            elif el.tag == "backup":
                pos -= int(float(el.find("duration").text))
            elif el.tag == "forward":
                pos += int(float(el.find("duration").text))
            elif el.tag == "note":
                if el.find("grace") is not None or el.find("cue") is not None: continue
                dur = el.find("duration"); dur = int(float(dur.text)) if dur is not None else 0
                voice = el.find("voice"); voice = voice.text if voice is not None else "1"
                chord = el.find("chord") is not None
                if chord: continue
                start = pos; pos += dur; mlen = max(mlen, pos)
                if voice != "1" or el.find("rest") is not None: continue
                p = el.find("pitch")
                if p is None: continue
                midi = 12 * (int(p.find("octave").text) + 1) + STEP[p.find("step").text] + int(float(p.find("alter").text if p.find("alter") is not None else 0))
                ties = [t.get("type") for t in el.findall("tie")]
                ly = None
                for l in el.findall("lyric"):
                    if l.get("number", "1") in ("1", "part1verse1") or ly is None:
                        tx = l.find("text"); sy = l.find("syllabic")
                        if tx is not None and tx.text:
                            ly = (tx.text, sy.text if sy is not None else "single")
                        if l.get("number", "1") == "1": break
                notes.append(dict(start=start / div, q=dur / div, p=midi, ly=ly, tie_stop="stop" in ties))
        bar_q = beats * 4 / btype
        shift = bar_q - mlen / div if (first and mlen / div < bar_q - 1e-6) else 0.0
        first = False
        for n in notes:
            n.update(bar=mi + 1, pos=round(n["start"] + shift, 4), meter=[beats, btype])
            out.append(n)
    return out
def song_notes(path):
    root = strip_ns(load_xml(path))
    for part in root.findall("part"):
        ns = part_notes(part)
        if sum(1 for n in ns if n["ly"]) >= 20: break
    else: return []
    res = []
    for n in ns:
        if n["tie_stop"] and res and not n["ly"]: res[-1]["q"] += n["q"]; continue
        if not n["ly"]:
            if res: res[-1]["melisma"] = res[-1].get("melisma", 1) + 1; res[-1]["q"] += n["q"]
            continue
        tx, sy = n["ly"]; tx = tx.strip()
        if not re.search(r"[A-Za-z]", tx): continue
        syl = ("-" if sy in ("middle", "end") else "") + tx + ("-" if sy in ("begin", "middle") else "")
        res.append(dict(bar=n["bar"], pos=n["pos"], q=n["q"], p=n["p"], syl=syl, stress=None, meter=n["meter"], label=None, line_start=False, rhyme=None))
    return res
if __name__ == "__main__":
    import sys
    ns = song_notes(sys.argv[1]); print(len(ns)); print([(n["bar"], n["pos"], n["q"], n["p"], n["syl"]) for n in ns[:16]])
