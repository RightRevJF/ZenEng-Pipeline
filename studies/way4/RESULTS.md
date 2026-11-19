# Way 4, the stranger and the learner: results (18 November 2026)

Predictions: PREDICTION.md, written before any surprise was computed. Code: graded.py (the graded set), listeners.py (the two listeners), test.py
(way4_results.json). The corpora are the maintainer's copies (Hooktheory, CoCoPops, BiMMuDa, the Hot 100 record) and are not in the repo.
Nothing here is in the engine.

The graded set: 2,252 Hooktheory songs joined to the Hot 100 (1,795 with 40 notes or more), 210 CoCoPops Billboard whole songs, 194 Rolling Stone
whole songs, 318 BiMMuDa songs. The record used until now was 131 songs.

The rule set beforehand: a measure works only at 0.10 or more on the primary set (p under 0.005) with the same sign at 0.05 or more on the replication set.

| Prediction | Primary: 1,795 Hooktheory songs (peak; weeks; holding year and notes) | Replication: 210 whole songs | Held? |
|---|---|---|---|
| F1 SHARE (surprise the song teaches away) relates to faring better | -0.027; -0.008 | 0.059; -0.002 | no |
| F2 the stranger's surprise alone relates to nothing | -0.061 (p 0.010); -0.069 (p 0.004) | -0.043; 0.073 | no, narrowly: a small lean to less surprise, under the bar |
| F3 inverted U | 0.027; 0.045 | 0.032; 0.069 | no |
| F4 LATE (the gain grows) relates to faring better | -0.017; 0.015 | 0.134 (p 0.054); 0.146 (p 0.035) | no: a hint on whole songs that the other sets contradict |
| F5 endings are the surest notes in three songs in four; no relation to grade | 56 in 100; 0.007, 0.027 | 66 in 100 | half: the lean is there, weaker; no relation to grade |
| F6 Rolling Stone songs over CoCoPops Billboard on SHARE | AUC 0.451; holding year -0.108 (p 0.034) | | no, the other way |

Also: Rolling Stone songs show LESS late gain than CoCoPops Billboard songs (AUC 0.403, p 0.0009; -0.197 holding year and notes); inside the Rolling
Stone list nothing relates to rank past 0.13; inside BiMMuDa nothing relates to year-end position past 0.05.

Reading. By the rule, no measure works, and nothing is built. The set is now large enough for that to mean something: on 1,795 songs a true relation of
0.10 would have been seen almost surely. What the primary set cannot test is the learner over a whole song (its songs are clips of about 88 notes);
the whole-song sets can, and are 210 and 194 songs. The one hint (LATE on CoCoPops Billboard) is one of some forty tests at p 0.035 and is contradicted
by the Rolling Stone set.
