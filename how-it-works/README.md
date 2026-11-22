# How it works

WanderBuddy is three products that feed each other: an **app** for travellers, a **CRM** for travel agencies, and a **marketplace** where agencies list trips and travellers book them.

```mermaid
flowchart LR
  A["Agency"] -- "lists trips" --> M["Marketplace"]
  T["Traveller"] -- "finds a trip" --> M
  M -- "books" --> C["CRM"]
  C -- "itinerary" --> P["Trip app"]
  T -- "travels" --> P
```

## The loop

1. An agency lists a trip on WanderBuddy. Listing is free.
2. We bring travellers to it: the website, trip search, and our ads. That last part is where you come in.
3. A traveller asks a question or holds a spot. It lands in the agency's CRM inbox, and the assistant answers in seconds.
4. The agency confirms, sends a branded itinerary and takes payment, all from the CRM.
5. The guests join the trip in the app and travel with it: chat, plan, map, costs.

WanderBuddy earns a fee only when a traveller books.

---

## 1. The app, for travellers

One place for the whole group: chat, vote on plans, a shared itinerary, a live map, split costs, a vault for tickets and passports, and Live Conversation, where everyone speaks their own language. Forward the reels you saved on Instagram and get a real plan back. Free on iPhone and Android.

<table><tr>
<td align="center"><img src="img/app-home.jpg" width="150"><br><sub>Home</sub></td>
<td align="center"><img src="img/app-chat.jpg" width="150"><br><sub>Group chat</sub></td>
<td align="center"><img src="img/app-live-map.jpg" width="150"><br><sub>Live map</sub></td>
<td align="center"><img src="img/app-split-costs.jpg" width="150"><br><sub>Split costs</sub></td>
<td align="center"><img src="img/app-saved-reels.jpg" width="150"><br><sub>Saved reels into a plan</sub></td>
</tr></table>

## 2. The CRM, for agencies

Where an agency runs its business. Every agency gets its own branded address, like `wanderbuddyapp.com/<agency>crm`. It is sold in three parts, and most agencies take all three:

- **CRM and itinerary maker.** Leads, bookings, payments, calendar, and beautiful PDF itineraries in the agency's brand.
- **The assistant.** AI on the agency's own WhatsApp and Instagram that answers travellers and hands over to a person.
- **The app dashboard.** The agency's guests get the trip app, and the agency sees who joined and how the trip is going.

<table><tr>
<td align="center"><img src="img/crm-inbox.jpg" width="380"><br><sub>Inbox with the assistant</sub></td>
<td align="center"><img src="img/crm-itinerary-studio.jpg" width="380"><br><sub>Itinerary maker</sub></td>
</tr><tr>
<td align="center"><img src="img/crm-listings.jpg" width="380"><br><sub>Listings and holds</sub></td>
<td align="center"><img src="img/crm-trip-app-dashboard.jpg" width="380"><br><sub>Who joined the trip app</sub></td>
</tr></table>

## 3. The marketplace, for both

Travellers describe the trip they want in their own words ("a beach week in Bali under US$900") and see group trips that fit, run by real agencies. They ask, hold a spot or book. Agencies list for free and pay a small fee only when a traveller books.

<table><tr>
<td align="center"><img src="img/site-home.jpg" width="380"><br><sub>wanderbuddyapp.com</sub></td>
<td align="center"><img src="img/site-trips.jpg" width="380"><br><sub>Find a group trip</sub></td>
</tr><tr>
<td align="center"><img src="img/market-trip-page.jpg" width="160"><br><sub>A trip page, on the phone</sub></td>
<td align="center"><img src="img/site-partners.jpg" width="380"><br><sub>For agencies: sell your trips free</sub></td>
</tr></table>

## Live links

| | |
|---|---|
| Website | https://wanderbuddyapp.com |
| Find a trip | https://wanderbuddyapp.com/trips |
| For agencies | https://wanderbuddyapp.com/partners |
| Agencies book a call | https://wanderbuddyapp.com/partners/call |
| CRM demo, no login | https://wanderbuddyapp.com/trydemo |
| App Store | https://apps.apple.com/app/id6795848498 |
| Google Play | https://play.google.com/store/apps/details?id=com.wanderbuddy.wanderbuddy |

The long version of all this, on film: [`ads/investor-demo`](../ads/investor-demo) (2 minutes) and [`films/launch-film`](../films/launch-film).
