#!/bin/zsh
# One-off (2026-11-12): re-render only the frames the three fixes touch, then re-cut.
cd "$(dirname "$0")/.." || exit 1
B=/Applications/Blender.app/Contents/MacOS/Blender
run() { WB_FROM=$2 WB_TO=$3 "$B" -b --factory-startup -P "build/$1.py" >> "render/$1_fix.log" 2>&1; echo "$1 $2-$3 exit $?"; }
run opened 0 239
run opened 352 419
python3 build/opened_compose.py && echo "opened cut ok"
run monsoon 0 83
run monsoon 440 515
python3 build/monsoon_compose.py && echo "monsoon cut ok"
run agencies2 192 347
run agencies2 468 563
python3 build/agencies2_compose.py && echo "agencies2 cut ok"
ls -la out/v2-opened-3-times.mp4 out/v2-monsoon.mp4 out/v3-three-agencies.mp4
