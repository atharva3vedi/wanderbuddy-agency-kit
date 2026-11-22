"""Shared pieces for the four B2B films, run inside Blender 5.3.

Units are metres. 1080 x 1920 at 24 fps. Materials, the phone and the
mark/wordmark import come from ../app-25s/build/wb.py (copied as wb_ref.py),
rewritten without its timeline file. Screens are pure emission so the app's
colours come out as the app draws them (Standard view transform).
"""
import bmesh
import bpy
import math
import os
import sys
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
W, H, FPS = 1080, 1920, 24

INK = "#0C1622"
AZURE = "#1E88D6"
FIELD = "#2072B8"
PAGE = "#F3F6F9"
TEAL = "#1BA89A"

QUICK = os.environ.get("WB_QUICK") == "1"


# --- maths -------------------------------------------------------------------

def clamp(t, a=0.0, b=1.0):
    return max(a, min(b, t))


def prog(f, f0, f1):
    return clamp((f - f0) / float(f1 - f0)) if f1 != f0 else float(f >= f1)


def smooth(t):
    return t * t * (3 - 2 * t)


def smoother(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def out_cubic(t):
    return 1 - (1 - t) ** 3


def in_cubic(t):
    return t ** 3


def out_expo(t):
    return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def vlerp(a, b, t):
    return Vector(a).lerp(Vector(b), t)


def rad(v):
    return math.radians(v)


def lin(hex_):
    h = hex_.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1.0,)


def sec(s):
    return int(round(s * FPS))


def args():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


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


