"""The fix list after v107 (fixes 286-295) from the song 38 rerun: fixlist_v2.md."""
import json, re
H = "/home/claude/p38"; R = json.load(open(f"{H}/readings_v2.json")); TB = json.load(open(f"{H}/tableb_v2.json"))
rep = open(f"{H}/test_report_v2.md").read()
def sect(a, b): i = rep.index(a); j = rep.index(b, i); return rep[i:j].strip()
md = ["# ZenEng fix list after v107\n\n*Song 38 rerun under v107 · fixes 286–295 · with the three runs, the deaths per gate, the tests of 257–285 and the readings the paper did not spell out*\n",
      "v107's last fix is 285 (Window 127, version row v141). This list starts at 286 and covers every song since v107: one, a regression run of song 38, *Stay Tuned*, "
      "rerun under v107 with the locked lyric, every intake answer, the form, key, tempo, chords, seed 20261491 and calibration seed 20261492 unchanged, and the judges' weights as fitted through song 37. "
      "It is the first song to run fixes 257–280. Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited.\n",
      "## Songs since v107\n", "| Song | Title | What it tested | Fixes found |\n|---|---|---|---|",
      "| 38 (rerun) | Stay Tuned | v107 on a song already built under v103: Run A the gates only (276–278, 270, 264, 267), Run B full v107 (257–274, 281, 282, 285 added), Run C B with 243 off. 3,000 builds each, each run twice. "
      f"Survivors A {R['1']['A']['survivors']}, B {R['1']['B']['survivors']}, C {R['1']['C']['survivors']} (v1: 43). Record from Run B's shortlist pick. | 286–295 |\n", "## The fixes\n"]
for blk in open(f"{H}/findings_v2.md").read().strip().split("\n\n"):
    m = re.match(r"\*\*(\d+)\. (.+?)\*\* \*Problem:\* (.+?) \*Evidence:\* (.+?) \*Fix:\* (.+?) \*Check:\* (.+)$", blk.strip(), re.S)
    n, t, p, e, f, c = m.groups()
    md.append(f"### {n}. {t.rstrip('.')}\n\n**Problem:** {p.strip()}\n\n**Evidence:** {e.strip()}\n\n**Fix:** {f.strip()}\n\n**Check:** {c.strip()}\n")
md.append("## Order of work\n")
md.append("1. 286 (the unaudited gates as soft limits): the spectral band now kills half of every run, and the seven together pass 75.7% of the calibration pairs.\n"
          "2. 287 (the return gate): two steps after 239 still change early shared notes; one rule exempts a built return from both.\n"
          "3. 291 (refit the judges on v107 builds): the shortlist is ranking v107's lines with a yardstick fitted to the old generator.\n"
          "4. 288 (the generator's palette and registers): the limits are loose but the builds still sit at five note lengths and a chorus ten semitones over the verse.\n"
          "5. 289 and 290 (the landing draw; beat 3 dropped as an aim).\n"
          "6. 293, 295 (a chosen axis calibrated whole; verse 2's bars drawn from verse 1's; section endings drawn, not moved).\n"
          "7. 294 (265's wording for a section the writer split from the era); 292 (a record).\n")
md.append("## Regression line\n")
md.append(f"After these fixes, song 38 reruns at PYTHONHASHSEED 0, seed 20261491 (calibration 20261492), N 3000, Run B and Run C, and must reproduce their frozen orders twice "
          f"(today's: B {R['1']['B']['order']}, C {R['1']['C']['order']}; they will change with the code). It must keep the six A4s on 'tuned' over A, the said-twice line moved whole on G4 over G, the tag E4–C♯4–A3, "
          "the bridge above the verse and under the summit (the two design gates); lose under one build in five at the spectral reading (286) and none at 267 where 239 built the return (287); "
          "spread the most note lengths in eight bars across 4–8 (288); put last stresses on 1 or 3 in 35–55% of lines (289); read the verse median on reciting inside 1.4–2.1 in B as well as C and verse 2's shared bar rhythms inside 25–75% in three builds of four (293); "
          "need the section-ending move in fewer than one build in ten (295); and pass every consistency check (55 of 55 today). The Table DJ readings that reached the kept middle half in Run B (arched or falling 68%, arch term +1.25, widening +0.20, entry after the downbeat 39%, the first note's extra surprise 1.74 bits) must stay there. "
          "The judges' claim stays what 27.47 says: like a kept song in content and order, not good.\n")
md.append("## Reports\n")
md.append("### Report 1: the runs and the pick\n\n" + sect("## 1. Survivors and frozen orders", "## 2.").split("\n", 1)[1].strip() + "\n")
md.append(sect("## 6. Fix 255: the three builds", "## 7.").split("\n", 1)[1].strip() + "\n")
md.append("### Report 2: deaths per gate, beside the first run\n\n" + sect("## 2. Deaths per gate, beside the first run", "## 3.").split("\n", 1)[1].strip() + "\n")
md.append("### Report 3: the limits, the pass rates and the line readings\n\n" + sect("## 3. Fix 277: soft breaks and hard limits", "## 4.").split("\n", 1)[1].strip() + "\n\n" +
          sect("## 4. Fixes 275 and 280", "## 5.").split("\n", 1)[1].strip() + "\n\n" + sect("## 5. The line readings of Table DJ", "## 6.").split("\n", 1)[1].strip() + "\n")
md.append("### Report 4: the tests of 257–285 and the regression line from the list after v103\n\n" + sect("## 8. The tests of fixes 257–285", "## 9.").split("\n", 1)[1].strip() + "\n\n" +
          sect("## 9. The regression line from the fix list after v103", "## The record").split("\n", 1)[1].strip() + "\n")
md.append("## Readings the paper did not spell out\n\n" + sect("## Readings the paper did not spell out", "## Findings").split("\n", 1)[1].strip() + "\n")
md.append("## Blind-pick tally\n\nNo blind pick: a regression run reuses the song's locked lyric. The tally stands at 27 songs: Annotated top 11, Remembered top 8, Middle 7, Refrain 1.\n")
open(f"{H}/fixlist_v2.md", "w").write("\n".join(md)); print(len("\n".join(md)))
