"""Film 4, Day 2: the trip app travellers join, as a shanshui hanging scroll.

  Blender -b --factory-startup -P build/day2.py -- land|phone [still f f ...]

land: a karst seascape in blue-hour mist (Phang Nga Bay, Krabi), read top to
bottom like a hanging scroll: peaks, mist, water, seven longtail lights in a
line coming back from the islands. Frames 0..359.
phone: the same evening on a boat bench. The camera starts inside the photo
of the app's trip card (screens/app-home.png: Krabi Islands, Small Group,
Day 2 of 5, 7 people) and pulls back to the phone; the ring lands on the card,
then the screen turns to the group chat (screens/app-chat.png) and the ring
lands on Mai's reminder: Phi Phi pickup 07:30. Frames 330..515.
The real card says "Evening" and Mai wrote at 7:15 PM, so this is dusk, not dawn.
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
LAND_END, PHONE_START = 360, 330
F_RING1, F_SWAP, F_RING2 = 392, 432, 452
CARD = (40, 640, 1040, 1292)            # in app-home.png (1080 x 2341)
BUBBLE = (172, 1360, 790, 1655)         # Mai's reminder in app-chat.png


def tower(name, x, y, h, r, rnd, rock, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=28, radius=1.0, location=(x, y, h * 0.42))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (r, r * rnd.uniform(0.7, 1.0), h * 0.58)
    ob.rotation_euler = (rnd.uniform(-0.05, 0.05), rnd.uniform(-0.05, 0.05), rnd.uniform(0, 6.28))
    sub = ob.modifiers.new("sub", "SUBSURF")
    sub.levels = sub.render_levels = 1
    tex = bpy.data.textures.new(name + "_t", "CLOUDS")
    tex.noise_scale = rnd.uniform(0.35, 0.6)
    tex.noise_depth = 4
    d = ob.modifiers.new("disp", "DISPLACE")
    d.texture = tex
    d.texture_coords = "LOCAL"
    d.strength = rnd.uniform(0.35, 0.55)
    d.mid_level = 0.5
    tex2 = bpy.data.textures.new(name + "_t2", "CLOUDS")
    tex2.noise_scale = 0.12
    d2 = ob.modifiers.new("disp2", "DISPLACE")
    d2.texture = tex2
    d2.texture_coords = "LOCAL"
    d2.strength = 0.1
    ob.modifiers["sub"].levels = ob.modifiers["sub"].render_levels = 2
    ob.data.materials.append(rock)
    bpy.ops.object.shade_smooth()
    return ob


def rock_material():
    m = principled("rock", "#2A383A", rough=0.9)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Normal"], sep.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.08
    nz.inputs["Detail"].default_value = 6
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs[1].default_value, mr.inputs[2].default_value = 0.15, 0.55
    nt.links.new(sep.outputs[2], mr.inputs[0])
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    nt.links.new(mr.outputs[0], add.inputs[0])
    sub = nt.nodes.new("ShaderNodeMath")
    sub.operation = "SUBTRACT"
    nt.links.new(nz.outputs["Fac"], sub.inputs[0])
    sub.inputs[1].default_value = 0.5
    nt.links.new(sub.outputs[0], add.inputs[1])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs[6].default_value = lin("#3A4646")   # wet limestone
    mix.inputs[7].default_value = lin("#1D3129")   # the jungle on top
    cl = nt.nodes.new("ShaderNodeClamp")
    nt.links.new(add.outputs[0], cl.inputs[0])
    nt.links.new(cl.outputs[0], mix.inputs[0])
    nt.links.new(mix.outputs[2], p.inputs["Base Color"])
    return m


def mist(sc):
    """Fog thick on the water, thinning to clear air by 170 m, in banks."""
    m = bpy.data.materials.new("mist")
    nt, out = (None, None)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    vs = nt.nodes.new("ShaderNodeVolumePrincipled")
    vs.inputs["Color"].default_value = lin("#CFDCEA")
    vs.inputs["Anisotropy"].default_value = 0.35
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs[1].default_value, mr.inputs[2].default_value = 0.0, 170.0
    mr.inputs[3].default_value, mr.inputs[4].default_value = 1.0, 0.0
    nt.links.new(sep.outputs[2], mr.inputs[0])
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "POWER"
    nt.links.new(mr.outputs[0], pw.inputs[0])
    pw.inputs[1].default_value = 2.2
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.006
    nz.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], nz.inputs["Vector"])
    bank = nt.nodes.new("ShaderNodeMapRange")
    bank.inputs[1].default_value, bank.inputs[2].default_value = 0.35, 0.7
    bank.inputs[3].default_value, bank.inputs[4].default_value = 0.35, 1.6
    nt.links.new(nz.outputs["Fac"], bank.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMath")
    m1.operation = "MULTIPLY"
    nt.links.new(pw.outputs[0], m1.inputs[0])
    nt.links.new(bank.outputs[0], m1.inputs[1])
    m2 = nt.nodes.new("ShaderNodeMath")
    m2.operation = "MULTIPLY"
    nt.links.new(m1.outputs[0], m2.inputs[0])
    m2.inputs[1].default_value = 0.0016
    nt.links.new(m2.outputs[0], vs.inputs["Density"])
    nt.links.new(vs.outputs[0], out.inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.active_object
    ob.name = "mist"
    ob.scale = (9000, 9000, 420)
    ob.location = (0, 2500, 205)
    ob.data.materials.append(m)
    ob.visible_shadow = False
    return ob


def water_material(name="water"):
    m = principled(name, "#13303A", rough=0.1, spec=0.6)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    wv = nt.nodes.new("ShaderNodeTexWave")
    wv.wave_type = "BANDS"
    wv.inputs["Scale"].default_value = 0.6
    wv.inputs["Distortion"].default_value = 6.0
    wv.inputs["Detail"].default_value = 4.0
    wv.name = "wave"
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.3
    nt.links.new(wv.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], p.inputs["Normal"])
    return m


def build_land():
    sc, cam = new_scene(LAND_END, engine="EEVEE", samples=64, world="#C9D9E8", world_strength=0.8, shutter=0.5)
    cam.data.clip_start, cam.data.clip_end = 0.5, 6000
    sc.eevee.volumetric_end = 2600
    sc.eevee.volumetric_start = 0.5
    sc.eevee.volumetric_tile_size = "8"
    sc.eevee.volumetric_sample_distribution = 0.9
    # the sky: paper white at the horizon, deepening blue overhead (no sunset colour)
    nt = sc.world.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.5
    cr.color_ramp.elements[0].color = lin("#DCE6EE")
    cr.color_ramp.elements[1].position = 0.78
    cr.color_ramp.elements[1].color = lin("#4D7299")
    nt.links.new(sep.outputs[2], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], bg.inputs["Color"])

    water = water_material()
    box("sea", (16000, 16000, 1), (0, 4000, -0.5), water)
    rock = rock_material()
    rnd = random.Random(21)
    # Towers: a near one on the left (the card's cliff), a ring of middle ones, ranks fading out.
    tower("hero", -14, -45, 125, 24, rnd, rock)
    spots = [(150, 120, 150, 40), (-180, 260, 185, 46), (40, 420, 205, 52), (260, 380, 140, 40),
             (-60, 600, 240, 62), (-330, 520, 170, 44), (330, 700, 230, 58), (120, 900, 200, 60),
             (-260, 980, 260, 70), (460, 1100, 210, 66), (-520, 1250, 240, 70), (60, 1400, 300, 85),
             (600, 1500, 220, 70), (-700, 1650, 280, 80), (300, 1850, 260, 80), (-200, 2100, 320, 95),
             (800, 2200, 250, 80), (-900, 2300, 300, 90), (220, 160, 70, 22), (-120, 180, 60, 18),
             (420, 260, 95, 28), (-420, 380, 120, 34), (520, 560, 150, 40), (-560, 760, 140, 40)]
    for k, (x, y, h, r) in enumerate(spots):
        tower(f"t{k}", x, y, h, r * 0.62, rnd, rock)
    if os.environ.get("WB_NOMIST") != "1":
        mist(sc)
    # no sun: blue hour after it has set, the light all from the sky, as in an ink wash

    # Seven longtails coming home in a line, each with a white lamp and a wake.
    hull_m = principled("hull", "#1C2A30", rough=0.6)
    lamp_m = emit("boatlamp", "#F4F8FF", strength=40.0)
    wake_m = bpy.data.materials.new("wake")
    wake_m.use_nodes = True
    wn = wake_m.node_tree
    for n in list(wn.nodes):
        if n.type != "OUTPUT_MATERIAL":
            wn.nodes.remove(n)
    wout = next(n for n in wn.nodes if n.type == "OUTPUT_MATERIAL")
    wtc = wn.nodes.new("ShaderNodeTexCoord")
    wsep = wn.nodes.new("ShaderNodeSeparateXYZ")
    wn.links.new(wtc.outputs["UV"], wsep.inputs[0])
    ramp = wn.nodes.new("ShaderNodeMath")
    ramp.operation = "POWER"
    wn.links.new(wsep.outputs[1], ramp.inputs[0])
    ramp.inputs[1].default_value = 2.5
    edge = wn.nodes.new("ShaderNodeMath")
    edge.operation = "PINGPONG"
    wn.links.new(wsep.outputs[0], edge.inputs[0])
    edge.inputs[1].default_value = 0.5
    em2 = wn.nodes.new("ShaderNodeMath")
    em2.operation = "MULTIPLY"
    wn.links.new(ramp.outputs[0], em2.inputs[0])
    wn.links.new(edge.outputs[0], em2.inputs[1])
    em3 = wn.nodes.new("ShaderNodeMath")
    em3.operation = "MULTIPLY"
    wn.links.new(em2.outputs[0], em3.inputs[0])
    em3.inputs[1].default_value = 1.4
    emw = wn.nodes.new("ShaderNodeEmission")
    emw.inputs["Color"].default_value = lin("#E8F0F7")
    emw.inputs["Strength"].default_value = 0.22
    trw = wn.nodes.new("ShaderNodeBsdfTransparent")
    mx = wn.nodes.new("ShaderNodeMixShader")
    wn.links.new(em3.outputs[0], mx.inputs[0])
    wn.links.new(trw.outputs[0], mx.inputs[1])
    wn.links.new(emw.outputs[0], mx.inputs[2])
    wn.links.new(mx.outputs[0], wout.inputs["Surface"])
    wake_m.surface_render_method = "BLENDED"
    boats = []
    for k in range(7):
        root = empty(f"boat{k}")
        hull = box(f"hull{k}", (1.7, 10.0, 0.9), (0, 0, 0.25), hull_m, parent=root)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        tp = hull.modifiers.new("taper", "SIMPLE_DEFORM")
        tp.deform_method = "TAPER"
        tp.deform_axis = "Y"
        tp.factor = -0.6
        box(f"roof{k}", (1.5, 3.0, 0.08), (0, -0.5, 1.55), hull_m, parent=root)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, location=(0, 4.2, 1.2))
        lp = bpy.context.active_object
        lp.data.materials.append(lamp_m)
        lp.parent = root
        pl = point(f"boatlight{k}", (0, 4.2, 1.6), 2500, radius=0.4, color="#EEF4FF")
        pl.parent = root
        wk = plane(f"wake{k}", 4.0, 55.0, wake_m, root)
        wk.location = (0, -32.0, 0.06)
        wk.visible_shadow = False
        boats.append(root)

    # camera: the scroll read from the top down
    shots = [
        (0, Vector((30, -470, 205)), Vector((0, 500, 215)), 55, 8.0),
        (150, Vector((22, -430, 120)), Vector((10, 400, 60)), 50, 8.0),
        (280, Vector((6, -330, 24)), Vector((30, 80, 6)), 45, 8.0),
        (LAND_END - 1, Vector((4, -305, 21)), Vector((26, 60, 10)), 45, 8.0),
    ]
    for f in range(LAND_END):
        i = max(k for k in range(len(shots) - 1) if shots[k][0] <= f) if f < shots[-1][0] else len(shots) - 2
        a, b = shots[i], shots[i + 1]
        tt = smooth(prog(f, a[0], b[0])) if i < 2 else smoother(prog(f, a[0], b[0]))
        cam.location = a[1].lerp(b[1], tt)
        look(cam, a[2].lerp(b[2], tt))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.lens = lerp(a[3], b[3], tt)
        cam.data.keyframe_insert("lens", frame=f)
        cam.data.dof.aperture_fstop = 8.0
        cam.data.dof.focus_distance = 350
        # the boats: a line heading right to left across the bay, home to the beach
        for k, bt in enumerate(boats):
            # a line receding up the frame into the mist, coming home toward the camera
            y = -95 + 52 * k - 5.5 * f / FPS
            x = 34 + 0.16 * (y + 95) + 1.5 * math.sin(f / 30 + k)
            bt.location = (x, y, 0.0)
            bt.rotation_euler = (math.sin(f / 9 + k) * 0.02, math.sin(f / 7 + k * 2) * 0.03, rad(180 + 9))
            bt.keyframe_insert("location", frame=f)
            bt.keyframe_insert("rotation_euler", frame=f)
        wv = water.node_tree.nodes["wave"]
        key_val(wv.inputs["Phase Offset"], f, f * 0.05)
    all_linear()
    return sc


def build_phone():
    n = N - PHONE_START
    sc, cam = new_scene(n, engine="EEVEE", samples=64, world="#7E9DBB", world_strength=0.8, shutter=0.5)
    # the boat's bench: teal paint worn back to grey wood
    paint = principled("bench", "#2C6E70", rough=0.7, bump=(30, 0.06, 8))
    noisy_color(paint, "#2B5F63", "#4F7F7E", scale=14.0, ramp=(0.42, 0.7))
    for k in range(3):
        box(f"plank{k}", (0.9, 0.145, 0.03), (0, -0.155 + 0.155 * k, -0.015), paint, bevel=0.004)
    sea = water_material("sea_near")
    box("sea", (60, 60, 0.1), (0, 8, -0.9), sea)
    lamp_m = emit("far_lamps", "#F4F8FF", strength=30.0)
    for k in range(7):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(-2.2 + 0.85 * k, 6.0 + 0.6 * k, -0.6))
        bpy.context.active_object.data.materials.append(lamp_m)
    # the phone, its screen turning from the trip card to the group chat
    m = bpy.data.materials.new("screen")
    m.use_nodes = True
    nt = m.node_tree
    for nd in list(nt.nodes):
        if nd.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(nd)
    out = next(nd for nd in nt.nodes if nd.type == "OUTPUT_MATERIAL")
    t1 = nt.nodes.new("ShaderNodeTexImage")
    t1.image = bpy.data.images.load(os.path.join(SCR, "app-home.png"))
    t2 = nt.nodes.new("ShaderNodeTexImage")
    t2.image = bpy.data.images.load(os.path.join(SCR, "app-chat.png"))
    for t in (t1, t2):
        t.interpolation = "Cubic"
        t.extension = "EXTEND"
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = "RGBA"
    mx.name = "swap"
    nt.links.new(t1.outputs["Color"], mx.inputs[6])
    nt.links.new(t2.outputs["Color"], mx.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(mx.outputs[2], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    ph, scr = phone("phone", m)
    ph.location = (0.0, 0.0, 0.0039)
    ph.rotation_euler = (0, 0, rad(-8))
    # the app screens are 1080 x 2341; on_screen() takes fractions, so pixels / that size
    def fx(px):
        return px / 1080

    def fy(py):
        return py / 2341
    rings = []
    for nm, (x0, y0, x1, y1), r_px, fin in (("card", CARD, 64, F_RING1), ("bubble", BUBBLE, 46, F_RING2)):
        rm = emit("ring_" + nm, AZURE, alpha=0.0)
        c = on_screen(fx((x0 + x1) / 2), fy((y0 + y1) / 2), lift=0.00012)
        rh = empty("ringh_" + nm, ph, c)
        k = PW / 1080
        ring("ring_" + nm, (x1 - x0) * k + 0.0014, (y1 - y0) * k + 0.0014, r_px * k + 0.0007, 0.00075, rm, rh)
        rings.append((rm, rh, fin - PHONE_START))
    s = sun("sky", (0, 0, 0), 1.0, angle=8, color="#CFDDEC")
    d = Vector((-0.3, 0.7, -0.6)).normalized()
    s.rotation_euler = (-d).to_track_quat("Z", "Y").to_euler()
    area("fill", (0.6, -0.8, 0.9), (0, 0, 0), 30, 1.0, color="#B8CCE0")

    bpy.context.view_layer.update()
    mw = ph.matrix_world
    card_c = mw @ on_screen(fx(560), fy(905))
    whole = mw @ on_screen(0.5, 0.5)
    card_mid = mw @ on_screen(fx(540), fy(966))
    bub = mw @ on_screen(fx((BUBBLE[0] + BUBBLE[2]) / 2), fy((BUBBLE[1] + BUBBLE[3]) / 2))
    up = Vector((0, 0, 1))
    shots = [
        (0, card_c + up * 0.045 + Vector((0, -0.004, 0)), card_c, 50, 4.0),
        (60, whole + Vector((0.0, -0.29, 0.60)), whole + Vector((0, 0.013, 0)), 50, 4.0),
        (100, whole + Vector((0.0, -0.28, 0.58)), whole + Vector((0, 0.012, 0)), 50, 4.0),
        (128, bub + Vector((0.0, -0.09, 0.2)), bub + Vector((0, 0.008, 0)), 50, 3.5),
        (n - 1, bub + Vector((0.0, -0.085, 0.188)), bub + Vector((0, 0.008, 0)), 50, 3.5),
    ]
    for f in range(n):
        i = max(k for k in range(len(shots) - 1) if shots[k][0] <= f) if f < shots[-1][0] else len(shots) - 2
        a, b = shots[i], shots[i + 1]
        tt = smoother(prog(f, a[0], b[0]))
        cam.location = a[1].lerp(b[1], tt)
        tgt = a[2].lerp(b[2], tt)
        look(cam, tgt)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.lens = 50
        cam.data.dof.aperture_fstop = lerp(a[4], b[4], tt)
        cam.data.dof.focus_distance = (tgt - cam.location).length
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        key_val(nt.nodes["swap"].inputs[0], f, smooth(prog(f, F_SWAP - PHONE_START, F_SWAP - PHONE_START + 8)))
    for rm, rh, fin in rings:
        ring_in(rh, rm, fin, 10)
    fade_card = rings[0][0]
    for f in range(F_SWAP - PHONE_START - 6, F_SWAP - PHONE_START + 2):
        fade_mat(fade_card, f, 1 - prog(f, F_SWAP - PHONE_START - 6, F_SWAP - PHONE_START))
    all_linear()
    return sc


if __name__ == "__main__":
    a = args()
    part = a[0]
    sc = build_land() if part == "land" else build_phone()
    out = os.path.join(AD, "render", "day2", part)
    if len(a) > 1 and a[1] == "still":
        render(sc, out + "_stills", stills=[int(x) for x in a[2:]])
    else:
        render(sc, out)
