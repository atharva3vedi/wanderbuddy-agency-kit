# WanderBuddy Reddit posters

Square (1:1) poster series for organic Reddit posting. Deliberately anti-ad:
they read as something a person made, land a joke, and only then point at the
app. One recognizable visual system so the deep-blue starts getting noticed in
the feed.

## The system

- **Field:** the app's dark "Mission Control" navy canvas (`app_colors.dart`
  dark bg), a `radial-gradient` from `#1d3d5e` down to `#0a1622`. Chosen over
  the light azure so white text pops and the poster keeps a crisp edge on
  dark-mode Reddit feeds too. Amber (`#F2A93B`) is the single accent, used on
  exactly one word/line per poster: the punchline.
- **Logo:** real mark (twin peaks + wave) drawn inline from `assets/icon-master.svg`,
  plus the "WanderBuddy" wordmark, locked in the footer of every poster.
- **Voice:** the running joke is "every group has one person who plans
  everything and keeps everyone alive, and they are tired." Warm, not cynical.
  Recurring tagline family: *book first, figure it out together* / *we plan the
  trip, you sit down*.
- **Hard rule:** no em dashes anywhere (founder's call, it's the AI-slop tell).
  Plain hyphens only.

## Files

| Concept | Source | PNG |
|---|---|---|
| Now Hiring (job-post parody) | `poster_now_hiring.html` | `now_hiring.png` |
| True Story (fake testimonial) | `poster_testimonial.html` | `testimonial.png` |
| Full Itinerary (`??????` = step 2) | `poster_itinerary.html` | `itinerary.png` |
| JAPAN (flat-geometric Fuji) | `poster_japan.html` | `japan.png` |
| Handle With Care (hazard label) | `poster_warning.html` | `warning.png` |
| Missing (lost-flyer + tear tabs) | `poster_missing.html` | `missing.png` |
| Support Group (community flyer) | `poster_support.html` | `support.png` |

## Re-rendering

Each HTML is a self-contained 1080x1080 page. Render to a crisp 2160x2160 PNG
with headless Edge (no fonts/CDN needed; uses Windows system fonts):

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
& $edge --headless=new --disable-gpu --hide-scrollbars `
  --force-device-scale-factor=2 --window-size=1080,1080 `
  --screenshot="now_hiring.png" "file:///<abs-path>/poster_now_hiring.html"
```

Edit the HTML, re-run, done. Keep the footer lockup and navy field constant so
the set stays recognizable; vary the middle.
