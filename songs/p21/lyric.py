"""Song 21, 'Make Do' -- the lyric, from the writing room (w1, w2). Every line is the top of its slot unless PICKS says why."""
TITLE = "Make Do"
V1 = [("verse", "windows blacked out, and the leather still holding our shape"), ("verse", "the air conditioner hums against the evidence"),
      ("verse", "a small tremor working its way out of me"), ("verse", "and the air smells of skin and cooling dust")]
V2 = [("verse", "your clothes lie in the footwell where they fell"), ("verse", "a black eyelid on the glass that will not quite close"),
      ("verse", "we wrestled the shade into place with all four hands"), ("verse", "one corner gone cattywumpus in the dark")]
V3 = [("verse", "you hand me my shirt from the floor"), ("verse", "I'm halfway back into my own shape"),
      ("verse", "I button myself back together, one hole wrong"), ("verse", "and neither of us reaching for the door")]
CHORUS = [("chorus", "I watch a blade of daylight find its way in"), ("chorus", "while the warmth is slow to leave"),
          ("chorus", "let the day go on without us"), ("hook", "the afternoon will have to make do")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Chorus 2", CHORUS), ("Verse 3", V3), ("Chorus 3", CHORUS)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [
 ("V1.1", "body (w2 #1, 0.724)", "pass 2: the poem's opening image kept without 'still warm' -- the chorus carries the warmth leaving (the warmth said twice, the critique the writer heard); over w1's 'the windows blacked out and the leather still warm' (0.700)"),
 ("V1.3", "object (#2, 0.689)", "over 'you beside me and a small tremor...' (0.757, 0.068): 'you beside me' was the poem's flattest line (the critique); the tremor carries it"),
 ("V2.1", "object (#2, 0.636)", "over '...are in the footwell' (0.642, 0.006): the poem's 'lie'"),
 ("V2.2", "body (#3, 0.670)", "over 'the shade a black eyelid...' (0.715, 0.045): 'shade' would come in two adjacent lines (28.6); the eyelid first, the shade named in the next line"),
 ("VERSE 3", "", "the writer (19:41): too short -- a third verse after the break; (19:44) C, coming back, and 'an abstract way to capture the feeling ... not quite turned to jelly, not quite what you were before' -- pass 3 (w3)"),
 ("V3.3", "body (#2, 0.613)", "over 'my shirt buttoned one hole off' (0.648, 0.035): 'shirt' is in V3.1; 'button myself back together, one hole wrong' carries 'not quite what you were before'"),
 ("NOTES 19:48", "", "the writer's lines, locked as his (w4, scored): C.1 'I watch a blade of daylight find its way in' (0.786; his first choice, the light given an action); C.2 'while the warmth is slow to leave me' (0.689; fulfilment, not depletion); V2.4 'one corner gone cattywumpus in the dark' (0.740; the word protected, the line lightened); V2.3 'all four hands' tested: stresses on FOUR and HANDS, alignment 1.0 -- kept, with 'both our hands' (0.699) ready if the melody finds it cumbersome"),
 ("NOTES 19:51", "", "the writer: V2.3 'into place' (the poem's words; a blackout shade goes up to let light in -- 0.840); V3.1 'from the floor' (footwell not twice; 'floor' rhymes with V3.4's 'door' -- 0.642); C.2 trim pending"),
 ("C.2", "writer A (0.676)", "'while the warmth is slow to leave' -- the line ends on a stressed note the melody can hold, 'me' understood"),
 ("V2.3", "object (#2, 0.791)", "over 'we fought the shade into place...' (0.792, 0.001): the poem's 'wrestled'"),
]
