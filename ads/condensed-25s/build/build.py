"""The 25 s ad's 3D layer, rendered headless in Blender 5.3 (EEVEE, Metal).

  Blender -b --factory-startup -P build.py -- stills 3.0,9.5,14 [--916]   (half-size checks)
  Blender -b --factory-startup -P build.py -- anim [first last] [--916]

30 s, 16:9 by default or 9:16 with --916. Writes ../render/v30_<fmt>/3d/####.png
(anim, frames 1-796; the end card covers the rest) or .../stills/t_<sec>.png.
Text, captions, wipes and the end card are not here: overlay.html draws them
frame by frame and compose.sh lays them over these frames.

0-7 s   the panic: a dark desk, Word itineraries landing, a phone buzzing under
        notifications, chat bubbles and a broken sheet piling up all at once,
        then everything pulled into the middle (the overlay's ring takes over).
7-26 s  a light stage, same world far off at X0: a laptop (the CRM) between two
        phones (the marketplace, the app). A hold flies from the marketplace
        into the CRM (listings, the WhatsApp inbox, trips), the plan flies from
        the CRM into the app (the plan, then the group's live map, whose
        travellers lift off the screen), then all three on one thread.
All screens are real captures (../screens, store/graphics/appstore screens_v2).
"""
import bmesh
import bpy
import math
import os
import random
import sys
from mathutils import Euler, Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
ROOT = os.path.normpath(os.path.join(AD, "../../.."))
SCR = os.path.join(AD, "screens")
CARDS = os.path.join(AD, "cards")
APP = os.path.join(ROOT, "store/graphics/appstore/build/screens_v2")
FPS = 30
LAST = 30 * FPS  # frames 1..900, t = (f - 1) / FPS
RENDER_END = 796  # 26.5 s: after that the end card covers the whole frame

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["stills", "3,10"]
MODE = argv[0]
FMT = "916" if "--916" in argv else "169"  # 16:9 (1920x1080) or 9:16 (1080x1920)
PORTRAIT = FMT == "916"
OUTDIR = os.path.join(AD, "render", f"v30_{FMT}")
argv = [a for a in argv if not a.startswith("--")]


def F(t):
    return int(round(t * FPS)) + 1


def lin(hex_):
    h = hex_.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def rad(v):
    return math.radians(v)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


# --- keyframes ---------------------------------------------------------------
# Blender 5 has no Action.fcurves; set the interpolation new keys get instead.

CUR = ["BEZIER"]


def interp(kind):
    """Interpolation for the keys inserted next (set on each key itself: the
    preference for new keys is not honoured in a headless run)."""
    CUR[0] = kind
    bpy.context.preferences.edit.keyframe_new_interpolation_type = kind


def fcurves_of(idd):
    ad = idd.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        return list(act.fcurves)
    except AttributeError:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(act, ad.action_slot)
        return list(cb.fcurves) if cb else []


def mark(target, prop, frame):
    if CUR[0] == "BEZIER":
        return
    path = target.path_from_id(prop)
    for fc in fcurves_of(target.id_data):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.01:
                    kp.interpolation = CUR[0]


def key(target, prop, t, value):
    setattr(target, prop, value)
    target.keyframe_insert(prop, frame=F(t))
    mark(target, prop, F(t))


def key_in(sock, t, value):
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=F(t))
    mark(sock, "default_value", F(t))


def hidden_until(ob, t):
    """Scale 0 from the start until t, held flat: a Bezier key at frame 1
    followed by a long gap overshoots below zero and shows the object early."""
    interp("CONSTANT")
    key(ob, "scale", 0, Vector((0.001,) * 3))
    interp("BEZIER")
    key(ob, "scale", t, Vector((0.001,) * 3))


# --- scene basics ------------------------------------------------------------

def link(ob, parent=None):
    bpy.context.scene.collection.objects.link(ob)
    if parent:
        ob.parent = parent
    return ob


