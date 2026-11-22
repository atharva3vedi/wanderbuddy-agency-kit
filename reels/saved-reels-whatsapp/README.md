# Reel: "saved reels → real plan" (WhatsApp feature demo)

Relatable 9:16 meme reel, ~27.3s, 1080x1920 / 30fps. Built 2026-09-22.
Same lane as `../overthink-steak` (silent b-roll + bold captions + brand outro),
but this one plugs the **WhatsApp reel-ingestion feature** with a built-in demo.

**Finals (two hooks, identical body):**
- `final/saved_reels_whatsapp_A.mp4` — "i could never…" meme hook
- `final/saved_reels_whatsapp_B.mp4` — "POV: your saved folder…" hook

## Concept / timeline (v2 — all-real montage, no AI clip)
A fast montage of REAL road-trip clips carries the relatable pain, a tiny
"here's how" transition bridges to a pixel-accurate mock of the actual feature.
No AI-generated footage. No shirtless clips. (No beach footage exists in source,
so a reservoir/lake still stands in for the scenic-water beat.)

| t (s) | visual | caption |
|-------|--------|---------|
| 0.0–1.7 | motorbike road POV (real) | A: "i could never be the / person who saves a reel"  ·  B: "POV: your saved folder / IS your dream trip 😍" |
| 1.7–3.4 | lake/reservoir still (Ken Burns) | A: "…and never finds it again 💀"  ·  B: "…and you can't find a single one of them" |
| 3.4–11.4 | montage: waterfall → dirt road → tea → monkey → pool (real) | — (vibes) |
| 11.4–12.3 | **"here's how 👇"** transition (darkened lake still) | baked-in |
| 12.3–21.6 | **mock demo** (WhatsApp → app, ~9.3s) | "just text the reel / to WhatsApp 📲" |
| 21.6–23.3 | people at a waterfall (real, clothed) | "wander more. / plan less." |
| 23.3–27.9 | brand outro | (wordmark → Download now) |

WanderBuddy app-icon badge is watermarked top-left across the real b-roll only
(never over the demo, which is itself a phone screen). Subtle waterfall ambient
bed under the body; outro keeps its own audio. **Swap in trending audio in-app.**
Build parts live in `build2/`; the earlier Seedance-based cut's parts are in
`build/` + `broll/seedance.mp4` (unused in v2).

## v3 — promo half from the REAL screen recording (for manual editing)
Source: `C:\Users\PC\Desktop\Screen_recording_20260922_062406.webm` (1344x2992,
15.3s) — real in-app flow: Profile → Connect WhatsApp (Connected +91…, example
prompts) → Saved reels (real ingested reels: Palermo, India trips, SEA…).
Reframed to 9:16 on a blurred bg (`promo/reframed_full.mp4`) so nothing is cropped.

Promo half = mock WhatsApp chat (the "send a reel" action, from the PIL demo) →
**real recording** as proof (really connected + all reels saved & searchable) →
brand outro. Captions in `captions/PW1,PW2,PR0,PR1,PR2`. Parts in `promo/`.
Deliverables in `final/`:
- `promo_half.mp4` (~15.2s, with outro) — ready 2nd-half.
- `promo_half_no_outro.mp4` (~10.6s) — for stitching to a custom first half.
- `recording_reframed_9x16.mp4` (15.3s) — raw reframed recording, no captions.

The mock WhatsApp beat is a deterministic PIL render (not AI, not a real chat
capture); swap it for a real WhatsApp screen-record if preferred.

## The demo (the whole point)
`make_demo.py` renders a deterministic 11s phone-screen recording in PIL — no
live app or recording needed. Scene 1: WhatsApp chat with "WanderBuddy" — user
shares an Instagram reel link (waterfall cover), bot replies "Reading that reel
now…" → "Found: Kuang Si Falls, Laos" → "Added to your Laos trip + 3 more spots
saved". Scene 2 (whip cut): the WanderBuddy itinerary with the **Kuang Si Falls**
card popping in (amber "📍 From your reel" chip) plus a "Saved from your reels"
row. Mirrors the real pipeline (WhatsApp → inspiration enrich → auto-add to trip
/ Saved-reels screen). Reel covers reuse frames from the real b-roll.

## Sources
- Real clips: `E:\Phone big gb stuff` (solo motorbike road-trip footage), cropped
  to 9:16. Selection + in-points in `build/` (s_*.mp4). Covers in `demo/`.
- Seedance ("bytedance"): `seedance` MCP, model dreamina-seedance-2-0-mini,
  seed 6602, 9:16 720p, prompt = phone + floating scattered travel reels.
  Raw in `src/seedance_raw.mp4`, normalized `broll/seedance.mp4`.
- Outro: `marketing/outro/outro.mp4` (shared brand outro).
- Captions rendered deterministically with PIL (`make_captions.py`), never by a
  video model.

## Rebuild
1. `python make_demo.py` → `demo/frames/*` → encode `demo/demo.mp4`.
2. `python make_captions.py` → `captions/*.png`.
3. Re-extract b-roll segments + `build/base.mp4` (concat + badge overlay), then
   overlay captions → `build/body{A,B}.mp4`, then concat outro + ambient →
   `final/saved_reels_whatsapp_{A,B}.mp4`. Exact ffmpeg graphs were run in the
   session; segment durations are in this table.
