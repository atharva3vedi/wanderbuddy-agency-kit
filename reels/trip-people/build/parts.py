"""Edit decision list for Pt 1/2/3. Caption lines use the script's spelling, timed from the
faster-whisper word timings in transcripts/ (seconds from the segment's own start, after trim)."""

from pathlib import Path

PLAY = Path(__file__).resolve().parents[4] / "store/graphics/appstore/play"
HOOK = "EVERY GROUP TRIP HAS THESE PEOPLE"
MID = 1080  # y-centre for mid-screen supers

# whisper fallbacks only; every dialogue clip below has explicit lines
CAPTION_FIXES: dict = {}

PLUG = dict(clip="PLUG", label=None, lines=[
    ("Or. Use WanderBuddy.", 0.0, 2.6), ("Plan trips with people", 2.8, 3.95),
    ("you actually want to travel with.", 3.95, 5.65), ("Share your reels,", 5.8, 7.25),
    ("get recommendations you'll actually like.", 7.3, 9.55), ("And get reminders,", 9.65, 10.65),
    ("so nobody loses their passport.", 10.65, 12.9)], pops=[
    (str(PLAY / "03-everyone-votes.png"), 2.8, 5.75),
    (str(PLAY / "02-dm-a-reel.png"), 5.8, 9.6),
    (str(PLAY / "06-the-vault.png"), 9.65, 13.1),
])

