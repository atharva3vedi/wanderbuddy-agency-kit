#!/usr/bin/env bash
# Lays the overlay over Blender's frames, adds the sound, writes the 30 s ad.
#   bash build/compose.sh          -> out/wanderbuddy-30s.mp4 (+ _share copy)
#   bash build/compose.sh 916      -> out/wanderbuddy-30s_9x16.mp4 (+ _share copy)
# Blender renders frames 1-796 (to 26.5 s); after that the end card covers the
# whole frame, so the last 3D frame is held under it. The hold is a 900-frame
# list of links in render/v30_<fmt>/base (ffmpeg's tpad ends early inside the
# overlay graph), kept apart from 3d/ so Blender never writes through one.
set -euo pipefail
cd "$(dirname "$0")/.."
fmt="${1:-169}"
R="render/v30_${fmt}"
name="wanderbuddy-30s"; [ "$fmt" = "916" ] && name="wanderbuddy-30s_9x16"
rm -rf "$R/base" && mkdir -p "$R/base"
last=""
for i in $(seq 1 900); do
  f=$(printf "%04d.png" "$i")
  [ -f "$R/3d/$f" ] && last="$f"
  ln -s "../3d/$last" "$R/base/$f"
done
# Chrome saves a fully opaque overlay frame (the wipe, the end card) without
# alpha; a format change mid-stream makes ffmpeg rebuild the graph and drop
# frames. Give every overlay frame the same RGBA format first.
rm -rf "$R/overlay_rgba" && mkdir -p "$R/overlay_rgba"
ffmpeg -y -hide_banner -loglevel error -framerate 30 -start_number 1 -i "$R/overlay/%04d.png" \
  -vf format=rgba -pix_fmt rgba -start_number 1 "$R/overlay_rgba/%04d.png"
ffmpeg -y -hide_banner -loglevel error \
  -framerate 30 -start_number 1 -i "$R/base/%04d.png" \
  -framerate 30 -start_number 1 -i "$R/overlay_rgba/%04d.png" \
  -i out/audio30.wav \
  -filter_complex "[0][1]overlay=format=auto,format=yuv420p[v]" \
  -map "[v]" -map 2:a -t 30 \
  -c:v libx264 -preset slow -crf 15 -profile:v high -tune film \
  -c:a aac -b:a 256k -movflags +faststart \
  "out/$name.mp4"
ffmpeg -y -hide_banner -loglevel error -i "out/$name.mp4" \
  -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 160k -movflags +faststart "out/${name}_share.mp4"
for f in "out/$name.mp4" "out/${name}_share.mp4"; do
  ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames:format=duration,size -of compact "$f"
done
