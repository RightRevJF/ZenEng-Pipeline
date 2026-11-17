"""Where the tonic sits in the sung range: BiMMuDa full melodies (381 top-five singles 1950-2022, tonic from metadata) and CoCoPops
Billboard (tonic from the first **kern key tandem), robust range = 5th to 95th percentile of the melody's pitches (note-weighted), the
lowest and highest notes as semitones above the tonic placed just at or below the low end. Writes tonic_in_range.json."""
import csv, glob, json, collections, statistics as st, warnings, re, os, sys
warnings.filterwarnings("ignore")
import pretty_midi
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(n):
    p = PC[n[0]]
    for a in n[1:]: p += 1 if a in "#" else -1 if a in "b" else 0
    return p % 12
def place(ps, ton):
    ps = sorted(ps); lo = ps[int(.05 * (len(ps) - 1))]; hi = ps[int(.95 * (len(ps) - 1))]
    base = lo - ((lo - ton) % 12)            # the tonic at or below the low end
    return lo - base, hi - base, hi - lo, lo, hi
R = collections.defaultdict(list)
meta = {(r["Year"], r["Position"]): r for r in csv.DictReader(open("/home/claude/data/bimmuda/BiMMuDa/metadata/bimmuda_per_song_metadata.csv"))}
for f in glob.glob("/home/claude/data/bimmuda/BiMMuDa/bimmuda_dataset/*/*/*_full.mid"):
    y, pos = f.split("/")[-3], f.split("/")[-2]; m = meta.get((y, pos))
    if not m: continue
    try: ton = pc(m["Tonic 1"].strip()); mid = pretty_midi.PrettyMIDI(f)
    except Exception: continue
    ps = [n.pitch for i in mid.instruments for n in i.notes]
    if len(ps) < 30: continue
    R["BiMMuDa"].append(place(ps, ton))
S = json.load(open("/home/claude/zeneng-pipeline/studies/words/sung_syllables.json"))
for f in glob.glob("/home/claude/data/cocopops/CoCoPops/Billboard/Data/*.hum"):
    k = re.search(r"^\*([A-Ga-g][#-]?):", open(f, errors="replace").read(), re.M)
    key = "BB:" + os.path.basename(f).split(".")[0]
    if not k or key not in S: continue
    t = k.group(1); ton = pc(t[0].upper() + t[1:].replace("-", "b"))
    ps = [n["p"] for n in S[key] if n.get("p") is not None]
    if len(ps) < 30: continue
    R["CoCoPops Billboard"].append(place(ps, ton))
def q(v): v = sorted(v); return [v[int(.25 * (len(v) - 1))], st.median(v), v[int(.75 * (len(v) - 1))]]
out = {}
for k, v in R.items():
    out[k] = dict(songs=len(v), low_above_tonic=q([x[0] for x in v]), high_above_tonic=q([x[1] for x in v]), span=q([x[2] for x in v]),
                  low_dist=dict(collections.Counter(x[0] for x in v).most_common(6)), high_dist=dict(collections.Counter(x[1] for x in v).most_common(6)))
json.dump(out, open("tonic_in_range.json", "w"), indent=1); print(json.dumps(out, indent=1))
