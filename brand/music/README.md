# Reel audio

The real recordings every WanderBuddy reel is scored with. Copied 2026-11-02 from
`WanderBuddy_Ad/b2b-reels` on the founder's PC so cloud sessions can use them.
Never swap these for synthesized beds, chimes or whooshes.

| File | What it is | Source |
|---|---|---|
| `musicalmix2020-bossa-nova-summer-instrumental-brazil-7969.mp3` | The bossa nova bed under the voice | Pixabay, "Bossa Nova Summer" by Musicalmix2020 (human-made, not Content ID registered) |
| `piano/*.wav` | Ten single Steinway notes (G2, D3, B3, D4, B4, G4, D5, G5, B5, D6), 4 s each, used as the effects | University of Iowa Musical Instrument Samples, free for any use |
| `endcard_piano.mp4` | The finished blue end card with its piano notes | Our Blender end card (`marketing/outro`), CTA wanderbuddyapp.com/partners |

How the B2B reels use them (`WanderBuddy_Ad/b2b-reels/build/audio.py`):

- Music sits at -26.5 dB and ducks under the voice. Piano effects sit at -31 dB.
- The notes are a G major set. E and A are made by shifting D and G up a whole tone.
- Effects are short note patterns, e.g. a quick run up the keys for a swipe, G4 + D5 for a tap.
- Append the end card with a 0.3 s crossfade. Mix the whole reel to -14 LUFS (two-pass loudnorm).

The Pixabay track may be used in our videos but not shared as a standalone file. Keep this
repo private.
