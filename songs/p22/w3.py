"""Song 22 writing room, pass 3: VERSE 4 rewritten to the writer's notes (06:47) -- preservation -> expansion -> discovery -> the
ordinary; the record given weight; the seam MOVING (a grammatical anchor); the bread kept, plain; and the verse beginning the ending's
movement from observing to living (he stops recording)."""
import sys; sys.path[:0] = ["/home/claude/p22", "/home/claude/carol", "/home/claude/pop"]
import engine_p22 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
def V(mate_line=None, **k):
    d = dict(role="verse", nslots=16, show=5, couplet=mate_line); d.update(k); return d
E.run("V4.1c the record, with weight", """
plain: I kept the record though nobody came
object: I kept the record of the widening
time: I kept the record until it changed
contradiction: I kept the record against the day
""", **V("the seam has moved a hand's width east"))
E.run("V4.2c the seam moving", """
object: the seam has moved a hand's width east
plain: the seam had shifted a hand's width east
body: the line had moved a hand's width east
""", **V("I kept the record though nobody came"))
E.run("V4.3c putting the pencil down", """
body: this morning I put the pencil down
plain: this morning I forgot to write it down
understatement: I didn't measure; I just looked
object: this morning I left the page blank and looked
""", **V("and bread was rising somewhere down the street"))
E.run("V4.4c the bread, plain", """
plain: and bread was rising somewhere down the street
object: the smell of bread came through the open door
time: the smell of bread moved through the street
""", **V("this morning I put the pencil down"))
E.save("/home/claude/p22/w3.json")