def empty(name, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    ob = link(bpy.data.objects.new(name, None), parent)
    ob.location = loc
    ob.rotation_euler = rot
    return ob


def setin(node, names, value):
    for n in (names if isinstance(names, (list, tuple)) else [names]):
        if n in node.inputs:
            node.inputs[n].default_value = value
            return node.inputs[n]


def principled(m):
    return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")


def mat(name, color, metallic=0.0, rough=0.4, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = principled(m)
    setin(p, "Base Color", lin(color) if isinstance(color, str) else color)
    setin(p, "Metallic", metallic)
    setin(p, "Roughness", rough)
    setin(p, ["Coat Weight", "Coat"], coat)
    setin(p, "Coat Roughness", 0.05)
    return m


def image(path, cubic=True):
    img = bpy.data.images.load(path, check_existing=True)
    return img


def tex_node(nt, path, extension="CLIP"):
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = image(path)
    t.interpolation = "Cubic"
    t.extension = extension
    return t


def screen_mat(name, paths, coat=0.3, strength=1.0):
    """A screen: emission from one or more images, crossfaded by inputs the
    caller keys (returns the material and the mix factor sockets)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = principled(m)
    setin(p, "Base Color", (0, 0, 0, 1))
    setin(p, "Roughness", 0.35)
    setin(p, ["Specular IOR Level", "Specular"], 0.2)
    setin(p, ["Coat Weight", "Coat"], coat)
    setin(p, "Coat Roughness", 0.03)
    setin(p, "Emission Strength", strength)
    texs = [tex_node(nt, pth) for pth in paths]
    out = texs[0].outputs["Color"]
    facs = []
    for t in texs[1:]:
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.inputs["Factor"].default_value = 0.0
        nt.links.new(out, mix.inputs["A"])
        nt.links.new(t.outputs["Color"], mix.inputs["B"])
        out = mix.outputs["Result"]
        facs.append(mix.inputs["Factor"])
    nt.links.new(out, p.inputs["Emission Color"])
    return m, facs, texs


def card_mat(name, path, emit=1.0, lit=False):
    """A flat cut-out (PNG alpha). Emission for UI, lit paper otherwise.
    Returns the material and the socket that scales its brightness."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = principled(m)
    t = tex_node(nt, path)
    nt.links.new(t.outputs["Alpha"], p.inputs["Alpha"])
    gain = None
    if lit:
        nt.links.new(t.outputs["Color"], p.inputs["Base Color"])
        setin(p, "Roughness", 0.85)
    else:
        setin(p, "Base Color", (0, 0, 0, 1))
        setin(p, "Roughness", 0.6)
        nt.links.new(t.outputs["Color"], p.inputs["Emission Color"])
        gain = setin(p, "Emission Strength", emit)
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "DITHERED"
    return m, gain


def rr_pts(w, h, r, seg=10):
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
                       (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(seg + 1):
            a = rad(a0 + 90 * i / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def slab(name, w, h, r, d, front, side=None, back=None, bevel=0.0, parent=None, seg=10):
    """Rounded-rect prism, front face +Z, UVs over its bounds."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    pts = rr_pts(w, h, r, seg)
    top = [bm.verts.new((x, y, d / 2)) for x, y in pts]
    bot = [bm.verts.new((x, y, -d / 2)) for x, y in pts]
    ft = bm.faces.new(top)
    bm.faces.new(list(reversed(bot))).material_index = 2
    n = len(pts)
    for i in range(n):
        f = bm.faces.new([bot[i], bot[(i + 1) % n], top[(i + 1) % n], top[i]])
        f.material_index = 1
        f.smooth = True
    ft.material_index = 0
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for lp in f.loops:
            x, y, _ = lp.vert.co
            lp[uv].uv = (x / w + 0.5, y / h + 0.5)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    for m in (front, side or front, back or side or front):
        me.materials.append(m)
    ob = link(bpy.data.objects.new(name, me), parent)
    if bevel > 0:
        mod = ob.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
        mod.limit_method = "ANGLE"
        mod.angle_limit = rad(50)
        mod.harden_normals = True
    return ob


def plane(name, w, h, m, parent=None):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((x * w / 2, y * h / 2, 0)) for x, y in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new("UVMap")
    for lp, c in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        lp[uv].uv = c
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    ob = link(bpy.data.objects.new(name, me), parent)
    ob.visible_shadow = False
    return ob


def png_size(path):
    img = image(path)
    return img.size[0], img.size[1]


def area(name, loc, target, power, color="#FFFFFF", size=1.0, shape="SQUARE", size_y=None):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = power
    ld.color = lin(color)[:3]
    ld.shape = shape
    ld.size = size
    if size_y:
        ld.size_y = size_y
    if hasattr(ld, "use_shadow_jitter"):
        ld.use_shadow_jitter = True
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return ob


# --- render setup ------------------------------------------------------------

def setup():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue
    ee = sc.eevee
    ee.taa_render_samples = 32
    for attr, val in (("use_raytracing", True), ("use_shadows", True), ("shadow_ray_count", 2),
                      ("shadow_step_count", 8), ("use_gtao", True), ("fast_gi_method", "GLOBAL_ILLUMINATION")):
        if hasattr(ee, attr):
            try:
                setattr(ee, attr, val)
            except Exception:
                pass
    sc.render.resolution_x = 1080 if PORTRAIT else 1920
    sc.render.resolution_y = 1920 if PORTRAIT else 1080
    sc.render.fps = FPS
    sc.frame_start = 1
    sc.frame_end = LAST
    sc.render.use_motion_blur = True
    sc.render.motion_blur_shutter = 0.45
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.film_transparent = False

    w = bpy.data.worlds.new("world")
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    sc.world = w
    interp("CONSTANT")
    key_in(bg.inputs["Color"], 0, lin("#04070B"))
    key_in(bg.inputs["Strength"], 0, 1.0)
    key_in(bg.inputs["Color"], 7.0, lin("#E4ECF4"))
    key_in(bg.inputs["Strength"], 7.0, 0.55)
    interp("BEZIER")

    cam = bpy.data.cameras.new("cam")
    # the long side always spans 36 mm, so a lens means the same in both formats
    cam.sensor_fit = "VERTICAL" if PORTRAIT else "HORIZONTAL"
    cam.sensor_width = 36
    cam.sensor_height = 36
    cam.clip_start = 0.02
    cam.clip_end = 60
    cam.dof.use_dof = True
    cob = link(bpy.data.objects.new("cam", cam))
    sc.camera = cob
    return cob


def cam_basis(yaw, pitch, roll=0.0):
    """Camera rotation for a view along +Y turned by yaw (deg, + to the left)
    and tipped down by pitch. Returns the Euler and the right/up/forward."""
    e = Euler((rad(90 - pitch), rad(roll), rad(yaw)), "XYZ")
    m = e.to_matrix()
    return e, m.col[0], m.col[1], -m.col[2]


def tan_half(lens):
    """Half-angle tangents (horizontal, vertical) of the frame."""
    long_, short = 18.0 / lens, (18.0 * 9 / 16) / lens
    return (short, long_) if PORTRAIT else (long_, short)


def frame_on(target, yaw, pitch, dist, lens, sx=0.0, sy=0.0):
    """Camera location so `target` sits at normalised screen (sx, sy)."""
    e, r, u, f = cam_basis(yaw, pitch)
    th, tv = tan_half(lens)
    loc = Vector(target) - f * dist - r * (sx * dist * th) - u * (sy * dist * tv)
    return loc, e


# --- the panic ---------------------------------------------------------------

PANIC_CAM0 = (Vector((0.04, -0.60, 0.80)), Vector((0.0, 0.0, 0.02)))
PANIC_CAM1 = (Vector((0.0, -0.40, 0.52)), Vector((0.0, 0.02, 0.0)))
PANIC_LENS = 32


def panic_cam_at(t):
    k = ease(t / 7.0)
    loc = PANIC_CAM0[0].lerp(PANIC_CAM1[0], k)
    tgt = PANIC_CAM0[1].lerp(PANIC_CAM1[1], k)
    rot = (tgt - loc).to_track_quat("-Z", "Y").to_euler()
    return loc, rot


def shake(t, seed):
    s = sum(math.sin(t * f + seed * p) * a for f, p, a in ((13.1, 1.7, 0.5), (23.7, 2.9, 0.3), (7.3, 0.4, 0.6), (41.0, 5.1, 0.15)))
    return s


def build_panic(cam):
    random.seed(7)
    desk_m = bpy.data.materials.new("desk")
    desk_m.use_nodes = True
    nt = desk_m.node_tree
    p = principled(desk_m)
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 6.0
    if "Detail" in noise.inputs:
        noise.inputs["Detail"].default_value = 8.0
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.0, 14.0, 1.0)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], noise.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = lin("#0B0E12")
    ramp.color_ramp.elements[1].color = lin("#1C2128")
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
    setin(p, "Roughness", 0.62)
    desk = slab("desk", 4, 4, 0.05, 0.02, desk_m)
    desk.location.z = -0.01

    area("lamp", (-0.55, 0.30, 0.95), (0.0, 0.0, 0.0), 9, "#FFF1E2", size=0.55, shape="DISK")
    area("screen_glow", (0.55, 0.55, 0.32), (0.0, 0.0, 0.0), 4, "#7FB2FF", size=0.6)
    area("back_rim", (0.0, 1.1, 0.6), (0.0, 0.0, 0.0), 3, "#9CC2FF", size=1.0)

    # Word itineraries: two already down, more land as it gets worse.
    docs = [("doc02", -0.13, 0.06, 17, -1.0), ("doc04", 0.11, 0.10, -12, -1.0), ("doc01", -0.02, -0.02, 6, 0.9),
            ("doc03", 0.15, -0.05, -24, 2.3), ("doc01", -0.17, -0.07, 28, 3.7), ("doc02", 0.03, 0.13, -8, 5.0)]
    for i, (name, x, y, rz, t0) in enumerate(docs):
        m, _ = card_mat(f"m_{name}_{i}", os.path.join(CARDS, f"{name}.png"), lit=True)
        ob = plane(f"paper{i}", 0.21, 0.297, m)
        ob.visible_shadow = True
        z_rest = 0.0006 + i * 0.0005
        if t0 < 0:
            ob.location = (x, y, z_rest)
            ob.rotation_euler = (0, 0, rad(rz))
            continue
        interp("BEZIER")
        key(ob, "location", t0 - 0.02, Vector((x + 0.05, y + 0.12, 0.42)))
        key(ob, "rotation_euler", t0 - 0.02, Euler((rad(38), rad(-12), rad(rz + 30))))
        key(ob, "location", t0 + 0.32, Vector((x, y, z_rest + 0.004)))
        key(ob, "rotation_euler", t0 + 0.32, Euler((rad(2), rad(-1), rad(rz))))
        key(ob, "location", t0 + 0.46, Vector((x, y, z_rest)))
        key(ob, "rotation_euler", t0 + 0.46, Euler((0, 0, rad(rz))))

    # The phone face up on the desk, buzzing.
    ph = empty("desk_phone", (0.13, -0.17, 0.0068), (0, 0, rad(-22)))
    ph.scale = (1.5, 1.5, 1.5)
    glass = mat("p_glass", "#030406", rough=0.08, coat=1.0)
    frame = mat("p_frame", "#3E4A58", metallic=1.0, rough=0.25)
    slab("dp_body", 0.0745, 0.1565, 0.012, 0.008, glass, frame, frame, bevel=0.0015, parent=ph)
    lm, _, _ = screen_mat("dp_screen", [os.path.join(CARDS, "lockscreen.png")], strength=0.85)
    s = slab("dp_scr", 0.0695, 0.1505, 0.0098, 0.0003, lm, glass, glass, parent=ph)
    s.location.z = 0.0043

    # Chat bubbles, banners and the sheet: all at once, faster and faster.
    pool = ["bub02", "not01", "bub01", "bub03", "sheet", "bub04", "not04", "bub05", "bub06", "not03", "bub07",
            "bub08", "bub09", "not02", "bub10", "bub11", "bub12", "not05", "bub13", "bub14", "bub15", "not06",
            "bub16", "bub01", "bub05", "bub09", "not01", "bub03", "bub11", "bub13", "bub02", "not04", "bub07",
            "bub15", "bub06", "bub12"]
    n = len(pool)
    pre = 3
    times = [-0.5] * pre + [0.35 + 5.85 * ((i - pre) / (n - 1 - pre)) ** 0.7 for i in range(pre, n)]
    placed = []
    buzz = []
    sc = bpy.context.scene
    for i, (name, t0) in enumerate(zip(pool, times)):
        path = os.path.join(CARDS, f"{name}.png")
        pw, ph_ = png_size(path)
        loc_c, rot_c = panic_cam_at(max(t0, 0.0))
        cm = rot_c.to_matrix()
        r, u, f = cm.col[0], cm.col[1], -cm.col[2]
        th, tv = tan_half(PANIC_LENS)
        band = (-0.80, -0.40) if PORTRAIT else (-0.70, -0.30)
        for _ in range(60):
            d = random.uniform(0.24, 0.44)
            sx, sy = random.uniform(-0.88, 0.88), random.uniform(-0.82, 0.86)
            if i < n - 8 and band[0] < sy < band[1] and abs(sx) < 0.75:
                continue  # keep the caption's band clear until the end
            if all((sx - a) ** 2 + (sy - b) ** 2 > 0.34 ** 2 for a, b, tt in placed if t0 - tt < 2.2):
                break
        placed.append((sx, sy, t0))
        frac = 0.42 if name == "sheet" else (0.36 if name.startswith("not") else random.uniform(0.25, 0.32))
        if PORTRAIT:
            frac = min(0.86, frac * 2.1)  # a narrow frame: cards fill most of its width
        wm = frac * 2 * d * th
        hm = wm * ph_ / pw
        pos = loc_c + f * d + r * (sx * d * th) + u * (sy * d * tv)
        m, gain = card_mat(f"m_card{i}", path, emit=1.0)
        ob = plane(f"card{i}", wm, hm, m)
        tilt = Euler((rad(random.uniform(-9, 9)), rad(random.uniform(-9, 9)), rad(random.uniform(-6, 6))))
        ob.rotation_euler = (cm @ tilt.to_matrix()).to_euler()
        drift = r * random.uniform(-0.012, 0.012) + u * random.uniform(0.004, 0.016)
        interp("BEZIER")
        if t0 > 0:
            key(ob, "scale", t0 - 0.04, Vector((0.001, 0.001, 0.001)))
            key(ob, "location", t0 - 0.04, pos - f * 0.03)
            key(ob, "scale", t0 + 0.09, Vector((1.1, 1.1, 1.1)))
            key(ob, "scale", t0 + 0.17, Vector((1, 1, 1)))
            buzz.append(t0)
        key(ob, "location", max(t0, 0) + 0.12, pos)
        key(ob, "location", 6.30, pos + drift)
        # older messages sink back as new ones arrive
        key_in(gain, max(t0, 0) + 0.2, 1.0)
        key_in(gain, max(t0, 0) + 1.6, 0.62)
        # pulled into the middle for the ring
        loc6, rot6 = panic_cam_at(6.8)
        c = loc6 + (-rot6.to_matrix().col[2]) * 0.28
        lag = 0.12 * random.random()
        key(ob, "location", 6.36 + lag, pos + drift)
        key(ob, "scale", 6.36 + lag, Vector((1, 1, 1)))
        key(ob, "location", 6.78, c)
        key(ob, "scale", 6.78, Vector((0.001, 0.001, 0.001)))

    # camera: the slow push with a shake that grows, every frame keyed
    interp("LINEAR")
    for fr in range(1, F(7.0)):
        t = (fr - 1) / FPS
        loc, rot = panic_cam_at(t)
        amp = 0.0012 + 0.0075 * (t / 6.6) ** 2
        ramp_r = 0.15 + 1.2 * (t / 6.6) ** 2
        cam.location = loc + Vector((shake(t, 1) * amp, shake(t, 2) * amp * 0.6, shake(t, 3) * amp))
        cam.rotation_euler = Euler((rot.x + rad(shake(t, 4) * ramp_r * 0.5), rot.y + rad(shake(t, 6) * ramp_r),
                                    rot.z + rad(shake(t, 5) * ramp_r * 0.5)))
        cam.keyframe_insert("location", frame=fr)
        cam.keyframe_insert("rotation_euler", frame=fr)
        mark(cam, "location", fr)
        mark(cam, "rotation_euler", fr)
    # the phone jumps with each banner
    for t0 in buzz[::2]:
        for j, dz in enumerate((1.6, -1.4, 1.1, -0.6, 0.0)):
            ph.rotation_euler = (0, 0, rad(-22 + dz))
            ph.keyframe_insert("rotation_euler", frame=F(t0) + j)
    interp("BEZIER")
    return buzz


# --- the light stage -----------------------------------------------------------

X0 = 100.0
LAPTOP = Vector((X0, 0.06, 0.0))
LID_TILT = 15.0
PHONE_L = Vector((X0 - 0.33, -0.03, 0.165))
PHONE_R = Vector((X0 + 0.33, -0.03, 0.165))
PH_YAW = 21.0
PHONE_W, PHONE_H, PHONE_D = 0.105, 0.2205, 0.0085
SCR_W, SCR_H = 0.0985, 0.2135


def cyc():
    """Floor curving up into a wall, white with the light's own falloff."""
    bm = bmesh.new()
    prof = [(-5.0, 0.0), (1.2, 0.0)]
    for i in range(1, 13):
        a = rad(90 * i / 12)
        prof.append((1.2 + 0.9 * math.sin(a), 0.9 - 0.9 * math.cos(a)))
    prof.append((2.1, 4.0))
    rows = []
    for x in (-6.0, 6.0):
        rows.append([bm.verts.new((X0 + x, y, z)) for y, z in prof])
    for i in range(len(prof) - 1):
        bm.faces.new([rows[0][i], rows[0][i + 1], rows[1][i + 1], rows[1][i]])
    bm.normal_update()
    me = bpy.data.meshes.new("cyc")
    bm.to_mesh(me)
    bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    m = mat("cyc", "#F4F7FA", rough=0.95)
    setin(principled(m), ["Specular IOR Level", "Specular"], 0.05)
    me.materials.append(m)
    ob = link(bpy.data.objects.new("cyc", me))
    if ob.data.polygons[0].normal.z < 0:
        ob.data.flip_normals()
    return ob


def phone_model(name, root, screen_material):
    glass = mat(f"{name}_glass", "#05070A", rough=0.06, coat=1.0)
    frame = mat(f"{name}_frame", "#9AA6B4", metallic=1.0, rough=0.22)
    slab(f"{name}_body", PHONE_W, PHONE_H, 0.017, PHONE_D, glass, frame, frame, bevel=0.0016, parent=root)
    s = slab(f"{name}_scr", SCR_W, SCR_H, 0.0135, 0.0003, screen_material, glass, glass, parent=root)
    s.location.z = PHONE_D / 2 + 0.0002
    btn = mat(f"{name}_btn", "#8A96A4", metallic=1.0, rough=0.3)
    for side, y, h in ((-1, 0.055, 0.012), (-1, 0.03, 0.02), (-1, 0.005, 0.02), (1, 0.035, 0.03)):
        b = slab(f"{name}_b", 0.003, h, 0.0012, 0.004, btn, parent=root)
        b.location = (side * (PHONE_W / 2 + 0.0006), y, 0)
    return s


def live_map_pops(phone, path):
    """The live map's three travellers (real rows of the screen, cropped)
    lift off the sheet toward the camera, leave a dark slot, then settle."""
    SW, SH = 1290.0, 2796.0
    px = SCR_H / SH
    edge = mat("pop_edge", "#16222E", rough=0.5)
    rows = [((24, 1495, 1266, 1750), 0.034, -0.004, -9, -2.5, 20.75),
            ((24, 1765, 1266, 2020), 0.025, 0.002, -6, 1.0, 20.92),
            ((24, 2035, 1266, 2285), 0.017, 0.006, -3, 2.5, 21.09)]
    for k, ((x0, y0, x1, y1), lift, dx, ry, rz, tu) in enumerate(rows):
        m = bpy.data.materials.new(f"pop{k}")
        m.use_nodes = True
        nt = m.node_tree
        p = principled(m)
        setin(p, "Base Color", (0, 0, 0, 1))
        setin(p, ["Coat Weight", "Coat"], 0.25)
        setin(p, "Coat Roughness", 0.04)
        setin(p, "Emission Strength", 1.0)
        t = tex_node(nt, path)
        mp = nt.nodes.new("ShaderNodeMapping")
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp.inputs["Scale"].default_value = ((x1 - x0) / SW, (y1 - y0) / SH, 1.0)
        mp.inputs["Location"].default_value = (x0 / SW, 1 - y1 / SH, 0.0)
        nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
        nt.links.new(t.outputs["Color"], p.inputs["Emission Color"])
        w, h = (x1 - x0) * px, (y1 - y0) * px
        rest = Vector((((x0 + x1) / 2 / SW - 0.5) * SCR_W, (0.5 - (y0 + y1) / 2 / SH) * SCR_H, PHONE_D / 2 + 0.0010))
        card = slab(f"pop{k}", w, h, 50 * px, 0.0012, m, edge, edge, parent=phone)
        card.visible_shadow = False
        # the slot it leaves
        sm = bpy.data.materials.new(f"slot{k}")
        sm.use_nodes = True
        sp_ = principled(sm)
        setin(sp_, "Base Color", (0, 0, 0, 1))
        setin(sp_, ["Specular IOR Level", "Specular"], 0.0)
        alpha = setin(sp_, "Alpha", 0.0)
        if hasattr(sm, "surface_render_method"):
            sm.surface_render_method = "DITHERED"
        slot = plane(f"slot{k}", w * 0.98, h * 0.94, sm, parent=phone)
        slot.location = rest - Vector((0, 0, 0.0004))
        interp("BEZIER")
        up = rest + Vector((dx, 0.0, lift))
        tilt = Euler((rad(-4), rad(ry), rad(rz)))
        hidden_until(card, tu - 0.03)
        key(card, "location", tu - 0.03, rest)
        key(card, "rotation_euler", tu, Euler((0, 0, 0)))
        key(card, "scale", tu, Vector((1, 1, 1)))
        key(card, "location", tu, rest)
        key(card, "location", tu + 0.45, up)
        key(card, "rotation_euler", tu + 0.45, tilt)
        key(card, "scale", tu + 0.45, Vector((1.06, 1.06, 1.06)))
        key(card, "location", 23.2, up + Vector((0, 0.0015, 0.003)))
        key(card, "rotation_euler", 23.2, tilt)
        key(card, "scale", 23.2, Vector((1.06, 1.06, 1.06)))
        key(card, "location", 23.6, rest)
        key(card, "rotation_euler", 23.6, Euler((0, 0, 0)))
        key(card, "scale", 23.6, Vector((1, 1, 1)))
        key(card, "scale", 23.64, Vector((0.001,) * 3))
        key_in(alpha, tu, 0.0)
        key_in(alpha, tu + 0.4, 0.55)
        key_in(alpha, 23.25, 0.55)
        key_in(alpha, 23.6, 0.0)


def build_stage(cam):
    cyc()
    area("key", (X0 - 0.35, -0.85, 1.55), (X0, 0.05, 0.05), 80, "#FFFFFF", size=1.8)
    area("fill", (X0 + 1.2, -0.7, 0.6), (X0, 0.05, 0.12), 14, "#EAF3FF", size=1.2)
    area("rim", (X0 - 0.9, 0.9, 0.7), (X0, 0.0, 0.12), 18, "#D6E8FF", size=1.0)
    area("top", (X0, 0.4, 1.6), (X0, 0.1, 0.0), 22, "#FFFFFF", size=1.4)

    alu = mat("alu", "#C9CED5", metallic=1.0, rough=0.3)
    alu_dark = mat("alu_dark", "#AEB4BC", metallic=1.0, rough=0.42)
    black = mat("bezel", "#06080B", rough=0.1, coat=1.0)

    # laptop
    lap = empty("laptop", LAPTOP)
    base = slab("lap_base", 0.36, 0.25, 0.014, 0.011, alu, alu, alu, bevel=0.002, parent=lap)
    base.location.z = 0.0055
    kb = bpy.data.materials.new("keys")
    kb.use_nodes = True
    nt = kb.node_tree
    p = principled(kb)
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.0
    brick.inputs["Color1"].default_value = lin("#1C2026")
    brick.inputs["Color2"].default_value = lin("#22272E")
    brick.inputs["Mortar"].default_value = lin("#8E959E")
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = 0.012
    brick.inputs["Brick Width"].default_value = 0.0667
    brick.inputs["Row Height"].default_value = 0.1667
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["UV"], brick.inputs["Vector"])
    nt.links.new(brick.outputs["Color"], p.inputs["Base Color"])
    setin(p, "Roughness", 0.55)
    keys = slab("lap_keys", 0.29, 0.105, 0.004, 0.0012, kb, alu_dark, parent=lap)
    keys.location = (0, 0.045, 0.0112)
    pad = slab("lap_pad", 0.125, 0.078, 0.006, 0.0008, alu_dark, parent=lap)
    pad.location = (0, -0.073, 0.0112)
    hinge = empty("lap_hinge", (0, 0.122, 0.011), (rad(90 - LID_TILT), 0, 0), parent=lap)
    lid = slab("lap_lid", 0.36, 0.238, 0.014, 0.006, black, alu, alu, bevel=0.0015, parent=hinge)
    lid.location = (0, 0.119, 0.0)
    crm_paths = [os.path.join(SCR, f) for f in ("home.png", "listings.png", "inboxThread.png", "trips.png")]
    crm_m, crm_f, _ = screen_mat("crm_screen", crm_paths, coat=0.06)
    scr = slab("lap_scr", 0.334, 0.2088, 0.004, 0.0003, crm_m, black, black, parent=hinge)
    scr.location = (0, 0.122, 0.0032)

    # marketplace phone: the trip page scrolls; the price bar stays put
    pl = empty("phone_L", PHONE_L, (rad(90), 0, rad(PH_YAW)))
    mk_m = bpy.data.materials.new("market_screen")
    mk_m.use_nodes = True
    nt = mk_m.node_tree
    p = principled(mk_m)
    setin(p, "Base Color", (0, 0, 0, 1))
    setin(p, ["Coat Weight", "Coat"], 0.06)
    setin(p, "Emission Strength", 1.0)
    full = tex_node(nt, os.path.join(SCR, "marketPhoneFull.png"))
    mp = nt.nodes.new("ShaderNodeMapping")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], full.inputs["Vector"])
    nt.links.new(full.outputs["Color"], p.inputs["Emission Color"])
    page_h, view_h = 2726.0, 932.0
    mp.inputs["Scale"].default_value = (1.0, view_h / page_h, 1.0)

    def scroll(t, css):
        key_in(mp.inputs["Location"], t, Vector((0.0, 1 - (css + view_h) / page_h, 0.0)))

    scroll(0, 0)
    scroll(9.7, 0)
    scroll(10.7, 470)
    scroll(11.3, 470)
    scroll(12.1, 1560)
    phone_model("mk", pl, mk_m)
    bar_m, _ = card_mat("bar", os.path.join(SCR, "marketPhoneBar.png"), emit=1.0)
    bar_h = SCR_H * 162 / 2796
    bar = plane("mk_bar", SCR_W - 0.0006, bar_h, bar_m, parent=pl)
    bar.location = (0, -SCR_H / 2 + bar_h / 2 + 0.0004, PHONE_D / 2 + 0.0006)

    # app phone
    pr = empty("phone_R", PHONE_R, (rad(90), 0, rad(-PH_YAW)))
    app_paths = [os.path.join(APP, f) for f in ("home.png", "plan.png", "iceland/live_composited.png")]
    app_m, app_f, _ = screen_mat("app_screen", app_paths, coat=0.06)
    phone_model("ap", pr, app_m)
    live_map_pops(pr, os.path.join(APP, "iceland", "live_composited.png"))

    # screen changes (crossfades of 0.2 s)
    def swap(sock, t):
        key_in(sock, t, 0.0)
        key_in(sock, t + 0.2, 1.0)

    for sock in crm_f + app_f:
        key_in(sock, 0, 0.0)
    swap(crm_f[0], 12.55)   # home -> listings with the new hold
    swap(crm_f[1], 14.45)   # -> the WhatsApp thread, answered in the inbox
    swap(crm_f[2], 16.1)    # -> trips, each with its trip app
    swap(app_f[0], 17.7)    # home -> the plan arrives
    swap(app_f[1], 19.9)    # -> the group's live map

    # devices rise in after the logo, then hover
    interp("BEZIER")
    for ob, t0 in ((lap, 8.0), (pl, 8.15), (pr, 8.3)):
        home = ob.location.copy()
        hidden_until(ob, t0)
        key(ob, "location", t0, home + Vector((0, 0, -0.06)))
        key(ob, "scale", t0 + 0.42, Vector((1.03, 1.03, 1.03)))
        key(ob, "scale", t0 + 0.6, Vector((1, 1, 1)))
        key(ob, "location", t0 + 0.6, home)
        if ob is not lap:
            for k, t in enumerate((10.5, 13.5, 16.5, 19.5, 22.4, 25.4, 28.0)):
                key(ob, "location", t, home + Vector((0, 0, 0.005 * (1 if k % 2 else -1))))

    # what passes between them
    chips = []
    for name, src, dst, t0 in (("chipHold", PHONE_L, None, 12.0), ("chipPlan", None, PHONE_R, 17.2)):
        path = os.path.join(CARDS, f"{name}.png")
        pw, ph_ = png_size(path)
        m, _ = card_mat(f"m_{name}", path, emit=1.0)
        w = 0.12
        ob = plane(name, w, w * ph_ / pw, m)
        c = ob.constraints.new("TRACK_TO")
        c.target = cam
        c.track_axis = "TRACK_Z"
        c.up_axis = "UP_Y"
        lap_scr = LAPTOP + Vector((0, 0.17, 0.13))
        a = (src or lap_scr) + Vector((0.0, -0.06, 0.05))
        b = (dst or lap_scr) + Vector((0.0, -0.06, 0.04))
        mid = (a + b) / 2 + Vector((0, -0.12, 0.09))
        # pops up over its device and holds still to be read, then flies
        tp = t0 - 0.45
        hidden_until(ob, tp - 0.12)
        key(ob, "location", tp - 0.12, a - Vector((0, 0, 0.02)))
        key(ob, "scale", tp + 0.08, Vector((1.06, 1.06, 1.06)))
        key(ob, "scale", tp + 0.16, Vector((1, 1, 1)))
        key(ob, "location", tp + 0.1, a)
        key(ob, "location", t0, a)
        key(ob, "location", t0 + 0.3, mid)
        key(ob, "location", t0 + 0.58, b)
        key(ob, "scale", t0 + 0.58, Vector((1, 1, 1)))
        key(ob, "scale", t0 + 0.74, Vector((0.001,) * 3))
        chips.append((name, t0))

    # the thread through all three in the wide shot
    cu = bpy.data.curves.new("thread", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.0024
    cu.bevel_resolution = 4
    sp = cu.splines.new("BEZIER")
    pts = [PHONE_L + Vector((0.06, -0.01, 0.07)), LAPTOP + Vector((0, 0.10, 0.36)), PHONE_R + Vector((-0.06, -0.01, 0.07))]
    sp.bezier_points.add(len(pts) - 1)
    for bp, co in zip(sp.bezier_points, pts):
        bp.co = co
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    th_m = bpy.data.materials.new("thread")
    th_m.use_nodes = True
    pp = principled(th_m)
    setin(pp, "Base Color", (0, 0, 0, 1))
    setin(pp, "Roughness", 1.0)
    setin(pp, ["Specular IOR Level", "Specular"], 0.0)
    setin(pp, ["Emission Color", "Emission"], lin("#1E88D6"))
    setin(pp, "Emission Strength", 1.0)
    cu.materials.append(th_m)
    thread = link(bpy.data.objects.new("thread", cu))
    thread.visible_shadow = False
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=F(24.2))
    cu.bevel_factor_end = 1.0
    cu.keyframe_insert("bevel_factor_end", frame=F(25.0))
    for i, co in enumerate((pts[0], pts[2])):
        dm = mat(f"dot{i}", "#000000", rough=1.0)
        setin(principled(dm), ["Specular IOR Level", "Specular"], 0.0)
        setin(principled(dm), ["Emission Color", "Emission"], lin("#1E88D6"))
        setin(principled(dm), "Emission Strength", 1.0)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0055, location=co, segments=24, ring_count=12)
        d = bpy.context.active_object
        d.data.materials.append(dm)
        hidden_until(d, 24.15 + i * 0.8)
        key(d, "scale", 24.3 + i * 0.8, Vector((1, 1, 1)))
    return lap, pl, pr


