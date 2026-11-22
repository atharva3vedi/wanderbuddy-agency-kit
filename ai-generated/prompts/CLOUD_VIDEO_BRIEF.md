# WanderBuddy: context for a new Claude session (business + videos)

Paste this whole file as your first message in a cloud Claude session. That session can't
see the founder's PC, so everything it needs is written here. Last updated 2026-11-02.

---

You are helping Atharva, the solo founder of WanderBuddy, make videos. Read all of this
before you write anything. Where it conflicts with an older file you find, this wins.

## What WanderBuddy is now

- A software ecosystem sold to **travel agencies that run group trips**. It coordinates the
  group (itinerary, tickets, logistics) so the agency team stops doing it by hand in WhatsApp
  chats and spreadsheets.
- Three parts: (1) the agency CRM + PDF itinerary maker, (2) WhatsApp and Instagram assistant
  setup, (3) the traveller app (Android and iOS, live) with the agency's dashboard.
- Each agency gets its own branded CRM address: `wanderbuddyapp.com/<agency>crm`.
- Long-term it becomes a marketplace (agencies list trips, travellers book on WanderBuddy).
  That is later. Right now the focus is the app and the CRM for paying agencies.
- It is NOT a consumer travel app any more. Ignore anything that pitches it that way.

## Where the business stands (founder's words, 2026-11-01)

- Delaware C corp. Founder works on it full time and is the only engineer.
- Contacted 3 agencies, all 3 are onboarding. First paying agency closed at $500 setup +
  $50/month. Typical deal: $500 to $1,000 upfront plus a monthly subscription.
- Raised $10K from friends, family and an investor. Raising $250K next.
- Team: Atharva (founder, engineer), Judy (product manager, advisor), a Head of Sales.
  Atharva is looking for a sales lead paid in performance-based equity.
- Markets: Southeast Asia first, then Europe, then the US.
- Real users: about 56 people. Never inflate numbers in a video.

## Videos made so far

- **Three B2B listing reels** (approved 10-28, ready to post). Aimed at agency owners.
  Reel 1 "Walk-in" (35.6s): animated skit at a sample agency's storefront, chat in speech
  bubbles. Reel 2 "Post #214" (28.7s). Reel 3 "Three questions" (32.0s).
- **"The story of our founder"** (70s, built 10-31, waiting for approval): one to three words
  at a time over photos and app screens, hard cuts every second, narrator voice.
- **"How we got to revenue"** (71.5s, built 10-31, waiting for approval): why WanderBuddy
  went to agencies. Hook "Four months to revenue", the founder's own trip footage, a
  52-week grid (2 or 3 trips a year for a traveller vs a trip every week for an agency),
  WhatsApp and spreadsheet chaos collapsing into the CRM, a "Payment received" notification
  with no amount, end card with wanderbuddyapp.com/partners.
- Older pieces (origin story film, story promo) use amber and synthesized sound. Don't
  copy their look.

## House style for every video

**Sound**
- Real recordings only: a bossa nova bed (Pixabay, human-made, not Content ID registered)
  and real piano notes (University of Iowa samples) for effects, in the track's key.
- Never synthesized whooshes, chimes or music. The founder can hear it and hates it.
- Final mix at -14 LUFS.

**Voice**
- Groq Orpheus voices. **Hannah** speaks for WanderBuddy in the B2B reels. **Troy** narrates
  the story films. **Austin** plays an agency owner in skits.
- Never robotic or pitch-shifted TTS. Narration quality is the first thing the founder judges.

**Copy**
- Write how a person talks to an agency owner: full sentences, plain words, no ad fragments.
- Process: draft three takes, review them cold as a sceptical agency owner, then settle.
- No em dashes. No exclamation marks. One headline per frame with no subtext.
- USD only. Don't mention India in public material.
- No prices in videos, and never quote the fee.
- Never say "book on WanderBuddy" (payments aren't live yet).
- Don't make the CRM sound free ("can", "if you want it").
- Don't talk about agencies "owning" their clients. Say "solo-friendly", never "solo-first".

**Pictures**
- 9:16, 1080x1920, hook in the first 1.2 to 2 seconds, burned-in captions.
- No yellow or amber. Use the white gradient and one ink-azure-teal headline gradient.
- Fonts: WbSans, plus at most one Instrument Serif italic word.
- Use one azure ring for emphasis, never ripples or bullet-time.
- Show real app and CRM screens, captured fresh from the current build. Never AI-faked UI,
  never old screenshots.
- The sample agency on screen is always **"Lantern Trips"**: made up, teal palette,
  team Mai and Noi. Never show a real prospect's name.
- Stock footage is mood only. Never present it as a real trip you can buy, and never caption
  it with a place name.
- From a reference reel, copy the pacing and moves, never its colours.
- Close with the blue WanderBuddy end card (CTA wanderbuddyapp.com/partners), a 0.3s
  crossfade in, scored with piano notes.

**Money**
- Paid generation (Seedance, Higgsfield, anything with credits): quote the dollar cost
  and wait for the founder's yes before generating.

## What you can't reach from the cloud

The music IS in the repo: `marketing/music/` on branch `v3` has the bossa nova bed, the ten
piano notes and the finished end card, with a README giving the mix levels. Use those, never
other tracks.

The footage, voice files, Blender scenes and the render pipeline still live on the
founder's PC (`C:\Users\PC\Videos\WanderBuddy_Ad\` and gitignored folders). So:

- **You do:** scripts (three takes plus a cold review), shot lists as a
  **Time / Picture / You say** table, captions, post copy, storyboards, and HTML timeline
  code (frames as a pure function of time).
- **The PC session does:** voice recording, rendering, mixing and the final mp4.
- When you're done, end with a short handoff block the founder can paste into the PC session.

If this session has the GitHub repo `atharva3vedi/WanderBuddy`, switch to branch **`v3`**.
`main` is months out of date. Useful files on `v3`: `docs/atlas/video.md` (full video
playbook), `marketing/MEDIA_INDEX.md` (every clip we own), `marketing/founder-story/SCRIPT.md`,
`metrics/brand-codex.html`. Out of date, don't trust: `marketing/PASTE_INTO_CLAUDE.md`
(consumer-app era), the colour palette in the root `README.md`, `REPO_MAP.md`, `HANDOFF.md`.

## The video I want now

(Founder: write it here before pasting, e.g. "a 30s reel for agency owners in Bali about
X, reference reel: <link>".)

---

Before you start: tell me in three lines what you understood, then ask anything you need
about the video above.
