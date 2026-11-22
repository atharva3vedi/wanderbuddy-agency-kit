# Meta ads plan, 26 Oct to 22 Nov 2026: agencies and travellers

*Written 22 Oct 2026. Builds on `metrics/marketing-plan.html` (budget lines and gates),
`CRM/CALL_FUNNEL.md` (the agency funnel and the Conversions API) and `CRM/META_AUTOMATIONS.md`
section 11 (the traveller install test, unchanged here). Nothing in this file is running.*

**Approved by the founder on 22 Oct 2026: lines A ($105), B ($28) and C ($245), $378 at most.**
The founder sets them up in Ads Manager. Line C still starts only once both of its gates pass.
Anything beyond these amounts, including the winning traveller ad set from 23 Nov, is a new ask.
Claude does not touch Ads Manager. Every number below is a ceiling, set as a campaign spending limit
in Ads Manager so it cannot be overspent.

## 1. The ask: approve each line

| # | Line | Dates | Daily | Most it can spend | Starts only when |
|---|---|---|---|---|---|
| A | Agency qualified calls, cold | Mon 2 Nov to Sun 22 Nov, 21 days | $5 | **$105** | The Conversions API test code is unset (section 3) |
| B | Agency qualified calls, warm | Mon 9 Nov to Sun 22 Nov, 14 days | $2 | **$28** | The agency video viewer audience reaches about 1,000 people |
| C | Traveller install test, section 11 as written | 7 days from the day both gates pass; earliest Wed 28 Oct | $35 | **$245** | The sign-in fix is live in both stores, and Events Manager shows installs and `CompleteRegistration` from the store build |
| D | Marketplace: travellers buying agency trips | | | **$0** | Listings and deposits are not live; `booking` is on the NOT_SHIPPED list |
| | **Total, these four weeks** | | | **$378** | |

This fits the Bootstrap budget: call ads are $200 a month (A and B run at $7 a day), and the $245
test is the first part of the $500 consumer line. The winning traveller ad set (about $130 a month)
is decided at the Mon 23 Nov read-out, after these four weeks, and gets its own ask then.

If the round lands, the Funded plan raises line A to $55 a day ($1,700 a month). Same structure,
same pause rules.

