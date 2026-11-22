"""Second pass, film 2, Monsoon: the whole desk in one place.

  Blender -b --factory-startup -P build/monsoon.py -- [still f f ...]

Peak season on the same street as Three Agencies. In the shop next door the phone
fills up (set dressing, screens/monsoon/lock*.png) and everything the week is made
of takes off under the ceiling fan: passport copies, payment screenshots, rate
sheets, old PDFs, chat printouts, sticky notes (screens/monsoon/props). The fan
stops, it all comes down, and one passport copy slides off the desk.
In Lantern Trips the same season sits in the real CRM (build/monsoon_capture.mjs):
the pipeline board, then Home's "Needs you today". Outside at 23:30 one shop is
still lit behind its shutter; the azure ring lands on the other's sign.
Frames: render/monsoon/3d/####.png, 0..659.
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
from film import *  # noqa: E402,F401,F403

N = sec(27.5)                           # 660
OUT = os.path.join(AD, "render", "monsoon", "3d")
SCRM = os.path.join(SCR, "monsoon")
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MB, MC, MD, ME = 84, 252, 324, 516      # the phone | the storm | it all comes down | Lantern Trips | the street
F_RING1, F_SWAP, F_RING2 = 410, 444, 474  # ring on a pipeline card, Home comes up, ring on what to do next
F_WIN = ME + 70                         # the ring on the winner's sign
LAP = Vector((0.0, 2.1, 0.76))
SW, SH = 0.286, 0.179                   # laptop screen, 1600 x 1000 css px
OPEN = 108
X1, X2, X3, X4 = -8.4, -5.2, -2.0, 2.6  # shop 1 | shop 2 | Lantern Trips |


def px(x, y):
    """A css point of the inbox capture, in the screen plane's local metres."""
    return ((x / 1600 - 0.5) * SW, (0.5 - y / 1000) * SH)


def pulse(f, a, b, rise=4, fall=7):
    return smooth(prog(f, a, a + rise)) * (1 - smooth(prog(f, b, b + fall)))


def wire(name, a, b, sag, m, r=0.007):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    cu.bevel_resolution = 1
    sp = cu.splines.new("POLY")
    n = 16
    sp.points.add(n - 1)
    for i in range(n):
        t = i / (n - 1)
        p = Vector(a).lerp(Vector(b), t)
        p.z -= sag * 4 * t * (1 - t)
        sp.points[i].co = (p.x, p.y, p.z, 1)
    ob = link(bpy.data.objects.new(name, cu))
    ob.data.materials.append(m)
    return ob


def sign_text(name, body, fnt, size, m, x, z, y=-0.11, align="CENTER"):
    t = text(name, body, fnt, size, m, align=align)
    t.rotation_euler = (rad(90), 0, 0)
    t.location = (x, y, z)
    return t


def bars(name, x0, x1, z0, z1, y, m, step=0.11, w=0.018):
    """Vertical railing bars as one mesh."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    x = x0
    while x <= x1 + 1e-6:
        bmesh.ops.create_cube(bm, size=1.0, matrix=__import__("mathutils").Matrix.Translation((x, y, 0.5 * (z0 + z1))) @
                              __import__("mathutils").Matrix.Diagonal((w, w, z1 - z0, 1)))
        x += step
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    return link(bpy.data.objects.new(name, me))


def slats(name, x0, x1, z0, z1, y, m, pitch=0.05, gap=0.012):
    """A roll shutter: horizontal slats with a sliver of gap between them. Origin at its foot."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    M = __import__("mathutils").Matrix
    z = 0.0
    while z < (z1 - z0) - 1e-6:
        h = pitch - gap
        bmesh.ops.create_cube(bm, size=1.0, matrix=M.Translation((0, 0, z + h / 2)) @ M.Diagonal((x1 - x0, 0.008, h, 1)))
        z += pitch
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    ob = link(bpy.data.objects.new(name, me))
    ob.location = (0.5 * (x0 + x1), y, z0)
    return ob


def upper_floor(tag, x0, x1, z, wall_m, rnd, lit=None):
    """One floor above the shop: a balcony, a door-window with louvred shutters."""
    xc, w = 0.5 * (x0 + x1), x1 - x0
    iron = principled(tag + "_iron", "#10161C", metallic=0.7, rough=0.45)
    pane = emit(tag + "_pane", lit or "#1C2A38", strength=0.9 if lit else 0.35)
    ww, wh = min(1.5, w - 1.5), 2.0
    p = plane(tag + "_win", ww, wh, pane)
    p.rotation_euler = (rad(90), 0, 0)
    p.location = (xc, -0.012, z + wh / 2 - 0.9)
    louv = principled(tag + "_louvre", rnd.choice(["#2F5A4E", "#31586A", "#4A5B45"]), rough=0.7)
    for s in (-1, 1):
        lv = box(tag + f"_lv{s}", (0.46, 0.04, wh), (xc + s * (ww / 2 + 0.25), -0.03, z + wh / 2 - 0.9), louv)
        lv.rotation_euler = (0, 0, rad(s * rnd.uniform(4, 22)))
    box(tag + "_lintel", (ww + 1.2, 0.1, 0.12), (xc, -0.05, z + wh - 0.86), wall_m)
    box(tag + "_slab", (w - 0.3, 0.8, 0.1), (xc, -0.4, z - 0.95), wall_m)
    box(tag + "_rail", (w - 0.34, 0.04, 0.04), (xc, -0.77, z - 0.02), iron)
    bars(tag + "_bars", x0 + 0.2, x1 - 0.2, z - 0.9, z - 0.02, -0.77, iron)
    if rnd.random() < 0.7:                      # an air-conditioner on the wall
        ac = principled(tag + "_ac", "#B9C2C9", rough=0.5)
        box(tag + "_acu", (0.78, 0.3, 0.52), (x0 + 0.62, -0.17, z + 1.45), ac)
    for k in range(rnd.randint(1, 3)):          # plants along the balcony
        px_ = rnd.uniform(x0 + 0.5, x1 - 0.5)
        cylinder(tag + f"_pot{k}", 0.11, 0.2, (px_, -0.55, z - 0.8), principled(tag + f"_potm{k}", "#6B4B3C", rough=0.8), verts=16)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rnd.uniform(0.18, 0.3), location=(px_, -0.55, z - 0.5))
        lf = bpy.context.active_object
        lf.scale.z = 1.3
        lf.data.materials.append(principled(tag + f"_leaf{k}", "#1F3B2C", rough=0.7))


