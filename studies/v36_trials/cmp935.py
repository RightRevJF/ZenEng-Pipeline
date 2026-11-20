import sys, json, random, importlib.util, collections
sys.path.insert(0, "lib/luthier")
def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ON = load(sys.argv[1], "eng_on"); OFF = load(sys.argv[2] if len(sys.argv) > 2 else "tmp_trial/no935/metre_engine.py", "eng_off")
for tag, p in (("55","songs/p65/lyric55"),("54","songs/p64/lyric54"),("58","songs/p68/lyric58"),("59","songs/p69/lyric59")):
    spec = json.load(open(p + ".song.json"))["spec"]; res = []
    for M in (ON, OFF):
        E = M.Engine(spec); rng = random.Random(4); out = []; d = collections.Counter()
        for _ in range(60):
            c, err = E.build(rng); out.append(None if err else [(n["on"], n["p"]) for n in c["notes"]]); d[err[0] if err else "ok"] += 1
        res.append((out, d))
    same = sum(a == b for a, b in zip(res[0][0], res[1][0])); print(tag, "identical builds", same, "of 60 | on", dict(res[0][1]), "| off", dict(res[1][1]))
