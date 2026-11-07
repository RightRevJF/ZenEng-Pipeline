"""Song 21 writing room, pass 3: VERSE 3, after the break (the writer, 19:44): coming back -- the footwell, the clothes, one more minute
-- and an abstract way into the in-between ('not quite turned to jelly, not quite what you were before'), the word itself never said
('afterglow' is on the never-say list)."""
import sys; sys.path[:0] = ["/home/claude/p21", "/home/claude/carol", "/home/claude/pop"]
import engine_p21 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
def V(mate_line=None, **k):
    d = dict(role="verse", nslots=16, show=5, couplet=mate_line); d.update(k); return d
E.run("V3.1 the footwell again", """
object: you reach into the footwell for what's yours
body: we fish our clothes out of the footwell one by one
plain: you hand me my shirt from the footwell
""", **V("I'm halfway back into my own shape"))
E.run("V3.2 the in-between", """
object: I'm halfway back into my own shape
contradiction: not who I was when I climbed in, not someone new
body: my edges coming back a little blurred
""", **V("you reach into the footwell for what's yours"))
E.run("V3.3 one hole off", """
object: my shirt buttoned one hole off
plain: I button up and miss a hole
body: I button myself back together, one hole wrong
""", **V("and neither of us reaching for the door"))
E.run("V3.4 the door", """
object: and neither of us reaching for the door
plain: one more minute, and then the door
understatement: give it a minute before the door
""", **V("my shirt buttoned one hole off"))
E.save("/home/claude/p21/w3.json")
