# 749.262, a genre the band tables do not hold: the form and marks, before any code or run

28 November 2026, 13:06 ET. The songwriting session's ask (c) (12:32 ET), numbered by it. Song 68's first attempt stopped at the band step with KeyError 'pop-punk'; no reading was made and the song was run from a copy with genre "rock".

**Read from the code:** `band.arrange` looks the lyric's genre up in the band tables (`studies/arrangement/lpd_band_tables.json`), whose keys are country, soul / r&b, gospel, pop, rock, folk, blues, jazz, hip hop, electronic, metal. Any other word stops the run after the melody is made. The melody reads the genre only through FAMILY, where an unknown genre already falls to "other" (as pop and rock do), so the notes do not depend on this. Two lyrics in the repository carry genres outside the keys: "pop-punk" (song 68) and "indie" (one other).

**The form (no switch: it acts only where the planner stops today, so no record that exists can change):** the band step takes the genre itself where the tables hold it; else a named nearest key from a short list written here (pop-punk, punk, indie, alternative to rock; americana, singer-songwriter to folk; soul, r&b to soul / r&b; hip-hop to hip hop; edm, dance to electronic); else a table key that stands as a whole word in the genre's name; else pop, the band step's own default. Where the genre used is not the genre asked, the record says so in its flags and in the band's own report (asked, used, and which rule chose it).
*Settled, mine to answer for:* the short list. It is a list of names, not a finding; the songwriting session may strike or add.

**Marks:**
1. Every switch unset, 54, 55, 52 and song 53's Essen arm come out byte for byte as now (their genres are table keys).
2. A seen lyric (song 55's words as in the repository, 4/4) with its genre set to "pop-punk" runs to the end; its notes and band parts are byte for byte those of the same lyric with genre "rock"; its flags name the genre asked and used.
3. The same with a nonsense genre ("zzz") runs to the end on pop and says so.
Room files after. Song 68 is not run.

## What I expect
All three met. Nothing else moves.
