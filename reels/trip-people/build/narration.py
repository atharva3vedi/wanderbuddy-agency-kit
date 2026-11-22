"""Documentary cut (v2): a British nature-documentary narrator over the same scenes.

Beat fields:
  clip    clip id in ../clips; t0/t1 trim (clip seconds)
  intro   lines read over a held first frame before the clip plays (frame holds, slow pull-out)
  vo      [(line, clip_time | None)]: None = straight after the previous line
  app     a real Play-store frame instead of a clip (slow push-in, dissolves in and out)
  outro   the brand outro with the closing line
Lines are captions; TTS spelling fixes live in SAY.
"""

SAY = {"WanderBuddy": "Wander Buddy", "7-Eleven": "Seven Eleven"}

PARTS = {
    1: [
        dict(clip="P1_00", vo=[("Every group trip has the same species.", 0.2),
                               ("This is the normal one. He is already tired.", None)]),
        dict(clip="P1_01", intro=["The trip captain. He has laminated the itinerary."],
             vo=[("And so, the itinerary returns to the sea.", 6.75)]),
        dict(clip="P1_02", intro=["The red dress. Thirty-eight degrees."],
             vo=[("Not one drop of sweat.", 0.1), ("Her simps respond instantly. They came as a set.", 3.5)]),
        dict(clip="P1_02b", vo=[("Meanwhile, the normal one carries his own bags.", 0.3)]),
        dict(clip="P1_03v2", intro=["The couple. Bonded for life."],
             vo=[("A mating ritual? Or a hostage situation?", "END")]),
        dict(clip="P1_04", intro=["The family. Two adults, and their two young."],
             vo=[("The young will remember none of this.", 8.15)]),
        dict(clip="P1_05", t1=9.3, intro=["The one who has been here before."],
             vo=[("The locals have asked him to stop coming back. He has not.", 9.15)]),
        dict(clip="P1_06", intro=["Danny. A creature of habit."],
             vo=[("He will be asleep by eleven. In the morning.", 4.95)]),
        # plug: the normal one escapes the herd
        dict(clip="PL1a", vo=[("But every so often, one member of the herd breaks away.", 0.2)]),
        dict(app="03-everyone-votes.png", vo=["He has found WanderBuddy.",
                                              "Now he only travels with the people he actually likes."]),
        dict(clip="PL1b", vo=[("No captain. No crash outs.", 0.3), ("A small, happy herd. Thriving.", None)]),
        dict(outro="WanderBuddy. Choose your herd wisely."),
    ],
    2: [
        dict(clip="P2_00", vo=[("Day three. The herd has multiplied.", 0.2),
                               ("The normal one has not slept.", None)]),
        dict(clip="P2_01", intro=["The group dad. Twenty-seven. Father to no one."],
             vo=[("He will not be thanked.", 8.25)]),
        dict(clip="P2_02", intro=["The weather watcher. Four forecasts. Zero clouds."]),
        dict(clip="P2_03a", intro=["Some species travel with their own food supply."],
             vo=[("And now, the suitcase.", 3.25)]),
        dict(clip="P2_03b", vo=[("Across the room, another of her kind.", 0.25), ("No words are necessary.", None)]),
        dict(clip="P2_04", intro=["The culture seeker. He has come for the real Thailand."],
             vo=[("And he has found it. In a 7-Eleven.", 8.6)]),
        dict(clip="P2_05", intro=["The local. He loves tourists."],
             vo=[("He has smiled for eleven hours. Inside, he is screaming.", 9.04)]),
        dict(clip="P2_06", intro=["The adrenaline junkie. No fear. No thoughts."],
             vo=[("A remarkable leap.", 3.2), ("His travel insurance does not cover it.", None)]),
        # plug: reels in, recommendations out
        dict(clip="PL2a", vo=[("The normal one, meanwhile, does something the herd never does.", 0.2),
                              ("He shares a reel he actually likes.", None)]),
        dict(app="02-dm-a-reel.png", vo=["WanderBuddy turns it into the plan.",
                                         "Recommendations he actually wants."]),
        dict(clip="PL2b", vo=[("Not where the herd goes. Where he wanted to go.", 0.4)]),
        dict(outro="WanderBuddy. Follow your reels, not the herd."),
    ],
    3: [
        dict(clip="P3_00", vo=[("The final day. The herd prepares to migrate home.", 0.2),
                               ("Not all of them will make it.", None)]),
        dict(clip="P3_01", intro=["The forgetful one."], vo=[("The shoe will never be found.", 7.95)]),
        dict(clip="P3_02", intro=["The peacock. He wears his gold to attract attention."],
             vo=[("It works.", 4.55), ("The city is not cruel. Merely efficient.", 6.95)]),
        dict(clip="P3_03", intro=["Ron. Sixty-two. Recently single. Recently not."],
             vo=[("Nature has many partnerships. This is one of them.", 9.6)]),
        dict(clip="P3_04", intro=["The content creator. She has filmed every moment, and lived none."],
             vo=[("Take forty-eight. The herd is beginning to break.", 6.95)]),
        dict(clip="P3_05", vo=[("Kevin. Day one.", 0.3)]),
        dict(clip="P3_05b", intro=["Day four."]),
        dict(clip="P3_05c", intro=["Day nine."],
             vo=[("He will not send it later. He has never sent it later.", "END")]),
        dict(clip="P3_06", vo=[("Same trip. Same herd. Every single time.", 0.5),
                               ("But the normal one has learned.", None)]),
        # plug: reminders, so nothing is left behind
        dict(clip="PL3a", vo=[("Before he leaves, WanderBuddy sends a gentle reminder.", 0.2)]),
        dict(app="06-the-vault.png", vo=["Passport. Tickets. Every document, sorted before it matters."]),
        dict(clip="PL3b", vo=[("He leaves with everything he arrived with. A first, for this herd.", 0.5)]),
        dict(outro="WanderBuddy. Leave the rest of the herd at home."),
    ],
}


def all_lines() -> list[str]:
    out = []
    for beats in PARTS.values():
        for b in beats:
            out += b.get("intro", [])
            out += [v[0] if isinstance(v, tuple) else v for v in b.get("vo", [])]
            if b.get("outro"):
                out.append(b["outro"])
    return list(dict.fromkeys(out))


def tts_text(line: str) -> str:
    for a, b in SAY.items():
        line = line.replace(a, b)
    return line
