"""The brand-blue end card for the second-pass films (two-line close) (Brand Codex 07): the white peaks
rise from the sea, the wave forms, the wordmark lifts, then the line and the URL.

  Blender -b --factory-startup -P build/endcard.py

The card itself is app-25s/build/shots.py end(), unchanged, on wb_ref.py (a copy
of app-25s/build/wb.py) with this folder's endcard.json: 24 fps, 84 frames.
Output: render/endcard/####.png (opaque #2072B8).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["WB_TL"] = os.path.join(HERE, "endcard_v2.json")
sys.path.insert(0, HERE)
import bpy  # noqa: E402
from wb_ref import *  # noqa: E402,F401,F403
import wb_ref  # noqa: E402

wb_ref.SCR = os.path.join(os.path.dirname(HERE), "screens")


def end():
    n = 84
    sc, cam = new_scene(n, samples=24, transparent=False, world=FIELD)
    ov = overlay(cam)
    E = TL["layout"]["end"]
    M = E["m"]
    MM = E["mm"]
    gap = 0.18 * M
    ww = 0.656 * M * 134 / 21
    total = MM + gap + ww
    mx, my = -total / 2 + MM / 2 - 14.5, E["y"]      # the wordmark estimate runs 29 px wide: centre the lockup on the lines
    holder = empty("mark_holder", ov, (mx * PX, my * PX, 0))
    _, peaks, wave, _ = mark(holder, MM, tile=False)
    pm, wvm = emit("peaks", "#FFFFFF"), emit("wave", "#FFFFFF", alpha=0.0)
    set_mat(peaks, pm)
    set_mat(wave, wvm)
    sea = plane("sea", 0.62 * MM * PX, 0.5 * MM * PX, emit("sea", FIELD), holder)
    sea.location = (0, -0.25 * MM * PX, 0.0009)
    wm = emit("word", "#FFFFFF", alpha=0.0)
    glyphs, wg, _ = word(ov, M, (mx + MM / 2 + gap) * PX, my * PX, mat=wm)
    fonts = {"bold": BOLD, "semi": SEMI, "reg": REG}
    lines = []
    for i, ln in enumerate(E["lines"]):
        lm = emit(f"line{i}", ln["color"], alpha=0.0)
        lo = text(f"line{i}", ln["text"], fonts[ln["font"]], ln["size"] * PX, lm, ov, align="CENTER")
        lines.append((lo, lm, ln))
    p0 = peaks.location.copy()
    w0 = wave.location.copy()
    g0 = wg.location.copy()
    k = peaks.parent.scale.x
    for f in range(n):
        a = out_cubic(prog(f, 4, 18))
        key_transform(peaks, f, loc=(p0.x, p0.y - (1 - a) * 0.34 * MM * PX / k, p0.z))
        b = out_cubic(prog(f, 9, 20))
        key_transform(wave, f, loc=(w0.x, w0.y - (1 - b) * 0.05 * MM * PX / k, w0.z))
        key_alpha(wvm, f, b)
        c = out_cubic(prog(f, 14, 25))
        key_transform(wg, f, loc=(g0.x, g0.y - (1 - c) * 0.03, g0.z))
        key_alpha(wm, f, c)
        for lo, lm, ln in lines:
            d = out_cubic(prog(f, ln["f"][0], ln["f"][1]))
            key_transform(lo, f, loc=(0, ln["y"] * PX - (1 - d) * 0.012, 0))
            key_alpha(lm, f, d)
    return sc, n


sc, n = end()
for ob in bpy.data.objects:
    linear_keys(ob)
    ad = ob.animation_data
    if ad and ad.action:
        try:
            from bpy_extras import anim_utils
            cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
            for fc in (cb.fcurves if cb else []):
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"
        except Exception:
            pass
for m in bpy.data.materials:
    if m.node_tree and m.node_tree.animation_data and m.node_tree.animation_data.action:
        try:
            from bpy_extras import anim_utils
            ad = m.node_tree.animation_data
            cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
            for fc in (cb.fcurves if cb else []):
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"
        except Exception:
            pass
out = os.path.join(os.path.dirname(HERE), "render", "endcard_v2", "")
os.makedirs(out, exist_ok=True)
sc.render.filepath = out
if "--" in sys.argv and "still" in sys.argv:
    for f in (10, 40, 83):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f"still_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print("DONE endcard", n)
