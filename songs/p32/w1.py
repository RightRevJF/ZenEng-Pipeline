"""Song 32 writing room (v64 port, v65 fixes as ports): 'I Took Him for the Gardener' -- draft 1's lines and the alternatives weighed,
scored for the record and to flag weak lines before the writer sees the lyric. 6/8 at dotted-q = 52, a line in two bars (12 eighths)."""
import sys; sys.path[:0] = ["/home/claude/p32", "/home/claude/carol", "/home/claude/pop"]
import engine_p32 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "6/8"
def V(**k):
    d = dict(role="verse", nslots=12, show=10); d.update(k); return d
E.run("V1: the dark", """
plain: it was still dark. I brought the spices
body: I knew how to wash the dead
plain: I came to do the last thing left
body: I'd tied my hair back for the work
object: and the stone was moved instead
""", **V())
E.run("refrain", """
plain: I took him for the gardener
object: the first one out at dawn
plain: I said, sir, if you carried him
plain: just tell me where he's gone
""", **V(role="refrain"))
E.run("V2: the linen", """
object: I found his linen lying flat
object: the cloth that wrapped his head
object: rolled up and laid apart, alone
object: folded in a place by itself
object: rolled up and set off by itself
object: as if he'd made the bed
""", **V())
E.run("V3: the two in white", """
object: two sat in white where he had lain
object: two sat in white, a body's length
object: of empty stone between
object: two sat in white on either side
object: the stone between them clean
plain: and asked me why I cried
plain: they've taken him, I said. I turned
plain: and someone stood outside
object: one at his head, one at his feet
object: and someone stood among the trees
plain: they asked me why I cried. I turned
""", **V())
E.run("bridge: the name", """
plain: he asked me who I came to find
plain: I begged him, tell me where
plain: I said, just tell me where
plain: I begged him for the dead
plain: I said, give back my dead
plain: I said, just give me back my dead
plain: I begged him for my dead
object: I said, just give me back the body
plain: and then he only said my name
plain: Mary. And I said, Rabboni
""", **V(role="bridge"))
E.run("V4: the first garden", """
object: in the first garden God came walking
object: God walked the first garden in the evening
plain: and called out, where are you
plain: and called out, Adam, where are you
plain: in this one I was asking where
plain: I walked this one asking where
plain: all night I'd asked them where
plain: and he called me, and I knew
plain: and he answered with my name
plain: I walked this one in the dark and called
plain: and called the man he'd made by name
object: and called for the man among the trees
plain: I walked this one in the dark, asking where
plain: in this one, in the dark, I asked him where
plain: and he called me by my name
""", **V())
E.run("refrain 3 (turned)", """
plain: I took him for the gardener
object: the first one out at dawn
object: the one who walked the first garden
body: his hands in the earth again
plain: come back to tend his own
plain: I took him for the gardener, and he was
""", **V(role="refrain"))
