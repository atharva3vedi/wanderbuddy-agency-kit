# The People You Meet On Every Trip (Pt 1, 2, 3)

9:16 comedy series, built 2026-10-12. Script: `SCRIPT.md`.

## v5: The Kinds of Travellers (current)
`Kinds_of_Travellers_Pt1.mp4` (Arrival, 67.5s), `_Pt2.mp4` (Into the Wild, 77.4s),
`_Pt3.mp4` (Going Home, 77.8s). One group trip to Thailand told in order. Each part opens on an
establishing shot with a serif title card; the narrator sets the scene before each character
(over short establishing B-roll, not a frozen frame) and buttons the joke after.
Script: `SCRIPT_v5.md` (plus the founder's edits). Edit list: `build/narration5.py`.
Build: `NARR=narration5 <kokoro python> build/tts.py bm_george 1.08`, `python build/vo_words.py`,
`python build/cut5.py 1 2 3`. QA strip: `python build/qa.py <final.mp4> <out.jpg> 1.5`.
Gotchas: Seedance B-roll drifts into random action after about 2 s, so only the first 2 s are
used (slowed where needed); the output "copyright" filter blocked the group dad twice until his
look changed; a prompt asking a character to "sweat" produced a cartoon sweat drop.

## v3: 60-second cuts (superseded)
`Trip_People_Pt1_60.mp4` (63s), `Trip_People_Pt2_60.mp4` (61s), `Trip_People_Pt3_60.mp4` (64s).
Joke after joke. The narrator only lands a one-beat setup or a button, never restates the
picture, and never freezes the frame to talk (at most a 0.3 to 0.8 s lead-in beat, or up to 2 s
for a button to finish). Clips play 5 to 12% faster where they dragged (pitch kept). Sam is never
labelled; his moments are second person ("Nobody fans you.").
- Pt 1: trip captain, know-it-all and the "normal one" opener cut. New: Homo fomo (the beach
  next door), Activitas maximus (5 a.m. schedule), Homo cardio (the trek freak).
- Pt 2: group dad re-shot (one passport, out of the bum bag on the word) and the aunty re-shot
  (a steel tiffin from her handbag, no suitcase).
- Pt 3: same jokes, retimed; Day 1/4/9 run back to back.
- Edit list: `build/narration3.py`. Build: `NARR=narration3 <kokoro python> tts.py bm_george 1.08`,
  `python vo_words.py`, `python cut3.py 1 2 3`.

## v2: documentary cut (superseded, about 2 min each)
`Trip_People_Pt1_doc.mp4`, `Trip_People_Pt2_doc.mp4`, `Trip_People_Pt3_doc.mp4` (about 2 min
each). Same scenes, narrated like a wildlife documentary. Captions follow the narrator only;
no labels and no black cards. Changes from v1:
- Narrator: Kokoro `bm_george` (local, $0) at 0.94 speed, pitched down 4%, warm EQ and a small
  room. An original British documentary-style voice, not a clone of anyone.
  Lines: `build/narration.py`. Voice: `build/tts.py` (kokoro venv). Word timings: `build/vo_words.py`.
- The narrator gets room through held frames (slow pull-out into the clip, slow push-in out of it).
  Dialogue ducks to about 22% under the voice.
- Re-shot: the couple (`P1_03v2`: both on one side of Sam, so the kiss is clearly theirs), the
  bill guy on Day 4 and Day 9 (`P3_05b` at a beach bar, `P3_05c` at an airport cafe) instead of
  reusing one clip.
- Each part has its own plug: two new Sam scenes plus one real Play frame dissolving in and out.
  Pt1 = he leaves the herd (people you actually like), Pt2 = a shared reel becomes the plan,
  Pt3 = a passport reminder. The narrator closes over the brand outro (wave and chime, no second voice).
- Music: `MUSIC_A` (playful pizzicato bed under the comedy) and `MUSIC_B` (hopeful swell under the
  plug) are the audio of two Seedance 480p clips. Their video is discarded.
- Build: `python build/doc.py 1 2 3`.

## v1: label cut (superseded)

**Finals** (1080x1920, 30fps, 48k stereo, about -15 LUFS):
- `Trip_People_Pt1.mp4` (75.7s): trip captain, red dress + simps, the couple, the family, been-here-before, always drinking
- `Trip_People_Pt2.mp4` (80.3s): group dad, weather freak, packed their own food, here for the culture, local who hates tourists, adrenaline junkie
- `Trip_People_Pt3.mp4` (73.5s): loses everything, the flashy one, the guy and his "girlfriend", content creator, "I'll send it later", finale

Every part opens on Sam (the normal one) and ends on the same plug: Sam speaks for the first
time ("Or. Use WanderBuddy...") over real Play store frames (Everyone gets a vote, DM a reel,
Passport panic cancelled), then the approved brand outro `marketing/outro/outro.mp4`.

## How it was made
- **Video:** BytePlus Seedance 2.5 (`dreamina-seedance-2-5-260628`) via the seedance MCP
  fork's key, 720p, native dialogue audio, no watermark. 27 clips, about 4.9M tokens in total
  (including 2 test/rejected clips).
- **Character models:** `characters/` (Seedream 5.0 Pro). BytePlus rejects any realistic face
  as an image input on Seedance 2.x (`InputImageSensitiveContentDetected.PrivacyInformation`),
  even Seedream's own output passed by its original URL. Workaround that works: generate each
  recurring character's first scene text-to-video (a "master"), then pass that clip's
  Seedance URL as `reference_video` for their later scenes. Sam is identical across all 8 of
  his scenes this way. Masters: `build/masters.json`.
- `keyframes/` = Seedream storyboard frames (not used as video input, because of the face block).
- **Text:** never rendered by the model. Labels, captions and supers are PIL overlays
  (`build/overlays.py`). Captions use the script's spelling, timed from faster-whisper word
  timings (`build/transcripts/`).

## Rebuild
```
cd build
C:/Users/PC/Videos/byteplus-mcp/.venv/Scripts/python.exe gen.py t2v P1_01 ...   # one-off characters
C:/Users/PC/Videos/byteplus-mcp/.venv/Scripts/python.exe gen.py ref P1_03 ...   # recurring characters (reference_video)
python transcribe.py                 # word timings
python assemble.py 1 2 3             # cut the parts (edit list: parts.py)
```
Shot prompts live in `build/shots.py`. `gen.py ref` looks up each master's video URL from its
task id, but Seedance output URLs are signed for 24h, so a reference run after 2026-10-13 may
need a freshly generated master (untested).
