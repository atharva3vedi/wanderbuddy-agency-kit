# Shot list for "The People You Meet On Every Trip" Pt 1-3.
# kf = Seedream keyframe prompt (first frame), refs = character models in ../characters,
# vid = Seedance 2.5 action + dialogue prompt, dur = seconds.

KF_PRE = ("Photorealistic vertical 9:16 smartphone photo, a frame from a TikTok comedy skit "
          "filmed on an iPhone, natural lighting, real skin texture, everyone is an original "
          "fictional person. ")
KF_POST = " No text, no captions, no logos, no watermark."
VID_POST = (" Keep exactly the same people, faces, outfits and setting as the first frame. "
            "Realistic, natural acting, sharp comedic timing. No background music. "
            "No subtitles, no on-screen text, no watermark.")

SAM = "Use the man from the reference image (same face, same messy brown hair, same plain grey t-shirt, same black backpack). "

SHOTS = {
    # ---------------- PART 1 ----------------
    "P1_00": dict(refs=["sam"], dur=4,
        kf=SAM + '''Medium shot. He sits slumped in a row of seats at a busy Bangkok airport departure gate, holding a giant plastic cup of iced coffee with a straw, staring straight into the camera with a dead-eyed deadpan expression. Other travellers and big windows with planes behind him.''',
        vid='''The man stares straight into the camera without blinking, slowly takes a long sip of iced coffee through the straw while keeping eye contact with the lens, then gives one slow, tired blink. Handheld camera, subtle shake. Airport ambience: a muffled boarding announcement, rolling suitcases. He does not speak.'''),
    "P1_01": dict(refs=[], dur=8,
        kf='''A wooden pier in Krabi, Thailand, turquoise water and limestone karst cliffs. In the background a white passenger ferry has just pulled away from the dock. In the foreground, facing the camera, a frazzled man in his late 20s, the group's self-appointed trip leader: neon green lanyard, a laminated printed itinerary in one hand, phone in the other, sweat patches on a light blue polo shirt, sunburnt nose, a forced, too-wide smile. Harsh midday sun.''',
        vid='''The trip leader talks to the camera with a forced, way-too-cheerful smile, gesturing back at the departing ferry, and says quickly in an American accent: "Okay! Small update. The ferry left. The backup ferry also left. Nobody panic." He pauses, his smile cracks, his eye twitches, and he screams: "I'M PANICKING!" and flings the laminated itinerary over his shoulder into the sea. Handheld camera. Waves, a ferry horn in the distance.'''),
    "P1_02": dict(refs=["bianca"], dur=6,
        kf='''Use the woman from the reference image (same face, same long dark wavy hair, same red satin dress, same sunglasses on her head). She walks confidently toward the camera through a crowded Bangkok street market, flawless, not sweating at all. Right behind her, three eager young men trail her like ducklings: one carries her handbag and a shopping bag, one holds a parasol over her head, one fans her with a paper menu. They gaze at her adoringly. Colourful market stalls, hanging lanterns, hot hazy daylight.''',
        vid='''The woman in the red dress struts slowly toward the camera through the market, unbothered. The three young men trail right behind her adoringly, one holding the parasol over her, one fanning her. Without looking back she says in a bored voice: "I'm kinda thirsty." Instantly all three men panic and sprint away in three different directions, the parasol falling to the ground. She keeps walking, unbothered. Market crowd ambience.'''),
    "P1_02b": dict(refs=["sam"], dur=4,
        kf=SAM + '''Medium close-up. He stands in a hot, crowded Bangkok street market, completely drenched in sweat, grey t-shirt soaked dark on the chest and under the arms, hair damp and stuck to his forehead, carrying his own black backpack and two heavy shopping bags, staring straight into the camera with a flat, dead-eyed deadpan expression.''',
        vid='''He stands still, drenched in sweat, breathing heavily, and stares straight into the camera with a flat deadpan expression. A drop of sweat runs down his face. He does not speak. Market ambience.'''),
    "P1_03": dict(refs=["sam"], dur=8,
        kf=SAM + '''A wooden bench on a Thai beach at sunset, golden light, palm trees. He sits squeezed in the exact middle of the bench holding a coconut with a straw, looking straight into the camera, expressionless and dead inside. On either side of him sits one half of a loved-up couple in their mid 20s (a woman in a sundress on his left, a man in a linen shirt on his right), both leaning in across him toward each other, glaring passionately at each other right in front of his face.''',
        vid='''The couple bicker intensely across the man in the middle. The woman says: "You're literally the worst." The man in the linen shirt says: "No, YOU'RE the worst." They lean in and kiss right in front of the face of the guy in the middle. The woman says: "I hate you." The man says: "I hate you more." They kiss again. The guy in the middle never moves, slowly sipping his coconut and staring into the camera, dead inside. Waves and seagulls.'''),
    "P1_04": dict(refs=["family"], dur=10,
        kf='''Use the family of four from the reference image (same faces, same outfits: the dad's bucket hat, tropical shirt and camera, the mom's white visor and tote bag, the boy with headphones and an iPad, the girl with a ponytail). They stand in front of a breathtaking ornate golden Thai temple with tiered roofs in bright sunshine. The dad throws his arms wide with wild excitement. The mom looks exhausted. The boy stares down at his iPad. The girl has her arms crossed, bored.''',
        vid='''The dad throws his arms wide toward the temple and shouts with huge excitement: "Kids! Look! This temple is eight hundred years old!" The boy, not looking up from his iPad, says flatly: "Is the wifi eight hundred years old too?" The mom, exhausted, says: "This trip cost eleven thousand dollars." The little girl, arms crossed, whines: "Can we go back to the pool?" The dad's smile slowly fades. Temple bells, tourist chatter, birds.'''),
    "P1_05": dict(refs=[], dur=10,
        kf='''On a wooden Thai longtail boat speeding over turquoise water toward limestone islands. In the foreground a smug, tanned man in his early 30s, white linen shirt unbuttoned almost to his navel, sunglasses pushed up on his head, puka shell necklace, smirking condescendingly at the camera. Behind him at the stern, the Thai boat driver, a weathered local man in his 50s, steering, giving him a flat, unimpressed look.''',
        vid='''The smug man smirks at the camera and says: "Oh, you're excited about THIS beach? Cute. I came in 2016, before it got touristy." He turns to the boat driver and says: "Actually my guy, you're saying it wrong." The driver stares at him and says flatly in a Thai accent: "I'm from here." The smug man shrugs and says: "And yet." The driver slowly turns to the camera, unimpressed. Boat engine, splashing water.'''),
    "P1_06": dict(refs=["family"], dur=6,
        kf='''Bright hotel breakfast buffet in Thailand, morning sunlight. At a table sits a man in his late 20s wearing dark sunglasses indoors and a white tank top, slumped, slurping from a huge colourful plastic bucket cocktail with four straws, a plate of untouched eggs in front of him. Standing beside the table is ONLY the mom from the reference image (white sun visor, sunglasses on her head, linen shirt, tote bag), holding a cup of coffee, staring down at him in disbelief. The rest of the family is not in this picture.''',
        vid='''The mom stares at him and says flatly: "Danny. It's breakfast." He lowers the bucket, raises it toward her like a toast and says proudly in a raspy voice: "Exactly. Most important drink of the day." He takes a loud slurp through all four straws. Breakfast restaurant ambience, cutlery clinking.'''),

    # ---------------- SHARED PLUG ----------------
    "PLUG": dict(refs=["sam"], dur=13,
        kf=SAM + '''He is now relaxed and genuinely happy for the first time. A calm, beautiful, quiet beach in Thailand at golden hour. He sits on the sand in the foreground, facing the camera, holding his phone casually in one hand. Behind him three easy-going friends (two women and one man, late 20s) relax on a blanket, laughing together. Warm, peaceful, soft light.''',
        vid='''The man looks into the camera with a small, relieved smile and speaks calmly and warmly in an American accent: "Or. Use Wander Buddy. Plan trips with people you actually want to travel with. Share your reels, get recommendations you'll actually like. And get reminders, so nobody loses their passport." Behind him his friends laugh softly. Gentle waves. Handheld, very subtle movement.'''),

    # ---------------- PART 2 ----------------
    "P2_00": dict(refs=["sam"], dur=4,
        kf=SAM + '''He looks even more exhausted: hair messier, darker circles under his eyes. He stands on a hotel balcony in Thailand at dusk, hands on the railing, palm trees and a lit-up pool party below behind him, staring straight into the camera, dead-eyed.''',
        vid='''He stares into the camera without blinking, then lets out a long, slow, defeated sigh, his shoulders dropping. Behind him, distant pool party noise and someone shrieking with laughter. He does not speak.'''),
    "P2_01": dict(refs=[], dur=9,
        kf='''A hotel lobby in Thailand. In the foreground a responsible-looking man in his late 20s, the friend group's unofficial dad: khaki shorts, a tucked-in polo shirt, a bum bag strapped across his chest, a lanyard holding six passports around his neck, a power bank in one hand, a big bottle of SPF 50 sunscreen under his arm, a red first aid kit clipped to his backpack. He points his finger, counting heads, very focused. Beside him a carefree friend in a tank top and flip-flops, rolling his eyes.''',
        vid='''The responsible man counts heads, pointing his finger: "Eleven, twelve, thirteen... where's Danny?" The friend in the tank top rolls his eyes and says: "Bro, you're not my dad." The responsible man turns to him and says calmly, holding up items one by one: "Then why do I have your passport, your charger, and your EpiPen?" The friend goes silent. Hotel lobby ambience.'''),
    "P2_02": dict(refs=[], dur=8,
        kf='''A blazing hot, sunny Thai beach, perfect cloudless blue sky, people sunbathing. In the foreground a young woman in her mid 20s wearing a full yellow rain poncho with the hood up and rubber rain boots, nervously checking the weather on her phone, holding a second phone in her other hand. Next to her, her friend in a swimsuit and sunglasses lies on a beach towel, staring at her in disbelief.''',
        vid='''The woman in the poncho stares at her phone and says nervously: "Thirty percent chance of rain at three fifteen." Her friend in sunglasses says: "It's literally sunny." The woman in the poncho narrows her eyes at the sky and says ominously: "For now." She pulls out a folded umbrella and pops it open. Waves, beach ambience.'''),
    "P2_03a": dict(refs=[], dur=8,
        kf='''An elegant upscale hotel restaurant in Thailand, white tablecloths, candles. A smiling waiter in a white jacket stands beside a table where a cheerful middle-aged Indian aunty in a colourful salwar kameez and reading glasses sits holding a leather menu. On the chair next to her rests a large rolling suitcase.''',
        vid='''The aunty reads the menu, her eyes go wide at the price, and she says in an Indian accent: "Twenty-eight dollars? For noodles?" She closes the menu, smiles politely at the waiter, lifts the suitcase onto the table and unzips it, revealing it is packed full of homemade food: stacks of flatbreads in foil, jars of pickle, instant noodle packs and a small rice cooker. She says sweetly: "Beta, I brought nine days of food." The waiter freezes. Restaurant ambience.'''),
    "P2_03b": dict(refs=[], dur=5,
        kf='''An elegant upscale hotel restaurant in Thailand, white tablecloths, candles. At a table sits an elderly East Asian grandma in a sun hat and a floral blouse. On her table is an open suitcase packed full of instant noodle cups, jars of kimchi and a small electric rice cooker. She is looking across the room toward the camera with a serious, knowing expression.''',
        vid='''The grandma slowly looks up across the room toward the camera, as if meeting someone's eyes, and gives one slow, deeply respectful nod. Then she calmly plugs in her rice cooker. Quiet restaurant ambience. She does not speak.'''),
    "P2_04": dict(refs=[], dur=9,
        kf='''Close-up of a white man in his mid 20s with a man bun, a wispy beard and beaded bracelets, wearing a loose tank top and patterned elephant pants, eyes closed in spiritual bliss, holding a grilled ham-and-cheese toastie in a paper wrapper near his mouth. He is inside a brightly lit convenience store with no brand logos, a drinks fridge blurred behind him.''',
        vid='''He opens his eyes, presses his palms together, bows deeply to the camera and says earnestly: "Sawasdee krap. I'm not a tourist. I'm a traveller." He takes a slow bite of the toastie, closes his eyes in ecstasy and says: "Wow. The most authentic thing I've ever eaten." The camera slowly pulls back to reveal he is standing in a fluorescent-lit convenience store aisle, a bored cashier watching him. A shop door chime.'''),
    "P2_05": dict(refs=[], dur=9,
        kf='''A busy Bangkok street. A colourful tuk-tuk is parked at the curb. The Thai driver, a man in his 40s with a cap and a polo shirt, stands beside it with a huge, warm, salesman smile and arms open toward a group of sunburnt tourists with backpacks.''',
        vid='''The driver beams at the tourists and says enthusiastically in a Thai accent: "Welcome my friend! Best price! Very special for you!" The tourists climb into the tuk-tuk. The driver turns to the camera, his smile switches off completely, and he says flatly: "Every year. More of you." Then he turns back, smile on full blast, and shouts cheerfully: "Seatbelt? No seatbelt!" Traffic, horns, scooters.'''),
    "P2_06": dict(refs=[], dur=6,
        kf='''The edge of a rocky cliff above deep turquoise sea in Krabi, Thailand. A shirtless, muscular man in his mid 20s with a GoPro strapped to his forehead and board shorts, gripping an energy drink can, bouncing with hyperactive energy near the edge. Beside him a calm local Thai guide in a cap and rash guard, arms crossed.''',
        vid='''The shirtless man asks excitedly: "How high is it?" The guide says flatly: "Too high." The shirtless man yells: "SAY LESS!", crushes the can and sprints forward, leaping off the cliff edge out of frame toward the water far below. The guide sighs and slowly turns to look at the camera. Wind, a distant splash.'''),
    "INS_B": dict(refs=["sam"], dur=4,
        kf=SAM + '''Sunburnt, he stands on a cliff top in Krabi with the turquoise sea behind him, holding his backpack straps, staring straight into the camera, deadpan and unimpressed.''',
        vid='''He stares into the camera, deadpan, then slowly shakes his head once. Wind. He does not speak.'''),

    # ---------------- PART 3 ----------------
    "P3_00": dict(refs=["sam"], dur=4,
        kf=SAM + '''He sits alone on the floor of an airport departures hall, back against a wall, hugging his black backpack tightly to his chest like a life jacket, staring straight into the camera, dead-eyed and haunted.''',
        vid='''He hugs his backpack tighter and stares into the camera without blinking. His eye twitches slightly. He does not speak. Airport ambience.'''),
    "P3_01": dict(refs=[], dur=8,
        kf='''A hotel reception desk in Thailand at checkout. A scruffy young man in his mid 20s in a wrinkled Hawaiian shirt and shorts, wearing only ONE flip-flop with his other foot bare, holds a smartphone to his ear while frantically patting his pockets. Behind him his friends with suitcases stare at him.''',
        vid='''The man, holding the phone to his ear, says in a panic: "Guys, I can't find my phone." His friends stare at the phone in his hand. He keeps patting his pockets and says: "Also my wallet. And my passport. And..." He looks down at his bare foot and says: "Where's my other shoe?" Hotel lobby ambience.'''),
    "P3_02": dict(refs=[], dur=7,
        kf='''A busy Bangkok street with scooters. A young man in his 20s dripping in bling: several thick gold chains, an iced-out diamond watch, a flashy monogram-pattern shirt with no real brand logos, white sunglasses, filming himself on his phone held at arm's length, grinning and showing off. Scooters pass behind him.''',
        vid='''He films himself and says loudly to his phone: "Yo chat, this place is SO safe. Look at the drip." A scooter zooms past right behind him and in a blur his gold chains are gone from his neck. He freezes, touches his bare neck, and says quietly: "It WAS safe." Traffic, a scooter whoosh.'''),
    "P3_03": dict(refs=[], dur=10,
        kf='''A luxury resort pool bar in Phuket. A 62-year-old deeply tanned man with slicked-back silver hair, an open Hawaiian shirt, a gold chain and a cocktail, proudly wraps his arm around a glamorous young woman in her mid 20s in a white sundress with big sunglasses on her head, chewing gum, bored, scrolling her phone. They face the camera as if being introduced to the group.''',
        vid='''The older man says proudly: "Everyone, this is my girlfriend. We met... recently." The young woman looks up and says brightly: "Hi! I'm..." She glances at him and whispers: "What did we say my name was?" He whispers: "Crystal." She says cheerfully: "Crystal!" Then she checks her watch and says: "Babe, that's two hours. Same card?" He starts sweating. Pool bar ambience.'''),
    "P3_04": dict(refs=[], dur=8,
        kf='''A beach at golden hour. In the foreground a young woman in her 20s, a content creator, stands behind a tripod with a phone and a ring light, directing. In the background a group of five friends stand waist-deep in the sea, soaked, sunburnt and miserable.''',
        vid='''The content creator calls out cheerfully: "Okay, one more take! Walk into the ocean again, but candid." A soaked friend in the water shouts back: "That was take forty-seven!" She thinks for a second and says: "Candid-er." The friends groan and trudge back out of the water. Waves.'''),
    "P3_05": dict(refs=[], dur=5,
        kf='''A busy Thai seafood restaurant at night, a group of friends around a table full of empty plates. The waiter has just placed the bill folder on the table. A guy in his late 20s in a backwards cap leans back, patting his pockets with a fake confused look, turning to the friend next to him.''',
        vid='''The guy pats his pockets and says casually to his friend: "Can you get this one? I'll send it later." He gives a confident thumbs up and leans back. Restaurant ambience.'''),
    "P3_06": dict(refs=["sam", "bianca", "family"], dur=6,
        kf='''The man from image 1 (messy brown hair, plain grey t-shirt, black backpack) stands in the exact centre, staring straight into the camera, completely deadpan. Around him in an airport departures hall, total chaos from his travel group: a sweaty trip leader with a neon lanyard crying into a laminated itinerary, a guy in sunglasses holding a bucket cocktail at the check-in desk, a guy wearing only one flip-flop, three young men struggling to carry a mountain of suitcases for the woman in the red dress from image 2, the two kids from image 3 glued to their iPads while their sunburnt dad photographs everything, a woman in a yellow rain poncho.''',
        vid='''Chaos continues all around him: the trip leader sobs, the young men drop the suitcases, people bump into each other. The man in the centre does not move at all. He stares into the camera for a very long time, then slowly blinks. Airport ambience and commotion.'''),
}

