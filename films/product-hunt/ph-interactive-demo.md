# Product Hunt — interactive demo

## Why `wanderbuddyapp.com/demo/` was rejected

Nothing is wrong with the link. It returns 200 on all three variants
(`www` / apex / with and without the trailing slash).

Product Hunt's **Interactive demo** field is domain-allowlisted. It only accepts
URLs hosted by the seven providers it names in the help text:

| Provider | Host it validates |
|---|---|
| Arcade | `arcade.software` |
| Storylane | `storylane.io` |
| Supademo | `supademo.com` |
| Hexus | `hexus.io` |
| Layerpath | `layerpath.com` |
| ScreenSpace | `screenspace.io` |
| Guideflow | `guideflow.com` |

A self-hosted URL can never validate, however good the demo is. The field is
also optional — leaving it blank costs nothing, and the demo link still works in
the launch description, the first comment, and as a gallery item.

To fill the field, the demo has to be **re-created inside one of those tools**.
All seven are free for PH launches. We're on Supademo.

## Route A — upload the pre-built frame pack (recommended)

`marketing/launch/ph-demo-frames/` holds the whole guided run already captured:
**24 PNGs at 620x900 @2x**, plus `HOTSPOTS.md` and `frames.json`.

In Supademo, create a demo from images, upload `step-01.png` … `step-24.png` in
order, then work down `HOTSPOTS.md`. It carries one row per frame with the
callout copy (lifted from the demo's own captions) and the hotspot position as
**x/y percentages of the frame**, so you place each hotspot by number instead of
hunting for the button by eye. Percentages survive whatever size Supademo
renders at.

Frame 24 is the end card. It has no hotspot and carries both store QR codes
(`shots/qr_ios.png`, `shots/qr_play.png`) — point the CTA button at the store
listing there.

### Why not just record it live

The demo animates. `screenIn` runs 0.55s, the typing indicators and the DM
notification arm on timers, and actions like "Settle up" fire a toast that holds
2s then fades over 0.3s. A capture extension screenshots the instant you click,
so frames land mid-fade — the first pass of the capture script baked a
half-transparent "Paid Leo ฿180" toast across the Budget frame before the settle
gates were added. The pack waits each screen out.

The one thing the pack gives up is motion: the map pan, the typing dots, the
mic waveform become stills. If you want those, record live (Route B) and accept
some mid-animation frames, or check whether your Supademo tier includes **HTML
capture** — it clones the live DOM instead of screenshotting, and since the demo
is a self-contained static page, that would preserve the real interactivity.

## Route B — record live with the Supademo extension

1. Install the Supademo Chrome extension.
2. Open `https://www.wanderbuddyapp.com/demo/?clean=1` — `?clean=1` hides our own
   caption bar and the ↻ replay button so Supademo's callouts are the only text
   on screen. The pulsing amber hint ring stays visible; that's what you follow.
3. **Size the browser window to roughly 620 x 900.** At that size the phone
   fills the frame edge to edge. At 1280 x 800 it sits in a wide field of empty
   gradient that needs cropping afterwards.
4. Follow the ring: 23 clicks, then the end card. You cannot misclick — during
   the guided run the demo only lets the highlighted element through (the
   capture-phase handler on `.glass`).
5. Pause a beat after each click so animations finish before Supademo grabs the
   frame.

`HOTSPOTS.md` still works here as the shot list.

## Regenerating the pack

```bash
node marketing/launch/capture-demo-frames.mjs
```

Drives headless Edge over CDP against the live demo and rewrites
`ph-demo-frames/`. The walk is generic: the demo puts a `.hint` class on
whatever you're meant to tap next, so the script screenshots, clicks `.hint`,
waits for a *different* `.hint` to arm, and repeats. If the demo's guided path
changes, the script needs no edits — just re-run it.

Two things it has to get right, both learned the hard way:

- **Wait for the hint to move, not a fixed delay.** The AI answer renders on a
  typing delay, so a fixed wait screenshots the old target and clicks it twice,
  which silently skips the next step. The first run lost the "Pin it for
  tonight" beat entirely that way. Targets are marked as they're clicked and
  only an unmarked `.hint` is accepted.
- **Wait for toasts to clear** before each screenshot.

## Source of truth

The demo is `website/public/demo/index.html` (single file, ~83 KB, plus
`shots/`). The guided path is the `Q` array at line 875; the path lock is the
capture-phase click handler on `.glass` just below it. Captions in `HOTSPOTS.md`
are read from the live DOM at capture time, so they can't drift from the demo —
re-run the script rather than editing them by hand.
