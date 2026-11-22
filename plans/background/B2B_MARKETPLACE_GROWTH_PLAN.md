# WanderBuddy: B2B + Marketplace Growth Plan

**Audience:** a skeptical operator/investor who will attack every soft number.
**Purpose:** show the model survives being attacked, not that it looks good on a slide.
**Companion to:** `marketing/GROWTH_PLAN.md` (consumer app strategy). This document adds the
two revenue layers on top of it: B2B SaaS and a curated-trips marketplace.

> A note on "predictive analysis, not model data." A spreadsheet that multiplies a made-up
> growth rate for 36 months is theater. This plan instead: (1) names the 3 variables the whole
> outcome hangs on, (2) reasons from real analog companies and funnel benchmarks, (3) gives
> bear/base/bull cases with the *driver* behind each, (4) states the leading indicators we watch
> monthly, and (5) states the kill criteria that would make us stop. If the reader can't attack
> the assumptions because they're hidden, it's bullshit. Everything load-bearing is labeled.

---

## 0. The one thesis (say this first, out loud)

**WanderBuddy is the operating system for group trips, monetized three ways off one product:
a SaaS subscription to professional operators, a take rate on a creator-led trips marketplace,
and a consumer app that aggregates the demand and manufactures the next generation of hosts.**

The non-obvious point, and the thing that makes it more than "another travel app": the B2B ops
tooling and the marketplace supply tooling are **the same product**. A travel agency running a
group tour needs exactly what a travel creator running a curated trip needs: coordination,
live translation, itinerary, live location, documents, payments, one shared room. So we monetize
the same supply-side software twice: predictable subscription revenue *and* variable take-rate
revenue on the trips that flow through it.

