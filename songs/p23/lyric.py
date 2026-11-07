"""Song 23, 'What Holds' -- the lyric, drafted with the writer over three rounds (w1) and locked by him (12:40). One male voice. The
chorus is sung four times: twice in full, once stripped after the bridge (the band drops out), and once with the turn."""
TITLE = "What Holds"
V1 = [("verse", "granite curve across the river"), ("verse", "every block bent toward the ground"),
      ("verse", "top stone hung on empty air"), ("verse", "trucks roll over all day long")]
CHORUS = [("hook", "what holds is the hand against me"), ("chorus", "locked like rafters at the ridge"),
          ("chorus", "take your weight away, I'm rubble"), ("hook", "push me, and I stand")]
V2 = [("verse", "wire strung between two towers"), ("verse", "one man out there, pole held wide"),
      ("verse", "wind on the left, wind on the right"), ("verse", "he walks it like a kitchen floor")]
BRIDGE = [("bridge", "every bone pulled two ways"), ("bridge", "one muscle bends, one straightens"),
          ("bridge", "not in spite of the strain"), ("bridge", "I stand because of it")]
LAST = CHORUS[:3] + [("hook", "push me, and I stand: that's what holds")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Chorus 2", CHORUS), ("Bridge", BRIDGE),
            ("Chorus 3", CHORUS), ("Chorus 4", LAST)]
SINGER = {s: "him" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [
 ("DRAFT 1 -> 2 (12:34)", "the writer's notes", "verse 1's last two lines explained the picture ('there's nothing beneath the middle stone / the falling is what keeps it standing'); the chorus plain; lines too conversational for the groove -> verse 1 rewritten to pictures only, verse 2 the same, every line 5-8 syllables, the hook 'push me, and I stand'"),
 ("DRAFT 2 -> 3 (12:36)", "the writer's notes", "the chorus's middle lines still plain; the final line abrupt -> 'locked like rafters at the ridge' (0.816, top of C.2), 'take your weight away, I'm rubble' (0.682, #2 under draft 1's 0.702), the final line 'push me, and I stand: that's what holds' (0.664, top of CF.4)"),
 ("RANK", "the writer's lock", "where an earlier draft scored higher (V1.1 0.662 over 0.620; V1.2's draft-2 line is the top; C.1 0.855 over 0.763; C.3 0.702 over 0.682; B.1 0.686 over 0.681; B.2 0.604 over 0.562; B.3 0.748 over 0.729) the writer's notes stand"),
 ("B.4", "the writer's lock", "'I stand because of it' dies on the weak ending ('it'); kept -- the line ends on the stressed CAUSE with an unstressed tail, a finding"),
]