def new_scene(frames, engine="EEVEE", samples=64, world="#000000", world_strength=0.0,
              transparent=False, mblur=True, shutter=0.5):
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    sc = bpy.context.scene
    if engine == "CYCLES":
        sc.render.engine = "CYCLES"
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type == "METAL"
        sc.cycles.device = "GPU"
        sc.cycles.samples = max(8, samples // (4 if QUICK else 1))
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.adaptive_threshold = 0.02
        sc.cycles.use_denoising = True
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
        sc.cycles.denoising_use_gpu = True
        sc.cycles.max_bounces = 6
        sc.cycles.caustics_reflective = False
        sc.cycles.caustics_refractive = False
    else:
        sc.render.engine = "BLENDER_EEVEE"
        ee = sc.eevee
        ee.taa_render_samples = max(8, samples // (4 if QUICK else 1))
        ee.use_raytracing = True
        ee.ray_tracing_method = "SCREEN"
        ee.ray_tracing_options.resolution_scale = "1"
        ee.ray_tracing_options.use_denoise = True
        ee.use_shadows = True
        ee.shadow_ray_count = 2
        ee.shadow_step_count = 8
        ee.shadow_resolution_scale = 1.0
        ee.use_volumetric_shadows = True
        ee.volumetric_tile_size = "4"
        ee.volumetric_samples = 96
        ee.volumetric_shadow_samples = 32
        ee.volumetric_light_clamp = 0.0
        ee.use_fast_gi = True
        ee.fast_gi_method = "GLOBAL_ILLUMINATION"
        ee.fast_gi_quality = 0.5
        ee.bokeh_max_size = 300
        ee.motion_blur_steps = 2
        ee.use_overscan = True
        ee.overscan_size = 3.0
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.resolution_percentage = 50 if QUICK else 100
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 0, frames - 1
    sc.render.film_transparent = transparent
    try:
        sc.view_settings.view_transform = "Standard"
    except TypeError:
        pass
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0
    sc.view_settings.gamma = 1
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    sc.render.image_settings.color_depth = "8"
    sc.render.use_motion_blur = mblur
    sc.render.motion_blur_shutter = shutter
    w = bpy.data.worlds.new("world")
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = lin(world)
    bg.inputs["Strength"].default_value = world_strength
    sc.world = w
    cam = bpy.data.cameras.new("cam")
    cam.sensor_fit = "VERTICAL"
    cam.sensor_height = 24.0
    cam.sensor_width = 24.0 * W / H
    cam.lens = 50
    cam.clip_start = 0.005
    cam.clip_end = 400
    cam.dof.use_dof = True
    cam.dof.aperture_fstop = 2.8
    cam.dof.aperture_blades = 7
    cob = link(bpy.data.objects.new("cam", cam))
    sc.camera = cob
    return sc, cob


def look(ob, target, roll=0.0):
    d = Vector(target) - ob.location
    q = d.to_track_quat("-Z", "Y")
    e = q.to_euler()
    if roll:
        from mathutils import Matrix
        e = (q.to_matrix() @ Matrix.Rotation(rad(roll), 3, "Z")).to_euler()
    ob.rotation_euler = e


def world_volume(sc, density=0.02, color="#FFFFFF", anisotropy=0.4):
    nt = sc.world.node_tree
    vs = nt.nodes.new("ShaderNodeVolumePrincipled")
    vs.inputs["Density"].default_value = density
    vs.inputs["Color"].default_value = lin(color)
    vs.inputs["Anisotropy"].default_value = anisotropy
    out = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
    nt.links.new(vs.outputs[0], out.inputs["Volume"])
    return vs


def fog_box(name, size, loc, density, color="#FFFFFF", anisotropy=0.5, falloff=None):
    """A box of fog. falloff=(z0, z1) thins it with height (z1 clear)."""
    m = bpy.data.materials.new(name)
    nt, out = _clean(m)
    vs = nt.nodes.new("ShaderNodeVolumePrincipled")
    vs.inputs["Color"].default_value = lin(color)
    vs.inputs["Anisotropy"].default_value = anisotropy
    if falloff:
        tc = nt.nodes.new("ShaderNodeNewGeometry")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs[1].default_value = falloff[0]
        mr.inputs[2].default_value = falloff[1]
        mr.inputs[3].default_value = density
        mr.inputs[4].default_value = 0.0
        nt.links.new(tc.outputs["Position"], sep.inputs[0])
        nt.links.new(sep.outputs[2], mr.inputs[0])
        nt.links.new(mr.outputs[0], vs.inputs["Density"])
    else:
        vs.inputs["Density"].default_value = density
    nt.links.new(vs.outputs[0], out.inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    ob.location = loc
    ob.data.materials.append(m)
    ob.visible_shadow = False
    return ob


# --- keys --------------------------------------------------------------------

def _fcurves(idb):
    ad = idb.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(act, ad.action_slot)
        return list(cb.fcurves) if cb else []
    except Exception:
        return list(getattr(act, "fcurves", []))


def set_interp(idb, kind="LINEAR"):
    for fc in _fcurves(idb):
        for k in fc.keyframe_points:
            k.interpolation = kind


def all_linear():
    for coll in (bpy.data.objects, bpy.data.cameras, bpy.data.lights, bpy.data.materials):
        for idb in coll:
            set_interp(idb, "LINEAR")
            nt = getattr(idb, "node_tree", None)
            if nt is not None:
                set_interp(nt, "LINEAR")
    for w in bpy.data.worlds:
        if w.node_tree:
            set_interp(w.node_tree, "LINEAR")


def key(ob, f, loc=None, rot=None, scale=None):
    if loc is not None:
        ob.location = loc
        ob.keyframe_insert("location", frame=f)
    if rot is not None:
        ob.rotation_euler = rot
        ob.keyframe_insert("rotation_euler", frame=f)
    if scale is not None:
        ob.scale = scale if isinstance(scale, (tuple, list, Vector)) else (scale,) * 3
        ob.keyframe_insert("scale", frame=f)


def key_val(sock, f, v):
    sock.default_value = v
    sock.keyframe_insert("default_value", frame=f)


# --- materials ---------------------------------------------------------------

def _clean(m):
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    return nt, next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")


def emit(name, color="#FFFFFF", strength=1.0, image=None, alpha=1.0, extension="EXTEND"):
    """Flat colour or image as emission; mat.node_tree.nodes['fade'].inputs[0] is the alpha."""
    m = bpy.data.materials.new(name)
    nt, out = _clean(m)
    em = nt.nodes.new("ShaderNodeEmission")
    em.name = "em"
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.name = "fade"
    mix.inputs[0].default_value = alpha
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.name = "tex"
        tex.image = bpy.data.images.load(image, check_existing=True)
        tex.interpolation = "Cubic"
        tex.extension = extension
        nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    else:
        em.inputs["Color"].default_value = lin(color)
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    m.surface_render_method = "BLENDED" if alpha < 1 else "DITHERED"
    return m


def fade_mat(m, f, a):
    key_val(m.node_tree.nodes["fade"].inputs[0], f, a)


def principled(name, color, rough=0.5, metallic=0.0, spec=0.5, coat=0.0, coat_rough=0.05,
               image=None, sss=0.0, transmission=0.0, ior=1.45, bump=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")

    def put(names, v):
        for n in names if isinstance(names, (list, tuple)) else [names]:
            if n in p.inputs:
                p.inputs[n].default_value = v
                return
    put("Base Color", lin(color))
    put("Metallic", metallic)
    put("Roughness", rough)
    put(["Specular IOR Level", "Specular"], spec)
    put(["Coat Weight", "Coat"], coat)
    put("Coat Roughness", coat_rough)
    put(["Subsurface Weight", "Subsurface"], sss)
    put(["Transmission Weight", "Transmission"], transmission)
    put("IOR", ior)
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(image, check_existing=True)
        tex.interpolation = "Cubic"
        tex.extension = "EXTEND"
        nt.links.new(tex.outputs["Color"], p.inputs["Base Color"])
    if bump:
        # bump = (scale, strength, detail): a fine noise for paper, plaster, concrete
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = bump[0]
        nz.inputs["Detail"].default_value = bump[2] if len(bump) > 2 else 8
        bp = nt.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump[1]
        bp.inputs["Distance"].default_value = 0.002
        nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], p.inputs["Normal"])
    return m


def noisy_color(m, c0, c1, scale=4.0, detail=6, ramp=(0.35, 0.75)):
    """Swap a principled material's base colour for a noise blend of two colours."""
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = detail
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = ramp[0]
    cr.color_ramp.elements[0].color = lin(c0)
    cr.color_ramp.elements[1].position = ramp[1]
    cr.color_ramp.elements[1].color = lin(c1)
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], p.inputs["Base Color"])
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
    """Rounded-rect prism, front face +Z, UVs over its bounds."""
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
        mod.segments = 3
        mod.limit_method = "ANGLE"
        mod.angle_limit = rad(50)
        mod.harden_normals = True
    return ob


