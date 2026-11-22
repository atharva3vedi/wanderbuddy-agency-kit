"""Film 1, Departures: the free listing on /trips, as a split-flap board.

  Blender -b --factory-startup -P build/departures.py -- [still f f ...]

A Solari-style board in a dark hall with one shaft of daylight. The agency's
departures flip into place (Lantern Trips and Kite Trips, the sample agencies),
the hero row's seats go from 4 to 3 as a traveller holds a spot, then the
camera comes down to a phone on a table showing the real /trips listing
(screens/marketPhone.png) and the ring lands on Hold my spot.
Frames: render/departures/3d/####.png, 0..515 (21.5 s at 24 fps).
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
OUT = os.path.join(AD, "render", "departures", "3d")
DRUM = " ABCDEFGHIJKLMNOPQRSTUVWXYZ9876543210.:-,'&/"
COLS_A, ROWS_A = 8, 6

# Board geometry (board-local XY, front +Z; metres)
FW, HH, G = 0.0427, 0.032, 0.0009          # flap width, half height, half gap at the hinge
PX_, PY_ = 0.0468, 0.0815                  # cell pitch
FIELDS = [("TRIP", 14), ("DEPARTS", 6), ("HOST", 13), ("SEATS", 6)]
NC = sum(n for _, n in FIELDS) + len(FIELDS) - 1   # 42 cells with one blank between fields
ROWS = [
    ("KRABI ISLANDS", "16 NOV", "LANTERN TRIPS", "4 LEFT"),
    ("PHANG NGA BAY", "23 NOV", "LANTERN TRIPS", "6 LEFT"),
    ("HA LONG BAY", "30 NOV", "KITE TRIPS", "2 LEFT"),
    ("SIEM REAP", "07 DEC", "LANTERN TRIPS", "7 LEFT"),
    ("LUANG PRABANG", "09 DEC", "KITE TRIPS", "8 LEFT"),
    ("EL NIDO", "11 JAN", "LANTERN TRIPS", "5 LEFT"),
    ("CHIANG MAI", "14 JAN", "KITE TRIPS", "4 LEFT"),
    ("UBUD", "18 JAN", "LANTERN TRIPS", "9 LEFT"),
    ("KOMODO", "02 FEB", "KITE TRIPS", "3 LEFT"),
    ("SAPA", "14 FEB", "LANTERN TRIPS", "6 LEFT"),
]
NR = len(ROWS)
BW, BH = NC * PX_, NR * PY_
BOARD_Z = 2.80                              # board centre height in the hall
F_SEAT, F_RING1, F_RING1_OUT, F_RING2 = 330, 336, 392, 466


def row_string(r):
    out = []
    for (name, n), val in zip(FIELDS, ROWS[r]):
        out.append(val.ljust(n)[:n])
    return " ".join(out)


def cell_xy(c, r):
    return (-BW / 2 + PX_ * (c + 0.5), BH / 2 - PY_ * (r + 0.5))


def board_to_world(x, y, z=0.0):
    return Vector((x, -z, BOARD_Z + y))


# --- time: the opening runs in slow motion, then ramps to real time ----------------

def speed(f):
    return lerp(0.2, 1.0, smooth(prog(f, 66, 136)))


TAU = [0.0]
for _f in range(1, N + 40):
    TAU.append(TAU[-1] + 0.5 * (speed(_f - 1) + speed(_f)) / FPS)


def frame_of(tau):
    """Inverse of TAU (fractional frame)."""
    lo, hi = 0, len(TAU) - 1
    if tau <= 0:
        return 0.0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if TAU[mid] < tau:
            lo = mid
        else:
            hi = mid
    return lo + (tau - TAU[lo]) / max(1e-9, TAU[hi] - TAU[lo])


# --- materials -----------------------------------------------------------------

ATLAS = os.path.join(SCR, "flap_atlas.png")


def flap_material(name, mode):
    """mode: 'top' | 'bot' | 'flap'. Reads the object's ["c"] (and ["n"]) glyph index."""
    m = bpy.data.materials.new(name)
    nt, out = (m.node_tree if m.use_nodes else None), None
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    N_ = nt.nodes.new
    L = nt.links.new

    def math_(op, a, b=None):
        n = N_("ShaderNodeMath")
        n.operation = op
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                L(v, n.inputs[i])
        return n.outputs[0]

    tc = N_("ShaderNodeTexCoord")
    sep = N_("ShaderNodeSeparateXYZ")
    L(tc.outputs["UV"], sep.inputs[0])
    u, v = sep.outputs[0], sep.outputs[1]
    ac = N_("ShaderNodeAttribute")
    ac.attribute_type = "OBJECT"
    ac.attribute_name = "c"
    idx = ac.outputs["Fac"]
    if mode == "flap":
        an = N_("ShaderNodeAttribute")
        an.attribute_type = "OBJECT"
        an.attribute_name = "n"
        geo = N_("ShaderNodeNewGeometry")
        bf = geo.outputs["Backfacing"]
        # idx = c + (n - c) * backfacing ; cell_v = 0.5 + 0.5 * v * (1 - 2 * backfacing)
        idx = math_("ADD", idx, math_("MULTIPLY", math_("SUBTRACT", an.outputs["Fac"], idx), bf))
        sgn = math_("SUBTRACT", 1.0, math_("MULTIPLY", bf, 2.0))
        cv = math_("ADD", 0.5, math_("MULTIPLY", math_("MULTIPLY", v, 0.5), sgn))
    elif mode == "top":
        cv = math_("ADD", 0.5, math_("MULTIPLY", v, 0.5))
    else:
        cv = math_("MULTIPLY", v, 0.5)
    idx = math_("ROUND", idx)
    col = math_("FLOORED_MODULO", idx, float(COLS_A))
    row = math_("FLOOR", math_("DIVIDE", idx, float(COLS_A)))
    U = math_("DIVIDE", math_("ADD", col, u), float(COLS_A))
    V = math_("DIVIDE", math_("ADD", math_("SUBTRACT", float(ROWS_A - 1), row), cv), float(ROWS_A))
    cmb = N_("ShaderNodeCombineXYZ")
    L(U, cmb.inputs[0])
    L(V, cmb.inputs[1])
    tex = N_("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(ATLAS, check_existing=True)
    tex.interpolation = "Linear"
    tex.extension = "CLIP"
    L(cmb.outputs[0], tex.inputs[0])
    # Flap colour: ink plastic, a touch lighter away from the hinge; glyphs in warm-free white.
    shade = math_("ADD", 0.82, math_("MULTIPLY", v, 0.18))
    base = N_("ShaderNodeMix")
    base.data_type = "RGBA"
    base.inputs[6].default_value = lin("#141E2A")
    base.inputs[7].default_value = lin("#EEF3F8")
    L(tex.outputs["Alpha"], base.inputs[0])
    mul = N_("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    L(base.outputs[2], mul.inputs[6])
    gray = N_("ShaderNodeCombineXYZ")
    for i in range(3):
        L(shade, gray.inputs[i])
    L(gray.outputs[0], mul.inputs[7])
    p = N_("ShaderNodeBsdfPrincipled")
    L(mul.outputs[2], p.inputs["Base Color"])
    rough = math_("SUBTRACT", 0.42, math_("MULTIPLY", tex.outputs["Alpha"], 0.12))
    L(rough, p.inputs["Roughness"])
    p.inputs["Specular IOR Level"].default_value = 0.45
    L(p.outputs[0], out.inputs["Surface"])
    return m


def half_mesh(name, top):
    """A flap half in board-local XY. Origin on the hinge line (y = 0)."""
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    y0, y1 = (G, HH) if top else (-HH, -G)
    r = 0.0022
    pts = []
    # rounded on the two outer corners only
    if top:
        pts = [(-FW / 2, y0), (FW / 2, y0)]
        for i in range(7):
            a = rad(0 + 90 * i / 6)
            pts.append((FW / 2 - r + r * math.cos(a), y1 - r + r * math.sin(a)))
        for i in range(7):
            a = rad(90 + 90 * i / 6)
            pts.append((-FW / 2 + r + r * math.cos(a), y1 - r + r * math.sin(a)))
    else:
        pts = []
        for i in range(7):
            a = rad(180 + 90 * i / 6)
            pts.append((-FW / 2 + r + r * math.cos(a), y0 + r + r * math.sin(a)))
        for i in range(7):
            a = rad(270 + 90 * i / 6)
            pts.append((FW / 2 - r + r * math.cos(a), y0 + r + r * math.sin(a)))
        pts += [(FW / 2, y1), (-FW / 2, y1)]
    vs = [bm.verts.new((x, y, 0)) for x, y in pts]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new("UVMap")
    for lp in f.loops:
        x, y, _ = lp.vert.co
        lp[uv].uv = ((x + FW / 2) / FW, (y - y0) / (y1 - y0))
    bm.to_mesh(me)
    bm.free()
    return me


# --- build ---------------------------------------------------------------------

def build():
    sc, cam = new_scene(N, engine="EEVEE", samples=64, world="#0A1420", world_strength=0.06)
    sc.eevee.volumetric_end = 40
    board = empty("board", None, (0, 0, BOARD_Z))
    board.rotation_euler = (rad(90), 0, 0)

    m_top, m_bot, m_flap = flap_material("top", "top"), flap_material("bot", "bot"), flap_material("flap", "flap")
    me_top, me_bot = half_mesh("top", True), half_mesh("bot", False)
    me_top.materials.append(m_top)
    me_bot.materials.append(m_bot)
    me_flap = half_mesh("flapm", True)
    me_flap.materials.append(m_flap)

    # Housing, frame and dividers
    housing = principled("housing", "#070C12", rough=0.55)
    frame = principled("frame", "#111B27", rough=0.32, metallic=0.6)
    back = plane("board_back", BW + 0.02, BH + 0.02, housing, board)
    back.location.z = -0.006
    fr = slab("board_frame", BW + 0.16, BH + 0.30, 0.02, 0.05, frame, frame, frame, bevel=0.006, parent=board)
    fr.location = (0, 0.07, -0.033)
    import bmesh
    me = bpy.data.meshes.new("dividers")
    bm = bmesh.new()

    def bar(x0, x1, y0, y1, z0, z1):
        bmesh.ops.create_cube(bm, size=1.0, matrix=__import__("mathutils").Matrix.LocRotScale(
            Vector(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)), None, Vector((x1 - x0, y1 - y0, z1 - z0))))
    for c in range(NC + 1):
        x = -BW / 2 + PX_ * c
        bar(x - 0.0012, x + 0.0012, -BH / 2, BH / 2, -0.006, 0.0045)
    for r in range(NR + 1):
        y = BH / 2 - PY_ * r
        bar(-BW / 2, BW / 2, y - 0.0016, y + 0.0016, -0.006, 0.006)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(principled("divider", "#0B121A", rough=0.4, metallic=0.5))
    link(bpy.data.objects.new("dividers", me), board)

    # Header: "Departures" and the field labels, painted on the frame
    paint = principled("paint", "#E8EEF4", rough=0.45)
    t = text("hdr", "Departures", SEMI, 0.072, paint, board)
    t.location = (-BW / 2, BH / 2 + 0.115, -0.0078)
    x = -BW / 2
    for name, n in FIELDS:
        lb = text("lbl_" + name, name.capitalize() if name != "SEATS" else "Seats", SEMI, 0.026, paint, board)
        lb.location = (x + 0.004, BH / 2 + 0.032, -0.0078)
        x += (n + 1) * PX_
    sub = text("hdr_r", "wanderbuddyapp.com/trips", REG, 0.03, paint, board, align="RIGHT")
    sub.location = (BW / 2, BH / 2 + 0.112, -0.0078)

    # Cells
    rnd = random.Random(7)
    cells = []
    for r in range(NR):
        s = row_string(r)
        for c in range(NC):
            x, y = cell_xy(c, r)
            obs = {}
            for k, mesh, z in (("top", me_top, 0.0), ("bot", me_bot, 0.0), ("flap", me_flap, 0.0004)):
                ob = link(bpy.data.objects.new(f"{k}_{r}_{c}", mesh), board)
                ob.location = (x, y, z)
                ob["c"] = 0.0
                if k == "flap":
                    ob["n"] = 0.0
                    ob.rotation_euler = (math.pi, 0, 0)
                else:
                    ob.rotation_euler = (rnd.uniform(-0.012, 0.012), 0, rnd.uniform(-0.004, 0.004))
                obs[k] = ob
            cells.append((r, c, s[c], obs))

    # Flip schedule (board time, seconds). Hero row's trip name first, in slow motion.
    DUR = 0.062
    sched = {}
    for r, c, ch, obs in cells:
        if ch == " ":
            continue
        tgt = DRUM.index(ch)
        if r == 0 and c < 14:
            t0 = 0.05 + 0.055 * c
        else:
            t0 = 1.55 + 0.16 * r + 0.011 * c + rnd.uniform(0, 0.05)
        seq = list(range(1, tgt + 1))
        sched[(r, c)] = [(t0 + i * DUR, t0 + (i + 1) * DUR, (seq[i - 1] if i else 0), s_) for i, s_ in enumerate(seq)]
    # The hold: the hero row's seat count steps from 4 to 3 (one flip, a little slower).
    seat_col = sum(n for _, n in FIELDS[:3]) + 3
    tau_seat = TAU[F_SEAT]
    sched.setdefault((0, seat_col), []).append((tau_seat, tau_seat + 0.11, DRUM.index("4"), DRUM.index("3")))

    def ckey(ob, prop, fr, v):
        ob[prop] = float(v)
        ob.keyframe_insert(f'["{prop}"]', frame=fr)

    for r, c, ch, obs in cells:
        flips = sched.get((r, c), [])
        top, bot, fl = obs["top"], obs["bot"], obs["flap"]
        ckey(top, "c", 0, 0)
        ckey(bot, "c", 0, 0)
        ckey(fl, "c", 0, 0)
        ckey(fl, "n", 0, 0)
        fl.rotation_euler = (math.pi, 0, 0)
        fl.keyframe_insert("rotation_euler", index=0, frame=0)
        for (t0, t1, a, b) in flips:
            f0, f1 = frame_of(t0), frame_of(t1)
            ckey(top, "c", f0, b)
            ckey(fl, "c", f0, a)
            ckey(fl, "n", f0, b)
            fl.rotation_euler = (0.0, 0, 0)
            fl.keyframe_insert("rotation_euler", index=0, frame=f0 + 0.002)
            fl.rotation_euler = (math.pi, 0, 0)
            fl.keyframe_insert("rotation_euler", index=0, frame=f1)
            ckey(bot, "c", f1, b)
        for ob in (top, bot, fl):
            set_interp(ob, "CONSTANT")
        # The falling flap accelerates like a flap under gravity.
        for fc in __import__("film")._fcurves(fl):
            if fc.data_path == "rotation_euler":
                pts = fc.keyframe_points
                for i, kp in enumerate(pts):
                    if abs(kp.co.y) < 1e-6:
                        kp.interpolation = "QUAD"
                        kp.easing = "EASE_IN"

    # The one azure ring, round the hero row.
    ring_m = emit("ring_board", AZURE, strength=1.6, alpha=0.0)
    rh = empty("ring_board_h", board, (0, cell_xy(0, 0)[1], 0.007))
    ring("ring_board", BW + 0.03, PY_ - 0.004, 0.012, 0.0045, ring_m, rh)
    ring_in(rh, ring_m, F_RING1, 10)
    for f in range(F_RING1_OUT, F_RING1_OUT + 9):
        fade_mat(ring_m, f, 1 - prog(f, F_RING1_OUT, F_RING1_OUT + 8))

    # --- the hall ----------------------------------------------------------------
    conc = principled("concrete", "#5A626C", rough=0.85, bump=(55, 0.08, 10))
    noisy_color(conc, "#3D444D", "#69717B", scale=3.0)
    wall = box("wall", (18, 0.2, 9), (0, 0.17, 4.5), conc)
    floor_m = principled("floor", "#3A414A", rough=0.55, bump=(40, 0.04))
    noisy_color(floor_m, "#2C323A", "#4A515A", scale=1.5)
    box("floor", (18, 16, 0.2), (0, -7.5, -0.1), floor_m)
    box("ceiling", (18, 16, 0.2), (0, -7.5, 7.6), conc)
    # Left wall with one tall window: daylight comes through it in a shaft.
    box("lwall_a", (0.3, 5.4, 7.6), (-5.0, -10.9, 3.8), conc)
    box("lwall_b", (0.3, 5.6, 7.6), (-5.0, -1.9, 3.8), conc)
    box("lwall_top", (0.3, 3.5, 0.9), (-5.0, -6.45, 7.15), conc)
    box("lwall_bot", (0.3, 3.5, 2.9), (-5.0, -6.45, 1.45), conc)
    for k in range(4):
        box(f"mullion{k}", (0.12, 0.07, 3.9), (-5.0, -8.2 + 3.5 * (k + 1) / 5, 4.85), frame)
    box("rwall", (0.3, 16, 7.6), (5.4, -7.5, 3.8), conc)
    box("bwall", (18, 0.3, 7.6), (0, -15.4, 3.8), conc)
    s = sun("sun", (0, 0, 0), 14.0, angle=0.6, color="#F1F6FF")
    d = Vector((1.0, 1.22, -0.47)).normalized()
    s.rotation_euler = (-d).to_track_quat("Z", "Y").to_euler()
    fog_box("fog", (10.0, 15.6, 7.4), (0.2, -7.6, 3.72), 0.03, color="#E1E9F2", anisotropy=0.1)
    # The board's own strip light under the frame lip, raking the flaps from above.
    strip = area("strip", board_to_world(0, BH / 2 + 0.45, 0.75), board_to_world(0, -0.05, 0.0), 22, BW + 0.3, shape="RECTANGLE", size_y=0.35, color="#EAF1FA")
    strip.data.energy = 9
    strip.data.spread = rad(70)
    area("fill", (2.5, -6.0, 3.2), (0, 0, 2.6), 10, 3.0, color="#C9D8EA")
    # Dust in the window light: only the motes the sun reaches show.
    mote_m = principled("mote", "#FFFFFF", rough=0.7)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0)
    mote_me = bpy.context.active_object.data
    bpy.data.objects.remove(bpy.context.active_object, do_unlink=True)
    mote_me.materials.append(mote_m)
    A, B = Vector((-4.6, -6.2, 4.7)), Vector((0.2, -0.6, 2.7))
    for k in range(380):
        t = rnd.random()
        p0 = A.lerp(B, t) + Vector((rnd.uniform(-0.7, 0.7), rnd.uniform(-1.0, 1.0), rnd.uniform(-0.9, 0.9)))
        mo = link(bpy.data.objects.new(f"mote{k}", mote_me))
        mo.scale = (rnd.uniform(0.0012, 0.0028),) * 3
        v = Vector((rnd.uniform(-0.02, 0.02), rnd.uniform(-0.02, 0.02), rnd.uniform(-0.012, 0.004)))
        key(mo, 0, loc=p0)
        key(mo, N - 1, loc=p0 + v * (N / FPS))
        set_interp(mo, "LINEAR")
        mo.visible_shadow = False

    # --- the table and the phone -----------------------------------------------------
    stone = principled("stone", "#D9DEE3", rough=0.32, bump=(90, 0.015))
    noisy_color(stone, "#CCD2D8", "#E7EBEF", scale=9.0)
    tbl = cylinder("table_top", 0.34, 0.028, (0.2, -3.25, 0.74), stone, verts=96)
    cylinder("table_leg", 0.03, 0.72, (0.2, -3.25, 0.36), frame)
    cylinder("table_foot", 0.2, 0.02, (0.2, -3.25, 0.01), frame)
    scr_m = emit("screen", image=os.path.join(SCR, "marketPhone.png"))
    ph, scr = phone("phone", scr_m)
    # Leaning back 16 degrees in a small ink stand, screen to the camera (-Y).
    ph.location = (0.18, -3.30, 0.754 + PH / 2 * math.cos(rad(16)) + 0.004)
    ph.rotation_euler = (rad(90 - 16), 0, 0)
    stand = principled("stand", "#16202B", rough=0.4)
    box("stand", (0.09, 0.05, 0.016), (0.18, -3.29, 0.762), stand, bevel=0.004)
    ceramic = principled("cup", "#F2F4F6", rough=0.18, coat=0.5)
    cylinder("cup", 0.041, 0.085, (0.38, -3.16, 0.7965), ceramic, verts=64)
    coffee = principled("coffee", "#1A2633", rough=0.05)
    cylinder("coffee", 0.036, 0.0006, (0.38, -3.16, 0.8393), coffee, verts=64)
    # Ring on Hold my spot (x 890-1242, y 2666-2766 of the 1290 x 2796 capture)
    ring2 = emit("ring_phone", AZURE, alpha=0.0)
    c = on_screen((890 + 1242) / 2 / 1290, (2666 + 2766) / 2 / 2796, lift=0.00012)
    rh2 = empty("ring_phone_h", ph, c)
    ring("ring_phone", 352 * PH_PX + 0.0016, 100 * PH_PX + 0.0016, 52 * PH_PX + 0.0008, 0.0007, ring2, rh2)
    ring_in(rh2, ring2, F_RING2, 10)
    point("screen_glow", (0.18, -3.37, 0.86), 0.12, radius=0.06, color="#E8F0FA")

    # --- camera ----------------------------------------------------------------------
    hero = [board_to_world(*cell_xy(c, 0)) for c in range(NC)]
    phone_c = Vector(ph.location)
    seat = hero[sum(n for _, n in FIELDS[:3]) + 3]
    shots = [
        # frame, position, target, lens, f-stop, focus point
        (0, hero[0] + Vector((-0.04, -0.15, -0.014)), hero[1] + Vector((0, 0, -0.004)), 50, 1.8, hero[0]),
        (80, hero[2] + Vector((-0.035, -0.17, -0.018)), hero[3] + Vector((0, 0, -0.005)), 50, 1.8, hero[2]),
        (170, Vector((-0.9, -2.6, 2.0)), Vector((-0.35, 0.0, 2.85)), 30, 3.5, Vector((-0.4, 0, 2.85))),
        (250, Vector((-0.35, -4.9, 1.45)), Vector((-0.05, 0.0, 2.95)), 24, 5.0, Vector((0, 0, 2.8))),
        (322, seat + Vector((-0.42, -1.05, -0.40)), seat + Vector((0.06, 0, -0.015)), 42, 3.2, seat),
        (392, seat + Vector((-0.36, -0.98, -0.36)), seat + Vector((0.05, 0, -0.01)), 44, 3.2, seat),
        (455, phone_c + Vector((0.03, -0.68, 0.19)), phone_c + Vector((0, 0, 0.008)), 50, 2.8, phone_c),
        (515, phone_c + Vector((0.03, -0.63, 0.175)), phone_c + Vector((0, 0, 0.006)), 50, 2.8, phone_c),
    ]
    ease = [smoother, smoother, smooth, smoother, smooth, smoother, smooth]
    for f in range(N):
        i = max(k for k in range(len(shots) - 1) if shots[k][0] <= f) if f < shots[-1][0] else len(shots) - 2
        a, b = shots[i], shots[i + 1]
        t = ease[i](prog(f, a[0], b[0]))
        if i == 1:      # the pull back from the macro arcs outward instead of reversing through the board
            mid = Vector((-0.95, -1.2, 2.9))
            p = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * mid + t * t * b[1]
        elif i == 5:    # down from the board to the table, arcing out over it
            mid = Vector((0.6, -2.4, 2.1))
            p = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * mid + t * t * b[1]
        else:
            p = a[1].lerp(b[1], t)
        tg = a[2].lerp(b[2], t)
        cam.location = p
        look(cam, tg)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.lens = lerp(a[3], b[3], t)
        cam.data.keyframe_insert("lens", frame=f)
        cam.data.dof.aperture_fstop = lerp(a[4], b[4], t)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        cam.data.dof.focus_distance = (a[5].lerp(b[5], t) - p).length
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    set_interp(cam, "LINEAR")
    set_interp(cam.data, "LINEAR")
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data:
            set_interp(m.node_tree, "LINEAR")
    for ob in bpy.data.objects:
        if ob.name.startswith("ring"):
            set_interp(ob, "LINEAR")
    for ob in bpy.data.objects:
        if ob.type == "LIGHT" and ob.data.type != "SUN":
            ob.data.volume_factor = 0.0
    return sc


if __name__ == "__main__":
    a = args()
    sc = build()
    if a and a[0] == "still":
        render(sc, OUT.replace("3d", "stills"), stills=[int(x) for x in a[1:]])
    else:
        render(sc, OUT)
