# Song 35 intake (ZenEng v88): a test of the hymn and concert classes' rules (fixes 135-163, 173-177).
TITLE = None
LOG = []
LOG.append({"q": "goal", "answer": "Here's the new engine. Lots of musical improvements. Ready to test it by writing a song?"})
LOG.append({"q": 1, "topic": "what kind of song", "options": {"A": "pop with verse, pre-chorus, chorus and bridge", "B": "a hymn", "C": "a standards-style ballad"}, "recommended": "A",
            "answer": "Start a songwriting session the way you did for songs 33 and 34. Give it two files: ZenEng_v88.docx, and a tables file I'm preparing now. Ask for a hymn or a concert solo. Those two classes carry the most untested rules. A hymn is the stricter test; a concert solo suits your recent songs. Either works, and the subject is yours. Build under ZenEng v88, not v64 plus old lists. Run as code every rule for the song's class from fixes 135 to 163 and 173 to 177, and say in the test report which ran, which could not, and why. Report how many candidates each new gate killed. Number new findings from 178, and check the paper's version before numbering.",
            "reading": "class: hymn or concert solo (the writer's choice next); build rules: v88 whole; run 135-163 and 173-177 for the class, report ran / could not / why; deaths per new gate; findings from 178 (v88's last fix is 177: checked)"})
LOG.append({"q": 2, "topic": "hymn or concert solo", "options": {"A": "a hymn (stricter: every class rule a gate)", "B": "a concert solo (art song)", "C": "a carol (the hymn and concert class; seasonal)"}, "recommended": "A", "answer": "C",
            "reading": "class: carol, in the hymn and concert classes (27.23: hymn, carol, art song, concert solo); the hymn gates bind (136, 137, 138, 155, 161) where v88 applies them to carols -- to be checked rule by rule"})
CLASS = "carol"
LOG.append({"q": 3, "topic": "whose eyes (10.10: the one moment, the object)", "options": {"A": "a shepherd: the cold field, the crook at the stable door", "B": "Joseph: a carpenter's hands; the rough manger he would have built better; the father nobody sings", "C": "Mary, the first night"},
            "recommended": "B", "answer": "B", "reading": "speaker Joseph; objects: his hands, the wood, the feed trough (manger)"})
OBJECTS = ["carpenter's hands", "wood", "manger (feed trough)"]
SPEAKER = "Joseph"
LOG.append({"q": 4, "topic": "the turn (10.1 Q4)", "options": {"A": "the wood: the trough is the first wood to hold him, not the last; the cross seen by a carpenter's eye, never named", "B": "the name (Matthew 1:25)", "C": "the gift: his trade"},
            "recommended": "A", "answer": "A.", "reading": "the turn: manger wood to cross wood, unnamed; the last stanza lands on the wood"})
LOG.append({"q": 5, "topic": "title", "options": {"A": "The First Wood", "B": "Joseph's Hands", "C": "The Carpenter's Carol"}, "recommended": "A", "answer": "A"})
TITLE = "The First Wood"
LOG.append({"q": 6, "topic": "form and metre", "options": {"A": "four stanzas of Common Metre (8.6.8.6), each with a two-line refrain that turns in the last stanza", "B": "four stanzas of 8.7.8.7, no refrain", "C": "five stanzas of Long Metre"}, "recommended": "A", "answer": "A"})
METRE = "CM (8.6.8.6) + a two-line refrain; four stanzas; the last refrain turns"
LOG.append({"q": 7, "topic": "metre, tempo, key, setting", "options": {"A": "3/4 at q = 92, F major, SATB and organ; the tune C4-D5", "B": "4/4 at q = 84, D major, SATB and organ", "C": "6/8, G major, unison and piano"}, "recommended": "A", "answer": "A"})
FEEL = {"meter": "3/4", "qbpm": 92, "key": "F major", "setting": "SATB and organ", "tune_range": "C4-D5"}
LOG.append({"q": 8, "topic": "never say (v77: a death)", "options": {"A": "carol cliches (silent night, holy night, lowly, humble, little Lord, baby boy, star so bright, angels sing, heavenly host, peace on earth) and the words that name the turn (cross, nails, Calvary, crucified, tree)", "B": "only the turn's words", "C": "no list"},
            "recommended": "A", "answer": "A"})
