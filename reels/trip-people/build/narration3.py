"""v3: 60-second cuts. The narrator only speaks when it adds a joke the picture can't:
a one-beat setup (over a silent first second) or a button after the laugh. Never restates
what we see, never labels the relatable guy, never freezes the frame to talk.

Beat: clip, t0/t1 (clip seconds), speed (>1 tightens; pitch kept), vo=[(line, clip_time)].
A negative or early clip_time lets a line start over the previous shot's tail (J-cut).
"""

SAY = {"WanderBuddy": "Wander Buddy", "7-Eleven": "Seven Eleven"}

PARTS = {
    1: [
        dict(clip="P1_02", t0=0.0, t1=5.4, vo=[("Every group trip has the same species.", 0.05),
                                                  ("They travel in packs.", 3.65)]),
        dict(clip="P1_02b", t0=0.4, t1=2.9, vo=[("Nobody fans you.", 0.75)]),
        dict(clip="P1_03v2", t0=0.0, t1=7.2, speed=1.05,
             vo=[("A mating ritual. Or a hostage situation.", 5.85)]),
        dict(clip="P1_F", t0=0.0, t1=6.08, speed=1.04, pre=0.3, vo=[("Homo fomo.", -0.25)]),
        dict(clip="P1_A", t0=0.0, t1=5.9, pre=0.4, vo=[("Activitas maximus.", -0.35)]),
        dict(clip="P1_04", t0=1.3, t1=8.6, speed=1.1, vo=[("They will remember none of this.", 8.1)]),
        dict(clip="P1_T", t0=0.0, t1=6.08, speed=1.05, vo=[("Homo cardio.", 5.6)]),
        dict(clip="P1_06", t0=0.0, t1=5.3, speed=1.05, vo=[("Asleep by eleven. In the morning.", 4.85)]),
        # plug: walk out on the chaos, travel with people you like
        dict(clip="PL1a", t0=2.0, t1=4.9, vo=[("Or. Plan your next trip with people you actually like.", 2.1)]),
        dict(app="03-everyone-votes.png", d=2.3),
        dict(clip="PL1b", t0=0.4, t1=2.9),
        dict(outro="WanderBuddy. Choose your herd wisely."),
    ],
    2: [
        dict(clip="P2_01v3", t0=0.0, t1=6.08, speed=1.05, vo=[("Every group has a dad.", 0.05),
                                                                ("He is twenty-seven.", "END")]),
        dict(clip="P2_02", t0=0.0, t1=7.0, speed=1.1),
        dict(clip="P2_03v3", t0=0.0, t1=6.08, speed=1.05),
        dict(clip="P2_03b", t0=0.2, t1=3.8, vo=[("Across the room, another of her kind.", 0.3)]),
        dict(clip="P2_04", t0=0.0, t1=9.06, speed=1.12, vo=[("He found it. In a 7-Eleven.", 8.6)]),
        dict(clip="P2_05", t0=0.0, t1=9.06, speed=1.1, vo=[("Inside, he is screaming.", 9.0)]),
        dict(clip="P2_06", t0=0.0, t1=5.6, vo=[("His travel insurance does not cover this.", 3.0)]),
        # plug: a reel becomes the plan
        dict(clip="PL2a", t0=0.3, t1=3.3, vo=[("Or. Share a reel you actually like.", 0.45)]),
        dict(app="02-dm-a-reel.png", d=2.6, vo=[("WanderBuddy turns it into the plan.", 0.15)]),
        dict(clip="PL2b", t0=0.5, t1=3.0),
        dict(outro="WanderBuddy. Follow your reels, not the herd."),
    ],
    3: [
        dict(clip="P3_00", t0=0.0, t1=2.9, vo=[("The last day. Not everyone will make it home.", 0.1)]),
        dict(clip="P3_01", t0=0.75, t1=8.06, speed=1.1, vo=[("The shoe will never be found.", 8.0)]),
        dict(clip="P3_02", t0=0.0, t1=6.95, speed=1.05),
        dict(clip="P3_03", t0=0.0, t1=10.0, speed=1.12, vo=[("Nature has many partnerships.", 9.6)]),
        dict(clip="P3_04", t0=0.0, t1=7.0, speed=1.08),
        dict(clip="P3_05", t0=1.3, t1=4.3, vo=[("Day one.", 1.35)]),
        dict(clip="P3_05b", t0=1.4, t1=4.3, vo=[("Day four.", 1.45)]),
        dict(clip="P3_05c", t0=0.0, t1=3.7, pre=0.8, vo=[("Day nine.", -0.82), ("He will not send it later.", 2.15)]),
        dict(clip="P3_06", t0=0.3, t1=3.6, vo=[("Same trip. Same people. Every time.", 0.4)]),
        # plug: reminders, and a callback to the guy who loses everything
        dict(clip="PL3a", t0=0.5, t1=5.0, speed=1.1, vo=[("Or. Let WanderBuddy remind you before you leave.", 0.6)]),
        dict(app="06-the-vault.png", d=2.2),
        dict(clip="PL3b", t0=1.0, t1=4.4),
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