# --- camera on the stage -------------------------------------------------------

def stage_camera(cam):
    camd = cam.data
    lap_scr = LAPTOP + Vector((0, 0.17, 0.125))
    wide_t = Vector((X0, 0.04, 0.14))
    map_t = PHONE_R + Vector((0, 0, -0.02))  # the map and the travellers, not the header
    if PORTRAIT:
        # devices sit low in the tall frame, under the overlay's line of text
        shots = {
            "logo": frame_on(wide_t, 0, 9, 2.55, 50),
            "wide0": frame_on(wide_t, 0, 9, 2.4, 50),
            "market": frame_on(PHONE_L, PH_YAW - 5, 5, 0.50, 50, sy=-0.20),
            "market2": frame_on(PHONE_L, PH_YAW - 2, 6, 0.47, 50, sy=-0.20),
            "crm": frame_on(lap_scr, 2, 16, 0.98, 50, sy=-0.12),
            "crm2": frame_on(lap_scr, 0, 17, 0.94, 50, sy=-0.12),
            "app": frame_on(PHONE_R, -PH_YAW + 5, 5, 0.50, 50, sy=-0.20),
            "app2": frame_on(PHONE_R, -PH_YAW + 2, 6, 0.47, 50, sy=-0.20),
            "appmap": frame_on(map_t, -PH_YAW + 3, 3, 0.47, 50, sy=-0.27),
            "appmap2": frame_on(map_t, -PH_YAW + 1, 3, 0.45, 50, sy=-0.27),
            "wide": frame_on(wide_t, -24, 14, 2.0, 50, sy=-0.10),
            "wide2": frame_on(wide_t, -21, 14, 1.9, 50, sy=-0.10),
        }
    else:
        shots = {
            "logo": frame_on(wide_t, 0, 9, 1.42, 50),
            "wide0": frame_on(wide_t, 0, 9, 1.34, 50),
            "market": frame_on(PHONE_L, PH_YAW - 7, 5, 0.70, 50, sx=0.30, sy=0.02),
            "market2": frame_on(PHONE_L, PH_YAW - 3, 6, 0.66, 50, sx=0.30, sy=0.02),
            "crm": frame_on(lap_scr, 4, 13, 0.88, 50, sx=0.20, sy=0.08),
            "crm2": frame_on(lap_scr, 1, 14, 0.84, 50, sx=0.20, sy=0.08),
            "app": frame_on(PHONE_R, -PH_YAW + 7, 5, 0.70, 50, sx=-0.30, sy=0.02),
            "app2": frame_on(PHONE_R, -PH_YAW + 3, 6, 0.66, 50, sx=-0.30, sy=0.02),
            "appmap": frame_on(map_t, -PH_YAW + 4, 3, 0.43, 50, sx=-0.26),
            "appmap2": frame_on(map_t, -PH_YAW + 2, 3, 0.41, 50, sx=-0.26),
            "wide": frame_on(wide_t + Vector((0, 0, 0.01)), 0, 10, 1.22, 50, sy=-0.12),
            "wide2": frame_on(wide_t + Vector((0, 0, 0.01)), 0, 10, 1.16, 50, sy=-0.12),
        }
    plan = [(7.0, "logo"), (8.55, "wide0"), (9.25, "market"), (12.0, "market2"), (12.7, "crm"),
            (17.2, "crm2"), (17.9, "app"), (19.85, "app2"), (20.55, "appmap"), (23.35, "appmap2"),
            (24.1, "wide"), (26.5, "wide2")]
    interp("CONSTANT")
    key(camd, "lens", 0, PANIC_LENS)
    key(camd, "lens", 7.0, 50)
    interp("BEZIER")
    for t, name in plan:
        loc, e = shots[name]
        key(cam, "location", t, loc)
        key(cam, "rotation_euler", t, e)
    # focus: the cards in the panic, then each subject; deeper on the map
    dof = camd.dof
    interp("CONSTANT")
    key(dof, "aperture_fstop", 0, 6.3)
    key(dof, "aperture_fstop", 7.0, 4.0)
    interp("BEZIER")
    key(dof, "aperture_fstop", 20.2, 4.0)
    key(dof, "aperture_fstop", 20.55, 7.1)
    key(dof, "aperture_fstop", 23.35, 7.1)
    key(dof, "aperture_fstop", 24.1, 4.0)
    for t, d in ((0, 0.40), (3.5, 0.36), (6.9, 0.30)):
        key(dof, "focus_distance", t, d)
    interp("CONSTANT")
    key(dof, "focus_distance", 7.0, (shots["logo"][0] - wide_t).length)
    interp("BEZIER")
    focus = {"wide0": wide_t, "market": PHONE_L, "market2": PHONE_L, "crm": lap_scr, "crm2": lap_scr,
             "app": PHONE_R, "app2": PHONE_R, "appmap": map_t, "appmap2": map_t, "wide": wide_t, "wide2": wide_t}
    for t, name in plan[1:]:
        key(dof, "focus_distance", t, (shots[name][0] - focus[name]).length - (0.02 if "map" in name else 0.0))


def main():
    cam = setup()
    build_panic(cam)
    build_stage(cam)
    stage_camera(cam)
    sc = bpy.context.scene
    if MODE == "stills":
        out = os.path.join(OUTDIR, "stills")
        os.makedirs(out, exist_ok=True)
        sc.render.resolution_percentage = 50
        sc.eevee.taa_render_samples = 24
        for t in (float(x) for x in argv[1].split(",")):
            sc.frame_set(F(t))
            sc.render.filepath = os.path.join(out, f"t_{t:05.2f}.png")
            bpy.ops.render.render(write_still=True)
            print("STILL", sc.render.filepath)
    else:
        first, last = (int(argv[1]), int(argv[2])) if len(argv) > 2 else (1, RENDER_END)
        sc.frame_start, sc.frame_end = first, last
        sc.render.filepath = os.path.join(OUTDIR, "3d", "")
        if "--save" in argv:
            bpy.ops.wm.save_as_mainfile(filepath=os.path.join(AD, "render", "ad25.blend"))
        bpy.ops.render.render(animation=True)


main()