Closest real comparables (so this isn't invented in a vacuum):
- **TrovaTrip** — creator brings the audience, platform runs the trip, take rate on seats. Proves
  the "creator-led group trip" demand model has real GMV. WanderBuddy's edge over it: deeper
  in-trip ops + live translation + a Southeast Asia supply base it doesn't own.
- **WeTravel** — B2B payments/ops for tour operators. Proves operators will adopt software to run
  group trips. Our edge: the traveler-facing experience and translation, not just back-office.
- **Airbnb Experiences / GetYourGuide** — ~20-30% take rates. Our 10% is a *deliberate* wedge to
  win supply, and we recapture margin through the subscription on the same host (see §3, §4).

---

## 1. The three attacks a serious person will make, and the honest answers

**Attack 1: "Why would anyone pay $500-1000/month when WhatsApp, spreadsheets, and existing tour
software are free or cheaper?"**
Answer: because for a small operator the alternative is not free, it's a person. A DMC or small
tour operator running group trips loses 10-15 hours/week to coordination chaos across WhatsApp,
sheets, PDFs, and manual translation. At even a modest SEA ops cost, that labor alone is worth
~$400-600/month, before any revenue upside. We price *under* the pain, not over the feature list.
The $500 tier is defended by ROI, not by a feature grid (§3).

**Attack 2: "Two-sided marketplaces are a graveyard. How do you solve cold start? Who shows up
first to an empty platform?"**
Answer: we never run a cold marketplace. We recruit **supply that carries its own demand**: travel
creators, expert guides, and community leaders who already have an audience. The host fills the
trip from their followers; the platform never pays to acquire that traveler. This is the entire
reason a group-travel marketplace can work where a pure consumer travel app burns cash on CAC.
We prove it with 10-20 lighthouse hosts before spending a dollar scaling supply (§4, §6).

**Attack 3: "Consumer travel CAC will bury you. Show me the payback."**
Answer: on the marketplace side we largely don't pay traveler CAC — the host does, with their
existing audience. Our paid acquisition is aimed at *hosts and agencies*, a far smaller, higher-
value, reachable population, not millions of consumers. That inverts the usual travel-app death
math. Where we do spend on consumers, it's to convert marketplace travelers into repeat app users
and future hosts, funded by GMV we've already earned (§5, §8).

---

## 2. Two motions, one product

| | **B2B SaaS (operators)** | **Marketplace (creators/hosts + travelers)** |
|---|---|---|
| Customer | Travel agencies, DMCs, small tour operators, hostel/adventure brands | Supply: creators, guides, community leaders. Demand: individuals |
| We charge | Subscription: $100 → $500 → $1,000/mo | 10% service fee on each seat sold |
| Their job-to-be-done | Run their existing group trips without ops chaos | Host: run sold-out trips with zero ops. Traveler: join a curated trip safely |
| Revenue shape | Predictable, recurring, expands with seats | Variable, scales with GMV, spiky per trip |
| Why it's the same product | Both need the coordination/translation/ops OS | Same, plus payments + discovery + trust |

The strategic insight to state explicitly: **a professional host is both customers at once.** They
pay the subscription to run trips *and* pay the 10% on seats sold. Blended take on an active
professional host is well above 10% (§4.3). That's how the low headline take rate is not a
giveaway.

---

## 3. B2B SaaS: the pricing ladder, defended

You're at $100/mo for the first 10 pilots. Correct move: price low to buy proof, not to make
money. The pilots are not a revenue line, they are a **case-study factory**. Instrument them now
(see §3.3) or you'll reach $500 with no evidence to justify it.

### 3.1 The tiers (capability + ROI gated, not arbitrary)

| Tier | Price | Who | What they get | What justifies the price |
|---|---|---|---|---|
| **Pilot / Starter** | $100/mo | Solo operator, first group trips | Core OS: coordination room, itinerary, live location, documents, translation, WhatsApp bot, up to a capped # of active travelers/trips | "Cheaper than the chaos." Land, prove, instrument |
| **Pro** | $500/mo | Established small operator/DMC | Higher seat caps, light white-label (their brand in the room), priority support, ROI dashboard (hours saved, traveler NPS) | Replaces ~10-15 hrs/wk of coordination labor + reduces refunds/complaints. Pays for itself on labor alone |
| **Scale** | $1,000/mo | Multi-trip operator, brand, or DMC network | Unlimited seats, API/integrations, dedicated CSM, co-marketing, **featured placement in the marketplace** (demand back to them), multi-user teams | Becomes a revenue *channel*, not just a cost saver: marketplace featuring fills their trips |

The ladder only works if each rung adds value the previous one didn't. The jump to $1,000 is
justified by turning the tool into a **demand channel** (marketplace featuring), which is the
one thing an operator can't get from generic software. That's the upsell hook.

### 3.2 ICP (be specific, "travel agencies" is too vague to sell to)

Beachhead: **Southeast Asia small-to-mid group tour operators and DMCs** running 2-10 group
departures/month, 8-20 travelers each, currently coordinating on WhatsApp + spreadsheets, with
multilingual traveler pools (the translation wedge is worth the most exactly here). Adjacent:
hostel chains and adventure brands that run group experiences. This is a **reachable** population
(trade associations, LinkedIn, trade shows), which is what makes the CAC math sane.

### 3.3 Instrument the pilots NOW (this is the credibility engine)

For each of the 10 pilots capture, from day one:
- Hours/week the operator spent coordinating before vs. after.
- Traveler NPS / complaint rate before vs. after.
- Any revenue the operator attributes to WanderBuddy (repeat bookings, referrals, premium pricing).
Three signed case studies with real numbers are worth more than any deck. They are also your
proof that $100 → $500 is earned, not hoped.

### 3.4 B2B GTM (how you actually get them)

1. **Founder-led outbound** to the SEA operator ICP: LinkedIn, direct email, trade associations
   (PATA, ASEANTA), and one anchor trade event (e.g., ITB Asia) for concentrated supply.
2. **Lead with the wedge, not the feature list.** A 5-minute live demo of the translation room +
   WhatsApp coordination closes better than a 30-slide feature tour. Show the one thing nobody
   else does.
3. **Land → prove → expand.** $100 pilot → 60-90 days → ROI review with their own numbers → move
   to $500. The expansion conversion rate is a top-3 metric to watch (§7).
4. **Partnerships as a channel:** DMC networks, hostel groups, language schools. One partnership
   that refers 10 operators beats 100 cold emails.

---

## 4. The marketplace, built to actually work

### 4.1 The model in one line

Creators/hosts list a curated group trip, set the ticket price, and keep 90%. WanderBuddy takes
**10%** and provides the software to run the trip end to end. Travelers discover and join.

### 4.2 Solving cold start (the only question that matters here)

Marketplaces die at the empty state. The rule: **supply first, and only supply that brings its
own demand.**
1. Recruit **10-20 lighthouse hosts** by hand: SEA travel creators/micro-influencers, expert
   guides, community leaders. Not "anyone," specifically people with an audience that trusts them.
2. Give the host the pitch: *"Run a sold-out group trip, keep 90%, and never touch logistics,
   translation, payments, or the group chat. We handle the operating system, you bring your
   people."*
3. Subsidize the **first** trip's risk for lighthouse hosts (marketing support, a fill guarantee,
   or fee waiver) to de-risk their leap. You are buying proof, not margin.
4. The host fills seats from their followers. Those travelers become WanderBuddy users inside a
   great trip. A fraction become future hosts or bring their own next group. That's the flywheel
   (§8), and it starts on the supply side, deliberately.

