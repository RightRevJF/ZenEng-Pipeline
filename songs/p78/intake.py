"""Song 68 (folder p78): a new song in 3/4, the real test of the engine writing outside 4/4 once the 3/4 trial on song 53's words has read."""
LOG = []
LOG.append({"when": "2026-11-27", "q": "The maintainer asked which words to try 3/4 on (no lyric yet for the engine in 3/4). A (Recommended) start a new 3/4 song now, the trial runs on song 53's words first and the new song is the real test; B the new song is the trial itself; C wait for the trial", "answer": "A"})
METRE = "3/4"
STATUS = "intake"
LOG.append({"when": "2026-11-27", "q": "How do we start? A (Recommended) you bring a poem or an idea; B an older lyric rebuilt in 3/4; C three seeds for a waltz",
            "answer": "A. I know we've done one on a muse before but i don't think that song captured what I was getting at. Having a muse is a real paradox. Yes, you're blessed with gifts and abilities BUT ALSO yes, you're consumed by it, becoming the ultimate mixture of pain and pleasure. [his poem 'Terpsichore', the comic-complaint version: hooks into me, pages flying, dying inside, always penning, no time for sinning, life a chore, help me create a ruse that I can escape my muse, save me from Terpsichore]",
            "done": "Earlier muse songs found: song 10 'Tara' (from the free-verse 'Terpsichore', woman or muse) and song 56 'Terpsichore' (p66, sung to her as 'you', the double meaning kept). Neither held the gift-and-consumption paradox, he says. This is the short rhymed poem; not copied into the repo."})
LOG.append({"when": "2026-11-27", "q": "What tone? A (Recommended) the poem's wry half-comic voice with the gift and the pleasure added, the plea half meant; B darker, serious; C comic on top, dark underneath: a bright, almost carnival waltz under words that get more desperate",
            "answer": "C. And it should be a bop. Uptempo unless 3/4 time works against that",
            "done": "3/4 does not work against it: a fast waltz is felt one beat a bar. Tempo provisional at about 180 quarters a minute (60 bars), to be confirmed against the Wikifonia 3/4 tables' tempo spread before music."})
TONE = "comic on top, dark underneath; uptempo"; BPM = 180
LOG.append({"when": "2026-11-27", "q": "The hook? A (Recommended) 'She's got her hooks into me' opens the chorus, 'Save me from Terpsichore' closes it; B 'Save me from Terpsichore' alone; C 'Help me escape my muse'",
            "answer": "I don't know that tersichore is singable. Might want to just switch to muse", "done": "'Terpsichore' dropped from the sung lines; 'muse' instead. Hook asked again with muse."})
LOG.append({"when": "2026-11-27", "q": "The hook with muse? A (Recommended) 'She's got her hooks into me' opens the chorus, 'Save me from my muse' closes it, flipping to 'Don't save me from my muse' in the last chorus; B 'Save me from my muse' alone; C 'I can't refuse my muse'", "answer": "A"})
HOOK = "Save me from my muse"
