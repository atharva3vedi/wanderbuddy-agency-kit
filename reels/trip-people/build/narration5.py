"""v5 "The Kinds of Travellers": one group trip told in order across three parts.

Beat: clip, t0/t1 (clip seconds), speed (<1 = slow motion, >1 = tighter), title (intro card),
fit (B-roll: length = its narrator lines), vo = [(line, at)] where at is a clip time,
None (right after the previous line), or:
  "SETUP"  ends just before the first spoken word (a short lead-in hold only if there is no room)
  "END"    the button, just after the last spoken word
  "TAIL"   ends at the very end of the shot, leading into the next one
"""

SAY = {"WanderBuddy": "Wander Buddy", "7-Eleven": "Seven Eleven", "a.m.": "A M"}
SERIES = "The Kinds of Travellers"

PARTS = {
    1: [
        dict(clip="E1", t0=0.0, t1=7.0, title=(SERIES, "Part 1: Arrival"),
             vo=[("Every year, millions of humans travel in groups.", 0.3),
                 ("We followed one to Thailand.", None),
                 ("Outside, a local welcomes them.", "TAIL")]),
        dict(clip="P2_05", t0=0.0, t1=9.06, speed=1.18),
        dict(clip="P1_T", t0=0.0, t1=6.08, speed=1.1, vo=[("Homo cardio.", "END")]),
        dict(clip="P1_D", speed=1.08, max_hold=3.0, vo=[("At the hotel, every group has a dad.", "SETUP"),
                              ("He's twenty-seven. Loves micromanaging.", "END")]),
        dict(clip="P1_02", t0=0.0, t1=2.0, speed=0.55,
             vo=[("And here we see the leader of the pack, with her loyal subjects.", 0.05)]),
        dict(clip="P1_02", t0=2.0, t1=5.6),
        dict(clip="P1_A", t0=0.0, t1=5.9, speed=1.05, vo=[("Day two. Five a.m.", "SETUP"), ("Activitas maximus.", "END")]),
        dict(clip="B_BREAKFAST", fit=True, vo=[("Breakfast. Danny has been found.", 0.2)]),
        dict(clip="P1_06", t0=0.0, t1=5.3, speed=1.1, vo=[("Homo alcoholicus.", "END")]),
        # plug: the app ends the chaos (callback: nobody needs a dad)
        dict(clip="PL1c", t0=0.3, t1=4.6, vo=[("Or. Plan the trip together, on WanderBuddy.", 1.0)]),
        dict(app="03-everyone-votes.png", d=2.4, vo=[("Nobody needs a dad.", 0.35)]),
        dict(outro="WanderBuddy. Let the herd decide."),
    ],
    2: [
        dict(clip="E2", t0=0.0, t1=4.3, speed=0.9, title=(SERIES, "Part 2: Into the Wild"),
             vo=[("Day four. The group ventures into the wild.", 0.3),
                 ("Some travel with their young.", "TAIL")]),
        dict(clip="P1_04", t0=1.3, t1=8.6, speed=1.15, vo=[("The young will remember none of this.", "END")]),
        dict(clip="B_TEMPLE", fit=True, speed=0.8, vo=[("Others come to find themselves.", 0.2)]),
        dict(clip="P2_04", t0=0.0, t1=9.06, speed=1.18, vo=[("He found it. In a 7-Eleven.", 8.6)]),
        dict(clip="P2_03v3", t0=0.0, t1=6.08, speed=1.1, vo=[("Dinner, at the hotel.", "SETUP")]),
        dict(clip="P2_03b", t0=0.2, t1=4.4, vo=[("Across the room, another of her kind.", 0.3),
                                               ("Game recognises game.", None)]),
        dict(clip="B_BEACH", fit=True, speed=0.55, vo=[("Day five. Not a cloud for a thousand miles.", 0.2)]),
        dict(clip="P2_02", t0=0.0, t1=7.0, speed=1.15),
        dict(clip="B_SUNSET", fit=True, speed=0.85, vo=[("At sunset, the couples emerge.", 0.2)]),
        dict(clip="P1_03v2", t0=0.0, t1=7.2, speed=1.1, vo=[("A mating ritual. Or a hostage situation.", 5.85)]),
        dict(clip="B_CLIFF", fit=True, vo=[("And then, there is this one.", 0.2)]),
        dict(clip="P2_06", t0=0.0, t1=5.6, speed=1.08, vo=[("His travel insurance does not cover this.", 3.0)]),
        # plug: a reel becomes the plan
        dict(clip="PL2a", t0=0.3, t1=3.0, vo=[("Or. Share a reel you actually like.", 0.45)]),
        dict(app="02-dm-a-reel.png", d=2.6, vo=[("WanderBuddy turns it into the plan.", 0.15)]),
        dict(clip="PL2b", t0=0.5, t1=2.6),
        dict(outro="WanderBuddy. Follow your reels, not the herd."),
    ],
    3: [
        dict(clip="E3", t0=0.0, t1=3.45, speed=0.7, title=(SERIES, "Part 3: Going Home"),
             vo=[("The final days. The group must find its way home.", 0.3),
                 ("Not all of them will make it.", None)]),
        dict(clip="P1_F", t0=0.0, t1=6.08, speed=1.1, vo=[("The last beach day.", "SETUP"), ("Homo fomo.", "END")]),
        dict(clip="B_FILMING", fit=True, vo=[("Some must post everything. For validation.", 0.2)]),
        dict(clip="P3_04", t0=0.0, t1=7.0, speed=1.15),
        dict(clip="B_POOLBAR", fit=True, vo=[("At the pool bar, an unusual pairing.", 0.2)]),
        dict(clip="P3_R", speed=1.1, max_hold=2.6, vo=[("Nature has many partnerships.", "END")]),
        dict(clip="P3_FL", speed=1.1, vo=[("The last night in the city.", "SETUP"),
                               ("He can no longer feel the weight.", "END")]),
        dict(clip="P3_05", t0=0.0, t1=4.3, vo=[("Every dinner, the same ritual. Day one.", "SETUP")]),
        dict(clip="P3_05b", t0=1.4, t1=4.3, vo=[("Day four.", "SETUP")]),
        dict(clip="P3_05c", t0=0.0, t1=3.7, vo=[("Day nine.", "SETUP"), ("He will not send it later.", "END")]),
        dict(clip="P3_FG", speed=1.1, vo=[("Checkout.", "SETUP"), ("It will never be found.", "END")]),
        dict(clip="P3_06", t0=0.3, t1=3.6, vo=[("Same trip. Same people. Every time.", 0.4)]),
        # plug: a reminder, so nothing is left behind
        dict(clip="PL3a", t0=0.5, t1=5.0, speed=1.1, vo=[("Or. Let WanderBuddy remind you before you leave.", 0.6)]),
        dict(app="06-the-vault.png", d=2.2),
        dict(outro="WanderBuddy. Leave the rest of the herd at home."),
    ],
}


def all_lines() -> list[str]:
    out = []
    for beats in PARTS.values():
        for b in beats:
            out += [v[0] for v in b.get("vo", [])]
            if b.get("outro"):
                out.append(b["outro"])
    return list(dict.fromkeys(out))


def tts_text(line: str) -> str:
    for a, b in SAY.items():
        line = line.replace(a, b)
    return line
