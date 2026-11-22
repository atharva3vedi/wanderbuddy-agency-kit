"""Shared pieces for the app-only 25 s ad, run inside Blender 5.3 (Cycles, Metal).

World: X right, Y up, Z toward the camera. 1 unit = 1000 output px on the
z = 0 plane (the camera sits D units back with a 50 mm lens on a 24 mm
vertical sensor). The phone model and its screen-space maths come from
store/graphics/appstore/build/pop/scene.py, with the Windows paths removed.
App screens are pure emission so their colours come out exactly as the app
draws them (Standard view transform).
"""
import bmesh
import bpy
import json
import math
import os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
ROOT = os.path.normpath(os.path.join(AD, "../../.."))
SCR = os.path.join(AD, "screens")
FONTS = os.path.join(ROOT, "metrics/fonts")
BOLD = os.path.join(FONTS, "WbSans-Bold.ttf")
SEMI = os.path.join(FONTS, "WbSans-SemiBold.ttf")
REG = os.path.join(FONTS, "WbSans-Regular.ttf")
SERIF = os.path.join(FONTS, "InstrumentSerif-Italic.ttf")
TL_PATH = os.environ.get("WB_TL") or os.path.join(HERE, "timeline.json")
TL = json.load(open(TL_PATH if os.path.isabs(TL_PATH) else os.path.join(HERE, TL_PATH), encoding="utf-8"))
FPS, W, H = TL["fps"], TL["w"], TL["h"]
PX = 0.001
# 16:9 uses a 50 mm lens; 9:16 widens it so the camera stays 2.25 units back.
LENS, SENSOR = float(TL.get("lens", 50.0)), 24.0
D = (H / 1000) * LENS / SENSOR

# Brand Codex Rev 03 (metrics/brand-codex.html) and lib/theme/app_colors.dart.
INK = "#0C1622"
AZURE = "#1E88D6"
FIELD = "#2072B8"      # the mark's tile and the end card's brand blue
PAGE = "#F3F6F9"
D_SURFACE = "#17293B"
D_INK = "#E7F1FA"
D_INK2 = "#C5D7E6"
D_MUTED = "#8DA7BC"


# --- maths -------------------------------------------------------------------

def clamp(t, a=0.0, b=1.0):
    return max(a, min(b, t))


def prog(f, f0, f1):
    return clamp((f - f0) / float(f1 - f0)) if f1 != f0 else float(f >= f1)


def out_cubic(t):
    return 1 - (1 - t) ** 3


def in_cubic(t):
    return t ** 3


def in_out(t):
    return t * t * (3 - 2 * t)


def out_expo(t):
    return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)


def out_back(t, s=1.4):
    t -= 1
    return t * t * ((s + 1) * t + s) + 1


def lerp(a, b, t):
    return a + (b - a) * t


def rad(v):
    return math.radians(v)


def lin(hex_):
    h = hex_.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1.0,)


# --- scene -------------------------------------------------------------------

def link(ob, parent=None):
    bpy.context.scene.collection.objects.link(ob)
    if parent is not None:
        ob.parent = parent
    return ob


def empty(name, parent=None, loc=(0, 0, 0)):
    ob = link(bpy.data.objects.new(name, None), parent)
    ob.location = loc
    return ob


def new_scene(frames, samples=64, transparent=True, world="#F3F6F9", world_strength=1.0, mblur=False):
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = d.type == "METAL"
    sc.cycles.device = "GPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.008
    sc.cycles.use_denoising = False
    sc.cycles.max_bounces = 6
    sc.cycles.transparent_max_bounces = 16
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.filter_width = 1.2
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.resolution_percentage = 100
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 0, frames - 1
    sc.render.film_transparent = transparent
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0
    sc.view_settings.gamma = 1
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    sc.render.image_settings.color_depth = "8"
    sc.render.use_motion_blur = mblur
    sc.render.motion_blur_shutter = 0.45
    w = bpy.data.worlds.new("world")
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = lin(world)
    bg.inputs["Strength"].default_value = world_strength
    sc.world = w
    cam = bpy.data.cameras.new("cam")
    cam.lens = LENS
    cam.sensor_fit = "VERTICAL"
    cam.sensor_height = SENSOR
    cam.sensor_width = SENSOR * W / H
    cam.clip_start = 0.01
    cam.clip_end = 60
    cob = link(bpy.data.objects.new("cam", cam))
    cob.location = (0, 0, D)
    sc.camera = cob
    return sc, cob


def overlay(cam_ob, dist=None):
    """An empty on the camera where 1 unit = 1000 output px, centre = frame centre."""
    d = D if dist is None else dist
    ov = empty("overlay", cam_ob, (0, 0, -d))
    ov.scale = (d / D,) * 3
    return ov


