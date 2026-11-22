# WanderBuddy — "TRAVESTY" (Frozen-World / Bullet-Time Spot)

> Ave Maria over a world frozen mid-catastrophe. The camera orbits each travel
> disaster in slow motion — a beautiful requiem for the group trip gone wrong —
> until one traveler downloads WanderBuddy and a wave of calm un-breaks everything.

- **Runtime:** ~55s (30s cut noted at the end)
- **Format:** 9:16 vertical (social-first; matches your locked pipeline)
- **Music:** Schubert's *Ave Maria* — one continuous, uninterrupted take. Sacred beauty over ugly reality is the whole joke and the whole heart. Use a public-domain / royalty-free performance or license a recording. Everything is cut TO the music, not the other way around.
- **Look (locked):** cinematic 35mm, shallow DOF, volumetric golden-hour light, teal-and-amber grade, soft film grain, azure `#1E88D6` accent light, ink-navy `#0B141F` shadows. (Same `soul_cinematic` look you already locked.)
- **Signature device — "the freeze":** every disaster is held in **bullet-time** — people suspended mid-shout, mid-tear, mid-fall; dust, cash, sweat, luggage all hanging in the air. The camera does a slow **360° orbital arc** around each frozen tableau (Quicksilver-kitchen energy). Nothing in the world moves in Act I. The only thing that ever moves at normal speed is our hero — and only after she opens the app.
- **End line:** **"Don't turn travel into a travesty."** → **"Download WanderBuddy."** + App Store & Google Play badges (iOS is live — Apple ID 6795848498).

### Brand eggs (reused from your cinematic-ad universe)
Seed these so this spot lives in the same world: **mustard backpack** (on the always-late runner), **orange cat** (frozen mid-leap in the temple), **paper airplane** (suspended in the airport hall). Continuity = free brand memory.

### Device / brand handling (important for generation)
Higgsfield rejects or garbles real logos (your "Apple-keynote → stamped an Apple logo" gotcha). So: **generate every phone with a BLANK azure screen** and describe devices generically ("glossy pale flagship" vs "dark slate Android"). **All real UI + all device/logo specifics are composited in post** from `marketing/src/img/screens/*` — this is your existing **Path A** method, unchanged.

---

## STORYBOARD — beat by beat

Act I is pure frozen chaos (7 orbits). The Turn introduces the one moving human. Act II sweeps an azure wave back through the same 7 tableaux, now resolved. Finale unfreezes into real-time warmth. Ave Maria carries the entire arc.

