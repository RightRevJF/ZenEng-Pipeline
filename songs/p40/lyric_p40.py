"""Nothing Else on Earth -- lyric draft 3 (locked 10 Nov: 'A'). From the parable 'The Garden That Grew by Itself' (Wild Fruit):
Lark sings to Briar. The verses are the walled garden's clean coded food, told in oblique snippets; the pre-choruses are the old man
speaking; the chorus is his sentence, the tasting list and the wholeness; the bridge is the girl at the crack in the wall; the last
chorus turns 'you' to 'she' and 'used to taste' to 'tastes'. No name from the book is said."""
TITLE = "Nothing Else on Earth"
V1 = [("verse", "Six letters stamped on every pear,"), ("verse", "a bell above the gate,"),
      ("verse", "ivy someone planted so the stone would look like welcome,"), ("verse", "a kind man at the window tells you what is safe to taste."),
      ("verse", "The food is very clean today."), ("verse", "Nobody looks fed.")]
PRE1 = [("pre", "You lean in, old as the vines,"), ("pre", "and say the first thing you've said in years:")]
CH = [("hook", "It used to taste like nothing else on earth:"), ("chorus", "honey and black pepper, rain on a hot stone,"),
      ("chorus", "bread from an oven nobody owned,"), ("chorus", "and the hands of someone gone."),
      ("hook", "It used to taste like nothing else on earth,"), ("chorus", "the bitter and the sweet grown on one vine,"),
      ("chorus", "you sat down hungry and you got up whole,"), ("chorus", "and nobody asked what it was worth.")]
V2 = [("verse", "A grey coat, a careful bite,"), ("verse", "a pleasant little nod:"),
      ("verse", "\"It reminds me of the gardens back home,\" and the whole room glows,"),
      ("verse", "and they fold another leaf of the long table, and nobody asks why."),
      ("verse", "Every plum tastes like the plum before."), ("verse", "You close your eyes.")]
PRE2 = [("pre", "You turn the bottle no one ever opened"), ("pre", "and say it to the cork instead of me:")]
BRIDGE = [("bridge", "Round the back, where the wall falls into green,"), ("bridge", "a girl with thistle on her sleeve"),
          ("bridge", "puts her whole arm through the light,"), ("bridge", "takes the shadow and the shine in one bite;"),
          ("bridge", "her face goes winter, then goes June,"), ("bridge", "and no one writes it down.")]
LAST = CH[:6] + [("chorus", "she sat down hungry and she got up whole,"), ("hook", "and it tastes like nothing else on earth."), ("tag", "Nothing else on earth.")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CH), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CH), ("Bridge", BRIDGE),
            ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
NEVER_SAY = ["aster", "briar", "clement", "flask", "moss", "lark", "thresh", "reed", "harmon", "aldric", "wren", "finch", "sable", "petra", "barrel"]
NEVER_PHRASES = ["classification", "faction", "dispensar", "the cities", "filter", "orientation", "eden", "paradise", "heaven", "holy",
                 "heart and soul", "set me free", "tears like rain", "broken wings", "fire inside", "against all odds", "meant to be", "light the way"]
import re
_words = set(re.findall(r"[a-z']+", " ".join(SUNG).lower()))
assert not any(w in _words for w in NEVER_SAY) and not any(p in " ".join(SUNG).lower() for p in NEVER_PHRASES)
