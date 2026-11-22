#!/bin/zsh
# One-off queue (2026-11-11): when the Monsoon render (pid $1) ends, cut Monsoon,
# then render and cut Opened 3 Times. One Blender at a time.
cd "$(dirname "$0")/.." || exit 1
B=/Applications/Blender.app/Contents/MacOS/Blender
while kill -0 "$1" 2>/dev/null; do sleep 10; done
echo "monsoon frames: $(ls render/monsoon/3d | wc -l)"
python3 build/monsoon_compose.py && echo "monsoon cut ok"
mkdir -p render/opened/3d
for f in $(seq 564 697); do
  cp "render/agencies2/3d/$(printf '%04d' "$f").png" "render/opened/3d/$(printf '%04d' $((f - 48))).png"
done
WB_RESUME=1 "$B" -b --factory-startup -P build/opened.py > render/opened_render.log 2>&1
echo "opened render exit $? frames: $(ls render/opened/3d | wc -l)"
python3 build/opened_compose.py && echo "opened cut ok"
ls -la out/v2-*.mp4 out/v3-*.mp4
