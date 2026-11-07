"""Song 26 writing room (v64 port, v65 fixes as ports): 'Five-Oh-One' -- the lines drafted with the writer (07:16-07:26), scored here for
the record: draft 1, draft 2 (the turn 'home' -> 'here') and draft 3 (the writer's attached suggestions). 4/4 at q = 112 on a SIXTEENTH
grid (the run's port, meter '4/4s': 16 slots a bar, stresses on the eighths, beats 1 and 3 strong): a line takes two bars (32 slots).
Both never-say lists are deaths; Rule V1 on the couplets."""
import sys; sys.path[:0] = ["/home/claude/p26", "/home/claude/carol", "/home/claude/pop"]
import engine_p26 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4s"
N = 32
def V(mate=None, **k):
    d = dict(role="verse", nslots=N, show=3, couplet=mate); d.update(k); return d
E.run("V1.1 the week (draft 1 -> 3)", """
time: clock on the wall's been dragging its feet since a quarter past two
time: five long days they've been borrowing every hour I've got
""", **V("I've been watching that second hand like it owes me money"))
E.run("V1.2 the second hand", "object: I've been watching that second hand like it owes me money", **V("five long days they've been borrowing every hour I've got"))
E.run("V1.3 the coat", "object: coat on the chair and my keys in my fist and one foot in the hall", **V("then the minute rolls over and the whole place lets out its breath"))
E.run("V1.4 the minute", "body: then the minute rolls over and the whole place lets out its breath", **V("coat on the chair and my keys in my fist and one foot in the hall"))
E.run("P1.1 speakers", "object: somebody's loading the speakers in the back of a car", role="pre", nslots=N, show=1)
E.run("P1.2 the address", "object: somebody's sending the address with a row of little flames", role="pre", nslots=N, show=1)
E.run("C.1 the tie", "object: five-oh-one, the whole town loosens its tie", role="chorus", nslots=N, show=1)
E.run("C.2 green", "object: five-oh-one, every light on the avenue's green", role="chorus", nslots=N, show=1)
E.run("C.3 sixty hours", "time: sixty hours and every single one of them's mine", role="chorus", nslots=N, show=1)
E.run("C.4 the payoff (draft 1 -> 3)", """
plain: five-oh-one, and I'm gone
plain: five-oh-one, good luck finding me now
""", role="hook", nslots=N, show=2)
E.run("H the hook", "plain: five-oh, five-oh, five-oh-one", role="hook", nslots=N, show=1)
E.run("V2.1 the radio", "object: radio's playing the song I pretended I hated in June", **V("now I'm singing every word at a red light, and so is the guy in the truck"))
E.run("V2.2 the red light", "object: now I'm singing every word at a red light, and so is the guy in the truck", **V("radio's playing the song I pretended I hated in June"))
E.run("V2.3 the arrival (draft 1 -> 3)", """
body: turn on the street and I feel it come up through the soles of my shoes
object: two blocks out and the bass is already rattling the glass
""", **V("somebody's dancing in the driveway before I've even parked"))
E.run("V2.4 the driveway (draft 1 -> 3)", """
object: string lights over the yard and the porch is already bouncing
body: somebody's dancing in the driveway before I've even parked
""", **V("two blocks out and the bass is already rattling the glass"))
E.run("P2.1 the neighbor (draft 1 -> 3)", """
object: somebody's cousin is running the music off a phone
object: the neighbor who swore he wasn't coming is dancing with a plate
""", role="pre", nslots=N, show=2)
E.run("P2.2 the grandmother", "body: somebody's grandmother's out in the middle, and she's winning", role="pre", nslots=N, show=1)
E.run("B.1-4 the days (draft 1 -> 3)", """
time: if your Monday tried to bury you, clap
time: if your Tuesday held the shovel, clap
time: if your Wednesday ran a week long, clap
time: if your Thursday wouldn't end, clap
plain: if you crawled your way to Friday on your hands and knees
plain: then you already know what time it is
""", role="breakdown", nslots=N, show=6)
E.run("L the lift", "body: look at your wrist and tell me, what does it say?", role="lift", nslots=N, show=1)
E.run("CF.4 the turn (draft 1 -> 2 -> 3)", """
plain: five-oh-one, and I'm home
plain: five-oh-one, and I'm here
plain: five-oh-one, and you'll find me here
""", role="hook", nslots=N, show=3)
E.save("/home/claude/p26/w1.json")
print("compounds:", E.COMPOUND_LOG)