def key_transform(ob, f, loc=None, rot=None, scale=None):
    if loc is not None:
        ob.location = loc
        ob.keyframe_insert("location", frame=f)
    if rot is not None:
        ob.rotation_euler = rot
        ob.keyframe_insert("rotation_euler", frame=f)
    if scale is not None:
        ob.scale = scale if isinstance(scale, (tuple, list)) else (scale,) * 3
        ob.keyframe_insert("scale", frame=f)


def linear_keys(ob):
    ad = ob.animation_data
    if ad and ad.action:
        for fc in getattr(ad.action, "fcurves", []):
            for k in fc.keyframe_points:
                k.interpolation = "LINEAR"


# --- materials ---------------------------------------------------------------

def _clean(m):
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    return nt, next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")


def emit(name, color, alpha=1.0, strength=1.0, image=None):
    """Flat colour (or image) as emission, with a keyable alpha.

    Returns the material; mat["fade"] is the Mix node whose Fac is the alpha.
    """
    m = bpy.data.materials.new(name)
    nt, out = _clean(m)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.name = "fade"
    mix.inputs[0].default_value = alpha
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(image, check_existing=True)
        tex.interpolation = "Cubic"
        tex.extension = "EXTEND"
        nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    else:
        em.inputs["Color"].default_value = lin(color)
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return m


def key_alpha(m, f, a):
    s = m.node_tree.nodes["fade"].inputs[0]
    s.default_value = a
    s.keyframe_insert("default_value", frame=f)


def solid(name, color, metallic=0.0, rough=0.35, coat=0.0, coat_rough=0.05):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")

    def put(names, v):
        for n in names if isinstance(names, (list, tuple)) else [names]:
            if n in p.inputs:
                p.inputs[n].default_value = v
                return
    put("Base Color", lin(color))
    put("Metallic", metallic)
    put("Roughness", rough)
    put(["Coat Weight", "Coat"], coat)
    put("Coat Roughness", coat_rough)
    return m


# --- geometry ----------------------------------------------------------------

