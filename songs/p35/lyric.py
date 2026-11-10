"""The First Wood -- the locked lyric (draft 4, locked 10 Nov: 'A'). Joseph at the manger; a carol in Common Metre with a refrain."""
TITLE = "The First Wood"
STANZAS = [
    ["I know this wood: a feed-trough, pine,", "cut green and roughly squared;", "the blade went wide along the line,", "the edges never pared."],
    ["These hands have joined a hundred beds", "for other fathers' sons;", "I made no part of trough or child;", "I hold them both at once."],
    ["I'll teach you how to read the grain,", "to set a mortise true;", "your hands will learn the saw, the plane,", "the work my father knew."],
    ["I know what weight a beam will bear,", "how long a post will stand;", "there's timber I will never square", "that waits beyond my hand."]]
REFRAIN1 = "Sleep in the first wood, child,"
REFRAIN2 = ["and I will hold you too.", "it holds you as it can.", "while I have arms to hold.", "it will not be the last."]
REFRAIN1_PUNCT = [",", ";", ",", ";"]          # stanzas 2 and 4: 'child;' (the line that follows is a clause of its own)
SECTIONS = [(f"Stanza {i+1}", [("verse", l) for l in s] + [("refrain", REFRAIN1.rstrip(",") + REFRAIN1_PUNCT[i]), ("refrain", REFRAIN2[i])]) for i, s in enumerate(STANZAS)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
