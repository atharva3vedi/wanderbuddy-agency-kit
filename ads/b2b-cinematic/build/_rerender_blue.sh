#!/bin/zsh
# One-off (2026-11-12): re-render what the blue alignment fixes touch, then re-cut all four films.
cd "$(dirname "$0")/.." || exit 1
B=/Applications/Blender.app/Contents/MacOS/Blender
"$B" -b --factory-startup -P build/endcard_v2.py > render/endcard_v2.log 2>&1; echo "endcard_v2 exit $?"
"$B" -b --factory-startup -P build/endcard_v3.py > render/endcard_v3.log 2>&1; echo "endcard_v3 exit $?"
run() { WB_FROM=$2 WB_TO=$3 "$B" -b --factory-startup -P "build/$1.py" >> "render/$1_fix.log" 2>&1; echo "$1 $2-$3 exit $?"; }
run agencies2 620 697
for f in $(seq 564 697); do
  cp "render/agencies2/3d/$(printf '%04d' "$f").png" "render/opened/3d/$(printf '%04d' $((f - 48))).png"
done
run opened 320 355
run monsoon 468 515
run monsoon 580 659
python3 build/agencies2_compose.py && echo "agencies2 cut ok"
python3 build/opened_compose.py && echo "opened cut ok"
python3 build/monsoon_compose.py && echo "monsoon cut ok"
python3 build/day2_compose_v2.py && echo "day2 cut ok"
ls -la out/v3-three-agencies.mp4 out/v2-opened-3-times.mp4 out/v2-monsoon.mp4 out/v2-day2.mp4
