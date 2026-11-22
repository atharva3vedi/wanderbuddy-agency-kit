"""Film 3, 23:48: the WhatsApp and Instagram assistant, after Hopper.

  Blender -b --factory-startup -P build/night.py -- [still f f ...]

A closed agency office on a wet street at night, Lantern Trips painted on the
glass. At 23:48 the laptop on the empty desk wakes and lights the room: the
camera goes in through the window to the CRM inbox (the real capture,
screens/crm-inbox_assistant_pickup.png), where "What time is pickup tomorrow?"
gets the assistant's answer from the trip plan, and the ring lands on it.
Then back out to the street while the clock runs to dawn, the laptop waking
twice more on its own.
Frames: render/night/3d/####.png, 0..515.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
from film import *  # noqa: E402,F401,F403

N = sec(21.5)
OUT = os.path.join(AD, "render", "night", "3d")
F_WAKE, F_REPLY, F_RING, F_SLEEP = 26, 286, 300, 392
WAKES = [(F_WAKE, F_SLEEP), (418, 432), (452, 466)]
LAP = Vector((0.0, 2.1, 0.76))          # laptop base centre on the desk
SW, SH = 0.286, 0.179                   # its screen (1600 x 1000)
OPEN = 108                              # lid angle from the base


def screen_on(f):
    v = 0.0
    for a, b in WAKES:
        v = max(v, smooth(prog(f, a, a + 5)) * (1 - smooth(prog(f, b, b + 7))))
    return v


def clock_minutes(f):
    """Minutes past 23:00 (23:48 at the start, 06:05 at the end)."""
    base = 48 + f / FPS / 60
    return base + (377 - base + 48) * smoother(prog(f, 396, 506))


def dawn(f):
    return smooth(prog(f, 410, 512))


def build():
    sc, cam = new_scene(N, engine="EEVEE", samples=64, world="#070C14", world_strength=0.06, shutter=0.5)
    bg = sc.world.node_tree.nodes["Background"]
    sc.eevee.volumetric_end = 30

    # --- street ---------------------------------------------------------------
    wet = principled("asphalt", "#0B0F14", rough=0.25, spec=0.6, bump=(30, 0.06, 4))
    nt = wet.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.6
    nz.inputs["Detail"].default_value = 3
    cr = nt.nodes.new("ShaderNodeMapRange")
    cr.inputs[1].default_value, cr.inputs[2].default_value = 0.45, 0.6
    cr.inputs[3].default_value, cr.inputs[4].default_value = 0.42, 0.04
    nt.links.new(nz.outputs["Fac"], cr.inputs[0])
    nt.links.new(cr.outputs[0], p.inputs["Roughness"])
    box("street", (30, 14, 0.2), (0, -8.5, -0.1), wet)
    kerb_m = principled("kerb", "#3A434E", rough=0.5)
    pave = principled("pavement", "#1D252F", rough=0.3, spec=0.5, bump=(12, 0.04))
    box("pavement", (30, 1.8, 0.14), (0, -0.9, 0.07), pave)
    box("kerb", (30, 0.16, 0.15), (0, -1.86, 0.075), kerb_m)

    # --- the building front, with one shop window and a door --------------------
    plaster = principled("facade", "#1A2632", rough=0.85, bump=(20, 0.05))
    noisy_color(plaster, "#16212C", "#223140", scale=2.0)
    WX0, WX1, WZ0, WZ1 = -1.45, 1.25, 0.55, 2.55
    box("f_left", (6.0, 0.3, 7.0), (WX0 - 3.0, 0.15, 3.5), plaster)
    box("f_right", (6.0, 0.3, 7.0), (WX1 + 3.0 + 1.2, 0.15, 3.5), plaster)
    box("f_bot", (WX1 - WX0, 0.3, WZ0), (0.5 * (WX0 + WX1), 0.15, WZ0 / 2), plaster)
    box("f_top", (WX1 - WX0 + 1.2, 0.3, 7.0 - WZ1), (0.5 * (WX0 + WX1) + 0.6, 0.15, (7.0 + WZ1) / 2), plaster)
    # door to the right of the window
    door_m = principled("door", "#121A23", rough=0.45, metallic=0.3)
    box("door", (1.0, 0.06, WZ1), (WX1 + 0.6, 0.27, WZ1 / 2), door_m)
    frame = principled("frame", "#0E151D", rough=0.35, metallic=0.6)
    for nm, sz, lc in (("fr_t", (WX1 - WX0 + 0.08, 0.12, 0.06), (0.5 * (WX0 + WX1), 0.04, WZ1)),
                       ("fr_b", (WX1 - WX0 + 0.08, 0.16, 0.06), (0.5 * (WX0 + WX1), 0.02, WZ0)),
                       ("fr_l", (0.06, 0.12, WZ1 - WZ0), (WX0, 0.04, 0.5 * (WZ0 + WZ1))),
                       ("fr_r", (0.06, 0.12, WZ1 - WZ0), (WX1, 0.04, 0.5 * (WZ0 + WZ1))),
                       ("fr_m", (0.04, 0.1, WZ1 - WZ0), (0.5 * (WX0 + WX1) + 0.5, 0.04, 0.5 * (WZ0 + WZ1)))):
        box(nm, sz, lc, frame)
    glass = principled("glass", "#6F8396", rough=0.04, spec=0.35)
    next(n for n in glass.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Alpha"].default_value = 0.03
    glass.surface_render_method = "BLENDED"
    gl = box("glass", (WX1 - WX0, 0.01, WZ1 - WZ0), (0.5 * (WX0 + WX1), 0.06, 0.5 * (WZ0 + WZ1)), glass)
    gl.visible_shadow = False
    # The name painted on the glass, read from the street.
    paint = principled("paint", "#EEF2F6", rough=0.5)
    t = text("sign", "Lantern Trips", SEMI, 0.2, paint)
    t.rotation_euler = (rad(90), 0, 0)
    t.location = (0.5 * (WX0 + WX1) - 0.18, 0.05, 2.18)
    t.data.align_x = "CENTER"
    t2 = text("sign2", "Small group trips   Krabi   Chiang Mai   Bali", REG, 0.062, paint)
    t2.rotation_euler = (rad(90), 0, 0)
    t2.location = (0.5 * (WX0 + WX1) - 0.18, 0.05, 1.98)
    t2.data.align_x = "CENTER"

    # --- the room ----------------------------------------------------------------
    wallm = principled("room_wall", "#7FA0A6", rough=0.9, bump=(25, 0.03))
    floor_m = principled("room_floor", "#2B3640", rough=0.45, spec=0.4)
    box("r_floor", (6, 5, 0.1), (0, 2.6, -0.05), floor_m)
    box("r_ceil", (6, 5, 0.1), (0, 2.6, 3.05), wallm)
    box("r_back", (6, 0.1, 3.1), (0, 4.6, 1.5), wallm)
    box("r_left", (0.1, 5, 3.1), (-2.6, 2.6, 1.5), wallm)
    box("r_right", (0.1, 5, 3.1), (2.6, 2.6, 1.5), wallm)
    wood = principled("desk", "#1C2731", rough=0.6)
    box("desk_top", (1.5, 0.75, 0.04), (0, LAP.y + 0.12, 0.74), wood)
    for sx in (-0.7, 0.7):
        box(f"desk_side{sx}", (0.04, 0.7, 0.72), (sx, LAP.y + 0.12, 0.36), wood)
    box("desk_modesty", (1.4, 0.03, 0.4), (0, LAP.y + 0.45, 0.5), wood)
    seat = principled("chair", "#1F5E63", rough=0.7)
    metal = principled("chair_metal", "#29323C", metallic=0.8, rough=0.35)
    ch = empty("chair", None, (0.1, LAP.y + 0.72, 0))
    ch.rotation_euler = (0, 0, rad(14))
    box("seat", (0.46, 0.44, 0.07), (0, 0, 0.47), seat, parent=ch, bevel=0.02)
    bk = box("back", (0.44, 0.06, 0.5), (0, 0.24, 0.8), seat, parent=ch, bevel=0.02)
    bk.rotation_euler = (rad(-8), 0, 0)
    cylinder("stem", 0.025, 0.4, (0, 0, 0.23), metal, parent=ch)
    for k in range(5):
        a = rad(72 * k)
        leg = box(f"leg{k}", (0.03, 0.3, 0.025), (0.13 * math.sin(a), 0.13 * math.cos(a), 0.04), metal, parent=ch)
        leg.rotation_euler = (0, 0, -a)
    # shelves of binders along the back wall
    shelf = principled("shelf", "#26313C", rough=0.5)
    cols = ["#1E88D6", "#0C1622", "#E8EEF3", "#1BA89A", "#2072B8", "#D7E2EC", "#0C1622"]
    import random
    rnd = random.Random(5)
    for row, z in enumerate((1.05, 1.55)):
        box(f"shelf{row}", (2.0, 0.32, 0.03), (1.35, 4.42, z), shelf)
        x = 0.42
        while x < 2.25:
            w = rnd.uniform(0.05, 0.08)
            hgt = rnd.uniform(0.3, 0.34)
            box(f"binder{row}_{x:.2f}", (w - 0.004, 0.26, hgt), (x + w / 2, 4.42, z + 0.015 + hgt / 2),
                principled("binder", rnd.choice(cols), rough=0.55))
            x += w
    # a framed map of the coast: a quiet azure rectangle with a white edge
    box("print_frame", (0.9, 0.03, 0.62), (-1.15, 4.53, 1.75), principled("pf", "#E8EEF3", rough=0.6))
    box("print", (0.8, 0.03, 0.52), (-1.15, 4.52, 1.75), principled("pp", "#2A5E86", rough=0.8))
    # the wall clock, facing the street
    clk = empty("clock", None, (-2.0, 0.32, 1.95))
    clk.rotation_euler = (0, 0, rad(180))
    face = cylinder("clock_face", 0.2, 0.03, (0, 0, 0), principled("clockface", "#F1F4F7", rough=0.4), verts=64, parent=clk)
    face.rotation_euler = (rad(90), 0, 0)
    rim = principled("rim", "#0E151D", metallic=0.6, rough=0.3)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.205, minor_radius=0.012, location=(0, 0, 0))
    tr_ = bpy.context.active_object
    tr_.rotation_euler = (rad(90), 0, 0)
    tr_.data.materials.append(rim)
    tr_.parent = clk
    for k in range(12):
        a = rad(30 * k)
        tk = box(f"tick{k}", (0.008, 0.005, 0.03 if k % 3 else 0.045), (0.17 * math.sin(a), -0.018, 0.17 * math.cos(a)), rim, parent=clk)
        tk.rotation_euler = (0, a, 0)
    hands = {}
    for nm, ln, wd in (("hour", 0.1, 0.012), ("minute", 0.155, 0.008)):
        piv = empty(nm, clk, (0, -0.022 - (0.002 if nm == "minute" else 0), 0))
        box(nm + "_m", (wd, 0.003, ln), (0, 0, ln / 2 - 0.015), rim, parent=piv)
        hands[nm] = piv

    # --- the laptop: its back to the window, its screen to the empty chair --------------
    alu = principled("lap_alu", "#7E8A98", metallic=1.0, rough=0.3)
    keys = principled("lap_keys", "#141B23", rough=0.6)
    lap = empty("laptop", None, LAP)
    base = slab("lap_base", 0.31, 0.215, 0.01, 0.012, alu, alu, alu, bevel=0.002, parent=lap)
    base.location.z = 0.006
    box("keys", (0.27, 0.105, 0.001), (0, -0.03, 0.0125), keys, parent=lap)
    hinge = empty("hinge", lap, (0, -0.1075, 0.012))
    hinge.rotation_euler = (rad(OPEN), 0, 0)
    lid = slab("lap_lid", 0.31, 0.215, 0.01, 0.006, alu, alu, principled("bezel", "#05080B", rough=0.05, coat=1.0), bevel=0.0015, parent=hinge)
    lid.location = (0, 0.1075, 0.003)
    scr_m = emit("screen", image=os.path.join(SCR, "inbox_before.png"))
    scr = plane("lap_screen", SW, SH, scr_m, hinge)
    scr.location = (0, 0.1075 + 0.006, -0.0004)
    scr.rotation_euler = (0, math.pi, 0)
    # the reply arriving: the real bubble, cut from the same capture
    rep_m = emit("reply", image=os.path.join(SCR, "inbox_reply.png"), alpha=0.0)
    rx, ry = ((822 + 230) / 1600 - 0.5) * SW, (0.5 - (352 + 69) / 1000) * SH
    rep = plane("reply", 460 / 1600 * SW, 138 / 1000 * SH, rep_m, scr)
    rep.location = (rx, ry, 0.0003)
    ring_m = emit("ring", AZURE, alpha=0.0)
    bx, by = ((826 + 1278) / 2 / 1600 - 0.5) * SW, (0.5 - (356 + 486) / 2 / 1000) * SH
    rh = empty("ring_h", scr, (bx, by, 0.0006))
    ring("ring", (1278 - 826) / 1600 * SW + 0.003, (486 - 356) / 1000 * SH + 0.003, 0.0045, 0.0011, ring_m, rh)
    ring_in(rh, ring_m, F_RING, 10)
    for f in range(F_SLEEP - 6, F_SLEEP + 3):
        fade_mat(ring_m, f, 1 - prog(f, F_SLEEP - 6, F_SLEEP + 2))
    # its light on the room
    glow = area("screen_light", (0, 0, 0), (0, 0, -1), 0, 0.34, color="#DCE8F5", shape="RECTANGLE", size_y=0.22)
    glow.parent = hinge
    glow.location = (0, 0.11, -0.09)
    glow.rotation_euler = (0, 0, 0)
    glow.data.spread = rad(75)

    # --- the street lamp ----------------------------------------------------------
    pole = principled("pole", "#1B232C", metallic=0.7, rough=0.4)
    cylinder("pole", 0.05, 4.6, (-0.95, -1.62, 2.3), pole)
    box("arm", (0.06, 0.7, 0.06), (-0.95, -1.3, 4.55), pole)
    head_m = emit("lamp_head", "#EEF4FF", strength=4.0)
    hd = box("lamp_head", (0.22, 0.36, 0.05), (-0.95, -1.0, 4.5), head_m)
    lamp = spot("lamp", (-0.95, -1.0, 4.44), (0.25, -1.7, 0.0), 1800, angle=78, blend=0.9, radius=0.12, color="#E6EEFA")
    lamp.data.use_custom_distance = False
    fog_box("street_fog", (14, 9, 6), (0, -5.0, 3.0), 0.0035, color="#C8D6E6", anisotropy=0.5)

    # dawn comes in through the window, cool, laying the window's shape on the floor and wall
    dsun = sun("dawn_sun", (0, 0, 0), 0.0, angle=0.8, color="#DDE8F7")
    dd = Vector((0.32, 1.0, -0.42)).normalized()
    dsun.rotation_euler = (-dd).to_track_quat("Z", "Y").to_euler()

    # neighbour windows up the street: cool and dim, for depth
    for k, (x, z) in enumerate(((6.4, 1.6), (8.8, 1.6), (6.4, 4.4), (-4.4, 4.4), (-7.0, 4.4))):
        win = plane(f"nwin{k}", 1.1, 1.3, emit(f"nw{k}", "#3E5872" if k % 2 else "#24384C", strength=0.6))
        win.rotation_euler = (rad(90), 0, 0)
        win.location = (x, -0.005, z)

    # --- animation ------------------------------------------------------------------
    for f in range(N):
        on = screen_on(f)
        key_val(scr_m.node_tree.nodes["em"].inputs["Strength"], f, 0.02 + 0.98 * on)
        glow.data.energy = (24.0 if f < 150 else 9.0) * on    # seen from the street it has to fill the room
        glow.data.keyframe_insert("energy", frame=f)
        r = smooth(prog(f, F_REPLY, F_REPLY + 10))
        if f >= F_SLEEP:
            r = 1.0
        fade_mat(rep_m, f, r * (0.02 + 0.98 * on) if f >= F_REPLY else 0.0)
        rep.location.z = 0.0003
        rep.location.y = ry - (1 - r) * 0.004
        rep.keyframe_insert("location", frame=f)
        m = clock_minutes(f)
        hands["minute"].rotation_euler = (0, rad(m / 60 * 360), 0)
        hands["hour"].rotation_euler = (0, rad((11 + m / 60) / 12 * 360), 0)
        hands["minute"].keyframe_insert("rotation_euler", frame=f)
        hands["hour"].keyframe_insert("rotation_euler", frame=f)
        dn = dawn(f)
        key_val(bg.inputs["Color"], f, tuple(lerp(a, b, dn) for a, b in zip(lin("#070C14"), lin("#8EA9C6"))))
        key_val(bg.inputs["Strength"], f, lerp(0.05, 0.32, dn))
        lamp.data.energy = 1800 * (1 - smooth(prog(f, 478, 496)))
        lamp.data.keyframe_insert("energy", frame=f)
        dsun.data.energy = 12.0 * smooth(prog(f, 462, 512))
        dsun.data.keyframe_insert("energy", frame=f)
        key_val(head_m.node_tree.nodes["em"].inputs["Strength"], f, 4.0 * (1 - smooth(prog(f, 478, 496))) + 0.05)

    # camera: the street, in through the glass, round to the screen, then the room at dawn
    # frame the question and the answer together (x 650-1278, y 282-486 of the capture)
    qa = empty("qa_c", scr, (((650 + 1278) / 2 / 1600 - 0.5) * SW, (0.5 - (282 + 486) / 2 / 1000) * SH, 0.0))
    bpy.context.view_layer.update()
    reply_c = qa.matrix_world.translation.copy()
    nrm = Vector((0, math.sin(rad(OPEN)), -math.cos(rad(OPEN))))
    scr_c = scr.matrix_world.translation.copy()
    shots = [
        (0, Vector((0.7, -6.0, 0.72)), Vector((0.0, 1.0, 1.5)), 30, 5.6, Vector((0, 0.1, 1.6))),
        (149, Vector((0.38, -2.5, 1.0)), Vector((0.0, 1.6, 1.22)), 30, 4.0, Vector((0, 0.1, 1.4))),
        (150, Vector((0.55, 3.2, 1.3)), scr_c + Vector((0.02, 0, 0.02)), 35, 3.2, scr_c),
        (276, reply_c + nrm * 0.44, reply_c, 50, 2.8, reply_c),
        (380, reply_c + nrm * 0.415 + Vector((-0.008, 0, 0.003)), reply_c + Vector((-0.003, 0, 0)), 50, 2.8, reply_c),
        (470, Vector((1.75, 4.2, 1.9)), Vector((-0.45, 1.3, 0.95)), 24, 5.0, LAP),
        (515, Vector((1.68, 4.24, 1.94)), Vector((-0.45, 1.25, 0.97)), 24, 5.0, LAP),
    ]
    ease = [smooth, smooth, smoother, smooth, smoother, smooth]
    for f in range(N):
        i = max(k for k in range(len(shots) - 1) if shots[k][0] <= f) if f < shots[-1][0] else len(shots) - 2
        a, b = shots[i], shots[i + 1]
        tt = ease[i](prog(f, a[0], b[0]))
        if i == 4:  # back over the chair to the corner of the room
            mid = Vector((1.1, 3.4, 1.35))
            pos = (1 - tt) ** 2 * a[1] + 2 * (1 - tt) * tt * mid + tt * tt * b[1]
        else:
            pos = a[1].lerp(b[1], tt)
        cam.location = pos
        look(cam, a[2].lerp(b[2], tt))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.lens = lerp(a[3], b[3], tt)
        cam.data.keyframe_insert("lens", frame=f)
        cam.data.dof.aperture_fstop = lerp(a[4], b[4], tt)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        cam.data.dof.focus_distance = max(0.05, (a[5].lerp(b[5], tt) - pos).length)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    all_linear()
    sc.render.motion_blur_position = "START"     # so the cut at 150 never smears
    for ob in bpy.data.objects:
        if ob.type == "LIGHT" and ob.name != "lamp":
            ob.data.volume_factor = 0.0
    return sc


if __name__ == "__main__":
    a = args()
    sc = build()
    if a and a[0] == "still":
        render(sc, OUT.replace("3d", "stills"), stills=[int(x) for x in a[1:]])
    else:
        render(sc, OUT)