def house(tag, x0, x1, h, col, col2, rnd, floors=(4.7, 7.6), lit=None):
    wall = principled(tag + "_wall", col, rough=0.9, bump=(18, 0.06))
    noisy_color(wall, col2, col, scale=1.4, detail=8)
    for k, z in enumerate(floors):
        upper_floor(f"{tag}_f{k}", x0, x1, z, wall, rnd, lit=lit if k == 1 else None)
    box(tag + "_cornice", (x1 - x0 + 0.06, 0.45, 0.16), (0.5 * (x0 + x1), 0.0, h), wall)
    return wall


def scooter(tag, loc, rz, colr):
    sco = empty(tag, None, loc)
    sco.rotation_euler = (0, rad(-7), rad(rz))
    dark = principled(tag + "_dark", "#0E1318", rough=0.4)
    body = principled(tag + "_body", colr, rough=0.3, coat=0.6)
    for xw in (-0.62, 0.62):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.2, minor_radius=0.06, location=(0, 0, 0))
        wh = bpy.context.active_object
        wh.rotation_euler = (rad(90), 0, 0)
        wh.location = (xw, 0, 0.26)
        wh.data.materials.append(dark)
        wh.parent = sco
    box(tag + "_floor", (0.6, 0.3, 0.07), (0.0, 0, 0.3), body, parent=sco, bevel=0.02)
    rear = box(tag + "_rear", (0.72, 0.32, 0.34), (-0.42, 0, 0.56), body, parent=sco, bevel=0.07)
    rear.rotation_euler = (0, rad(-8), 0)
    box(tag + "_seat", (0.7, 0.3, 0.09), (-0.36, 0, 0.78), dark, parent=sco, bevel=0.035)
    shield = box(tag + "_shield", (0.1, 0.36, 0.62), (0.44, 0, 0.62), body, parent=sco, bevel=0.04)
    shield.rotation_euler = (0, rad(-18), 0)
    col = cylinder(tag + "_col", 0.03, 0.5, (0.53, 0, 0.95), dark, verts=12, parent=sco)
    col.rotation_euler = (0, rad(-18), 0)
    hb = cylinder(tag + "_bar", 0.018, 0.62, (0.6, 0, 1.17), dark, verts=12, parent=sco)
    hb.rotation_euler = (rad(90), 0, 0)
    box(tag + "_head", (0.1, 0.2, 0.14), (0.63, 0, 1.06), principled(tag + "_lamp", "#C9D3DA", rough=0.1), parent=sco, bevel=0.03)
    return sco


