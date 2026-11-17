"""All vocal parts of a MusicXML score, aligned in time: for each part with lyrics, voice 1, its notes with absolute onset (quarters
from the start, bar starts taken from the first part), length (ties merged), pitch, whether a syllable starts there, the part's name,
and the bar and position. Reads .mxl or .musicxml (PDMX, OpenEWLD, the engine's own scores)."""
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "words"))
from mxl_words import load_xml, strip_ns, STEP
def parts_of(path):
    root = strip_ns(load_xml(path))
    names = {}
    for sp in root.iter("score-part"):
        n = sp.find("part-name"); names[sp.get("id")] = (n.text or "").strip() if n is not None and n.text else ""
    parts = root.findall("part")
    if not parts: return []
    # bar starts from the first part
    starts = []; t = 0.0; div = 1; beats, btype = 4, 4
    for meas in parts[0].findall("measure"):
        starts.append(t); pos = 0; mlen = 0
        for el in meas:
            if el.tag == "attributes":
                d = el.find("divisions")
                if d is not None: div = int(float(d.text))
                tm = el.find("time")
                if tm is not None and tm.find("beats") is not None:
                    try: beats, btype = int(tm.find("beats").text), int(tm.find("beat-type").text)
                    except ValueError: pass
            elif el.tag == "backup": pos -= int(float(el.find("duration").text))
            elif el.tag == "forward": pos += int(float(el.find("duration").text)); mlen = max(mlen, pos)
            elif el.tag == "note" and el.find("chord") is None and el.find("grace") is None:
                d = el.find("duration"); pos += int(float(d.text)) if d is not None else 0; mlen = max(mlen, pos)
        t += (mlen / div) if mlen else beats * 4 / btype
    out = []
    for part in parts:
        div = 1; beats, btype = 4, 4; notes = []; nly = 0
        for mi, meas in enumerate(part.findall("measure")):
            if mi >= len(starts): break
            pos = 0
            for el in meas:
                if el.tag == "attributes":
                    d = el.find("divisions")
                    if d is not None: div = int(float(d.text))
                    tm = el.find("time")
                    if tm is not None and tm.find("beats") is not None:
                        try: beats, btype = int(tm.find("beats").text), int(tm.find("beat-type").text)
                        except ValueError: pass
                elif el.tag == "backup": pos -= int(float(el.find("duration").text))
                elif el.tag == "forward": pos += int(float(el.find("duration").text))
                elif el.tag == "note":
                    if el.find("grace") is not None or el.find("chord") is not None: continue
                    d = el.find("duration"); dur = int(float(d.text)) if d is not None else 0
                    v = el.find("voice"); v = v.text if v is not None else "1"
                    st = pos; pos += dur
                    if v != "1" or el.find("rest") is not None: continue
                    p = el.find("pitch")
                    if p is None: continue
                    midi = 12 * (int(p.find("octave").text) + 1) + STEP[p.find("step").text] + int(float(p.find("alter").text if p.find("alter") is not None else 0))
                    ties = [x.get("type") for x in el.findall("tie")]
                    ly = el.find("lyric"); has = ly is not None and ly.find("text") is not None and (ly.find("text").text or "").strip() != ""
                    nly += has
                    on = starts[mi] + st / div
                    if "stop" in ties and notes and notes[-1]["p"] == midi and abs(notes[-1]["on"] + notes[-1]["q"] - on) < 1e-6 and not has:
                        notes[-1]["q"] += dur / div; continue
                    notes.append(dict(on=round(on, 4), q=dur / div, p=midi, syl=has, bar=mi + 1, pos=round(st / div, 4), meter=[beats, btype]))
        out.append(dict(name=names.get(part.get("id"), ""), notes=notes, n_lyrics=nly))
    return out
if __name__ == "__main__":
    for p in parts_of(sys.argv[1]): print(p["name"], len(p["notes"]), p["n_lyrics"], [(n["on"], n["p"]) for n in p["notes"][:6]])
