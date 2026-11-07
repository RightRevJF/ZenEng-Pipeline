"""Song 25 writing room (v64 port): 'Through Its Breaking' -- the lines drafted with the writer (15:01-15:10), scored here for the record:
draft 1 (the run's) and draft 2 (the writer's notes: verse 1 trimmed to its pictures; the chorus's second couplet; one more interior moment).
6/8 in two at dotted-q = 54: a line takes two bars (12 eighth slots; span 10). Both never-say lists are deaths; Rule V1 on the couplets."""
import sys; sys.path[:0] = ["/home/claude/p25", "/home/claude/carol", "/home/claude/pop"]
import engine_p25 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "6/8"
def V(mate=None, **k):
    d = dict(role="verse", nslots=12, show=3, couplet=mate); d.update(k); return d
E.run("V1.1 the tower", "object: high in the tower over the town", **V("a bell too big for a place this small"))
E.run("V1.2 too big", "object: a bell too big for a place this small", **V("high in the tower over the town"))
E.run("V1.3 the crack", "object: green as moss, with a crack up the side", **V("wide enough to hold a thumbnail"))
E.run("V1.4 the thumbnail", "object: wide enough to hold a thumbnail", **V("green as moss, with a crack up the side"))
E.run("V1.x the functions (cut in draft 2)", """
plain: it rings the hour, it rings the market
plain: it calls the meeting to the hall
""", **V("close to the note it was made to sing"))
E.run("V1.5 the note", "contradiction: close to the note it was made to sing", **V("never quite the note at all"))
E.run("V1.6 never quite", "plain: never quite the note at all", **V("close to the note it was made to sing"))
E.run("C.1 the tune", "plain: close enough to know the tune", role="chorus", nslots=12, show=1)
E.run("C.2 true", "contradiction: not close enough to call it true", role="chorus", nslots=12, show=1)
E.run("C.3 the couplet", """
plain: two almost-notes where one should be
object: like your name in a stranger's mouth
""", role="chorus", nslots=12, show=2)
E.run("C.4 she rings it", """
plain: and still she rings it anyway
plain: and every hour she rings it through
""", role="hook", nslots=12, show=2)
E.run("V2.1 brilliance", "plain: she was never made for brilliance", **V("she was made for oil and rope"))
E.run("V2.2 oil and rope", "object: she was made for oil and rope", **V("she was never made for brilliance"))
E.run("V2.3 love (draft 2)", """
time: eleven years of every hour
body: she never meant to love the thing
""", **V("it found her, year by year, at the wheel"))
E.run("V2.4 the wheel (draft 2)", """
object: measuring a crack that never grows
body: it found her, year by year, at the wheel
""", **V("she never meant to love the thing"))
E.run("V2.5 sleep", "body: some nights she couldn't find her sleep", **V("she'd climb up in the dark and sit"))
E.run("V2.6 the dark", "object: she'd climb up in the dark and sit", **V("some nights she couldn't find her sleep"))
E.run("V2.7 the palm", "body: her palm flat on the cold green bronze", **V("she thought: the note is still in it"))
E.run("V2.8 the thought", "plain: she thought: the note is still in it", **V("her palm flat on the cold green bronze"))
E.run("B.1 the valley bell", "time: one winter night the valley bell fell still", role="bridge", nslots=12, show=1)
E.run("B.2 the need", "object: and the need came down like snow", role="bridge", nslots=12, show=1)
E.run("B.3 the only bell", "contradiction: the wrong bell was the only bell", role="bridge", nslots=12, show=1)
E.run("B.4 the rope", "body: she took the rope in both her hands", role="bridge", nslots=12, show=1)
E.run("B.5 again", "plain: again, again, the split note went", role="bridge", nslots=12, show=1)
E.run("B.6 the fields", "object: out over roofs and frozen fields", role="bridge", nslots=12, show=1)
E.run("B.7 the doors", "object: and doors came open down the valley", role="bridge", nslots=12, show=1)
E.run("B.8 farther", "plain: farther out than it had ever reached", role="bridge", nslots=12, show=1)
E.run("CF.3-4 the turn", """
contradiction: it didn't ring in spite of the crack
contradiction: it never rang in spite of the crack
""", role="chorus", nslots=12, show=2)
E.run("CF.4 the title", "plain: it rang through its breaking", role="hook", nslots=12, show=1)
E.run("TAG", """
object: the crack runs up the bronze
plain: the bell rings
plain: the sound carries
""", role="tag", nslots=12, show=3)
E.save("/home/claude/p25/w1.json")
print("compounds:", E.COMPOUND_LOG)
