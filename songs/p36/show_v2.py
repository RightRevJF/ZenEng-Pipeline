import pickle, sys
sys.argv=["x","1","main"]; sys.path.insert(0,"/home/claude/p36")
import melody_p36 as M
R = pickle.load(open("/home/claude/p36/melody_v2.pkl","rb")); c = R["pick"]; L2 = R["lines2"]
NM=["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
nm=lambda p: f"{NM[p%12]}{p//12-1}"
pos=lambda t: f"{t//48+1}:{(t%48)//12+1}.{(t%12)//3+1}"
for ln in dict.fromkeys(n["line"] for n in c["notes"]):
    sec,i=ln.split(":"); i=int(i)
    if sec not in ("Bridge",) and (sec,i) not in [("Chorus 1",5),("Verse 2",2),("Pre 2",1)] and "all" not in sys.argv[1:]: continue
    sy=L2[sec][i]; ns=[n for n in c["notes"] if n["line"]==ln]
    print(f"{ln:12s}"," ".join(f"{('-' if n['slur'] else (sy[n['syl']][0][:5].upper() if sy[n['syl']][1] else sy[n['syl']][0][:5]))}/{nm(n['p'])}/{pos(n['on'])}/{n['dur']//3}" for n in ns))
r = R["riff"]; print("riff onsets", r[1], "steps", r[2])
for sl in R["riff_slots"][:4]:
    import melody_v2_p36 as V