# Text-only descriptions of the 3 character models (BytePlus blocks realistic faces as image
# input on Seedance 2.x, so recurring characters are carried by these exact words in t2v mode).
SAM_DESC = ("a lanky man about 30 with messy, shaggy medium-length brown hair, light stubble, pale "
            "skin, tired eyes with dark circles, wearing a plain heather-grey crew-neck t-shirt, dark "
            "blue jeans and white sneakers, a small black backpack on one shoulder")
BIANCA_DESC = ("a glamorous woman in her late 20s with long dark brown wavy hair, wearing a fitted red "
               "satin midi dress with thin straps, gold hoop earrings, black sunglasses pushed up on "
               "her head, strappy heels and a small cream handbag")
FAMILY_DESC = ("an American tourist family of four: a sunburnt dad in his mid 40s in a khaki bucket hat, "
               "a loud tropical print shirt, cargo shorts, socks with sandals and a big camera round his "
               "neck; a tired mom in her mid 40s in a white sun visor, linen shirt and big canvas tote; a "
               "12-year-old boy with headphones round his neck staring at an iPad; a 9-year-old girl "
               "with a ponytail, arms crossed")

SHOTS["P1_00"]["kf_t2v"] = ("Medium shot of " + SAM_DESC + ". He sits slumped in a row of seats at a busy "
    "Bangkok airport departure gate, holding a giant plastic cup of iced coffee with a straw, staring "
    "straight into the camera with a dead-eyed deadpan expression. Other travellers and big windows "
    "with planes behind him.")
