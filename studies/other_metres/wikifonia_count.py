import sys, glob, zipfile, collections, json
from multiprocessing import Pool
def one(path):
    from lxml import etree
    try:
        z = zipfile.ZipFile(path); root = etree.fromstring(z.read([n for n in z.namelist() if n.endswith(".xml") and not n.startswith("META")][0])); parts = root.findall("part"); part = max(parts, key=lambda q: len(q.findall(".//lyric")))
    except Exception: return None
    ts = None; bars = collections.Counter(); notes = 0; ly = 0
    for m in part.findall("measure"):
        tm = m.find("attributes/time")
        if tm is not None and tm.find("beats") is not None:
            try: ts = f"{int(tm.find('beats').text)}/{int(tm.find('beat-type').text)}"
            except ValueError: pass
        bars[ts] += 1
        for el in m.findall("note"):
            if el.find("rest") is None and el.find("grace") is None and el.find("chord") is None: notes += 1; ly += el.find("lyric") is not None
    if not bars: return None
    return (bars.most_common(1)[0][0], notes, ly, len(root.findall(".//harmony")))
if __name__ == "__main__":
    fs = sorted(glob.glob(sys.argv[1] + "/*.mxl")); R = [r for r in Pool(2).map(one, fs, chunksize=50) if r]; out = {}
    for m in sorted(set(r[0] for r in R if r[0]), key=lambda m: -sum(r[0] == m for r in R)):
        v = [r for r in R if r[0] == m]; out[m] = dict(lead_sheets=len(v), with_60_notes=sum(r[1] >= 60 for r in v), with_60_notes_and_words=sum(r[1] >= 60 and r[2] >= 0.5 * r[1] for r in v), and_chords=sum(r[1] >= 60 and r[2] >= 0.5 * r[1] and r[3] >= 8 for r in v))
    print(len(fs), len(R)); print(json.dumps(out, indent=0)); json.dump(dict(files=len(fs), read=len(R), by_main_metre=out), open(sys.argv[2], "w"), indent=1)
