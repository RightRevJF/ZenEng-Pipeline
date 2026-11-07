"""Song 24 writing room (v64 port): 'The Song You Sang Me' -- the lines drafted with the writer (13:27-13:35), each slot's versions
scored here for the record: draft 1/2 (the run's; draft 2 moved the lullaby from bridge to chorus, words unchanged) and draft 3 (the
writer's notes: verse 3's third line explained; the chorus's imagery familiar; one harder image). 3/4 at q = 76: a line takes four bars
(24 eighth slots). Both never-say lists are deaths; Rule V1 on the verse couplets."""
import sys; sys.path[:0] = ["/home/claude/p24", "/home/claude/carol", "/home/claude/pop"]
import engine_p24 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "3/4"
def V(mate=None, **k):
    d = dict(role="verse", nslots=24, show=3, couplet=mate); d.update(k); return d
E.run("V1.1 the napkin", "object: you're folding the same napkin by the window", **V("you ask me if I've come to fix the heat"))
E.run("V1.2 the heat", "object: you ask me if I've come to fix the heat", **V("you're folding the same napkin by the window"))
E.run("V1.3 the chair", "body: I pull my chair in close like I've always done", **V("you ask me if I've come to fix the heat"))
E.run("REFRAIN", """
plain: it's me. I'm your son.
""", role="refrain", nslots=24, show=1)
E.run("V2.1 the pictures", "object: I brought the pictures from the lake in August", **V("you touch a face and say, she used to swim"))
E.run("V2.2 the face", "object: you touch a face and say, she used to swim", **V("I brought the pictures from the lake in August"))
E.run("V2.3 the hand", "body: you hold my hand the way you'd hold anyone", **V("you touch a face and say, she used to swim"))
E.run("C.1 the dark", """
object: lay your head, the lamp is low
contradiction: go to sleep, I've got the dark
""", role="chorus", nslots=24, show=2)
E.run("C.2 folded", """
object: the river knows the way to go
object: I'll keep it folded, keep it near
""", role="chorus", nslots=24, show=2)
E.run("C.3 if you wake", """
object: I'll leave the hall light on for you
plain: and if you wake and don't know where you are
""", role="chorus", nslots=24, show=2)
E.run("C.4 your name", """
plain: and I'll be here the whole night through
plain: I'll say your name till you know you're here
""", role="hook", nslots=24, show=2)
E.run("V3.1 the wrong name", """
plain: you don't ask me who I am now
object: you called me by your brother's name on Tuesday
""", **V("now you watch the birds come to the feeder"))
E.run("V3.2 the birds", """
object: you watch the birds come to the feeder
object: now you watch the birds come to the feeder
""", **V("you called me by your brother's name on Tuesday"))
E.run("V3.3 the name", """
contradiction: I tell you anyway, the way you'd leave a light on
object: I write my name in marker underneath the date
""", **V("now you watch the birds come to the feeder"))
E.run("V4.1 the second line", "time: I sang it soft, and somewhere in the second line", **V("your hand came up and kept the time"))
E.run("V4.2 the time", "body: your hand came up and kept the time", **V("I sang it soft, and somewhere in the second line"))
E.run("V4.3 along", "plain: you didn't know my face, but you sang along", **V("your hand came up and kept the time"))
E.run("REFRAIN 4 (the turn)", """
plain: it's me. I'm your song.
""", role="refrain", nslots=24, show=1)
E.save("/home/claude/p24/w1.json")
print("compounds:", E.COMPOUND_LOG)
