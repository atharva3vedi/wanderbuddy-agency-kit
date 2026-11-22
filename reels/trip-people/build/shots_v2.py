# v2 (documentary cut): re-staged couple, new bill-dodger days, per-part plugs, music beds.
# Imported at the bottom of shots.py.

REF_SAM = ("The man from the reference video (same face, same messy brown hair, same plain grey "
           "t-shirt, same black backpack)")
MUSIC_POST = " Instrumental music only. No speech, no voices, no singing, no narration, no on-screen text."

V2 = {
    # couple re-staged: both on ONE side of him, facing each other, so the kiss is clearly theirs
    "P1_03v2": dict(refs=[], refvid=["sam"], dur=8, kf="",
        kf_ref=REF_SAM + ''' is squashed against the right-hand armrest of a wooden bench on a Thai beach at sunset, golden light, palm trees, holding a coconut with a straw, staring straight into the camera, dead inside. Pressed up against his left side, a loved-up couple in their mid 20s (a woman in a floral sundress and a man in a linen shirt) sit facing EACH OTHER in profile, nose to nose, hogging the bench. He is clearly not part of their moment.''',
        vid='''The couple bicker nose to nose, facing each other. The woman says: "You're literally the worst." The man says: "No, YOU'RE the worst." They kiss each other passionately, in profile, away from him. The woman says: "I hate you." The man says: "I hate you more." They kiss each other again. The man squashed against the armrest leans even further away, slowly sips his coconut and keeps staring into the camera, dead inside. Waves and seagulls.'''),
    "P3_05b": dict(refs=[], refvid=["kevin"], dur=5, kf="",
        kf_ref='''The same guy as in the reference video (backwards cap, same face, same t-shirt), now at a sandy beach-shack bar in the afternoon with the same friends, empty cocktail glasses and a small tray with the bill in front of him, the sea behind.''',
        vid='''The guy pats his pockets and says casually to his friend: "Can you get this one? I'll send it later." He gives a confident thumbs up and leans back. Beach bar ambience, waves.'''),
    "P3_05c": dict(refs=[], refvid=["kevin"], dur=5, kf="",
        kf_ref='''The same guy as in the reference video (backwards cap, same face, same t-shirt), now at a busy airport cafe on the last day of the trip, suitcases next to the table, coffee cups and a receipt in front of him, the same friends looking at him with dead eyes.''',
        vid='''The guy pats his pockets and says casually to his friend: "Can you get this one? I'll send it later." He gives a confident thumbs up. His friends stare at him. Airport cafe ambience, a boarding announcement.'''),
    "PL1a": dict(refs=[], refvid=["sam"], dur=5, kf="",
        kf_ref=REF_SAM + ''' sits on a sofa in a messy hostel common room in Bangkok, surrounded by his chaotic travel group: a sweaty guy with a lanyard crying over a laminated itinerary, a guy in sunglasses holding a rainbow bucket drink, people shouting and arguing.''',
        vid='''Chaos all around him. He calmly stands up, puts on his backpack and walks out of the room through the door without a word, as the arguing continues behind him. Loud overlapping arguing, music from a speaker.'''),
    "PL1b": dict(refs=[], refvid=["sam"], dur=6, kf="",
        kf_ref=REF_SAM + ''', relaxed and genuinely happy for the first time, sits at the front of a wooden longtail boat gliding over calm turquoise water at golden hour between limestone islands, with three easy-going friends (two women and one man, late 20s), everyone laughing.''',
        vid='''He laughs with his friends. One friend hands him a slice of mango. He leans back, closes his eyes and smiles in the warm sun. Peaceful. Boat engine hum, water lapping, soft laughter, no clear words.'''),
    "PL2a": dict(refs=[], refvid=["sam"], dur=5, kf="",
        kf_ref=REF_SAM + ''' lies in a hammock between two palm trees outside a quiet beach bungalow in Thailand, scrolling on his phone, the phone screen facing away from the camera.''',
        vid='''He scrolls, stops on something he likes, smiles slightly, and taps the screen to share it. Gentle waves, birds. He does not speak.'''),
    "PL2b": dict(refs=[], refvid=["sam"], dur=6, kf="",
        kf_ref=REF_SAM + ''' swims with three happy friends in a stunning hidden emerald lagoon surrounded by jungle cliffs and a small waterfall in Krabi, Thailand, bright sunshine.''',
        vid='''He surfaces from the water laughing and pushes his wet hair back. A friend splashes him and they all float and laugh together near the waterfall. Water splashing, laughter, birds, no clear words.'''),
    "PL3a": dict(refs=[], refvid=["sam"], dur=5, kf="",
        kf_ref=REF_SAM + ''' stands in a tidy hotel room in Thailand calmly packing his backpack. His phone lies on the bed, screen facing away from the camera.''',
        vid='''His phone buzzes on the bed. He glances at it and nods, opens the bedside drawer, takes out his passport, holds it up toward the camera with a small satisfied smile, and tucks it into his backpack. A phone buzz, quiet room tone. He does not speak.'''),
    "PL3b": dict(refs=[], refvid=["sam", "tom"], dur=6, kf="",
        kf_ref='''The man from reference video 1 (messy brown hair, plain grey t-shirt, black backpack) walks calmly toward the camera through a bright, modern airport terminal, relaxed, passport and boarding pass in hand. In the background behind him, the man from reference video 2 (wrinkled Hawaiian shirt, wearing only ONE flip-flop) runs past in total panic, patting his pockets.''',
        vid='''The calm man walks toward the camera and gives a tiny satisfied nod. Behind him the panicked man sprints across the terminal shouting: "Has anyone seen my passport?!" Airport ambience, a boarding announcement.'''),
    "MUSIC_A": dict(refs=[], dur=15, res="480p", post=MUSIC_POST, kf="",
        kf_t2v='''A slow, static wide shot of misty jungle and limestone cliffs in Thailand at dawn, birds gliding.''',
        vid='''Soundtrack: a playful, curious, light orchestral nature-documentary score: plucked pizzicato strings, soft woodwinds and a gentle bassoon, sneaky and comedic, steady tempo.'''),
    "MUSIC_B": dict(refs=[], dur=15, res="480p", post=MUSIC_POST, kf="",
        kf_t2v='''A slow aerial drone shot gliding over turquoise sea and green islands in Thailand at golden hour.''',
        vid='''Soundtrack: an emotional, sweeping, uplifting orchestral nature-documentary score: soaring strings and warm French horns building to a grand, hopeful swell.'''),
}
