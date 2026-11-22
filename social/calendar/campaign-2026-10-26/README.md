# Two audiences, first four weeks: 26 Oct to 22 Nov 2026

*Written 22 Oct 2026 from `metrics/marketing-plan.html`, the 2.0 launch plan, `CRM/META_AUTOMATIONS.md`,
`CRM/CALL_FUNNEL.md`, the brand codex (sections 05 to 07) and `metrics/growth-plan.html`.*

Agencies buy the CRM ($100 a month and $500 setup for the founding five). Travellers get the free
app, and later the marketplace trips. Both are marketed from the same accounts, at different hours,
in different voices. Nothing in this folder posts, sends or spends anything.

| File | What it is | Who acts |
|---|---|---|
| [CALENDAR.md](CALENDAR.md) | Every post, week by week, per audience and platform: what to film, the caption, the YouTube title | Judy queues, founder films and publishes |
| `drafts.sql` | The same 28 posts as drafts for the dashboard's Channels tab (`social_posts`, status `draft`, source `claude`) | Founder runs it once |
| `build_drafts.py` | The one list both files come from, with the brand-rule checks. Edit captions here | Anyone, then rerun |
| [META_ADS_PLAN.md](META_ADS_PLAN.md) | Meta ads for both audiences: structure, USD budgets, targeting, events, pause rules | Founder approves each dollar line |
| `../../business/b2b/outreach/SEQUENCES_V2.md` | Agency outreach run from `/crm`: messages, cadence, replies | Atharva (DMs, WhatsApp), Vaibhav (email) |
| `../../business/b2b/outreach/crm_import.csv` | 80 ICP prospects ready for `/crm` > Import, 11 marked This week | Vaibhav imports once |

## Load the drafts

1. Migration `0154_founder_channels.sql` is pushed (`supabase db push`). `drafts.sql` stops with a
   clear error if it isn't.
2. Paste `drafts.sql` into the Supabase SQL editor and run it. It adds 28 drafts (8 for agencies,
   20 for travellers) and skips any caption that is already there, so running it twice is safe.
   Checked on 22 Oct against the 0154 table in a local Postgres: 28 rows, then 28 again on the
   second run, earliest post on top.
3. On the dashboard, open Channels. The drafts show newest first, which is calendar order. For
   each one: Edit, attach the video or image, then Schedule for the date in `CALENDAR.md`, or
   Publish now on the day.

Two posts are held back as commented-out blocks at the end of `drafts.sql`: a departure listing
(needs listings live and the agency's written OK) and a Raasta Theory Collab post (needs Raasta's
written OK).

## Money

The ads plan spends at most **$378** over these four weeks, all three lines approved by the founder
on 22 Oct 2026, who sets them up in Ads Manager: $105 and $28 for agency call ads from 2 and 9 Nov, and the $245 traveller install
test, which waits until the sign-in fix is live and Events Manager shows store-build events.
Filming and posting cost $0.

## Check before publishing

- Anything in `[BRACKETS]`: the three Reel of the week posts and the founding places left (A08).
- T05, Sat 31 Oct: the prize is lifetime Premium (founder's call, 25 Oct).
- Agency screens use a made-up sample agency (Kite Trips) labelled Sample. Never a real agency's
  name or trip without their written OK.
- `NOT_SHIPPED` in `website/src/lib/site.ts` before every post: no booking, offline itineraries,
  in-chat translation, documents or packing lists.
