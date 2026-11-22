#!/usr/bin/env bash
# Lays the overlay over Blender's frames, adds the score, writes the investor demo.
#   bash build/compose.sh   -> out/wanderbuddy-investor-demo.mp4 (+ _share copy)
# The 3D comes from two renders (see below); after the agency film's last frame the end card
# covers the whole frame, so the last 3D frame is held under it. The hold is a list of links in
# render/base (ffmpeg's tpad ends early inside the overlay graph).
set -euo pipefail
cd "$(dirname "$0")/.."
N=2856   # 119 s at 24 fps
name="wanderbuddy-investor-demo"
rm -rf render/base && mkdir -p render/base
# The film's clock: 0-7 s and the agency film come from render/3d (old timeline), the friends' act
# (7-40 s, frames 168-959) from render/3d_act. The agency film is the old one moved 792 frames later.
A0=168; AN=792
last=""
for i in $(seq 0 $((N - 1))); do
  f=$(printf "%04d.png" "$i")
  if   [ "$i" -lt "$A0" ];          then src="3d/$f"
  elif [ "$i" -lt $((A0 + AN)) ];   then src="3d_act/$f"
  else
    j=$((i - AN)); [ "$j" -gt 1920 ] && j=1920
    src="3d/$(printf "%04d.png" "$j")"
  fi
  ln -s "../$src" "render/base/$f"
done
# Chrome saves a fully opaque overlay frame (the end card) without alpha; a format
# change mid-stream makes ffmpeg rebuild the graph and drop frames. Normalise first.
rm -rf render/overlay_rgba && mkdir -p render/overlay_rgba
ffmpeg -y -hide_banner -loglevel error -framerate 24 -start_number 0 -i "render/overlay/%04d.png" \
  -vf format=rgba -pix_fmt rgba -start_number 0 "render/overlay_rgba/%04d.png"
ffmpeg -y -hide_banner -loglevel error \
  -framerate 24 -start_number 0 -i "render/base/%04d.png" \
  -framerate 24 -start_number 0 -i "render/overlay_rgba/%04d.png" \
  -i out/score.wav \
  -filter_complex "[0][1]overlay=format=auto,format=yuv420p[v]" \
  -map "[v]" -map 2:a -t 119 \
  -c:v libx264 -preset slow -crf 16 -profile:v high -tune film \
  -c:a aac -b:a 256k -movflags +faststart \
  "out/$name.mp4"
ffmpeg -y -hide_banner -loglevel error -i "out/$name.mp4" \
  -c:v libx264 -preset slow -crf 24 -c:a aac -b:a 160k -movflags +faststart "out/${name}_share.mp4"
for f in "out/$name.mp4" "out/${name}_share.mp4"; do
  ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames:format=duration,size -of compact "$f"
done