NEVER_SAY = ["lowly", "humble", "cross", "nails", "calvary", "crucified", "tree"]
NEVER_PHRASES = ["silent night", "holy night", "little lord", "baby boy", "star so bright", "angels sing", "heavenly host", "peace on earth"]
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md",
            "answer": "B. (1) stanza 2 the softest: lines 3-4 ('tonight I run my thumb along / to find the splintered ones') feel forced; domestic and true but do not deepen the central tension; merely tender rather than weighty. (2) the refrain's first three appearances are identical; the final change is so effective that the earlier refrains could carry more variation or pressure without losing their simplicity. (3) metre and singability: a few places crowded or uneven spoken aloud: 'the adze ran crooked down the line', 'I cannot plane the wood out there'. (4) theological understatement almost too complete: one earlier, quieter foreshadowing, still inside Joseph's limited knowledge, could strengthen the arc"})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md",
            "answer": "(1) stanza 2: 'I did not make this trough, this child.' strong, but the comma creates a slight hesitation in singing; a lightly adjusted version might flow better, same meaning. (2) refrain 3 'while I am here to hold' the only refrain a touch abstract; the least vivid of the four. (3) metre: 'I did not make this trough, this child.' and 'there's wood I cannot reach to square' sit a fraction long or short in strict hymn metre; worth watching"})
LOG.append({"q": "lyric draft 3", "file": "lyric_draft3.md",
            "answer": "rhyme slips: stanza 1 squared/pared slant; stanza 3 grain/plane mismatched acoustically with true/knew (ballad stanza holds it); repetition: stanza 2 'I hold them both at once' and refrain 3 'while these two hands can hold' echo hands/hold too closely across consecutive verses",
            "reply": "squared/pared, grain/plane and true/knew are full rhymes (kept); refrain 3 changed to 'while I have arms to hold' (hold kept as the refrain's verb; 'these hands' no longer echoes stanza 2)"})
LOG.append({"q": "lyric draft 4 (shown)", "file": "lyric_draft4.md",
            "answer": "https://claude.ai/artifact/928T1fs3RkMvtyihLqxCJ3",
            "reading": "the tables file: ZenEng v88 tables (zeneng_v88_tables.json, 451,281 bytes, sha256 561355b1...68255): pitch_model, rhythm_tables, bar_rhythm_vocabulary, surprise bands (pitch, rhythm), rhythm_by_class, declamation, harmony by class and section, outer_voices, phrase_cadence, repetition, text_setting, gate_audit; its note: the paper's band decides at an edge. Draft 4 not yet locked."})
TABLES = "/home/claude/p35/tables/zeneng_v88_tables.json"
LOG.append({"q": "lock", "answer": "A", "locked": "lyric_draft4.md"})
WRITER_PHRASES = ["the first wood"]
WRITER_WORDS = ["wood"]
LEXICON = {}
ROLES = {"verse", "refrain"}
COMMERCIAL = {"profile": "congregational carol", "hold": [], "depart": []}
SENSES = "touch and grain: hands, thumb, wood, edges"
INSTRUMENT = "SATB choir and organ"
OBJECTS += ["feed-trough", "pine", "adze/blade", "mortise", "saw", "plane", "beam", "post", "timber"]
LOG.append({"q": "music", "pick": "d99d993b5228", "search": "500 built, 86 survivors, order 638be4d08765, reproduced (three runs)", "control": "root-position bass, outer-voice terms off: 136 would fail 157/209/35 of 458"})
LOG.append({"q": "delivery", "songbook_doc": "https://claude.ai/artifact/C31Uq3LK5mDT8ZKqS27PzJ", "consistency": "42/42"})