If line C never passes its gates in these four weeks, its $245 is not spent on consumers. It waits
for the gates, or moves to agency call ads at the read-out (the marketing plan's rule).

## 2. Which events Meta optimises for

| Audience | Event | Where it comes from | Use it for |
|---|---|---|---|
| Agencies | `Lead` on dataset wanderbuddyapp.com (1068707946171546) | `partner-call` sends it server side when a booking passes the 4+ trips a month gate. `custom_data.lead_type = qualified_call`, plus `fit_score` and `trips_band`. Turned-away agencies send nothing. | Optimisation goal for lines A and B from day one |
| Agencies | Custom conversion **Qualified agency call** = `Lead` where `lead_type` equals `qualified_call` | Make it in Events Manager once the first real Lead lands | Swap the goal to it then. Today it equals `Lead`; it keeps working if another page ever sends a Lead |
| Travellers | App install | Meta SDK (`facebook_app_events`), counted by Meta | Line C, first 7 days |
| Travellers | `fb_mobile_complete_registration` | `MetaEvents.completedRegistration()` on a brand-new account | Switch line C's goal to it at about 50 sign-ups a week. Decide budgets on cost per sign-up, not per install |
| Travellers | `first_value_achieved` (custom, `kind` = create_trip, join_trip or add_activity) | `MetaEvents.firstValue()` | Read it every Monday. Make it the goal only once it passes about 50 a week |

The website dataset has no pixel. That means no page views, no landing page view optimisation and no
website visitor audiences: warm audiences come from video viewers and engagers instead (line B).

## 3. Before anything runs

1. `supabase secrets list` shows no `META_CAPI_TEST_CODE`. While it is set, every Lead is a test
   event and Meta does not optimise on it (`CALL_FUNNEL.md` step 4).
2. `wb_call_booked` is approved in WhatsApp Manager. Without it a booked agency gets no WhatsApp
   confirmation, and shows drop.
3. In Ads Manager, create these audiences:
   - **App users, 180 days** (app activity, any event): every traveller ad set excludes it.
   - **Agency video viewers, 90 days**: people who watched 50% of the agency videos A01 to A07 in
     `CALENDAR.md`. Line B targets it.
4. Set a campaign spending limit on each campaign equal to its line above.

## 4. Agencies: campaign structure

**Campaign** `WB / Agencies / Qualified calls / Nov26`

| Setting | Value |
|---|---|
| Objective | Leads |
| Conversion location | Website |
| Dataset | wanderbuddyapp.com (1068707946171546) |
| Performance goal | Maximise number of conversions, event `Lead` |
| Advantage campaign budget | Off, so each ad set gets its own spend |
| Bid strategy | Highest volume, no cap |
| Spending limit | $133 |
| Website URL | `https://wanderbuddyapp.com/partners/call`, never the homepage |
| URL parameters | `utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}` |
| Call to action | Book now |

At $7 a day Meta will say "Learning limited". That is expected at this size. If an ad set spends
under half its budget for three days running, switch it to Traffic > Link clicks with the same
targeting and switch back to Leads once three qualified calls have come in.

### Ad set A: cold

| Setting | Value |
|---|---|
| Name | `WB / Agencies / Owners SEA` |
| Budget | $5 a day |
| Locations | India, Singapore, Malaysia, Thailand, Indonesia, Vietnam, Philippines. India added 25 Oct (founder). After three days, check Breakdown > Delivery > Country: India's cheaper impressions can take most of the $5 |
| Age | 25 to 60 |
| Advantage+ audience | Off. Its suggestions drift to holidaymakers, and this ad set wants the people who sell the holidays |
| Detailed targeting | Interests, if the account still lists them: Travel agency, Tour operator, Destination management company, Group travel, Tourism. Narrow further (must also match): Entrepreneurship, Small business, Small business owners. Check each one in Ads Manager; Meta has removed many business interests |
| Languages | Any. The call page is translated into Thai, Indonesian, Vietnamese, Malay, Filipino and more |
| Placements | Manual: Instagram Feed, Reels and Stories; Facebook Feed and Reels. Audience Network off: it sends accidental clicks, not agency owners |

### Ad set B: warm

| Setting | Value |
|---|---|
| Name | `WB / Agencies / Video viewers` |
| Budget | $2 a day, from Mon 9 Nov, only once the audience is about 1,000 |
| Audience | Agency video viewers, 90 days. Not all Instagram engagers: those are mostly travellers |
| Placements | Same as ad set A |

### Agency ads, batch 1 (Mon 2 Nov)

One headline on the visual, real CRM or app screens in a sample agency's logo and colours, labelled
Sample. 9:16 for Reels and Stories, 4:5 for Feed. The headline field carries the same words.
Primary text is one sentence that qualifies the reader, so fewer agencies under 4 trips a month book:

> For agencies running 4 or more Southeast Asia departures a month. $100 a month and $500 setup for the first five.

In Advantage+ creative, turn off text improvements and generated text so Meta adds no subtext.

| # | Headline | Visual |
|---|---|---|
| AG1 | Who answers this at 11:48 pm? | The 23:48 chat film from /partners/call, cut to 9:16 (A01) |
| AG2 | Your travellers ask the assistant, not you. | A traveller asks "what time is pickup tomorrow?" on WhatsApp; the assistant answers from the plan |
| AG3 | One inbox for WhatsApp and Instagram enquiries. | The CRM inbox, a WhatsApp enquiry and an Instagram DM in one list (A03) |
| AG4 | Your logo on the trip. Not ours. | The join page and itinerary in the sample agency's colours (A02) |
| AG5 | The PDF and the costing, on one screen. | The PDF maker: costs, markup, then the branded PDF (A04) |

Ad set B runs the two best of these after a week, plus the founder video (A07) once it exists.

**Batch 2, Mon 16 Nov:** replace the two weakest with headlines from `/crm` > Ad angles, the
agency's own words from call notes (press Extract after every call). Batch 3, at the read-out: the
founder video as an ad.

Never in an agency ad: ad results, a cost per booking, Meta approval dates, client counts we do not
have, anything not live (comment-to-DM, Boost a trip, listings, deposits), or any promise about
whose clients they are.

## 5. Travellers: campaign structure

Run `CRM/META_AUTOMATIONS.md` section 11 as written: campaign `WB / App installs / Travellers / Oct26`,
objective App promotion, Google Play first, three ad sets (airport $10, destination $10, planning a
trip $15 a day), 15 ads, every ad set excluding App users, 180 days. Nothing in it changes here
except the start date, which follows the gates in line C.

After the day-7 read, keep the two cheapest creatives in each ad set and add the 2.0 swaps from the
launch plan: "Landed. Your trip knows." for the airport, "One clip each. One reel for the trip."
for the destination, and the organic reel with the most comments (T01 to T09 in `CALENDAR.md`) for
planning a trip, run with Use existing post so its likes and comments carry over.

Add the App Store version only after Android installs show in Events Manager.

## 6. What to pause, and when

Read every Monday at the 30-minute scoreboard. Pause first, ask after: a pause costs nothing.

| Signal | Where to read it | Do this |
|---|---|---|
| An agency ad has spent $15 with link click-through under 0.5% | Ads Manager, ad level | Pause the ad, keep the ad set |
| An agency ad set has spent $50 with no qualified call | Ads Manager plus the `/crm` funnel strip | Swap two ads, keep the targeting, once |
| An agency ad set has spent $100 with no qualified call | Same | Pause the ad set and bring it to the Monday read |
| Cost per qualified call over $100 across two weeks (target under $50) | Ads Manager, Results = Lead | Pause line A; its money goes to outreach time at the read-out |
| Turned away outnumbers booked 3 to 1 while ads run (the strip does not split turned-away by source, so compare with the weeks before ads) | `/crm` funnel strip: turned away, booked, and how many bookings came from ads | Tighten ad set A: drop the broad interests, keep Travel agency and Tour operator |
| Fewer than half of 4 or more ad-booked calls show | `/crm`, showed / no-show | Pause both agency ad sets; check `wb_call_booked` reaches people, then restart |
| Line B frequency over 3 a week | Ads Manager | Add a new video or pause B |
| A traveller ad set costs over 2x the cheapest per install, or per sign-up once events flow | Ads Manager | Pause that ad set (section 11 rule) |
| Cost per sign-up over $8 (target under $4) | Ads Manager plus Events Manager | Stop line C. The money waits for the read-out |
| Installs show in Ads Manager but sign-ups do not rise on the dashboard | Founder dashboard, opened but never signed in | Stop line C: the sign-in wall is back. Do not buy installs into the leak |
| Any spend line reaches its limit in section 1 | Ads Manager spending limit | It stops by itself. Raising it is a new ask |

## 7. Read-outs

| Date | What gets decided |
|---|---|
| Wed 4 Nov, or 7 days after line C starts | Line C: keep, cut or swap creatives per ad set |
| Mon 9 Nov | Line B on or held (audience size); first ad-booked calls and show rate |
| Mon 16 Nov | Agency batch 2 from call notes |
| Mon 23 Nov | Scale, iterate or kill each line. The winning traveller ad set gets its own dollar ask. The reserve is released |

## 8. Answered questions

1. India-based agencies are in ad set A's locations (founder, 25 Oct). The no-India rule still
   covers copy: no India and no rupees in any ad.
2. The Halloween prize (T05) is lifetime Premium (founder, 25 Oct).

## 9. In Meta as drafts (25 to 26 Oct)

Set up through Meta's ads MCP server, every call approved by the founder, on ad account
act_1666690181650949 (WanderBuddy, business 1040173725686270, bills in INR, time zone
America/Los_Angeles). The server runs in draft mode: both objects sit unpublished in the Ads
Manager draft and cannot spend. Publishing makes them live, so it is its own ask once ads exist.

| Object | ID | Settings |
|---|---|---|
| Campaign `WB / Agencies / Qualified calls / Nov26` | 23859613425750794 | Draft, status PAUSED. Leads, auction, Advantage campaign budget off, spending limit Rs 11,704 ($133) |
| Ad set A `WB / Agencies / Owners SEA` | 23859618942400794 | Draft, status PAUSED. Rs 440 a day ($5). Mon 2 Nov 00:00 to Sun 22 Nov 23:59 Los Angeles time (2 Nov 1:30 pm in India). Website conversions on dataset 1068707946171546, event Lead, highest volume, no cap. India, Singapore, Malaysia, Thailand, Indonesia, Vietnam, Philippines; age 25 to 60; Advantage+ audience off. Instagram Feed, Stories and Reels; Facebook Feed and Reels |
| Audience **App users, 180 days** | 23859618995120794 | Created 26 Oct after the founder accepted the custom audience terms. App 1111963268004981, people who opened the app (`fb_mobile_activate_app`), 180 days, backfilled. On day one Meta showed delivery INACTIVE (status 441) while it fills; check it is usable before a traveller ad set excludes it |

Not done yet:

- **Ad set A interests**: the MCP server has no interest search, so none are set and nothing was
  checked against Meta's list. Add them in Ads Manager before publishing, or the ad set reaches
  everyone aged 25 to 60 in those seven countries.
- Ads, ad set B and the traveller campaign: not created (no creatives, audience gate, launch gates).
- The same draft also holds two older drafts from 19 Sep, "WanderBuddy IOS" and "New App promotion
  Campaign", both set to ACTIVE. Never publish them along with these.