| # | t (s) | Beat | Frozen tableau (Act I) | Resolved by the wave (Act II) | WanderBuddy feature |
|---|-------|------|------------------------|-------------------------------|---------------------|
| 0 | 0–3 | **Cold open** | Black. First notes of Ave Maria. A single suspended dust mote catches azure light. Title flicker: *"every trip has a plan…"* | — | — |
| 1 | 3–8 | **Budget war** | 4 friends around a hostel table, one jabbing a finger, receipts + banknotes frozen mid-air, faces contorted, a glass tipping mid-spill | Cash settles, faces soften, phone shows a clean shared split; everyone nods | Shared trip budget & transparent split |
| 2 | 8–13 | **Missed train** | Runner sprinting the platform (**mustard backpack**, strap flying), train doors frozen shut, a sweat bead suspended, face in despair | Same runner, relaxed by the window, seat booked, city sliding past | Live itinerary times + navigation/alerts |
| 3 | 13–18 | **Bored in the group** | A young guy slumped, dead-eyed, mid-yawn at a museum the group adores; excited friends blur around him | Same guy mid-laugh at a thing HE loves (street gig / skate spot / food stall) | AI planner balances every member's interests |
| 4 | 18–23 | **Lost, can't find each other** | Vast ancient island temple — towering stone columns, labyrinth courtyards, sea beyond. Two friends frozen back-to-back, looking the wrong ways, phones reading "No Signal." **Orange cat** frozen mid-leap between pillars | Live map with glowing member pins; the two frozen mid-run toward each other, relief breaking | Live member location pins on the trip map |
| 5 | 23–28 | **Immigration wall** | Immigration desk. Officer's hand frozen sliding a passport BACK, stern face. Traveler's face falling. A **paper airplane** hangs in the hall behind | Docs vault open (visa, return ticket, hotel); officer frozen mid-stamp, gate light green | Tickets + Documents vault (visa/docs ready) |
| 6 | 28–33 | **The photo that never came** | Scenic overlook. One friend holds a glossy pale phone showing a gorgeous group photo; the other (dark slate phone) frozen mid-tear, a single teardrop suspended — the photo won't cross devices | The dark phone buzzes; the same photo lands in the shared album; tear turns to a laugh | Cross-platform shared album (iOS ↔ Android) |
| 7 | 33–38 | **Lost in translation** | A tourist leaning too close, mouth wide mid-shout (loud slow English), hands flailing; a local vendor recoiling, baffled | Both frozen mid-warm-handshake, real understanding, phone translating live | Live Conversation real-time translation |
| — | 38–43 | **THE TURN** | The world stays frozen. One traveler (the girl from beat 1) is the **only thing that moves** — normal speed, calm. She lifts her phone, opens WanderBuddy. A soft **azure ripple** pulses out from the screen | — | — |
| — | 43–52 | **The sweep** | The azure wave rolls back through all 7 tableaux; as it passes each, time resumes — but corrected (the right-column states above), quick orbital cross-cuts, everyone moving and connected | — | — |
| — | 52–55 | **Finale + end card** | Everything unfreezes at once into ONE real-time golden group moment — the whole friend-group together, laughing, moving. Ave Maria hits its final cadence. Cut to azure. Text: **"Don't turn travel into a travesty."** → logo (white twin-peak + water glyph) → **"Download WanderBuddy"** + App Store & Google Play badges | — | — |

**Emotional engine:** Ave Maria's opening = the chaos orbits; each swell aligns with an orbit reveal; the climactic phrase lands on the group un-freeze + logo. Beautiful music mourns the broken trip, then blesses the fixed one.

---

## GLOBAL KEYS (paste into every prompt)

> **Casting is locked.** Soul Cinematic defaults to middle-aged/older men and reads
> like a tavern, not a backpacker trip. Every people-shot MUST open with the CAST
> token below or the friend-group story collapses. (Verified 2026-08-27: adding it
> flipped the budget/bored/temple/overlook stills to correct young mixed-gender
> casting on the first try.)

**CAST (open every people-shot with this):**
```
a group of young friends in their twenties, mixed genders, modern casual travel
clothing, backpacker travelers
```

**STILL_STYLE (append to every `soul_cinematic` image prompt):**
```
cinematic still, 35mm, shallow depth of field, volumetric golden-hour light,
teal-and-amber cinema grade, soft film grain, photoreal, azure #1E88D6 rim light,
ink-navy shadows, bullet-time frozen moment with fine dust and debris suspended
in mid-air, 9:16 vertical
```

**MOTION_KEY (append to every image-to-video prompt):**
```
camera performs a slow smooth 360-degree orbital arc around the frozen subject,
bullet-time, extreme slow motion, subjects frozen mid-action, suspended dust and
debris drift almost imperceptibly, cinematic parallax, shallow depth of field,
no cuts, no camera shake
```

**AVOID (do not put in prompts — they trip safety / logo-stamping):** brand names (Apple, iPhone, Samsung, Android, Google), "keynote," real public figures, visible UI text on phone screens (keep screens **blank azure** — comp real UI in post).

---

## SHOT-BY-SHOT PROMPT SHEET

For each beat: an **[A] "broken" still** (Act I) and a **[B] "resolved" still** (Act II). Generate the still with `soul_cinematic`, then animate it to an orbit with `kling3_0` (Pro 1080p) or `seedance_2_0`. `{STILL_STYLE}` and `{MOTION_KEY}` = the global keys above.

> Phones anywhere in frame = **blank azure screen**. Real screens get composited later.