Demand-side paid acquisition of random travelers comes **last, if ever.** If the host can't fill
the trip from their own audience, the thesis is wrong and we want to learn that on trip #1 for
20 hosts, not after we've spent on ads (§9 kill criteria).

### 4.3 Unit economics (assumptions labeled; attack them)

Base-case assumptions (SEA mid-market, deliberately conservative):
- Avg curated trip ticket price: **$1,200** (range $600 budget group → $3,000 premium). `ASSUMPTION`
- Seats sold per completed trip: **10** (capacity ~15, ~67% fill). `ASSUMPTION`
- Trips per active host per year: **3**. `ASSUMPTION`

Then, per completed trip:
- GMV = 10 × $1,200 = **$12,000**
- WanderBuddy take @10% = **$1,200/trip**

Per active professional host per year (the real unit):
- Marketplace take: 3 trips × $1,200 = **$3,600/yr**
- If also on the $500 SaaS tier: **$6,000/yr**
- **Combined: ~$9,600/yr per professional host**, i.e. a blended effective take far above 10%.

That last number is the answer to "isn't 10% too low to build a business on." We don't build it
on 10%. We build it on 10% **plus** subscription on the same account, plus (later) payment float
and add-on services. The low headline take is a customer-acquisition weapon against TrovaTrip and
Airbnb's 20%+, not a resignation to thin margins.

### 4.4 Host economics (why they choose you)

A host selling 10 seats at $1,200 grosses $12,000, keeps **$10,800** after our fee, and does
**none** of the logistics. On TrovaTrip/Airbnb-style 20% they'd keep $9,600. We are $1,200/trip
cheaper to the host *and* we run more of the trip. That is a concrete, defensible reason for
supply to pick us. State it in dollars, not adjectives.

---

## 5. Predictive analysis: bear / base / bull (24 months, with drivers)

Not a single hockey stick. Three futures, each tied to *why*.

**BEAR — "the creator thesis is weak."**
Driver: hosts can't fill trips from their own audience (fill <50%), few stay active (~15 hosts),
pilots resist the jump to $500 (only ~30% convert).
Outcome: ~$150k-250k ARR at month 24, mostly B2B. Signal to **pivot to a pure B2B SaaS company**
and shelve the marketplace.

**BASE — "unsexy but real."**
Drivers: ~60 paying agencies at a blended ~$450/mo (mix of $100/$500/$1,000) = **~$324k B2B ARR**;
~40 active hosts × 3 trips × $1,200 take = **~$144k marketplace**, with subscription overlap on
the professional hosts.
Outcome: **~$450k-600k combined ARR by month 24.** Legible, defensible, fundable. This is the
number you should quote as the plan, not the bull case.

**BULL — "the flywheel ignites."**
Drivers: 2-3 lighthouse hosts go viral, fill rate climbs to ~75%, repeat travelers appear, host
count reaches ~150 and agencies ~120.
Outcome: **~$1.5M-2M ARR.** Possible, not promised. Present it as upside, and immediately say what
has to be true for it (below). A skeptic trusts you *more* when you refuse to lead with this.

### 5.1 Sensitivity: the outcome hangs on 3 variables, not 30