def build():
    rnd = random.Random(11)
    sc, cam = new_scene(N, engine="EEVEE", samples=64, world="#0A1220", world_strength=0.11, shutter=0.5)
    bg = sc.world.node_tree.nodes["Background"]
    sc.eevee.volumetric_end = 45
    try:
        sc.eevee.shadow_pool_size = "1024"
    except Exception:
        pass

    # --- the street ------------------------------------------------------------
    wet = principled("asphalt", "#0B0F14", rough=0.25, spec=0.6, bump=(30, 0.06, 4))
    nt = wet.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.3
    nz.inputs["Detail"].default_value = 3
    cr = nt.nodes.new("ShaderNodeMapRange")
    cr.inputs[1].default_value, cr.inputs[2].default_value = 0.42, 0.6
    cr.inputs[3].default_value, cr.inputs[4].default_value = 0.45, 0.035
    nt.links.new(nz.outputs["Fac"], cr.inputs[0])
    nt.links.new(cr.outputs[0], p.inputs["Roughness"])
    box("street", (70, 19.6, 0.2), (-3, -11.6, -0.1), wet)
    pave = principled("pavement", "#232B34", rough=0.32, spec=0.5, bump=(9, 0.05))
    box("pavement", (70, 1.8, 0.14), (-3, -0.9, 0.07), pave)
    box("kerb", (70, 0.16, 0.15), (-3, -1.86, 0.075), principled("kerb", "#3A434E", rough=0.5))
    # the far side: dark fronts, a few dim windows, for the view out of the shop
    far = principled("far", "#111A23", rough=0.9)
    box("far_wall", (70, 0.5, 8), (-3, -21.6, 4.0), far)
    box("far_pave", (70, 1.8, 0.14), (-3, -20.5, 0.07), pave)
    for k in range(9):
        w = plane(f"far_win{k}", 1.1, 1.5, emit(f"fw{k}", "#2B3F55" if k % 3 else "#3E5872", strength=0.5))
        w.rotation_euler = (rad(90), 0, rad(180))
        w.location = (-14 + k * 3.3 + rnd.uniform(-0.5, 0.5), -21.34, rnd.choice([2.0, 4.6, 6.4]))

    # --- three tube houses -------------------------------------------------------
    wall1 = house("h1", X1, X2, 10.4, "#7C6A45", "#5E5136", rnd)                 # faded ochre
    wall2 = house("h2", X2, X3, 11.6, "#5F7C76", "#465C59", rnd, floors=(4.9, 8.0), lit="#3E5872")  # washed mint
    wall3 = house("h3", X3, X4, 9.8, "#77848F", "#5B6873", rnd, floors=(4.6, 7.4))   # blue-grey
    shut_m = principled("shutter", "#59636D", metallic=0.85, rough=0.42)
    shutters = []
    sign_lights = []
    for tag, x0, x1, hh, wall in (("h1", X1, X2, 10.4, wall1), ("h2", X2, X3, 11.6, wall2)):
        ox0, ox1, oz = x0 + 0.35, x1 - 0.35, 2.7
        box(tag + "_pl", (ox0 - x0, 0.3, hh), (0.5 * (x0 + ox0), 0.15, hh / 2), wall)
        box(tag + "_pr", (x1 - ox1, 0.3, hh), (0.5 * (x1 + ox1), 0.15, hh / 2), wall)
        box(tag + "_top", (ox1 - ox0, 0.3, hh - oz), (0.5 * (ox0 + ox1), 0.15, (hh + oz) / 2), wall)
        box(tag + "_step", (ox1 - ox0, 0.34, 0.08), (0.5 * (ox0 + ox1), 0.13, 0.14 + 0.04), pave)
        shutters.append(slats(tag + "_shutter", ox0 - 0.02, ox1 + 0.02, 0.24, oz + 0.04, 0.17, shut_m))
        # the room behind: pale walls so a lit phone shows through the slats
        rw = principled(tag + "_room", "#AEB9B4", rough=0.9)
        box(tag + "_rf", (x1 - x0, 4.2, 0.1), (0.5 * (x0 + x1), 2.4, 0.17), principled(tag + "_floor", "#3A424A", rough=0.5))
        box(tag + "_rc", (x1 - x0, 4.2, 0.1), (0.5 * (x0 + x1), 2.4, 3.05), rw)
        box(tag + "_rb", (x1 - x0, 0.1, 3.0), (0.5 * (x0 + x1), 4.45, 1.6), rw)
        box(tag + "_rl", (0.08, 4.2, 3.0), (x0 + 0.04, 2.4, 1.6), rw)
        box(tag + "_rr", (0.08, 4.2, 3.0), (x1 - 0.04, 2.4, 1.6), rw)
        wood = principled(tag + "_desk", "#4A372B", rough=0.5, bump=(60, 0.05))
        noisy_color(wood, "#33251C", "#5C4535", scale=7.0, detail=10)
        xc = 0.5 * (x0 + x1)
        box(tag + "_desk_top", (1.5, 0.75, 0.04), (xc, 1.55, 0.74), wood)
        for sx in (-0.7, 0.7):
            box(tag + f"_desk_side{sx}", (0.04, 0.7, 0.72), (xc + sx, 1.55, 0.38), wood)
        for k, (cx, colr) in enumerate(((-0.75, "#2A5E86"), (0.2, "#1F6E66"), (0.95, "#C9D3DA"))):
            box(tag + f"_poster{k}", (0.7, 0.02, 0.95), (xc + cx, 4.38, 1.85), principled(tag + f"_pm{k}", colr, rough=0.8))
    # signs: what these streets really say, no agency names
    sg1 = emit("sign1", "#1F5A45", strength=0.9)
    box("sign1", (2.7, 0.08, 0.8), (0.5 * (X1 + X2), -0.05, 3.3), sg1)
    wht = emit("sign_white", "#F2F6FA", strength=2.0)
    sign_text("s1a", "DU LỊCH · TOURS", ARIAL, 0.27, wht, 0.5 * (X1 + X2), 3.4)
    sign_text("s1b", "VISA · BUS TICKETS · MOTORBIKE", ARIAL, 0.105, wht, 0.5 * (X1 + X2), 3.08)
    sg2 = emit("sign2", "#DDE4EA", strength=0.7)
    box("sign2", (2.7, 0.08, 0.8), (0.5 * (X2 + X3), -0.05, 3.3), sg2)
    navy = emit("sign_navy", "#16284A", strength=1.0)
    sign_text("s2a", "TRAVEL & TOURS", ARIAL, 0.27, navy, 0.5 * (X2 + X3), 3.4)
    sign_text("s2b", "VÉ XE · VÉ TÀU · HA LONG · SAPA", ARIAL, 0.105, navy, 0.5 * (X2 + X3), 3.08)

    # --- Lantern Trips: a glass front and a door ----------------------------------
    WX0, WX1, WZ0, WZ1 = -1.45, 1.25, 0.55, 2.55
    DX1 = 2.45
    H3 = 9.8
    box("h3_pl", (WX0 - X3, 0.3, H3), (0.5 * (X3 + WX0), 0.15, H3 / 2), wall3)
    box("h3_pr", (X4 - DX1, 0.3, H3), (0.5 * (X4 + DX1), 0.15, H3 / 2), wall3)
    box("h3_bot", (WX1 - WX0, 0.3, WZ0), (0.5 * (WX0 + WX1), 0.15, WZ0 / 2), wall3)
    box("h3_top", (DX1 - WX0, 0.3, H3 - WZ1), (0.5 * (WX0 + DX1), 0.15, (H3 + WZ1) / 2), wall3)
    box("door", (DX1 - WX1, 0.06, WZ1), (0.5 * (WX1 + DX1), 0.27, WZ1 / 2), principled("door", "#121A23", rough=0.45, metallic=0.3))
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
    sg3 = principled("sign3", "#0C1622", rough=0.4)
    box("sign3", (3.9, 0.08, 0.8), (0.5 * (WX0 + DX1), -0.05, 3.3), sg3)
    sign_text("s3a", "Lantern Trips", SEMI, 0.36, wht, 0.5 * (WX0 + DX1), 3.36)
    sign_text("s3b", "Small group trips   Ha Giang   Sapa   Ninh Binh", REG, 0.105, wht, 0.5 * (WX0 + DX1), 3.04)

    for k, (xc_, e_, w_) in enumerate(((0.5 * (X1 + X2), 150, 2.2), (0.5 * (X2 + X3), 190, 2.2), (0.5 * (WX0 + DX1) - 0.5, 60, 2.6))):
        sl = area(f"sign_light{k}", (xc_, -0.2, 3.3), (xc_, -2.6, 0.0), e_, w_, color=("#7FD0B0", "#E6EEF8", "#DCE6F5")[k], shape="RECTANGLE", size_y=0.5)
        sl.data.use_shadow = False
        sign_lights.append((sl, e_))

    win_m = emit("win_ring", AZURE, alpha=0.0)
    wh_ = empty("win_ring_h", None, (0.5 * (WX0 + DX1), -0.17, 3.23))   # its top stays under the balcony
    wh_.rotation_euler = (rad(90), 0, 0)
    ring("win_ring", 3.78, 0.63, 0.12, 0.085, win_m, wh_)
    ring_in(wh_, win_m, F_WIN, 12)

    # --- the room behind the glass (as in the first film) ---------------------------
    wallm = principled("room_wall", "#7FA0A6", rough=0.9, bump=(25, 0.03))
    box("r_floor", (4.6, 5, 0.1), (0.3, 2.6, -0.05), principled("room_floor", "#2B3640", rough=0.45, spec=0.4))
    box("r_ceil", (4.6, 5, 0.1), (0.3, 2.6, 3.05), wallm)
    box("r_back", (4.6, 0.1, 3.1), (0.3, 4.6, 1.5), wallm)
    box("r_left", (0.1, 5, 3.1), (X3 + 0.05, 2.6, 1.5), wallm)
    box("r_right", (0.1, 5, 3.1), (X4 - 0.05, 2.6, 1.5), wallm)
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
    shelf = principled("shelf", "#26313C", rough=0.5)
    cols = ["#1E88D6", "#0C1622", "#E8EEF3", "#1BA89A", "#2072B8", "#D7E2EC", "#0C1622"]
    r5 = random.Random(5)
    for row, z in enumerate((1.05, 1.55)):
        box(f"shelf{row}", (1.9, 0.32, 0.03), (1.4, 4.42, z), shelf)
        x = 0.5
        while x < 2.3:
            w = r5.uniform(0.05, 0.08)
            hgt = r5.uniform(0.3, 0.34)
            box(f"binder{row}_{x:.2f}", (w - 0.004, 0.26, hgt), (x + w / 2, 4.42, z + 0.015 + hgt / 2),
                principled("binder", r5.choice(cols), rough=0.55))
            x += w
    box("print_frame", (0.9, 0.03, 0.62), (-1.0, 4.53, 1.75), principled("pf", "#E8EEF3", rough=0.6))
    box("print", (0.8, 0.03, 0.52), (-1.0, 4.52, 1.75), principled("pp", "#2A5E86", rough=0.8))
    # the wall clock beside the window, facing the room
    clk = empty("clock", None, (-1.72, 0.32, 2.0))
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

    # --- the laptop -----------------------------------------------------------------
    alu = principled("lap_alu", "#7E8A98", metallic=1.0, rough=0.3)
    lap = empty("laptop", None, LAP)
    base = slab("lap_base", 0.31, 0.215, 0.01, 0.012, alu, alu, alu, bevel=0.002, parent=lap)
    base.location.z = 0.006
    box("keys", (0.27, 0.105, 0.001), (0, -0.03, 0.0125), principled("lap_keys", "#141B23", rough=0.6), parent=lap)
    hinge = empty("hinge", lap, (0, -0.1075, 0.012))
    hinge.rotation_euler = (rad(OPEN), 0, 0)
    lid = slab("lap_lid", 0.31, 0.215, 0.01, 0.006, alu, alu, principled("bezel", "#05080B", rough=0.05, coat=1.0), bevel=0.0015, parent=hinge)
    lid.location = (0, 0.1075, 0.003)
    scr_m = emit("screen", image=os.path.join(SCRM, "board.png"))
    scr = plane("lap_screen", SW, SH, scr_m, hinge)
    scr.location = (0, 0.1075 + 0.006, -0.0004)
    scr.rotation_euler = (0, math.pi, 0)
    home_m = emit("home", image=os.path.join(SCRM, "home_needs.png"), alpha=0.0)
    hp = plane("home", SW, SH, home_m, scr)
    hp.location = (0, 0, 0.0003)
    ring_m = emit("ring", AZURE, alpha=0.0)                    # one enquiry's card: Erik, quote v2, follow up today
    rh = empty("ring_h", scr, (*px(812 + 223 / 2, 302 + 143 / 2), 0.0006))
    ring("ring", 223 / 1600 * SW + 0.003, 143 / 1000 * SH + 0.003, 0.004, 0.0011, ring_m, rh)
    ring_in(rh, ring_m, F_RING1, 10)
    fade_mat(ring_m, F_SWAP - 1, 1.0)                          # gone on the cut to Home
    fade_mat(ring_m, F_SWAP, 0.0)
    ring2_m = emit("ring2", AZURE, alpha=0.0)                  # the same Erik on Home: what to do next
    rh2 = empty("ring2_h", scr, (*px(336 + 470 / 2, 161 + 59 / 2), 0.0009))
    ring("ring2", 470 / 1600 * SW + 0.004, 59 / 1000 * SH + 0.002, 0.003, 0.0011, ring2_m, rh2)
    ring_in(rh2, ring2_m, F_RING2, 10)
    glow = area("screen_light", (0, 0, 0), (0, 0, -1), 0, 0.34, color="#DCE8F5", shape="RECTANGLE", size_y=0.22)
    glow.parent = hinge
    glow.location = (0, 0.11, -0.09)
    glow.rotation_euler = (0, 0, 0)
    glow.data.spread = rad(75)

    # --- next door: the phone, the fan, the paper ----------------------------------------
    xc2 = 0.5 * (X2 + X3)
    lock_m = [emit(f"mlock{k}", image=os.path.join(SCRM, f"lock{k}.png"), alpha=1.0 if k == 0 else 0.0) for k in range(3)]
    phl, _ = phone("phone_l", emit("phone_l_off", "#020304"))
    PL = Vector((xc2 - 0.16, 1.66, 0.7645))
    phl.location = PL
    phl.rotation_euler = (0, 0, rad(180 + 7))
    for k, m in enumerate(lock_m):
        lp = slab(f"mlockp{k}", PW, PH, 165 * PH_PX, 0.00002, m, m, m, parent=phl)
        lp.location = (0, 0, 0.0039 + 0.00006 * (k + 2))
    point("phone_l_light", (PL.x, PL.y, 0.95), 1.4, radius=0.06, color="#DCE8F5")
    dk = principled("mon_dark", "#12181E", rough=0.4)
    box("mon_foot", (0.22, 0.16, 0.012), (xc2 + 0.4, 1.3, 0.768), dk)
    box("mon_stand", (0.05, 0.04, 0.22), (xc2 + 0.4, 1.28, 0.87), dk)
    box("mon_body", (0.56, 0.025, 0.39), (xc2 + 0.4, 1.3, 1.1), dk)
    mon = plane("monitor", 0.53, 0.36, emit("sheet", image=os.path.join(SCRM, "props", "sheet.png"), strength=0.8))
    mon.rotation_euler = (rad(90), 0, rad(180))
    mon.location = (xc2 + 0.4, 1.3145, 1.1)
    box("cabinet", (0.5, 0.6, 1.25), (X2 + 0.36, 3.6, 0.845), principled("cabinet", "#59636D", metallic=0.7, rough=0.5))
    for k in range(3):
        box(f"carton{k}", (0.42, 0.34, 0.26), (X3 - 0.36, 3.3 + 0.02 * k, 0.35 + 0.265 * k), principled(f"carton{k}", "#8A6F52", rough=0.9)).rotation_euler = (0, 0, rad(-6 + 7 * k))
    fanm = principled("fan", "#C9D0D6", rough=0.45)
    FAN = Vector((xc2, 1.95, 2.72))
    cylinder("fan_rod", 0.012, 0.3, (FAN.x, FAN.y, 2.87), dk, verts=12)
    fan = empty("fan", None, FAN)
    cylinder("fan_hub", 0.095, 0.09, (0, 0, 0), fanm, verts=32, parent=fan)
    for k in range(3):
        piv = empty(f"blade_p{k}", fan)
        piv.rotation_euler = (0, 0, rad(120 * k))
        bl = box(f"blade{k}", (0.58, 0.135, 0.008), (0.38, 0, 0), fanm, parent=piv)
        bl.rotation_euler = (rad(11), 0, 0)
    fan_l = point("fan_light", (FAN.x + 0.04, FAN.y - 0.03, 2.93), 0.0, radius=0.022, color="#EEF3FA")
    # everything the week is made of
    sizes = json.load(open(os.path.join(SCRM, "props", "sizes.json")))
    WIDE = {"sticky": 0.076, "rates": 0.21, "pdf": 0.297, "passport": 0.2, "transfer": 0.105, "chat": 0.105, "boarding": 0.08, "sheet": 0.297}
    pm = {}
    papers = []
    rp = random.Random(17)
    k = 0
    for copy in range(2):
        for nm in sorted(sizes):
            w = WIDE[nm.split("_")[0]]
            h = w * sizes[nm][1] / sizes[nm][0]
            if nm not in pm:
                pm[nm] = principled("p_" + nm, "#FFFFFF", rough=0.85, image=os.path.join(SCRM, "props", nm + ".png"))
                bs = next(n for n in pm[nm].node_tree.nodes if n.type == "BSDF_PRINCIPLED")     # paper lets light through: its dark side is never black
                tx_ = next(n for n in pm[nm].node_tree.nodes if n.type == "TEX_IMAGE")
                pm[nm].node_tree.links.new(tx_.outputs["Color"], bs.inputs["Emission Color"])
                bs.inputs["Emission Strength"].default_value = 0.16
            ob = plane(f"paper_{nm}_{copy}", w, h, pm[nm])
            on_desk = rp.random() < 0.42
            while True:                                   # nothing lies on the phone
                rest = Vector((xc2 + rp.uniform(-0.62, 0.62), rp.uniform(1.24, 1.86), 0.763 + 0.0007 * k))
                if abs(rest.x - PL.x) > 0.06 + w / 2 or abs(rest.y - PL.y) > 0.1 + h / 2:
                    break
            papers.append(dict(
                ob=ob, rest=rest, yaw=rp.uniform(-0.5, 0.5),
                lift=rp.choice([rp.randint(58, 80), rp.randint(84, 150), rp.randint(84, 128)]), a0=rp.uniform(0, 6.28), w=rp.uniform(1.3, 2.7) * rp.choice([1, 1, 1, -1]),
                r=rp.uniform(0.28, 1.22), h=rp.uniform(1.05, 2.3), ph=rp.uniform(0, 6.28),
                t0=[rp.uniform(0, 6.28) for _ in range(3)], tw=[rp.uniform(-3.2, 3.2) for _ in range(3)],
                fall=MC - 10 + rp.randint(0, 28), fd=rp.randint(22, 38),
                land=Vector((xc2 + rp.uniform(-0.65, 0.65), rp.uniform(1.24, 1.86), 0.764 + 0.0007 * k)) if on_desk
                else (Vector((xc2 + 0.32 + rp.uniform(-0.55, 0.55), 2.52 + rp.uniform(-0.45, 0.5), 0.2255 + 0.0006 * k)) if rp.random() < 0.6
                      else Vector((xc2 + rp.uniform(-1.25, 1.25), rp.uniform(0.7, 3.3), 0.2255 + 0.0006 * k))), lyaw=rp.uniform(-3.1, 3.1)))
            k += 1
    HERO_LAND = Vector((xc2 + 0.32, 2.52, 0.262))      # on top of whatever fell first
    hero = dict(ob=plane("paper_hero", 0.2, 0.2 * 880 / 1250, pm["passport_a"]), rest=Vector((xc2 + 0.1, 1.72, 0.79)), yaw=0.4, lift=96,
                a0=1.0, w=1.9, r=0.55, h=1.55, ph=0.3, t0=[0.2, 0.5, 0.1], tw=[1.6, -2.1, 1.2], fall=MC - 8, fd=24,
                land=Vector((xc2 + 0.22, 1.9, 0.7665)), lyaw=rad(172))
    papers.append(hero)

    def paper_pose(P, f):
        if f < P["lift"]:
            return P["rest"], (0.0, 0.0, P["yaw"])
        ts = (f - P["lift"]) / FPS
        ang = P["a0"] + P["w"] * ts
        orb = Vector((xc2 + P["r"] * math.cos(ang), 1.85 + 0.8 * P["r"] * math.sin(ang), P["h"] + 0.16 * math.sin(1.9 * ts + P["ph"])))
        orot = [P["t0"][i] + P["tw"][i] * ts for i in range(3)]
        up = smooth(prog(f, P["lift"], P["lift"] + 34))
        pos = P["rest"].lerp(orb, up)
        rot = [lerp(a, b, up) for a, b in zip((0.0, 0.0, P["yaw"]), orot)]
        if f >= P["fall"]:
            q = prog(f, P["fall"], P["fall"] + P["fd"])
            land = P["land"]
            pos = Vector((lerp(orb.x, land.x, out_cubic(q)), lerp(orb.y, land.y, out_cubic(q)),
                          lerp(orb.z, land.z, smooth(q)) + 0.05 * math.sin(q * math.pi * 3) * (1 - q)))
            rot = [lerp(a, b, smoother(q)) for a, b in zip(orot, (0.0, 0.0, P["lyaw"]))]
        return pos, tuple(rot)

    tubes = []
    for tag, x0, x1 in (("h1", X1, X2), ("h2", X2, X3)):
        tm = emit(tag + "_tube", "#F2F7FF", strength=0.0)
        box(tag + "_tube", (1.2, 0.05, 0.04), (0.5 * (x0 + x1), 2.2, 2.96), tm)
        ta = area(tag + "_tube_l", (0.5 * (x0 + x1), 2.2, 2.9), (0.5 * (x0 + x1), 2.2, 0), 0, 1.2, color="#EEF4FF", shape="RECTANGLE", size_y=0.2)
        tubes.append((tm, ta))

    # --- the pole, its wires, the lamp ----------------------------------------------
    conc = principled("pole", "#3B434B", rough=0.8, bump=(30, 0.04))
    PX_, PY_ = -2.35, -1.62
    cylinder("pole", 0.11, 8.4, (PX_, PY_, 4.2), conc, verts=20)
    box("cross1", (1.5, 0.07, 0.07), (PX_, PY_, 7.5), conc)
    box("cross2", (1.1, 0.07, 0.07), (PX_, PY_, 6.9), conc)
    box("jbox", (0.42, 0.24, 0.5), (PX_, PY_ - 0.2, 5.3), principled("jbox", "#59636D", metallic=0.6, rough=0.5))
    cable = principled("cable", "#07090C", rough=0.6)
    wr = random.Random(3)
    for k in range(13):                           # along the street, both ways
        z = wr.uniform(6.2, 7.6)
        dy = wr.uniform(-0.6, 0.6)
        wire(f"w_l{k}", (PX_ + wr.uniform(-0.6, 0.6), PY_ + dy * 0.2, z), (-24, PY_ + dy, z + wr.uniform(-0.5, 0.5)), wr.uniform(0.5, 1.6), cable, r=wr.uniform(0.006, 0.014))
        wire(f"w_r{k}", (PX_ + wr.uniform(-0.6, 0.6), PY_ + dy * 0.2, z), (20, PY_ + dy, z + wr.uniform(-0.5, 0.5)), wr.uniform(0.5, 1.6), cable, r=wr.uniform(0.006, 0.014))
    for k, (tx, tz) in enumerate(((-7.2, 6.4), (-6.0, 9.2), (-3.6, 6.8), (-4.4, 9.9), (-0.6, 6.2), (1.2, 8.6), (2.2, 5.9))):
        wire(f"w_h{k}", (PX_, PY_, wr.uniform(5.4, 7.4)), (tx, -0.02, tz), wr.uniform(0.15, 0.5), cable, r=0.006)
    for k in range(4):                            # across the street
        wire(f"w_x{k}", (PX_, PY_, wr.uniform(6.4, 7.5)), (PX_ + wr.uniform(-6, 6), -21.3, wr.uniform(6.5, 9.0)), wr.uniform(0.6, 1.3), cable, r=0.008)
    for k in range(5):                            # the coil every pole wears
        bpy.ops.mesh.primitive_torus_add(major_radius=wr.uniform(0.2, 0.34), minor_radius=0.012, location=(PX_ + wr.uniform(-0.08, 0.08), PY_ - 0.13, wr.uniform(5.7, 6.5)))
        tq = bpy.context.active_object
        tq.rotation_euler = (rad(90 + wr.uniform(-14, 14)), wr.uniform(-0.3, 0.3), 0)
        tq.data.materials.append(cable)
    box("arm", (0.06, 0.9, 0.06), (PX_, PY_ - 0.45, 5.9), conc)
    head_m = emit("lamp_head", "#EEF4FF", strength=4.0)
    box("lamp_head", (0.24, 0.4, 0.06), (PX_, PY_ - 0.9, 5.84), head_m)
    lamp = spot("lamp", (PX_, PY_ - 0.9, 5.78), (PX_ + 0.6, -2.4, 0.0), 3400, angle=96, blend=0.9, radius=0.14, color="#E3ECFA")
    lamp2 = spot("lamp2", (-15.5, -2.5, 5.8), (-14.5, -3.0, 0.0), 1700, angle=90, blend=0.9, radius=0.14, color="#DCE6F5")
    fog_box("street_fog", (44, 22, 9), (-3, -10.5, 4.5), 0.0032, color="#C8D6E6", anisotropy=0.5)

    # --- the lantern over the door: the one warm light --------------------------------
    LX, LY, LZ = 0.5 * (WX1 + DX1), -0.52, 2.86
    box("lant_arm", (0.03, 0.6, 0.03), (LX, -0.28, 3.14), frame)
    cylinder("lant_cord", 0.004, 0.1, (LX, LY, 3.08), cable, verts=8)
    lant_m = emit("lantern", "#FF8A2C", strength=2.3)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=14, radius=0.19, location=(LX, LY, LZ))
    lant = bpy.context.active_object
    lant.scale = (1, 1, 1.22)
    lant.data.materials.append(lant_m)
    bpy.ops.object.shade_smooth()
    cap = principled("lant_cap", "#2A1B12", rough=0.6)
    cylinder("lant_top", 0.075, 0.03, (LX, LY, LZ + 0.225), cap, verts=20)
    cylinder("lant_bot", 0.075, 0.03, (LX, LY, LZ - 0.225), cap, verts=20)
    cylinder("lant_tassel", 0.012, 0.22, (LX, LY, LZ - 0.36), principled("tassel", "#8E2F22", rough=0.8), verts=10)
    lant_l = point("lantern_light", (LX, LY - 0.02, LZ), 260, radius=0.19, color="#FFA250")

    # --- what lives on the pavement -----------------------------------------------------
    scooter("sco_a", (-5.25, -1.15, 0.14), 262, "#7D1F1F")
    scooter("sco_b", (-8.75, -1.1, 0.14), 255, "#27384A")
    scooter("sco_c", (-9.5, -1.15, 0.14), 262, "#9AA5AE")
    scooter("sco_d", (3.9, -1.2, 0.14), 190, "#1F4D3C")
    bark = principled("bark", "#2A2520", rough=0.9, bump=(14, 0.2))
    cylinder("trunk", 0.24, 6.0, (-9.05, -1.3, 3.0), bark, verts=14)
    leafm = principled("canopy", "#16301F", rough=0.8)
    tr3 = random.Random(8)
    for k in range(11):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=tr3.uniform(1.0, 1.7), location=(-9.05 + tr3.uniform(-1.8, 1.9), -1.7 + tr3.uniform(-1.6, 0.9), 6.9 + tr3.uniform(-0.6, 2.4)))
        bpy.context.active_object.data.materials.append(leafm)
    box("pho_sign", (2.2, 0.08, 0.62), (4.5, -0.05, 3.25), principled("pho", "#D9DEE2", rough=0.5))
    sign_text("pho_t", "PHỞ BÒ · BÚN CHẢ", ARIAL, 0.2, principled("pho_red", "#8E2F22", rough=0.5), 4.5, 3.25)
    stool_cols = ["#8E2F22", "#1B4E7A", "#8E2F22"]
    for k in range(3):                              # the stools every pavement has, stacked for the night
        st = box(f"stool{k}", (0.28, 0.28, 0.06), (-2.2, -0.42, 0.44 + 0.07 * k), principled(f"stool{k}", stool_cols[k], rough=0.35))
        for sx in (-1, 1):
            for sy in (-1, 1):
                box(f"stool{k}_{sx}{sy}", (0.035, 0.035, 0.28), (-2.2 + sx * 0.11, -0.42 + sy * 0.11, 0.28 + 0.07 * k), st.data.materials[0])
    for k, (pxx, pyy, rr) in enumerate(((2.75, -0.45, 0.34), (-1.95, -0.4, 0.26), (-8.3, -0.4, 0.3))):
        cylinder(f"gpot{k}", 0.2, 0.4, (pxx, pyy, 0.34), principled(f"gpotm{k}", "#4E5A63", rough=0.7), verts=20)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rr, location=(pxx, pyy, 0.34 + 0.2 + rr * 1.1))
        lf = bpy.context.active_object
        lf.scale.z = 1.5
        lf.data.materials.append(principled(f"gleaf{k}", "#1C3A2B", rough=0.7))
    # the rest of the street, left and right, shuttered
    nb = principled("neigh", "#33414C", rough=0.9, bump=(18, 0.05))
    noisy_color(nb, "#26323B", "#3B4A56", scale=1.2)
    box("nb_l", (14, 0.3, 11.2), (X1 - 7, 0.15, 5.6), nb)
    box("nb_r", (14, 0.3, 10.6), (X4 + 7, 0.15, 5.3), nb)
    for k in range(4):
        xx = X1 - 1.7 - 3.3 * k
        slats(f"nb_sh_l{k}", xx - 1.25, xx + 1.25, 0.2, 2.75, -0.02, shut_m)
        upper_floor(f"nbl{k}", xx - 1.6, xx + 1.6, 4.8, nb, rnd)
        xx = X4 + 1.7 + 3.3 * k
        slats(f"nb_sh_r{k}", xx - 1.25, xx + 1.25, 0.2, 2.75, -0.02, shut_m)
        upper_floor(f"nbr{k}", xx - 1.6, xx + 1.6, 4.7, nb, rnd)

    # --- rain: streaks in a tall box, falling one tile at a time -----------------------
    TILE = 10.0
    rain_m = emit("rain", "#A9BDD4", strength=1.0, alpha=0.1)
    me = bpy.data.meshes.new("rain")
    bm = bmesh.new()
    rr_ = random.Random(21)
    for _ in range(5200):
        x, y, z = rr_.uniform(-16, 9), rr_.uniform(-17, -0.2), rr_.uniform(0, 2 * TILE)
        ln, w = rr_.uniform(0.2, 0.42), rr_.uniform(0.0016, 0.0034)
        a = rr_.uniform(0, math.pi)
        dx, dy = math.cos(a) * w, math.sin(a) * w
        vs = [bm.verts.new(v) for v in ((x - dx, y - dy, z), (x + dx, y + dy, z), (x + dx + 0.04, y + dy, z + ln), (x - dx + 0.04, y - dy, z + ln))]
        bm.faces.new(vs)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(rain_m)
    rain = link(bpy.data.objects.new("rain", me))
    rain.visible_shadow = False

    # dawn: a low sun from across the street, through the gaps in the shutters
    dsun = sun("dawn_sun", (0, 0, 0), 0.0, angle=1.0, color="#FFDDBA")
    HX, HY = Vector((-0.42, 0.9)).normalized()
    # night: a little cool sky light from above so the fronts keep their shape
    nsun = sun("night_fill", (0, 0, 0), 0.0, angle=30, color="#8FA9CC")
    nd = Vector((0.5, 0.55, -0.67)).normalized()
    nsun.rotation_euler = (-nd).to_track_quat("Z", "Y").to_euler()
    nsun.data.use_shadow = False
    lamp2.data.use_shadow = False

    # --- animation ----------------------------------------------------------------------
    nsun.data.energy = 0.3
    glow.data.energy = 9.0
    ang = 0.0
    for f in range(N):
        fade_mat(rain_m, f, 0.1)
        rain.location = (0, 0, -((f * 0.44) % TILE))
        rain.keyframe_insert("location", frame=f)
        # the phone fills up
        for k, lm in enumerate(lock_m):
            fade_mat(lm, f, 1.0 if k == 0 else smooth(prog(f, 26 * k, 26 * k + 3)))
        # the fan: turning until it all comes down, on again for whoever is still in there at 23:30
        spin = 1.0 - smoother(prog(f, MC - 6, MC + 34)) if f < MD else (1.0 if f >= ME else 0.0)
        ang += 2 * math.pi * 2.05 * spin / FPS
        fan.rotation_euler = (0, 0, ang)
        fan.keyframe_insert("rotation_euler", frame=f)
        inside = f < MD or f >= ME
        fan_l.data.energy = 190.0 if inside else 0.0
        fan_l.data.keyframe_insert("energy", frame=f)
        tm, ta = tubes[1]
        key_val(tm.node_tree.nodes["em"].inputs["Strength"], f, 3.0 if inside else 0.0)
        ta.data.energy = (26.0 if f < MD else 420.0) if inside else 0.0
        ta.data.keyframe_insert("energy", frame=f)
        if f <= MD:
            for P in papers:
                pos, rot = paper_pose(P, f)
                if P is hero and f >= MC + 20:                       # it lands on the edge, then goes over
                    q = smoother(prog(f, MC + 20, MC + 42))
                    pos = P["land"].lerp(HERO_LAND, q) + Vector((0, 0, 0.12 * math.sin(math.pi * q) * (1 - q)))
                    rot = (-1.1 * math.sin(math.pi * q), 0.0, lerp(P["lyaw"], rad(186), q))
                key(P["ob"], f, loc=pos, rot=rot)
        # Lantern Trips: the board, then Home
        fade_mat(home_m, f, 1.0 if f >= F_SWAP else 0.0)      # a cut, with the camera
    ring_in(wh_, win_m, F_WIN, 12)

    # --- camera --------------------------------------------------------------------------
    bpy.context.view_layer.update()
    bc = empty("board_c", scr, (*px(924, 300), 0.0))
    hc = empty("home_c", scr, (*px(571, 300), 0.0))
    bpy.context.view_layer.update()
    board_c = bc.matrix_world.translation.copy()
    home_c = hc.matrix_world.translation.copy()
    nrm = Vector((0, math.sin(rad(OPEN)), -math.cos(rad(OPEN))))
    scr_c = scr.matrix_world.translation.copy()
    pl = PL + Vector((0, 0, 0.004))
    room = Vector((xc2, 1.8, 1.5))
    street = Vector((-1.3, 0, 3))
    # (frame, position, look at, lens, f-stop, focus point)
    shots = [
        (0, pl + Vector((0.02, 0.15, 0.37)), pl + Vector((0.0, -0.006, 0)), 50, 4.0, pl),
        (MB - 1, pl + Vector((0.012, 0.135, 0.335)), pl + Vector((0.0, -0.005, 0)), 50, 4.0, pl),
        (MB, Vector((-2.5, 3.95, 1.2)), Vector((xc2 - 0.1, 1.7, 1.62)), 21, 4.0, room),
        (MC - 1, Vector((-2.7, 3.55, 1.28)), Vector((xc2 - 0.1, 1.7, 1.6)), 22, 4.0, room),
        (MC, Vector((xc2 + 0.4, 3.02, 0.98)), HERO_LAND + Vector((0.0, -0.1, 0.0)), 32, 2.8, HERO_LAND),
        (MD - 1, Vector((xc2 + 0.38, 2.96, 0.9)), HERO_LAND + Vector((0.0, -0.08, 0.0)), 32, 2.8, HERO_LAND),
        (MD, Vector((0.55, 3.2, 1.3)), scr_c + Vector((0.02, 0, 0.02)), 35, 3.2, scr_c),
        (346, Vector((0.5, 3.12, 1.29)), scr_c + Vector((0.018, 0, 0.02)), 35, 3.2, scr_c),
        (404, board_c + nrm * 0.4, board_c, 50, 2.8, board_c),
        (F_SWAP - 1, board_c + nrm * 0.39, board_c, 50, 2.8, board_c),
        (F_SWAP, home_c + nrm * 0.4, home_c, 50, 2.8, home_c),
        (ME - 1, home_c + nrm * 0.385, home_c, 50, 2.8, home_c),
        (ME, Vector((-1.0, -12.4, 1.5)), Vector((-1.0, 0.0, 4.3)), 21, 8.0, street),
        (N - 1, Vector((-1.0, -11.7, 1.5)), Vector((-1.0, 0.0, 4.2)), 21.6, 8.0, street),
    ]
    MOVES = (346,)
    for f in range(N):
        i = max(k for k in range(len(shots) - 1) if shots[k][0] <= f)
        a, b = shots[i], shots[i + 1]
        tt = (smoother if a[0] in MOVES else smooth)(prog(f, a[0], b[0]))
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
    set_interp(rain, "CONSTANT")                  # the streaks are the blur; a wrapped tile must not smear
    sc.render.motion_blur_position = "START"
    for ob in bpy.data.objects:
        if ob.type == "LIGHT" and ob.name not in ("lamp", "lamp2", "lantern_light", "dawn_sun"):
            ob.data.volume_factor = 0.0
    return sc


def per_frame(f):
    # the frame before a cut would smear half way into the next shot
    bpy.context.scene.render.use_motion_blur = (f + 1) not in (MB, MC, MD, F_SWAP, ME)


if __name__ == "__main__":
    a = args()
    sc = build()
    if a and a[0] == "still":
        render(sc, OUT.replace("3d", "stills"), stills=[int(x) for x in a[1:]], per_frame=per_frame)
    else:
        render(sc, OUT, per_frame=per_frame)