def rr_pts(w, h, r, seg=12):
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
                       (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(seg + 1):
            a = rad(a0 + 90 * i / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def slab(name, w, h, r, d, front, side=None, back=None, bevel=0.0, parent=None, seg=12):
    """Rounded-rect prism, front face +Z with UVs over its bounds."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    pts = rr_pts(w, h, r, seg)
    top = [bm.verts.new((x, y, d / 2)) for x, y in pts]
    bot = [bm.verts.new((x, y, -d / 2)) for x, y in pts]
    ft = bm.faces.new(top)
    fb = bm.faces.new(list(reversed(bot)))
    n = len(pts)
    sides = [bm.faces.new([bot[i], bot[(i + 1) % n], top[(i + 1) % n], top[i]]) for i in range(n)]
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for lp in f.loops:
            x, y, _ = lp.vert.co
            lp[uv].uv = (x / w + 0.5, y / h + 0.5)
    ft.material_index = 0
    fb.material_index = 2
    for f in sides:
        f.material_index = 1
        f.smooth = True
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    for m in (front, side or front, back or side or front):
        me.materials.append(m)
    ob = link(bpy.data.objects.new(name, me), parent)
    if bevel > 0:
        mod = ob.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 4
        mod.limit_method = "ANGLE"
        mod.angle_limit = rad(50)
        mod.harden_normals = True
    return ob


def plane(name, w, h, m, parent=None):
    return slab(name, w, h, 0.0001, 0.00001, m, parent=parent, seg=1)


def ring(name, w, h, r, stroke, m, parent=None):
    """A flat rounded-rect outline (the codex's one azure ring)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    o = rr_pts(w + stroke, h + stroke, r + stroke / 2, 16)
    i = rr_pts(w - stroke, h - stroke, max(r - stroke / 2, 0.0001), 16)
    vo = [bm.verts.new((x, y, 0)) for x, y in o]
    vi = [bm.verts.new((x, y, 0)) for x, y in i]
    n = len(vo)
    for k in range(n):
        bm.faces.new([vi[k], vi[(k + 1) % n], vo[(k + 1) % n], vo[k]])
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    return link(bpy.data.objects.new(name, me), parent)


def disc(name, r, m, parent=None, segs=64):
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=segs, radius=r)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    return link(bpy.data.objects.new(name, me), parent)


_fonts = {}


def font(path):
    if path not in _fonts:
        _fonts[path] = bpy.data.fonts.load(path, check_existing=True)
    return _fonts[path]


def text(name, body, path, size, m, parent=None, align="LEFT", space_line=1.0):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.font = font(path)
    cu.size = size
    cu.align_x = align
    cu.align_y = "BOTTOM_BASELINE"
    cu.space_line = space_line
    cu.resolution_u = 10
    ob = link(bpy.data.objects.new(name, cu), parent)
    ob.data.materials.append(m)
    return ob


def local_bounds(ob):
    bpy.context.view_layer.update()
    bb = [Vector(c) for c in ob.bound_box]
    return (min(v.x for v in bb), min(v.y for v in bb), max(v.x for v in bb), max(v.y for v in bb))


def text_width(ob):
    x0, _, x1, _ = local_bounds(ob)
    return x1 - x0


# --- SVG (the real logo files, never redrawn) --------------------------------

def _bounds(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(p.x for p in pts), min(p.y for p in pts), max(p.x for p in pts), max(p.y for p in pts))


def svg(path, parent, ref, rect):
    """Import an SVG and map its reference shape's bounds onto rect=(x0,y0,x1,y1).

    ref: "largest" (the mark's tile) or "magenta" (a helper rect added to the
    file, deleted after measuring). Returns (objects, group empty).
    """
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    bpy.context.view_layer.update()
    area_of = lambda o: (_bounds(o)[2] - _bounds(o)[0]) * (_bounds(o)[3] - _bounds(o)[1])
    if ref == "largest":
        r = max(new, key=area_of)
    else:
        def is_magenta(o):
            for sl in o.material_slots:
                if sl.material and tuple(round(c, 2) for c in sl.material.diffuse_color[:3]) == (1.0, 0.0, 1.0):
                    return True
            return False
        r = next(o for o in new if is_magenta(o))
    x0, y0, x1, y1 = _bounds(r)
    X0, Y0, X1, Y1 = rect
    k = (X1 - X0) / (x1 - x0)
    g = empty("svg_" + os.path.basename(path), parent)
    g.scale = (k, k, k)
    g.location = (X0 - x0 * k, Y0 - y0 * k, 0)
    for o in new:
        mw = o.matrix_world.copy()
        for c in list(o.users_collection):
            c.objects.unlink(o)
        bpy.context.scene.collection.objects.link(o)
        o.parent = g
        o.matrix_parent_inverse.identity()
        o.matrix_basis = mw
        if o.type == "CURVE":
            o.data.resolution_u = 24
            o.data.fill_mode = "BOTH"
    if ref != "largest":
        new = [o for o in new if o != r]
        bpy.data.objects.remove(r, do_unlink=True)
    return new, g


def set_mat(o, m):
    o.data.materials.clear()
    o.data.materials.append(m)


def mark(parent, size, tile=True, z_step=0.0006):
    """The mark (screens/mark-tile.svg = website/partials/brand-mark.html), centred, size px square.

    Returns (tile, peaks, wave, group). With tile=False the tile is removed.
    """
    s = size * PX
    objs, g = svg(os.path.join(SCR, "mark-tile.svg"), parent, "largest", (-s / 2, -s / 2, s / 2, s / 2))
    bpy.context.view_layer.update()
    objs.sort(key=lambda o: -(_bounds(o)[2] - _bounds(o)[0]) * (_bounds(o)[3] - _bounds(o)[1]))
    t = objs[0]
    p, w = sorted(objs[1:], key=lambda o: -(_bounds(o)[1] + _bounds(o)[3]))
    k = g.scale.x
    p.location.z += z_step / k
    w.location.z += 2 * z_step / k
    if not tile:
        bpy.data.objects.remove(t, do_unlink=True)
        t = None
    return t, p, w, g


def word(parent, mark_size, left_x, mid_y=0.0, mat=None):
    """The wordmark at the place and size of screens/word.svg (website/partials/brand-word.html).

    Sized like brand.css: the word's box is 0.656 of the mark, centred on it.
    The SVG is the WbSans Bold outline; Blender's curve fill leaves pin-holes
    in a few of its glyphs, so the SVG only sets the bounds and the word is
    set in WbSans Bold itself, fitted to them. Returns ([text], group, box width).
    """
    src = open(os.path.join(SCR, "word.svg"), encoding="utf-8").read()
    tmp = os.path.join(bpy.app.tempdir or "/tmp", "wb_word_ref.svg")
    src = src.replace("</svg>", '<rect x="40" y="6" width="134" height="21" fill="#ff00ff"/></svg>')
    open(tmp, "w", encoding="utf-8").write(src)
    hh = 0.656 * mark_size * PX
    ww = hh * 134 / 21
    glyphs, g = svg(tmp, parent, "magenta", (left_x, mid_y - hh / 2, left_x + ww, mid_y + hh / 2))
    bpy.context.view_layer.update()
    inv = parent.matrix_world.inverted()
    pts = [inv @ (o.matrix_world @ Vector(c)) for o in glyphs for c in o.bound_box]
    tx0, ty0 = min(p.x for p in pts), min(p.y for p in pts)
    tx1 = max(p.x for p in pts)
    for o in glyphs:
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.objects.remove(g, do_unlink=True)
    wg = empty("word", parent)
    t = text("wordmark", "WanderBuddy", BOLD, 1.0, mat or emit("word", INK), wg)
    t.data.resolution_u = 16
    x0, y0, x1, y1 = local_bounds(t)
    k = (tx1 - tx0) / (x1 - x0)
    t.scale = (k, k, k)
    t.location = (tx0 - x0 * k, ty0 - y0 * k, 0)
    return [t], wg, ww


# --- the phone (after store/graphics/appstore/build/pop/scene.py) -----------

BEZ, BODY_R, BODY_D = 40, 200, 95
SCREEN_Z = BODY_D / 2 * PX + 0.0006


def phone(name, screen_mat, parent=None):
    root = empty(name, parent)
    glass = solid(name + "_glass", "#030406", rough=0.08, coat=1.0, coat_rough=0.02)
    frame = solid(name + "_frame", "#56657A", metallic=1.0, rough=0.24)
    PW, PH = (1290 + 2 * BEZ) * PX, (2796 + 2 * BEZ) * PX
    slab(name + "_body", PW, PH, BODY_R * PX, BODY_D * PX, glass, frame, frame, bevel=0.016, parent=root)
    scr = slab(name + "_screen", 1290 * PX, 2796 * PX, 165 * PX, 0.0004, screen_mat, glass, glass, parent=root)
    scr.location.z = SCREEN_Z
    btn = solid(name + "_btn", "#4B596C", metallic=1.0, rough=0.3)
    for side, y, h in ((-1, 0.86, 0.11), (-1, 0.58, 0.19), (-1, 0.33, 0.19), (1, 0.52, 0.30)):
        b = slab(name + "_b", 0.03, h, 0.012, 0.045, btn, btn, btn, parent=root)
        b.location = (side * (PW / 2 + 0.004), y, 0)
    return root


def on_screen(fx, fy, lift=0.0008):
    """A point on the phone's screen from fractions of the screen image (top-left origin)."""
    return Vector(((fx - 0.5) * 1290 * PX, (0.5 - fy) * 2796 * PX, SCREEN_Z + lift))


def shadow_wall(z=-0.45):
    m = solid("wall", "#808080")
    w = slab("wall", 40, 40, 0.1, 0.001, m)
    w.location = (0, 0, z)
    w.is_shadow_catcher = True
    return w


def area(name, loc, target, power, size, color="#FFFFFF"):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = power
    ld.size = size
    ld.color = lin(color)[:3]
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return ob


def shadow_decal(name, parent, w, h, loc, opacity=0.3, color="#0C1622"):
    """A soft drop shadow from screens/shadow.png (no sampling noise).

    w, h are the size of the object casting it; the texture's core is 400x940
    of its 700x1240 canvas, so the plane is scaled up to keep the falloff.
    """
    m = bpy.data.materials.new(name)
    nt, out = _clean(m)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(os.path.join(SCR, "shadow.png"), check_existing=True)
    tex.image.colorspace_settings.name = "Non-Color"
    tex.extension = "CLIP"
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.name = "fade"
    mul.inputs[1].default_value = opacity
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = lin(color)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Color"], mul.inputs[0])
    nt.links.new(mul.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    ob = plane(name, w * 700 / 400, h * 1240 / 940, m, parent)
    ob.location = loc
    ob.visible_shadow = False
    return ob


def crop_slab(name, image, rect, r, depth, side, parent=None):
    """A card cut from a screen image: rect = (x0, y0, x1, y1) fractions, top-left origin.

    Sized in the phone's own units (1290 x 2796 screen px), UVs remapped to the crop.
    """
    x0, y0, x1, y1 = rect
    w, h = (x1 - x0) * 1290 * PX, (y1 - y0) * 2796 * PX
    m = emit(name, None, image=image)
    ob = slab(name, w, h, r, depth, m, side, side, parent=parent)
    uv = ob.data.uv_layers[0]
    for lp in ob.data.loops:
        u, v = uv.data[lp.index].uv
        uv.data[lp.index].uv = (x0 + u * (x1 - x0), (1 - y1) + v * (y1 - y0))
    return ob, w, h