PARTS = {
    1: [
        dict(clip="P1_00", hook=HOOK, tag="PT 1", caps=False),
        dict(clip="P1_01", label="THE TRIP CAPTAIN", sub="complete crash out", lines=[
            ("Okay! Small update.", 0.0, 1.6), ("The ferry left.", 1.7, 2.62),
            ("The backup ferry also left.", 2.66, 4.15), ("Nobody panic.", 4.2, 5.5),
            ("I'M PANICKING!", 5.6, 8.0)]),
        dict(clip="P1_02", label="THE ONE IN THE RED DRESS", lines=[("I'm kinda thirsty.", 2.05, 3.9)],
             supers=[("+ HER SIMPS\n(they came as a set)", 3.9, 6.1, 64, 1450)]),
        dict(clip="P1_02b", caps=False, supers=[("me, carrying my own bags", 0.6, 4.0, 58, 1450)]),
        dict(clip="P1_03", label="THE COUPLE", sub="madly in love, constantly at war", lines=[
            ("You're literally the worst.", 0.0, 1.55), ("No, YOU'RE the worst.", 1.66, 3.1),
            ("I hate you.", 3.9, 4.98), ("I hate you more.", 5.05, 6.6)]),
        dict(clip="P1_04", label="THE FAMILY", sub="and the kids who won't remember any of it", lines=[
            ("Kids! Look!", 0.0, 1.3), ("This temple is 800 years old!", 1.35, 3.3),
            ("Is the wifi 800 years old too?", 3.35, 5.05), ("This trip cost $11,000.", 5.1, 6.85),
            ("Can we go back to the pool?", 6.9, 8.3)],
             supers=[("THEY WILL REMEMBER\nNONE OF THIS.", 8.35, 10.1, 70, MID)]),
        dict(card="“wait, we went to Thailand?”", card_sub="2041", dur=1.9),
        dict(clip="P1_05", label="THE ONE WHO'S BEEN HERE BEFORE", trim=(0.0, 9.6), lines=[
            ("Oh, you're excited about THIS beach?", 0.35, 2.2), ("Cute.", 2.25, 2.78),
            ("I came in 2016,", 2.8, 3.56), ("before it got touristy.", 3.57, 5.08),
            ("Actually my guy,", 5.12, 5.72), ("you're saying it wrong.", 5.74, 6.75),
            ("I'm from here.", 6.8, 7.95), ("And yet.", 8.0, 9.6)]),
        dict(clip="P1_06", label="THE ONE WHO'S ALWAYS DRINKING", lines=[
            ("Danny. It's breakfast.", 0.0, 1.9), ("Exactly.", 1.9, 2.72),
            ("Most important drink of the day.", 2.74, 5.4)]),
        PLUG,
    ],
    2: [
        dict(clip="P2_00", hook=HOOK, tag="PT 2: THEY MULTIPLIED", caps=False),
        dict(clip="P2_01", label="THE GROUP DAD", sub="27, not anyone's dad", lines=[
            ("Eleven, twelve, thirteen.", 0.0, 1.86), ("Where's Danny?", 1.88, 2.4),
            ("Bro, you're not my dad.", 2.4, 3.9), ("Then why do I have your passport,", 4.9, 6.62),
            ("your charger,", 6.62, 7.05), ("and your EpiPen?", 7.05, 8.9)]),
        dict(clip="P2_02", label="THE WEATHER FREAK", lines=[
            ("30% chance of rain at 3:15.", 0.0, 2.45), ("It's literally sunny.", 2.55, 4.1),
            ("For now.", 5.7, 7.6)]),
        dict(clip="P2_03a", label="THE ONES WHO PACKED THEIR OWN FOOD", lines=[
            ("$28? For noodles?", 1.1, 3.7), ("Beta, I brought nine days of food.", 5.55, 8.06)]),
        dict(clip="P2_03b", label="THE ONES WHO PACKED THEIR OWN FOOD", caps=False,
             supers=[("*mutual respect*", 1.3, 5.0, 64, 1450)]),
        dict(clip="P2_04", label="THE ONE WHO'S HERE FOR THE CULTURE", lines=[
            ("Sawasdee krap.", 0.0, 1.5), ("I'm not a tourist.", 1.6, 2.7), ("I'm a traveller.", 2.86, 4.3),
            ("Wow.", 4.9, 5.95), ("The most authentic thing I've ever eaten.", 6.25, 8.7)],
             supers=[("(it's a 7-Eleven toastie)", 8.0, 9.06, 58, MID)]),
        dict(clip="P2_05", label="THE LOCAL WHO HATES TOURISTS", sub="but has rent to pay", lines=[
            ("Welcome my friend!", 0.0, 1.5), ("Best price! Very special for you!", 1.5, 4.12),
            ("Every year. More of you.", 4.14, 7.22), ("Seatbelt? No seatbelt!", 7.24, 9.06)]),
        dict(clip="P2_06", label="THE ADRENALINE JUNKIE", lines=[
            ("How high is it?", 0.0, 1.32), ("Too high.", 1.36, 1.96), ("SAY LESS!", 1.98, 3.2)]),
        dict(clip="INS_B", caps=False),
        PLUG,
    ],
    3: [
        dict(clip="P3_00", hook=HOOK, tag="PT 3: I SHOULD'VE STAYED HOME", caps=False),
        dict(clip="P3_01", label="THE ONE WHO LOSES EVERYTHING", lines=[
            ("Guys, I can't find my phone.", 0.85, 2.55), ("Also my wallet.", 2.6, 4.15),
            ("And my passport.", 4.15, 5.12), ("And... where's my other shoe?", 5.14, 8.06)]),
        dict(clip="P3_02", label="THE FLASHY ONE", lines=[
            ("Yo chat, this place is SO safe.", 0.0, 2.45), ("Look at the drip.", 2.46, 3.9),
            ("It WAS safe.", 5.8, 7.07)]),
        dict(clip="P3_03", label='THE GUY AND HIS "GIRLFRIEND"', lines=[
            ("Everyone, this is my girlfriend.", 0.0, 1.98), ("We met... recently.", 2.06, 3.5),
            ("Hi! I'm...", 3.5, 5.06), ("What did we say my name was?", 5.08, 6.3),
            ("Crystal.", 6.3, 6.74), ("Crystal!", 6.74, 7.46), ("Babe, that's two hours.", 7.5, 8.82),
            ("Same card?", 8.82, 10.08)]),
        dict(clip="P3_04", label="THE CONTENT CREATOR", lines=[
            ("Okay, one more take!", 0.0, 1.55), ("Walk into the ocean again,", 1.6, 2.64),
            ("but candid.", 2.64, 3.62), ("That was take 47!", 3.66, 5.6), ("Candid-er.", 6.3, 8.06)]),
        dict(clip="P3_05", label='THE "I\'LL SEND IT LATER" GUY', lines=[
            ("Can you get this one?", 2.05, 3.22), ("I'll send it later.", 3.22, 4.6)],
             supers=[("DAY 1", 0.0, 5.06, 96, 1180)]),
        dict(clip="P3_05", label='THE "I\'LL SEND IT LATER" GUY', trim=(1.9, 4.4), lines=[
            ("Can you get this one?", 0.15, 1.32), ("I'll send it later.", 1.32, 2.5)],
             supers=[("DAY 4", 0.0, 2.5, 96, 1180)]),
        dict(clip="P3_05", label='THE "I\'LL SEND IT LATER" GUY', trim=(1.9, 5.06), lines=[
            ("Can you get this one?", 0.15, 1.32), ("I'll send it later.", 1.32, 2.2)],
             supers=[("DAY 9", 0.0, 3.16, 96, 1180)]),
        dict(card="HE DID NOT SEND IT LATER.", dur=1.6),
        dict(clip="P3_06", caps=False, supers=[("SAME TRIP.\nSAME PEOPLE.\nEVERY TIME.", 0.8, 6.1, 80, MID)]),
        PLUG,
    ],
}