Ranked by impact on ARR:
1. **Fill rate per trip** (empty seats = zero GMV). The single most important number in the model.
2. **Active host count and host retention** (do lighthouse hosts run trip #2, #3?).
3. **Pilot → $500 expansion rate** on the B2B side.

Notably **low-impact:** the take rate (10% vs 15%) and the exact ticket price move the answer far
less than fill × active hosts. So the one metric to obsess over is **seats filled per active host
per year**, not the fee. Optimizing the fee would be optimizing the wrong thing, and saying so
signals you understand your own model.

### 5.2 Leading indicators (the monthly dashboard)

- B2B: pilot→paid conversion %, $100→$500 expansion %, logo churn, documented hours-saved/agency.
- Marketplace: host **activation** rate (listed a trip within 30 days of joining), **fill rate**
  per trip, GMV per host, repeat-host rate, realized blended take.
These are the numbers that move *before* revenue does. They tell you the thesis is working months
ahead of the ARR line.

---

## 6. The 90-day plan (concrete, testable, cheap)

**B2B (prove the ladder):**
- Instrument all 10 pilots for hours-saved and NPS. Produce 3 signed case studies with real numbers.
- Move at least 4 of 10 pilots from $100 to $500 on the strength of their own ROI data.
- Open 20 new SEA operator conversations via founder outbound + 1 partnership channel.

**Marketplace (prove cold start solves):**
- Sign 10-20 lighthouse hosts. Ship the host onboarding + payments + a "run your trip" flow good
  enough to run a real trip.
- Get at least 10 hosts to **list** a trip and run **first departures**. Measure fill rate honestly.
- Do NOT spend on demand-side ads. The test is whether hosts fill from their own audience.

**The 90-day verdict:** if lighthouse hosts fill >50% from their own followers, the marketplace is
real and you scale supply. If not, you have a very good B2B SaaS company and you say so.

---

## 7. Metrics that would convince the skeptic (and that we hold ourselves to)

| Metric | Base target by mo 24 | Why he cares |
|---|---|---|
| Pilot → paid ($500) conversion | ≥ 40% | Proves B2B value is real, not charity pricing |
| Net revenue retention (B2B) | ≥ 110% | Proves the ladder ($100→$500→$1,000) expands |
| Host activation (listed within 30d) | ≥ 60% | Proves supply isn't dead weight |
| Fill rate per trip | ≥ 60% | The variable the whole model hangs on |
| Repeat-host rate | ≥ 50% | Proves host LTV, the real asset |
| CAC payback (B2B) | < 12 months | Proves you can scale without burning |

---

## 8. The flywheel (draw this on one slide)

Hosts bring travelers → travelers experience the WanderBuddy OS + translation inside a great trip →
a fraction become hosts or bring their own next group → agencies see marketplace demand and want
the SaaS tooling to compete → more supply → more trips → more demand and more trip data → better
curation and trust → more hosts. Community and multilingual trip data compound into a moat a
generic clone (e.g. Welago) can't copy quickly, because the moat is **supply relationships +
in-trip data**, not features.

---

## 9. Risks, and the parts most plans hide (this is where you win his trust)

**Regulatory / liability — do not skip this, he will ask.**
Running trips means someone is legally the seller of travel and someone is liable when a trip goes
wrong. Position: **WanderBuddy is software + a marketplace facilitator, not the tour operator.**
The host is the operator/seller of record.
- **Payments:** use a licensed processor with connected accounts (e.g. Stripe Connect or SEA
  equivalent); WanderBuddy takes the 10% as a platform application fee. **Warning:** holding
  travelers' money for future travel can trigger money-transmission / escrow / seller-of-travel
  rules in some jurisdictions. This is a real legal workstream, not a checkbox.
- **Liability:** TOS allocates trip liability to the host; require hosts to carry/attest insurance;
  traveler waivers. Platform carries its own coverage.
- **Licensing:** some markets require sellers of travel to register (e.g. Singapore travel-agent
  licensing under STB; California Seller of Travel; others). Map this per launch market with a
  lawyer before opening the marketplace, not after.
Saying this unprompted is the single strongest "not bullshit" signal in the whole conversation.

**Other risks and the honest mitigations:**
- **Marketplace cold start** → supply-first + creator-brings-audience + subsidized lighthouse trips.
- **Traveler LTV is thin** (people take 1-2 group trips/year). Be honest: the recurring asset is the
  **host relationship (SaaS) and the community**, not the individual traveler. Don't model traveler
  subscriptions as the engine.
- **Infra cost wall** (Stream free tier caps ~2.9k users; Tokyo→Singapore DB migration). Known,
  budgeted, sequenced in `GROWTH_PLAN.md`. Marketplace GMV funds the upgrade.
- **Trust and safety** (strangers on a trip). Verification, reviews, host vetting, incident process.
  This is a cost of doing marketplace business; budget for it.
- **Competition** (Welago near-clone). Moat = supply relationships + ops depth + translation + SEA
  focus, not a feature list.

**Kill criteria (state these before he does):**
- If <50% of lighthouse hosts fill their first trip from their own audience in 90 days → the
  creator-demand thesis is unproven → stop scaling supply, become a B2B SaaS company.
- If <40% of pilots convert to $500 in 90 days → the B2B value prop needs rework before scaling.
Naming your own kill switches is the move that separates you from every founder who thinks their
idea can't fail.

---

## 10. What I need from you to tighten the numbers

The model above uses three labeled assumptions that drive everything. Confirm or correct them and
the predictive cases sharpen immediately:
1. **Average trip ticket price** in your beachhead (I used $1,200).
2. **Seats per trip and realistic fill** (I used 10 of ~15).
3. **Who exactly is the $500-$1,000 B2B buyer** — I assumed SEA tour operators/DMCs. If it's the
   professional *hosts* instead, the two motions collapse into one and the story gets simpler.

---

*Complements `marketing/GROWTH_PLAN.md`. Pricing here (B2B $100/$500/$1,000; marketplace 10% take)
supersedes the consumer-only pricing spine for these two motions.*
