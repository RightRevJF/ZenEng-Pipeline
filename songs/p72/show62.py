import json,statistics as st,sys
from collections import defaultdict
r=json.load(open(sys.argv[1])); ns=r["melody"]["notes"]; ck=r["checks"]; bt=12
names=["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]; nm=lambda m: names[m%12]+str(m//12-1)
run=best=1
for a,b in zip(ns,ns[1:]):
    run=run+1 if a["midi"]==b["midi"] else 1; best=max(best,run)
K=lambda s: s.split()[0]
v=[n["dur"] for n in ns if K(n["sec"])=="Verse"]; c=[n["dur"] for n in ns if K(n["sec"])=="Chorus"]
print("range",nm(min(n["midi"] for n in ns)),nm(max(n["midi"] for n in ns)),"run",best,"ratio %.2f"%(st.mean(c)/st.mean(v)))
for k in ck:
    if any(x in k for x in ("words' fit","plainness (floor","chorus's median","title's stressed","long notes on stressed")): print(" ",k[:50],"=",ck[k])
L=defaultdict(list)
for n in ns: L[(n["sec"],n["line"])].append(n)
for key in sorted(L, key=lambda k: L[k][0]["on"]):
    if key[0] in ("Verse 2","Chorus 2","Verse 3"): continue
    print(f"{key[0]:8} {key[1]}", " ".join(f"{n['text']}:{nm(n['midi'])}/{n['dur']/bt:.2g}" for n in L[key]))