SHOTS["P1_02"]["kf_t2v"] = ("A crowded Bangkok street market in hot hazy daylight, colourful stalls and "
    "hanging lanterns. Walking confidently toward the camera is " + BIANCA_DESC + ", flawless, not "
    "sweating at all. Right behind her three eager young men trail her like ducklings: one carries her "
    "handbag and a shopping bag, one holds a parasol over her head, one fans her with a paper menu, all "
    "gazing at her adoringly.")
SHOTS["P1_04"]["kf_t2v"] = ("In front of a breathtaking ornate golden Thai temple with tiered roofs in "
    "bright sunshine stands " + FAMILY_DESC + ". The dad throws his arms wide with wild excitement, the "
    "mom looks exhausted, the boy stares down at his iPad, the girl is bored.")

# P2_06 reworded: the first version tripped BytePlus's text filter (read as self-harm).
SHOTS["P2_06"]["kf"] = ("A popular cliff-jumping spot in Krabi, Thailand: a rocky ledge a few metres above "
    "deep, calm turquoise water where happy tourists are swimming and floating below. On the ledge a "
    "shirtless, muscular man in his mid 20s with a GoPro strapped to his forehead and board shorts, "
    "holding an energy drink can, bouncing with hyperactive excitement. Beside him a calm local Thai "
    "guide in a cap and rash guard, arms crossed.")
