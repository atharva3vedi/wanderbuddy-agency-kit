# WanderBuddy — "TRAVESTY" spot · editor handoff

Bullet-time / frozen-world ad. *Ave Maria* over a world frozen mid-catastrophe; the
camera orbits each travel disaster in slow motion until one traveler downloads
WanderBuddy and an azure wave un-breaks everything. 9:16, ~55s.

Full creative script + all prompts: `WanderBuddy/marketing/quicksilver-ad/SCRIPT.md`.

## What's in this folder
- **`WanderBuddy_Travesty_reel.mp4`** — the assembled cut (real bullet-time slow-mo, music, end card). Start here.
- **`WanderBuddy_Travesty_demo.mp4`** — earlier previz (stills + push-ins). Superseded; keep for reference.
- **`clips/`** — every shot as its own 5-second Kling clip (`01a.mp4 … 07b.mp4`, `T_turn.mp4`, `F_finale.mp4`). **Drop these straight into your NLE** to re-time, re-order, or add transitions.
- **`stills/`** — every final frame. Use `*_v2.png` where present (the re-rolled/locked versions); `_contact_sheet_v2.png` is the board.
- **`audio/avemaria.mp3`** — the music bed (see caveat below).
- **`clips/tmpf/endcard.png`** — the end-card graphic.

## Cut order & timing (as assembled)
ACT I pains → the Turn → ACT II fixes → Finale → end card.

| Segment | Shots | Each |
|---|---|---|
| Act I (pains) | 01a 02a 03a 04a 05a 06a 07a | ~2.9 s |
| The Turn | T_turn (real orbit + azure ripple) | ~5.0 s |
| Act II (fixes) | 01b 02b 03b 04b 05b 06b 07b | ~2.9 s |
| Finale | F_finale (real-time, alive) | ~4.5 s |
| End card | tagline + logo + stores + QR | ~4.8 s |

Total ~55 s, cut to the music. Clean cuts — add dissolves / an azure-ripple wipe between A→B pairs in your editor if you want the "sweep" more explicit.

## ⚠️ Two things to finish
1. **Music is a placeholder.** `avemaria.mp3` is an AI-generated *Ave Maria–style* instrumental (license-clean) so the demo has feel. For release, drop in a properly cleared/public-domain *Ave Maria* performance and re-sync (the beats are already spaced to it).
2. **Phone screens are blank azure — comp real UI (Path A).** Every phone was generated with a blank glowing azure screen. Track-and-replace them with real app captures from `WanderBuddy/marketing/src/img/screens/`:
   - 01b split budget · 02b itinerary times · 03b (activity) · 04b map w/ member pins · 05b Documents/visa · 06b shared album · 07b Live Conversation · Turn = app open.

## Notes / known softs
- **Fresh-face drift:** 03b, 05b, 07b (and the 06 pair) were generated fresh to make the emotion flip, so those people aren't a pixel-exact match to their pain-frame twin. Reads fine at montage speed. For pixel-locked identity, we'd train Soul characters — not done.
- Beat 1's pain/fix look similar (both huddled at the table) — intentional continuity; trim as you like.
- Brand eggs seeded: mustard backpack (02a), orange cat (04a), paper airplane (05a).

## How it was made (to regenerate)
- Stills: `soul_cinematic --aspect_ratio 9:16 --quality 2k` (+ a "young travelers in their twenties…" cast token, restrained-performance clause, and a→b `--image` reference-chaining for same-scene continuity).
- Motion: `kling3_0 --mode pro --sound off --duration 5 --aspect_ratio 9:16 --start-image <still>` with a bullet-time-orbit prompt.
- Music: `sonilo_music`. Assembly: `ffmpeg` (build scripts in the session scratchpad).
- End line: **"Don't turn travel into a travesty. Download WanderBuddy."**
