"""Film 2, Order: the CRM's itinerary maker, as knolling.

  Blender -b --factory-startup -P build/order.py -- [still f f ...]

Top down on a pale desk under slatted window light. The week's paper lands in
a heap (rate sheet, a dense old PDF with a coffee ring, voucher, boarding pass,
passport, polaroid, sticky notes, a buzzing phone, a pen, a coffee), squares
itself up at right angles, then is swept away leaving one note: the trip in one
line. The real itinerary pages (screens/pages, the public demo's Krabi Islands,
small group, drawn as the PDF prints) deal out from under it, and a tablet
slides in with the CRM's Itineraries screen (screens/crm-itinerary_pdf.png):
the same line, typed into Ask, and the ring lands on it.
Frames: render/order/3d/####.png, 0..515.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
from film import *  # noqa: E402,F401,F403

N = sec(21.5)
OUT = os.path.join(AD, "render", "order", "3d")
PROPS = os.path.join(SCR, "props")
PAGES = os.path.join(SCR, "pages")
F_CLEAR, F_DEAL, F_NOTE, F_TAB, F_RING = 236, 276, 352, 384, 446

# name: (w, h, thickness, texture, chaos (x, y, rot), knolled (x, y, rot), drop frame)
ITEMS = {
    "old_pdf": (0.297, 0.21, 0.0004, "old_pdf.png", (0.02, 0.08, -18), (-0.1215, 0.135, 0), 4),
    "rate": (0.21, 0.297, 0.0004, "rate_sheet.png", (-0.12, -0.10, 24), (-0.165, -0.1385, 0), 12),
    "voucher": (0.099, 0.21, 0.0004, "voucher.png", (0.14, 0.18, 35), (0.0965, 0.135, 0), 20),
    "polaroid": (0.088, 0.107, 0.0009, "polaroid.png", (-0.16, 0.20, -28), (0.199, -0.0435, 0), 27),
    "passport": (0.088, 0.125, 0.005, "passport.png", (0.10, -0.12, 62), (0.091, -0.0525, 0), 34),
    "sticky_pickup": (0.076, 0.076, 0.0003, "sticky_pickup.png", (-0.05, 0.02, 12), (0.085, -0.173, 0), 40),
    "boarding": (0.08, 0.19, 0.0004, "boarding.png", (0.16, -0.25, -40), (0.206, 0.145, 0), 46),
    "phone": (0.0716, 0.155, 0.0078, None, (-0.14, -0.30, 18), (-0.234, -0.3845, 0), 52),
    "sticky_diet": (0.076, 0.076, 0.0003, "sticky_diet.png", (0.05, 0.25, -22), (0.181, -0.173, 0), 58),
    "pen": (0.011, 0.14, 0.011, None, (0.02, -0.20, 70), (-0.035, -0.06, 0), 63),
    "cup": (0.14, 0.14, 0.09, None, (0.17, 0.02, 0), (-0.10, -0.377, 0), 70),
    "sticky_line": (0.076, 0.076, 0.0003, "sticky_line.png", (-0.06, -0.17, -14), (0.085, -0.269, 0), 78),
}
PAGE_FILES = ["pg00.png", "pg01.png", "pg02.png", "pg03.png", "pg09.png", "pg11.png"]
PW_, PH_ = 0.26, 0.185
PAGE_XY = [(-0.137, 0.17), (0.137, 0.17), (-0.137, -0.035), (0.137, -0.035), (-0.137, -0.24), (0.137, -0.24)]
NOTE_C = Vector((0.0, -0.07))
NOTE_END = (-0.215, 0.232, -7)
TAB_W, TAB_H, SCR_W, SCR_H = 0.252, 0.168, 0.236, 0.1475
TAB_XY = (0.0, -0.06)


def paper(name, tex):
    return principled(name, "#FFFFFF", rough=0.78, spec=0.25, image=os.path.join(PROPS, tex))


def build_items():
    obs = {}
    white = principled("paper_edge", "#F4F5F3", rough=0.8)
    for name, (w, h, t, tex, *_rest) in ITEMS.items():
        root = empty(name)
        if name == "phone":
            back = principled("phone_back", "#1A222C", rough=0.32, coat=0.6)
            fr = principled("phone_rim", "#3E4A5A", metallic=1.0, rough=0.3)
            body = slab("phone_body", w, h, 0.011, t, back, fr, back, bevel=0.0012, parent=root)
            body.location.z = t / 2
            bump = slab("phone_cam", 0.03, 0.03, 0.007, 0.0016, principled("cam", "#222C38", rough=0.2, coat=1.0), fr, fr, bevel=0.0006, parent=root)
            bump.location = (-w / 2 + 0.006 + 0.015, h / 2 - 0.006 - 0.015, t + 0.0008)
            for k, (lx, ly) in enumerate(((-0.006, 0.006), (0.006, -0.006))):
                lens = cylinder(f"lens{k}", 0.0042, 0.0012, (bump.location.x + lx, bump.location.y + ly, t + 0.0018), principled("glass", "#05080B", rough=0.05, coat=1.0), verts=32, parent=root)
        elif name == "pen":
            ink = principled("pen", "#141C26", rough=0.22, coat=0.8)
            p = cylinder("pen_body", 0.0055, 0.14, (0, 0, 0.0055), ink, verts=32, parent=root)
            p.rotation_euler = (rad(90), 0, 0)
            tip = principled("pen_tip", "#A9B4C0", metallic=1.0, rough=0.25)
            cl = box("pen_clip", (0.0022, 0.045, 0.0016), (0.0, 0.035, 0.0115), tip, parent=root)
            bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.0055, depth=0.012, location=(0, -0.076, 0.0055))
            cone = bpy.context.active_object
            cone.rotation_euler = (rad(90), 0, 0)
            cone.data.materials.append(tip)
            cone.parent = root
        elif name == "cup":
            cer = principled("ceramic", "#F4F6F8", rough=0.16, coat=0.6)
            sau = cylinder("saucer", 0.07, 0.008, (0, 0, 0.004), cer, verts=96, parent=root)
            m = sau.modifiers.new("bev", "BEVEL")
            m.width, m.segments = 0.003, 3
            cup = cylinder("cup_body", 0.042, 0.075, (0, 0, 0.008 + 0.0375), cer, verts=96, parent=root)
            m = cup.modifiers.new("bev", "BEVEL")
            m.width, m.segments = 0.002, 3
            cylinder("coffee", 0.0385, 0.0008, (0, 0, 0.0835), principled("coffee", "#241C17", rough=0.04, coat=1.0), verts=96, parent=root)
            bpy.ops.mesh.primitive_torus_add(major_radius=0.016, minor_radius=0.0045, location=(0.052, 0, 0.05))
            hd = bpy.context.active_object
            hd.rotation_euler = (rad(90), 0, 0)
            hd.data.materials.append(cer)
            hd.parent = root
            bpy.ops.object.shade_smooth()
        else:
            face = paper(name, tex)
            if name == "passport":
                side = principled("pp_side", "#18253C", rough=0.6)
                ob = slab(name + "_m", w, h, 0.004, t, face, side, side, bevel=0.0008, parent=root)
            elif name == "polaroid":
                ob = slab(name + "_m", w, h, 0.0005, t, face, white, white, parent=root)
            else:
                ob = slab(name + "_m", w, h, 0.0002, t, face, white, white, parent=root, seg=2)
            ob.location.z = t / 2
        obs[name] = root
    return obs


def item_pose(name, f, order):
    w, h, t, tex, chaos, knoll, f_drop = ITEMS[name]
    cx, cy, cr = chaos
    kx, ky, kr = knoll
    z_chaos = 0.0012 * order
    # 1. tossed on from outside the frame, landing and sliding to rest
    d = Vector((cx, cy)).normalized() if Vector((cx, cy)).length > 1e-3 else Vector((0, 1))
    start = Vector((cx, cy)) + d * 0.75
    t1 = prog(f, f_drop, f_drop + 13)
    pos = start.lerp(Vector((cx, cy)), out_cubic(t1))
    z = lerp(0.16, z_chaos, smooth(prog(f, f_drop, f_drop + 6)))
    rot = cr + (1 - out_cubic(t1)) * (35 if order % 2 else -35)
    tilt = (1 - smooth(prog(f, f_drop, f_drop + 6))) * rad(14)
    # the phone buzzes face down, twice
    if name == "phone":
        for b0 in (88, 104):
            if b0 <= f < b0 + 8:
                rot += math.sin((f - b0) * 2.6) * 1.6
                pos += Vector((math.sin((f - b0) * 3.1) * 0.0012, 0))
    # 2. squared up, lifted a little on the way so nothing passes through anything
    fk = 118 + 9 * (len(ITEMS) - 1 - order)
    t2 = smoother(prog(f, fk, fk + 15))
    if t2 > 0:
        pos = pos.lerp(Vector((kx, ky)), t2)
        rot = lerp(rot, kr, t2)
        z = lerp(z_chaos, 0.0, t2) + math.sin(math.pi * t2) * (0.03 + 0.003 * order)
        tilt = 0.0
    # 3. swept out of frame, all but the one-line note
    if name == "sticky_line":
        t4 = smoother(prog(f, F_CLEAR + 4, F_CLEAR + 34))
        if t4 > 0:
            pos = Vector((kx, ky)).lerp(NOTE_C, t4)
            rot = lerp(kr, -3, t4)
            z = 0.012 * math.sin(math.pi * t4) + 0.004 * t4
        t5 = smoother(prog(f, F_NOTE, F_NOTE + 20))
        if t5 > 0:
            pos = NOTE_C.lerp(Vector(NOTE_END[:2]), t5)
            rot = lerp(-3, NOTE_END[2], t5)
            z = 0.004 + 0.01 * math.sin(math.pi * t5) + 0.0006
    else:
        fc = F_CLEAR + 2 * order
        t3 = in_cubic(prog(f, fc, fc + 14))
        if t3 > 0:
            k = Vector((kx, ky))
            out = Vector((math.copysign(1, kx), 0)) if abs(kx) / 0.30 > abs(ky) / 0.53 else Vector((0, math.copysign(1, ky)))
            pos = k + out * 0.9 * t3
            rot = kr + t3 * (10 if order % 2 else -10)
    return pos, z, rot, tilt


def build():
    sc, cam = new_scene(N, engine="EEVEE", samples=64, world="#EEF2F6", world_strength=0.5, shutter=0.45)
    desk = principled("desk", "#E3E8EC", rough=0.6, bump=(160, 0.025, 6))
    noisy_color(desk, "#DDE2E7", "#E9EDF0", scale=6.0)
    box("desk", (3.0, 3.0, 0.04), (0, 0, -0.02), desk)

    # Window light through slatted blinds, off to the right and turned so the stripes run diagonally.
    win = empty("window", None, (0.95, 0.0, 0.0))
    win.rotation_euler = (0, 0, rad(28))
    wall = principled("wall", "#D8DEE4", rough=0.9)
    for nm, sz, lc in (("w_bot", (0.06, 3.0, 0.25), (0, 0, 0.125)), ("w_top", (0.06, 3.0, 1.4), (0, 0, 1.15 + 0.7)),
                       ("w_l", (0.06, 0.6, 0.9), (0, -1.2, 0.7)), ("w_r", (0.06, 0.6, 0.9), (0, 1.2, 0.7))):
        box(nm, sz, lc, wall, parent=win)
    slat = principled("slat", "#E9EDF1", rough=0.5)
    for k in range(13):
        s = box(f"slat{k}", (0.07, 1.8, 0.003), (0, 0, 0.29 + k * 0.068), slat, parent=win)
        s.rotation_euler = (0, rad(-32), 0)
    sn = sun("sun", (0, 0, 0), 3.0, angle=1.4, color="#F6F9FF")
    d = Vector((-0.78, 0.18, -0.6)).normalized()
    sn.rotation_euler = (-d).to_track_quat("Z", "Y").to_euler()

    obs = build_items()
    names = list(ITEMS)

    # The real pages, drawn as the PDF prints them.
    pages = []
    edge = principled("page_edge", "#F2F0EA", rough=0.8)
    for k, fn in enumerate(PAGE_FILES):
        m = principled(f"page{k}", "#FFFFFF", rough=0.7, spec=0.25, image=os.path.join(PAGES, fn))
        root = empty(f"page{k}")
        pg = slab(f"page{k}_m", PW_, PH_, 0.0003, 0.0004, m, edge, edge, parent=root, seg=2)
        pg.location.z = 0.0002
        pages.append(root)
    rnd = random.Random(3)
    page_rest = [rnd.uniform(-0.7, 0.7) for _ in pages]

    # The tablet with the CRM.
    tab = empty("tablet")
    glass = principled("tab_glass", "#05080B", rough=0.06, coat=1.0)
    alu = principled("tab_alu", "#8B97A5", metallic=1.0, rough=0.32)
    slab("tab_body", TAB_W, TAB_H, 0.012, 0.0065, glass, alu, alu, bevel=0.0012, parent=tab).location.z = 0.00325
    scr = slab("tab_screen", SCR_W, SCR_H, 0.004, 0.00002, emit("crm", image=os.path.join(SCR, "crm-itinerary_pdf.png")), glass, glass, parent=tab)
    scr.location.z = 0.0066
    # Ring on the line typed into Ask (x 1230-1548, y 282-348 of the 1600 x 1000 capture).
    rm = emit("ring", AZURE, strength=1.0, alpha=0.0)
    bx, by = ((1230 + 1548) / 2 / 1600 - 0.5) * SCR_W, (0.5 - (282 + 348) / 2 / 1000) * SCR_H
    rh = empty("ring_h", tab, (bx, by, 0.0068))
    ring("ring", 318 / 1600 * SCR_W + 0.002, 66 / 1000 * SCR_H + 0.002, 0.0022, 0.0009, rm, rh)
    ring_in(rh, rm, F_RING, 10)

    for f in range(N):
        for order, nm in enumerate(names):
            pos, z, rot, tilt = item_pose(nm, f, order)
            key(obs[nm], f, loc=(pos.x, pos.y, z), rot=(tilt, tilt * 0.6, rad(rot)))
        for k, pg in enumerate(pages):
            fd = F_DEAL + 11 * k
            t = out_cubic(prog(f, fd, fd + 16))
            if f < fd:
                key(pg, f, loc=(NOTE_C.x, NOTE_C.y, -0.01), rot=(0, 0, 0))
                continue
            gx, gy = PAGE_XY[k]
            p = NOTE_C.lerp(Vector((gx, gy)), t)
            r = lerp(6 if k % 2 else -6, page_rest[k], t)
            key(pg, f, loc=(p.x, p.y, 0.0012 + 0.0004 * (len(pages) - k) - 0.0008 * t), rot=(0, 0, rad(r)))
        tt = out_cubic(prog(f, F_TAB, F_TAB + 26))
        key(tab, f, loc=(TAB_XY[0], lerp(-0.95, TAB_XY[1], tt), 0.0016), rot=(0, 0, rad(lerp(-5, 0.0, tt))))

        # Camera: top down, breathing in, then down onto the tablet's Ask panel.
        a = smooth(prog(f, 0, F_TAB))
        h0 = lerp(3.1, 2.9, a)
        c0 = Vector((0.0, lerp(0.0, -0.01, a)))
        rot0 = lerp(0.0, 1.2, a)
        b = smoother(prog(f, F_TAB + 6, 470))
        tgt = Vector((TAB_XY[0] + 0.055, TAB_XY[1] + 0.016))
        h = lerp(h0, 1.02, b) - 0.05 * smooth(prog(f, 470, N - 1))
        c = c0.lerp(tgt, b)
        cam.location = (c.x, c.y, h)
        cam.rotation_euler = (0, 0, rad(lerp(rot0, 0.0, b)))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.lens = 70
        cam.data.dof.aperture_fstop = lerp(5.6, 4.0, b)
        cam.data.dof.focus_distance = h - 0.004
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
    all_linear()
    return sc


if __name__ == "__main__":
    a = args()
    sc = build()
    if a and a[0] == "still":
        render(sc, OUT.replace("3d", "stills"), stills=[int(x) for x in a[1:]])
    else:
        render(sc, OUT)
