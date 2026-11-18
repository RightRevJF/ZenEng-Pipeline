"""Luthier v8, stage 1 (Module 27.89; fixes 750, 751): make a song's v8 engine file from its Luthier v7 file.

    python3 lib/luthier/gen_l8.py /home/claude/p64        # reads melody_l7_p64.py, writes melody_l8_p64.py beside it

Every patch must match exactly once, as the song generators' patches do. What it changes:
750  The kept-bar table (652) held three rhythms with one onset twice ([0, 0]; [0, 0, 6]; [0, 0, 12, 18, 24, 36]): 38 of the kept
     songs' 48,763 notes share an onset with the note before in the transcriptions, and those bars reached the table. A drawn bar
     that took one sang two syllables on one onset, the first with no length (749.1, 749.26). The loader now keeps only rhythms
     whose onsets rise strictly inside the bar.
751  A build with two notes on one onset, or a note of no length, is a death in evaluate, whatever wrote it.
752  The pick is luthier_judge6's: 730's eligibility and, besides, no doubled onset, the longest run of one pitch at or under the kept
     90th percentile, steps and leaps in the kept middle halves, and the notes in runs of four or more at or under the writer's ceiling.
     luthier_judge6.py is copied beside the engine. The run's files go to runl8/."""
import sys, os, re, shutil
def patch(s, old, new, name):
    if s.count(old) != 1: raise SystemExit(f"patch {name}: found {s.count(old)} times, wanted once")
    return s.replace(old, new)
def main(folder):
    folder = folder.rstrip("/"); nn = re.search(r"p(\d+)$", folder).group(1); src = f"{folder}/melody_l7_p{nn}.py"; s = open(src).read()
    s = patch(s, 'KB652 = {int(k_): v_ for k_, v_ in _T3[_k3("652: kept bar rhythms")].items() if v_}',
              'KB652 = {int(k_): [r_ for r_ in v_ if 0 <= r_[0][0] and r_[0][-1] < 48 and all(a_ < b_ for a_, b_ in zip(r_[0], r_[0][1:]))] for k_, v_ in _T3[_k3("652: kept bar rhythms")].items() if v_}   # 750: no rhythm with an onset twice\n'
              'KB652 = {k_: v_ for k_, v_ in KB652.items() if v_}', "750")
    s = patch(s, '    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))\n',
              '    if any(b_["on"] <= a_["on"] for a_, b_ in zip(notes, notes[1:])) or any(n_["dur"] <= 0 for n_ in notes): return ("two notes on one onset, or a note of no length (751)", 1), None\n'
              '    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))\n', "751")
    s = patch(s, 'import luthier_judge5 as J5\n', 'import luthier_judge5 as J5\nimport luthier_judge6 as J6                                                               # 752\n', "752a")
    s = patch(s, '(J5 if ON23("730") else J4).pick(', '(J6 if ON23("730") else J4).pick(', "752b")
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), "luthier_judge6.py"), f"{folder}/luthier_judge6.py")
    n_run = s.count(f"{folder}/runl7/")
    if n_run < 1: raise SystemExit("no runl7 path found")
    s = s.replace(f"{folder}/runl7/", f"{folder}/runl8/").replace(f"melody_l7_p{nn}_", f"melody_l8_p{nn}_").replace(f"python3 melody_l7_p{nn}.py", f"python3 melody_l8_p{nn}.py")
    s = '"""Luthier v8 stage 1 (Module 27.89; by lib/luthier/gen_l8.py from melody_l7_p%s.py: 750, 751, 752)."""\n' % nn + s
    os.makedirs(f"{folder}/runl8", exist_ok=True); open(f"{folder}/melody_l8_p{nn}.py", "w").write(s); print("wrote", f"{folder}/melody_l8_p{nn}.py", "(run files to runl8/)")
if __name__ == "__main__": main(sys.argv[1])