def box(name, size, loc, m, parent=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    ob.location = loc
    ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    if bevel:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        mod = ob.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return ob


def plane(name, w, h, m, parent=None):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0)) for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new("UVMap")
    for lp in f.loops:
        x, y, _ = lp.vert.co
        lp[uv].uv = (x / w + 0.5, y / h + 0.5)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    return link(bpy.data.objects.new(name, me), parent)


def cylinder(name, r, depth, loc, m, verts=48, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    if parent:
        ob.parent = parent
    return ob


def ring(name, w, h, r, stroke, m, parent=None):
    """A flat rounded-rect outline: the codex's one azure ring."""
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


def ring_in(holder, m, f_in, dur=10):
    """The ring settles from 107 % with a fade, as in the earlier ads."""
    for f in range(f_in - 1, f_in + dur + 2):
        t = out_cubic(prog(f, f_in, f_in + dur))
        key(holder, f, scale=lerp(1.07, 1.0, t))
        fade_mat(m, f, t)


_fonts = {}


def font(path):
    if path not in _fonts:
        _fonts[path] = bpy.data.fonts.load(path, check_existing=True)
    return _fonts[path]


def text(name, body, path, size, m, parent=None, align="LEFT", extrude=0.0):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.font = font(path)
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.extrude = extrude
    cu.resolution_u = 8
    ob = link(bpy.data.objects.new(name, cu), parent)
    ob.data.materials.append(m)
    return ob


def bounds_local(ob):
    bpy.context.view_layer.update()
    bb = [Vector(c) for c in ob.bound_box]
    return (min(v.x for v in bb), min(v.y for v in bb), max(v.x for v in bb), max(v.y for v in bb))


# --- lights ------------------------------------------------------------------

def area(name, loc, target, power, size, color="#FFFFFF", shape="SQUARE", size_y=None, spread=180):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = power
    ld.shape = shape
    ld.size = size
    if size_y is not None:
        ld.size_y = size_y
    ld.color = lin(color)[:3]
    ld.spread = rad(spread)
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    look(ob, target)
    return ob


def spot(name, loc, target, power, angle=30, blend=0.3, radius=0.05, color="#FFFFFF"):
    ld = bpy.data.lights.new(name, "SPOT")
    ld.energy = power
    ld.spot_size = rad(angle)
    ld.spot_blend = blend
    ld.shadow_soft_size = radius
    ld.color = lin(color)[:3]
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    look(ob, target)
    return ob


def sun(name, rot, power, angle=0.5, color="#FFFFFF"):
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy = power
    ld.angle = rad(angle)
    ld.color = lin(color)[:3]
    ob = link(bpy.data.objects.new(name, ld))
    ob.rotation_euler = [rad(v) for v in rot]
    return ob


def point(name, loc, power, radius=0.02, color="#FFFFFF"):
    ld = bpy.data.lights.new(name, "POINT")
    ld.energy = power
    ld.shadow_soft_size = radius
    ld.color = lin(color)[:3]
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    return ob


# --- the phone (after app-25s/build/wb.py) -------------------------------------

PH_PX = 0.0000545          # metres per screen px: a 1290 px wide screen is 70 mm
PW, PH = 1290 * PH_PX, 2796 * PH_PX


def phone(name, screen_mat, parent=None, frame_color="#3E4A5A"):
    """A 71.6 x 155 mm phone lying in its local XY plane, screen facing +Z."""
    root = empty(name, parent)
    glass = principled(name + "_glass", "#020304", rough=0.06, coat=1.0, coat_rough=0.02)
    frame = principled(name + "_frame", frame_color, metallic=1.0, rough=0.28)
    bez = 40 * PH_PX
    body = slab(name + "_body", PW + 2 * bez, PH + 2 * bez, 200 * PH_PX, 0.0078, glass, frame, frame,
                bevel=0.0009, parent=root)
    scr = slab(name + "_screen", PW, PH, 165 * PH_PX, 0.00002, screen_mat, glass, glass, parent=root)
    scr.location.z = 0.0039 + 0.00003
    btn = principled(name + "_btn", "#3A4554", metallic=1.0, rough=0.3)
    for side, y, h in ((-1, 0.86, 0.11), (-1, 0.58, 0.19), (-1, 0.33, 0.19), (1, 0.52, 0.30)):
        b = slab(name + "_b", 0.0017, h * 0.0545, 0.0007, 0.0026, btn, btn, btn, parent=root)
        b.location = (side * ((PW + 2 * bez) / 2 + 0.0002), y * 0.0545, 0)
    return root, scr


def on_screen(fx, fy, lift=0.00005):
    """A point on the phone's screen from fractions of a 1290 x 2796 screen image."""
    return Vector(((fx - 0.5) * PW, (0.5 - fy) * PH, 0.0039 + lift))


def screen_uv(ob, rect):
    """Remap a plane's UVs to show rect=(x0,y0,x1,y1) (fractions, top-left origin) of its image."""
    x0, y0, x1, y1 = rect
    uv = ob.data.uv_layers[0]
    for lp in ob.data.loops:
        u, v = uv.data[lp.index].uv
        uv.data[lp.index].uv = (x0 + u * (x1 - x0), (1 - y1) + v * (y1 - y0))


# --- render ------------------------------------------------------------------

def render(sc, out, frames=None, per_frame=None, stills=None):
    """Render frames one by one (per_frame(f) can set state first). stills: list of frames."""
    os.makedirs(out, exist_ok=True)
    todo = stills if stills is not None else (frames or range(sc.frame_start, sc.frame_end + 1))
    if stills is None and os.environ.get("WB_FROM"):
        todo = range(int(os.environ["WB_FROM"]), int(os.environ.get("WB_TO", sc.frame_end)) + 1)
    for f in todo:
        path = os.path.join(out, (f"still_{f:04d}.png" if stills is not None else f"{f:04d}.png"))
        if stills is None and os.environ.get("WB_RESUME") == "1" and os.path.exists(path):
            continue
        sc.frame_set(f)
        if per_frame:
            per_frame(f)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print("FRAME", f, flush=True)