### 1 — BUDGET WAR
- **1A img:** `Four young travelers around a cheap hostel table erupting in an argument, one jabbing a finger across the table, crumpled receipts and paper banknotes flung upward and frozen in mid-air, a glass tipping mid-spill, contorted frustrated faces, warm tungsten room light. {STILL_STYLE}`
- **1B img:** `The same four travelers around the same table now calm and reconciled, soft smiles and nods, banknotes settled in a neat stack, one holds a glossy phone with a blank azure screen, relief in the room. {STILL_STYLE}`
- **vid (both):** `the argument is frozen; {MOTION_KEY}`

### 2 — MISSED TRAIN
- **2A img:** `A traveler sprinting down a train platform with a bright mustard-yellow backpack, one strap flying, mouth open in a shout, a single bead of sweat suspended by the temple, the train's doors frozen mid-close, a departure board glowing, everything frozen. {STILL_STYLE}`
- **2B img:** `The same traveler with the mustard backpack now seated calmly by a train window, relaxed, city sliding past outside, a blank-azure-screen phone resting on the knee. {STILL_STYLE}`
- **vid:** `frozen platform sprint; {MOTION_KEY}`

### 3 — BORED IN THE GROUP
- **3A img:** `A bored young man slumped on a museum bench mid-yawn, dead-eyed, while three excited friends gesture at a painting, his boredom sharp against their delight, cold gallery light. {STILL_STYLE}`
- **3B img:** `The same young man mid-laugh and alive at a lively street music stall he actually loves, warm string-lights, energy on his face. {STILL_STYLE}`
- **vid:** `frozen boredom; {MOTION_KEY}`

### 4 — LOST IN THE TEMPLE
> Reference: the sprawling island temple you named — swap in the real location's architecture (e.g. Elephanta-style cave temple / Ephesus-style ruins).
- **4A img:** `A vast ancient island temple complex, towering weathered stone columns and labyrinthine courtyards, sea horizon beyond. Two travelers frozen back-to-back among the pillars looking the wrong ways, phones raised showing blank azure screens, lost; an orange cat frozen mid-leap between two columns, dust suspended in shafts of light. {STILL_STYLE}`
- **4B img:** `The same two travelers among the temple columns frozen mid-run toward each other, arms rising, relief and joy on their faces, a blank-azure phone in one hand, golden light. {STILL_STYLE}`
- **vid:** `frozen among ancient columns; {MOTION_KEY}`

### 5 — IMMIGRATION WALL
- **5A img:** `An airport immigration desk, a stern officer's hand frozen sliding a passport back across the counter, the traveler's face falling in disbelief, cold overhead light, a small paper airplane suspended in the hall behind. {STILL_STYLE}`
- **5B img:** `The same immigration desk, the officer frozen mid-stamp with an approving nod, the gate light glowing green, the traveler relieved, holding a blank-azure phone showing documents. {STILL_STYLE}`
- **vid:** `frozen at the immigration counter; {MOTION_KEY}`

### 6 — THE PHOTO THAT NEVER CAME
- **6A img:** `Two friends at a scenic mountain overlook at golden hour. One holds a glossy pale phone showing a beautiful group photo; the other holds a dark slate phone and is frozen mid-cry, a single teardrop suspended on the cheek, the photo unable to cross between the two phones. {STILL_STYLE}`
- **6B img:** `The same two friends at the overlook, the one who was crying now frozen mid-laugh with joy, the dark slate phone lit, the same group photo now on both blank-azure screens. {STILL_STYLE}`
- **vid:** `frozen at the overlook; {MOTION_KEY}`

### 7 — LOST IN TRANSLATION
- **7A img:** `A tourist leaning far too close to a street vendor, mouth wide open mid-shout speaking loudly, hands flailing in exaggerated gestures, the local vendor recoiling and baffled, a crowded market frozen around them. {STILL_STYLE}`
- **7B img:** `The same tourist and vendor frozen mid warm handshake, both smiling with real understanding, a blank-azure phone held between them, market glowing behind. {STILL_STYLE}`
- **vid:** `frozen mid-argument in the market; {MOTION_KEY}`