SHOTS["P2_06"]["vid"] = ('''The excited man asks: "How high is it?" The guide says flatly: "Too high." The man yells happily: "SAY LESS!", crushes the can, runs and does a huge cannonball jump into the deep water below, whooping, with a big fun splash. The guide sighs and slowly turns to look at the camera. Wind, a splash, people cheering in the water.''')

# Sam v2: the first t2v Sam read as gaunt/ill. He is a likeable, normal, mildly tired everyman.
SAM_DESC = ("an average-looking, friendly man about 30, tall with a slight slouch, healthy skin, messy "
            "medium-length brown hair, light stubble, mildly tired and unimpressed eyes, wearing a plain "
            "heather-grey crew-neck t-shirt, dark blue jeans and white sneakers, a small black backpack "
            "on one shoulder")
SHOTS["P1_00"]["kf_t2v"] = ("Medium shot of " + SAM_DESC + ". He sits slumped in a row of seats at a busy "
    "Bangkok airport departure gate, holding a giant plastic cup of iced coffee with a straw, staring "
    "straight into the camera with a flat, deadpan, unimpressed expression, like a guy in a mockumentary "
    "sitcom looking at the camera. Other travellers and big windows with planes behind him.")

# Recurring characters in ref mode: each references its own master clip (masters.json).
for _sid in ["P1_02b", "P1_03", "PLUG", "P2_00", "INS_B", "P3_00", "P3_06"]:
    SHOTS[_sid]["refvid"] = ["sam"]
SHOTS["P3_06"]["kf_ref"] = ("The man from the reference video (same face, same messy brown hair, same plain "
    "grey t-shirt, same black backpack) stands in the exact centre of a busy airport departures hall, "
    "staring straight into the camera, completely deadpan. All around him, total chaos from his travel "
    "group: a sweaty trip leader with a neon lanyard sobbing into a laminated itinerary, a guy in "
    "sunglasses holding a rainbow bucket cocktail at the check-in desk, a guy wearing only one flip-flop, "
    "three young men struggling under a mountain of suitcases behind " + BIANCA_DESC + ", a sunburnt dad "
    "in a bucket hat and tropical shirt photographing everything while his two kids stare at iPads, and "
    "a woman in a yellow rain poncho.")


from shots_v2 import V2 as _V2  # noqa: E402

SHOTS.update(_V2)

from shots_v3 import V3 as _V3  # noqa: E402

SHOTS.update(_V3)

from shots_v5 import V5 as _V5  # noqa: E402

SHOTS.update(_V5)

from shots_v5b import V5B as _V5B  # noqa: E402

SHOTS.update(_V5B)
