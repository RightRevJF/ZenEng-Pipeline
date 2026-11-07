"""Song 28 writing room (v64 port, v65 fixes as ports): 'Tinted Glass' -- the lines drafted with the writer (14:11-14:38), scored for
the record and to flag weak lines before the music (his choice C). 6/8 at dotted-q = 54, verses and bridge a line in four bars (24 eighths; his choice A), the chorus a line in two bars (12 eighths)."""
import sys; sys.path[:0] = ["/home/claude/p28", "/home/claude/carol", "/home/claude/pop"]
import engine_p28 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "6/8"
def V(**k):
    d = dict(role="verse", nslots=24, show=10); d.update(k); return d
E.run("V1 him: the car (drafts 1-5)", """
plain: I said that I was out visiting the sick
object: and parked where the lot runs out of light
body: you had your shoes off and the seat laid down
object: you put the cardboard beach up in the windshield
object: on the top deck at the furniture company
object: you'd pressed black vinyl over every window
plain: we made a Tuesday afternoon into night
object: and we were twenty under a paper sun
plain: and we were twenty in the dark at noon
""", **V())
E.run("V2 her: the car (drafts 1-5)", """
plain: I mark up other people's words all day
object: and lost all of mine in my own car
object: my rings went in the cup with the red pens
object: I kept the shades rolled up with my red pens
body: you laughed when your glasses fogged
body: your hands were shaking worse than mine
body: and I swear I could hear your heart
plain: and after you left I'd count to six hundred
object: and we'd pull the shades down together
""", **V())
E.run("V3 him: the theater (drafts 1-5)", """
object: past the county line, a door with no name
object: we paid a stranger for the dark
object: we paid in quarters for the dark
object: we paid in dollars for the dark
plain: then I drove home and couldn't sleep
object: and wrote fourteen lines about your laugh
""", **V())
E.run("V4 her: the theater (drafts 1-5)", """
object: the screen was showing somebody else's love
object: the screen was full of strangers, loud and bored
plain: we never once looked up
body: you hummed a hymn into my neck
body: you spread your jacket on the seat for me
body: we got the giggles like two kids in the back row
body: you held my face like something holy
body: you held my face like you were memorizing it
plain: and for once in my life it was enough
""", **V())
E.run("Bridge: caught (drafts 1-5)", """
object: he took my watch while I was in the shower
object: and read every line I ever wrote you
object: he didn't shout, he laid it on the table
object: my phone lit up with nothing but his name
plain: he read them all and never made a sound
object: that Sunday he was waiting at the door
object: he plugged my watch in by my side of the bed
body: he shook my hand and said he liked the words
""", **V(role="bridge"))
E.run("V5 him: going home", """
object: Sundays I still say the words they pay me for
object: my wife still waves from the second row
object: it's a good life, I built it board by board
object: and I know where every road in it goes
""", **V())
E.run("V6 her: going home", """
object: he never brought the watch up again
object: he still pours my coffee before the sun
object: there's a red pen and a stack of papers
object: I traded the car for one with clear glass
plain: and I know how every day will run
""", **V())
E.run("Chorus (drafts 1-5)", """
object: behind the tinted glass
plain: the world went dark and small
body: I knew you by your breathing
plain: and I loved you, that was all
plain: the world looked far away
object: I couldn't see the people
plain: we'd have to face someday
plain: the world is safe and small
body: I still know you by your breathing
object: I still fog the window on your street
plain: and I never make the call
""", role="chorus", nslots=12, show=12)
E.save("/home/claude/p28/w1.json")
print("compounds:", E.COMPOUND_LOG)