### THE TURN (the one moving human)
- **T img:** `A calm young woman standing perfectly still and alive amid a world frozen in bullet-time around her, other travelers suspended mid-motion, she lifts a phone with a glowing azure screen, a soft ring of azure light beginning to pulse outward from the phone. {STILL_STYLE}`
- **T vid:** `everyone around her stays frozen; she moves at normal speed and lifts the phone; a soft azure ripple pulses outward from the screen; slow push-in on her calm face, cinematic, no cuts`

### FINALE (real-time warmth — the only non-frozen shot)
- **F img:** `A whole group of young friends together at a golden-hour viewpoint, genuinely laughing and leaning on each other, warm natural motion, no frozen debris, alive and connected, cinematic 35mm, teal-and-amber grade, 9:16 vertical`
- **F vid:** `natural real-time motion, the friends laugh and turn to camera, a gentle slow push-in, warm golden light, celebratory, no cuts`

### END CARD (build in edit, not generated)
Azure `#1E88D6` field → white type: **"Don't turn travel into a travesty."** (hold) → wipe → **WanderBuddy** logo (white twin-peak + water glyph, `marketing/src/img/brand/glyph-white.png`) → **"Download WanderBuddy"** + App Store + Google Play badges. Final Ave Maria chord lands here.

---

## RUN PLAN (how to actually generate this)

**Order of operations — cheap, review-gated:**

1. **Roll the stills first** (`soul_cinematic`, 9:16, `--quality 2k`, ~0.12 cr each). 16 stills (7×A + 7×B + Turn + Finale) ≈ **~2 credits**. Review the look before spending on video.
2. **Approve / re-roll** any weak stills.
3. **Animate** each approved still to its orbit. Your locked pick = **Kling 3.0 Pro 1080p ≈ 8.75 cr / 5s**. ~16 clips ≈ **~140 cr**. (Cheaper test path: `kling3_0` std 720p ≈ 7.5 cr; Seedance 1080p = 45 cr each — pricey.)
4. **Assemble** in your editor (below).

**Still command (per shot):**
```bash
higgsfield generate create soul_cinematic \
  --prompt "PASTE 1A PROMPT WITH {STILL_STYLE} EXPANDED" \
  --aspect_ratio 9:16 --quality 2k --wait
```

**Animate command (per still) — Kling Pro:**
```bash
higgsfield generate create kling3_0 \
  --prompt "frozen tableau; PASTE {MOTION_KEY} EXPANDED" \
  --start-image <STILL_ID_OR_PATH> \
  --duration 5 --resolution 1080p --wait
```

**Animate command — Seedance alt (must disable audio or the job fails):**
```bash
higgsfield generate create seedance_2_0 \
  --prompt "frozen tableau; PASTE {MOTION_KEY} EXPANDED" \
  --start-image <STILL_ID_OR_PATH> \
  --duration 5 --resolution 1080p --generate_audio false --wait
```

Same jobs are available through the Higgsfield MCP tools (`generate_image` → `generate_video`) if driving it from here instead of the CLI. Reuse each still's upload UUID as the `start-image` to skip re-uploads.

---

## EDIT / ASSEMBLY (After Effects / DaVinci)

1. **Lay Ave Maria first**, then cut every clip to it. Act I orbits ride the rising phrases; the Turn ripple hits a swell; the Finale un-freeze lands on the final cadence.
2. **The azure ripple = the transition engine.** A single expanding azure ring wipe carries you from each broken tableau (A) to its resolved one (B). One motion, reused 7×, ties the whole sweep together.
3. **Comp real UI (Path A):** track the blank azure phone screens and replace with real captures from `marketing/src/img/screens/*` — budget split, itinerary times, map with member pins, Documents vault, shared album, Live Conversation. Never let generated fake UI show.
4. **Slow-mo polish:** the orbits are already slow; add optical-flow retime only if a clip feels fast. Keep debris drift subtle.
5. **End card** built on the azure field with the real logo + store badges. Grade everything to the teal-amber look for one continuous world.

---

## 30-SECOND CUT
Drop beats 3 (bored) and 7 (translation); keep budget, missed train, lost-in-temple, immigration, the photo. Same Turn + sweep + finale. 5 orbits fits :30 cleanly and keeps the strongest visuals.
