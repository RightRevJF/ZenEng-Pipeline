"""Song 26, 'Five-Oh-One' -- the lyric, drafted over three rounds and locked by the writer (07:26). One voice (male tenor) with a gang
shout; first person. Draft 2 changed the last chorus's turn ('home' -> 'here'); draft 3 followed the writer's attached suggestions."""
TITLE = "Five-Oh-One"
V1 = [("verse", "five long days they've been borrowing every hour I've got"), ("verse", "I've been watching that second hand like it owes me money"),
      ("verse", "coat on the chair and my keys in my fist and one foot in the hall"), ("verse", "then the minute rolls over and the whole place lets out its breath")]
PRE1 = [("pre", "somebody's loading the speakers in the back of a car"), ("pre", "somebody's sending the address with a row of little flames")]
CHORUS = [("chorus", "five-oh-one, the whole town loosens its tie"), ("chorus", "five-oh-one, every light on the avenue's green"),
          ("chorus", "sixty hours and every single one of them's mine"), ("hook", "five-oh-one, good luck finding me now")]
HOOK = [("hook", "five-oh, five-oh, five-oh-one"), ("hook", "five-oh, five-oh, five-oh-one")]
V2 = [("verse", "radio's playing the song I pretended I hated in June"), ("verse", "now I'm singing every word at a red light, and so is the guy in the truck"),
      ("verse", "two blocks out and the bass is already rattling the glass"), ("verse", "somebody's dancing in the driveway before I've even parked")]
PRE2 = [("pre", "the neighbor who swore he wasn't coming is dancing with a plate"), ("pre", "somebody's grandmother's out in the middle, and she's winning")]
BREAK = [("breakdown", "if your Monday tried to bury you, clap"), ("breakdown", "if your Tuesday held the shovel, clap"),
         ("breakdown", "if your Wednesday ran a week long, clap"), ("breakdown", "if your Thursday wouldn't end, clap")]
LIFT = [("lift", "look at your wrist and tell me, what does it say?"), ("shout", "five-oh-one")]
LAST = CHORUS[:3] + [("hook", "five-oh-one, and you'll find me here")]
OUTRO = [("tag", "five-oh, five-oh, five-oh-one")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CHORUS), ("Hook 1", HOOK), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CHORUS),
            ("Hook 2", HOOK), ("Breakdown", BREAK), ("Lift", LIFT), ("Chorus 3", CHORUS), ("Chorus 4", LAST), ("Hook 3", HOOK), ("Outro", OUTRO)]
SINGER = {s: "him" for s, _ in SECTIONS}
GANG = {("Lift", 1): "everybody", ("Hook 1", 0): "(hey!)", ("Hook 1", 1): "(go!)"}   # the shout, and the band's answers after each hook line
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [
 ("DRAFT 1 -> 2 (07:19)", "the writer's note", "'he's not going home, is he?' -> the last chorus's turn 'and I'm home' became 'and I'm here' (his pick, A)"),
 ("DRAFT 2 -> 3 (07:24)", "the writer's attached suggestions", "the jailbreak ('five long days they've been borrowing every hour I've got'); the chorus's last line "
  "'good luck finding me now', answered by the turn 'and you'll find me here'; verse 2's arrival in shots; the neighbor with the plate; the breakdown Monday to "
  "Thursday into the shouted title"),
 ("LOCK (07:26)", "the writer's lock", "draft 3"),
]
