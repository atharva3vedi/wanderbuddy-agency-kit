"""WanderBuddy outro v2, built in Blender (5.2).

A whitewater wave surges UP over the brand-blue field, carries the card elements
in with it, then pulls back and leaves them locked into the final layout.

The card elements are NOT keyframed: each one is a rigid body hanging on a damped
spring from an anchor that rides the foam front. A turbulence force field, keyed
up during the crash, jumbles them; when the field dies and the wave recedes the
springs settle each element into its slot (different masses/pivots -> different
settle rhythms). The sim is baked to keyframes at the end so headless renders are
deterministic.

Run headless (from anywhere):
  blender -b --python build_outro.py -- test      # 4 preview PNG frames
  blender -b --python build_outro.py -- full      # full 30fps H.264 render
or live in an open Blender (via MCP):
  OUTRO_MODE = "live"; exec(open(path).read())    # rebuilds into the open scene

Frame coords: 1080x1920 px = 10.8 x 19.2 m, 1 px = 1 cm, origin at frame centre,
X right, Z up, camera looks down +Y (smaller Y = nearer the camera = on top).
"""
import bpy, math, os, sys
import numpy as np
from mathutils import Vector

HERE = globals().get("OUTRO_HERE") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.dirname(os.path.abspath(bpy.data.filepath)))
ASSETS = os.path.normpath(os.path.join(HERE, ".."))          # marketing/outro
MODE = globals().get("OUTRO_MODE") or ((sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "test").lower())

FPS, FRAMES = 30, 138                     # 4.6 s
W_PX, H_PX = 1080, 1920
W, H = W_PX / 100, H_PX / 100             # 10.8 x 19.2 m
def srgb(r, g, b):
    def c(v): v /= 255; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return (c(r), c(g), c(b), 1)
BLUE = srgb(0x20, 0x72, 0xB8)             # #2072B8 brand field (linear)
def px_to_x(x_px): return x_px / 100 - W / 2
def px_to_z(y_px): return H / 2 - y_px / 100

# --- wave choreography (WaveRig z = crest centre) ---------------------------
P = globals().get("OUTRO_PARAMS", {})
Z_OFF = -12.5                             # crest fully below the bottom edge
RUN_START, RUN_END = 8, 62                # run-up: fast in, decelerates (ease-out)
Z_PEAK, CREEP_END, Z_CREEP = 4.35, 74, 4.6    # crest peaks where the card lives: block reaches home AT the peak
WET_RAMP = 2.0                                # m over which an element goes from "in the water" to "dry" as the edge passes
BLOCK_LIFT = 0.35                             # on the run-up the anchors aim this far ABOVE the slot; on the backwash they sink to it with the water
LID_CLEARANCE = 1.0                           # foam-front barrier sits this far above the mean crest (inside the tongues)
DRAIN_KEYS = [(CREEP_END, 1.0), (116, 0.45)]  # wash thins as the sheet drains
ROLL_KEYS = [(CREEP_END, 1.0), (104, 0.45)]   # the roll becomes a ragged receding line
PULL_END = 116                            # backwash: starts slow, accelerates (ease-in)
BLOCK_TOP_Z = px_to_z(460)                # logo top at px 460 -> z = 5.0
RIDE_OFFSET = 0.8                         # anchors sit this far into the foam below the crest
CREST_R = 0.15                            # mean front thickness reference (m); the visible front is a wavy fringe
FRONT_REACH = 2.6                         # how far the wash plane extends above the mean crest line (lobes live here)
LOBE_KEYS = [(1, 0.7), (RUN_END, 1.0), (CREEP_END, 0.85), (116, 0.6)]   # lobe amplitude (m): surges unevenly on the run-up

# --- simulation tuning -------------------------------------------------------
TURB_STRENGTH = P.get("TURB_STRENGTH", 1800.0)
TURB_SIZE, TURB_SEED = P.get("TURB_SIZE", 1.2), P.get("TURB_SEED", 7)
TURB_KEYS = P.get("TURB_KEYS", [(1, 0), (14, 0), (26, 1.0), (58, 1.0), (CREEP_END + 2, 0.0), (FRAMES, 0.0)])   # nothing stirs once the water recedes   # x TURB_STRENGTH
OMEGA = P.get("OMEGA", 3.6)               # spring natural frequency (rad/s) ~ settle in ~1.5 s
DAMP_RATIO = P.get("DAMP_RATIO", 0.8)    # < 1 -> one soft overshoot, then lock
TILT_LIMIT = P.get("TILT_LIMIT", 18.0)   # degrees, in-plane
SHADOW_FADE = (86, 118)                   # drop shadows (lift cue) fade out here
LOCK_FRAMES = 12                          # each element blends to its exact slot over this many frames...
LOCK_AFTER_DRY = 8                        # ...starting this many frames after the edge has passed it (last resort: end of clip)
DRY_DAMPING = (0.55, 0.6)                 # linear/angular damping once an element sits on the dry field (friction)

sc = bpy.context.scene

# ---------------------------------------------------------------- scene reset
def wipe_scene():
    if sc.rigidbody_world:
        with bpy.context.temp_override(scene=sc):
            bpy.ops.rigidbody.world_remove()
    for o in list(bpy.data.objects):
        if o.name in ("Camera", "Sun"): continue
        bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions):
        for d in list(coll):
            if d.users == 0: coll.remove(d)

if bpy.app.background and not bpy.data.filepath:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
else:
    wipe_scene()

try: sc.render.engine = "BLENDER_EEVEE_NEXT"
except TypeError: sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = W_PX, H_PX
sc.render.resolution_percentage = 100
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, FRAMES
sc.eevee.taa_render_samples = 32
sc.view_settings.view_transform = "Standard"   # keep #2072B8 exact
sc.view_settings.look = "None"
sc.render.film_transparent = False

def fcurves_of(ad):
    """All F-curves of an animation-data block (works with 5.x slotted actions and 4.x)."""
    act = ad.action
    if hasattr(act, "fcurves"): return list(act.fcurves)
    return [fc for layer in act.layers for strip in layer.strips for cb in strip.channelbags for fc in cb.fcurves]

def link(o):
    sc.collection.objects.link(o)
    return o

def plane(name, w, h, loc, mat=None, parent=None, z_anchor="center"):
    """Axis-aligned quad facing -Y. z_anchor: 'center' | 'top' (top edge at loc z)."""
    mesh = bpy.data.meshes.new(name)
    hw = w / 2
    z0, z1 = (-h / 2, h / 2) if z_anchor == "center" else (-h, 0.0)
    verts = [(-hw, 0, z0), (hw, 0, z0), (hw, 0, z1), (-hw, 0, z1)]
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    uv = mesh.uv_layers.new(name="UVMap")
    for li, co in zip(range(4), [(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[li].uv = co
    o = link(bpy.data.objects.new(name, mesh))
    o.location = loc
    if mat: o.data.materials.append(mat)
    if parent: o.parent = parent
    return o

# ---------------------------------------------------------------- node helpers
def N(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items():
        if k == "inputs":
            for ik, iv in v.items(): n.inputs[ik].default_value = iv
        else: setattr(n, k, v)
    return n
def L(nt, a, b): nt.links.new(a, b)
def M(nt, op, a, b=None, c=None):
    n = nt.nodes.new("ShaderNodeMath"); n.operation = op; n.use_clamp = False
    for i, v in enumerate((a, b, c)):
        if v is None: continue
        if hasattr(v, "is_linked"): L(nt, v, n.inputs[i])
        else: n.inputs[i].default_value = v
    return n.outputs[0]
def smoothstep(nt, x, lo, hi):
    n = nt.nodes.new("ShaderNodeMapRange"); n.interpolation_type = "SMOOTHSTEP"; n.clamp = True
    L(nt, x, n.inputs["Value"])
    for sock, v in (("From Min", lo), ("From Max", hi)):
        if hasattr(v, "is_linked"): L(nt, v, n.inputs[sock])
        else: n.inputs[sock].default_value = v
    return n.outputs["Result"]

def flat_mat(name, rgba):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = N(nt, "ShaderNodeOutputMaterial")
    em = N(nt, "ShaderNodeEmission", inputs={"Color": rgba})
    L(nt, em.outputs[0], out.inputs[0])
    return m

def foam_base(nt, emission=0.3):
    """Shared foam surface: white principled + some self-emission (foam scatters light);
    keep lit facets just under clipping so the lumps still shade."""
    return N(nt, "ShaderNodeBsdfPrincipled", inputs={"Base Color": (1, 1, 1, 1), "Roughness": 0.6,
                                                   "Emission Color": (1, 1, 1, 1), "Emission Strength": emission})

def keyed_value(nt, name, keys, interp="BEZIER"):
    """A Value node whose output is keyframed: keys = [(frame, value), ...]."""
    n = N(nt, "ShaderNodeValue"); n.name = n.label = name
    for f, v in keys:
        n.outputs[0].default_value = v; n.outputs[0].keyframe_insert("default_value", frame=f)
    for fc in fcurves_of(nt.animation_data):
        if fc.data_path.startswith('nodes["%s"]' % name):
            for kp in fc.keyframe_points: kp.interpolation = interp
    return n.outputs[0]

def lace_field(nt, flow):
    """The foam pattern, in the coordinate frame of the FoamFlow empty (world
    space that advances with the water on run-up and mostly stays on backwash):
    blobby patches + ridged veins + fine bubble edge, stretched along the flow.
    Returns (field, patch, coord)."""
    coord = N(nt, "ShaderNodeTexCoord"); coord.object = flow
    mp = N(nt, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 1.0, 0.62)
    L(nt, coord.outputs["Object"], mp.inputs["Vector"])
    loc = mp.inputs["Location"]
    loc.default_value = (0, 0, 0); loc.keyframe_insert("default_value", frame=1)
    loc.default_value = (0.5, 0, -0.6); loc.keyframe_insert("default_value", frame=FRAMES)
    for fc in fcurves_of(nt.animation_data):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    blobs = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 0.85, "Detail": 4.0, "Roughness": 0.58, "Lacunarity": 2.1})
    L(nt, mp.outputs[0], blobs.inputs["Vector"])
    veins = N(nt, "ShaderNodeTexNoise", noise_type="RIDGED_MULTIFRACTAL",
              inputs={"Scale": 1.3, "Detail": 4.0, "Roughness": 0.55, "Lacunarity": 2.2, "Offset": 0.8, "Gain": 1.3})
    L(nt, mp.outputs[0], veins.inputs["Vector"])
    patch = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 0.3, "Detail": 2.0, "Roughness": 0.5})
    L(nt, mp.outputs[0], patch.inputs["Vector"])
    fine = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 9.0, "Detail": 3.0, "Roughness": 0.55})
    L(nt, mp.outputs[0], fine.inputs["Vector"])
    field = M(nt, "ADD", M(nt, "MULTIPLY", blobs.outputs["Fac"], 0.62), M(nt, "MULTIPLY", veins.outputs["Fac"], 0.42))
    field = M(nt, "ADD", field, M(nt, "MULTIPLY", M(nt, "SUBTRACT", fine.outputs["Fac"], 0.5), 0.14))
    return field, patch.outputs["Fac"], coord

def foam_from_cov(nt, field, cov):
    """Soft foam mask from the lace field and a 0..1 coverage."""
    thr = M(nt, "ADD", 0.24, M(nt, "MULTIPLY", 0.56, M(nt, "SUBTRACT", 1.0, cov)))
    return smoothstep(nt, M(nt, "SUBTRACT", field, thr), -0.16, 0.14)      # wide ramp = soft thin edges

def foam_shader(nt, out, alpha, field, shade, emission):
    bsdf = foam_base(nt, emission)
    col = N(nt, "ShaderNodeMixRGB", blend_type="MIX", inputs={"Color1": (0.62, 0.72, 0.86, 1), "Color2": (1, 1, 1, 1)})
    L(nt, shade, col.inputs["Fac"])
    L(nt, col.outputs[0], bsdf.inputs["Base Color"]); L(nt, col.outputs[0], bsdf.inputs["Emission Color"])
    bump = N(nt, "ShaderNodeBump", inputs={"Strength": 0.7}); L(nt, field, bump.inputs["Height"]); L(nt, bump.outputs[0], bsdf.inputs["Normal"])
    tr = N(nt, "ShaderNodeBsdfTransparent"); mix = N(nt, "ShaderNodeMixShader")
    L(nt, alpha, mix.inputs["Fac"]); L(nt, tr.outputs[0], mix.inputs[1]); L(nt, bsdf.outputs[0], mix.inputs[2]); L(nt, mix.outputs[0], out.inputs[0])

def edge_profile(nt, lobe_amp, field):
    """A(x, t): the leading edge's offset from the mean crest line (m). Big lobes
    + medium tongues sampled along x only, drifting in time, plus fingers from
    the lace field. Zero-mean -> level on average. Identical in every material
    that uses it (same noise, same drift keys) so edges line up across planes."""
    own = N(nt, "ShaderNodeTexCoord"); osep = N(nt, "ShaderNodeSeparateXYZ"); L(nt, own.outputs["Object"], osep.inputs[0])
    xvec = N(nt, "ShaderNodeCombineXYZ"); L(nt, osep.outputs["X"], xvec.inputs["X"])
    tmap = N(nt, "ShaderNodeMapping"); L(nt, xvec.outputs[0], tmap.inputs["Vector"])
    tloc = tmap.inputs["Location"]
    tloc.default_value = (0, 0, 0); tloc.keyframe_insert("default_value", frame=1)
    tloc.default_value = (0.8, 1.6, 0); tloc.keyframe_insert("default_value", frame=FRAMES)
    for fc in fcurves_of(nt.animation_data):
        if fc.data_path.startswith('nodes["' + tmap.name + '"]'):
            for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    big = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 0.30, "Detail": 1.0, "Roughness": 0.4}); L(nt, tmap.outputs[0], big.inputs["Vector"])
    med = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 1.1, "Detail": 2.0, "Roughness": 0.5}); L(nt, tmap.outputs[0], med.inputs["Vector"])
    A = M(nt, "ADD", M(nt, "MULTIPLY", M(nt, "SUBTRACT", big.outputs["Fac"], 0.5), 6.5), M(nt, "MULTIPLY", M(nt, "SUBTRACT", med.outputs["Fac"], 0.5), 2.4))   # fbm Fac has ~0.1 std: gains bring lobes to ~+-0.8 m
    A = M(nt, "MULTIPLY", A, lobe_amp)
    A = M(nt, "ADD", A, M(nt, "MULTIPLY", M(nt, "SUBTRACT", field, 0.5), 0.7))     # fingers/feathering from the lace field itself
    return A, tmap

def wash_mat(name, flow, crest_keys, reach_keys):
    """The whole wave as ONE surface on a world-fixed plane. Everything is a
    function of the current edge line (keyed mean crest + the wavy profile) and
    the highest line the water has reached so far:
      below the edge      -> the wash (dense front foam, lace by ~5 m, wisps)
      edge .. reach line  -> foam the receding water left behind, thinning with
                             height above the edge (only exists once the wave
                             is retreating, because reach == crest until then)
    so the foam never pops in or jumps: it is continuous in space and time."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    m.surface_render_method = "BLENDED"
    nt = m.node_tree; nt.nodes.clear()
    out = N(nt, "ShaderNodeOutputMaterial")
    field, patch, coord = lace_field(nt, flow)
    drain = keyed_value(nt, "Drain", DRAIN_KEYS)
    rollfade = keyed_value(nt, "RollFade", ROLL_KEYS)
    lobe_amp = keyed_value(nt, "LobeAmp", LOBE_KEYS)
    crest = keyed_value(nt, "CrestZ", crest_keys, "LINEAR")
    reach = keyed_value(nt, "Reach", reach_keys, "LINEAR")
    own = N(nt, "ShaderNodeTexCoord"); osep = N(nt, "ShaderNodeSeparateXYZ"); L(nt, own.outputs["Object"], osep.inputs[0])
    z = osep.outputs["Z"]
    A, tmap = edge_profile(nt, lobe_amp, field)
    edge = M(nt, "ADD", crest, A)
    d = M(nt, "SUBTRACT", edge, z)                                    # distance behind (below) the actual wavy edge
    # --- the wash
    cov = M(nt, "SUBTRACT", 1.12, M(nt, "DIVIDE", d, 5.5))
    cov = M(nt, "MAXIMUM", cov, M(nt, "SUBTRACT", 0.30, M(nt, "DIVIDE", d, 30.0)))
    cov = M(nt, "ADD", cov, M(nt, "MULTIPLY", M(nt, "SUBTRACT", patch, 0.5), 0.7))
    cov = M(nt, "MINIMUM", M(nt, "MAXIMUM", M(nt, "MULTIPLY", cov, drain), 0.0), 1.0)
    wash = M(nt, "MULTIPLY", foam_from_cov(nt, field, cov), smoothstep(nt, d, -0.30, 0.20))
    # --- what the water left behind: between the edge and the reach line, thinning upward
    dz = M(nt, "SUBTRACT", z, edge)
    below_reach = smoothstep(nt, M(nt, "SUBTRACT", M(nt, "ADD", reach, A), z), -0.2, 0.5)
    band = M(nt, "MULTIPLY", smoothstep(nt, dz, -0.8, -0.15), smoothstep(nt, dz, 2.8, 0.9))
    cov_r = M(nt, "SUBTRACT", M(nt, "MULTIPLY", 1.12, drain), M(nt, "MULTIPLY", dz, 0.28))
    cov_r = M(nt, "ADD", cov_r, M(nt, "MULTIPLY", M(nt, "SUBTRACT", patch, 0.5), 0.7))
    cov_r = M(nt, "MINIMUM", M(nt, "MAXIMUM", cov_r, 0.0), 1.0)
    left = M(nt, "MULTIPLY", M(nt, "MULTIPLY", foam_from_cov(nt, field, cov_r), band), below_reach)
    alpha = M(nt, "MAXIMUM", wash, left)
    # thick bright foam right behind the edge, slightly shaded water-heavy zone behind that (both fade on the backwash)
    thick = M(nt, "MULTIPLY", smoothstep(nt, d, 1.0, 0.05), rollfade)
    shade = M(nt, "SUBTRACT", 1.0, M(nt, "MULTIPLY", M(nt, "MULTIPLY", 0.22, rollfade), M(nt, "MULTIPLY", smoothstep(nt, d, 0.5, 1.2), smoothstep(nt, d, 2.6, 1.6))))
    shade = M(nt, "MULTIPLY", shade, M(nt, "ADD", 0.86, M(nt, "MULTIPLY", 0.14, M(nt, "MAXIMUM", alpha, thick))))
    lumps = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 1.6, "Detail": 3.0, "Roughness": 0.5}); L(nt, tmap.outputs[0], lumps.inputs["Vector"])
    height = M(nt, "ADD", field, M(nt, "MULTIPLY", M(nt, "MULTIPLY", lumps.outputs["Fac"], 0.9), thick))
    foam_shader(nt, out, alpha, height, shade, 0.24)
    return m

def crest_mat(name):
    """The foam roll: white, lumpy shading, a soft irregular leading edge at the
    scale of foam lumps (not speckle), mean line stays perfectly level. Fades
    into a ragged line on the backwash."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    m.surface_render_method = "BLENDED"
    nt = m.node_tree; nt.nodes.clear()
    out = N(nt, "ShaderNodeOutputMaterial")
    coord = N(nt, "ShaderNodeTexCoord")
    mp = N(nt, "ShaderNodeMapping"); L(nt, coord.outputs["Object"], mp.inputs["Vector"])
    loc = mp.inputs["Location"]
    loc.default_value = (0, 0, 0); loc.keyframe_insert("default_value", frame=1)
    loc.default_value = (2.0, 0, 0); loc.keyframe_insert("default_value", frame=FRAMES)
    for fc in fcurves_of(nt.animation_data):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    lumps = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 1.4, "Detail": 3.0, "Roughness": 0.5})
    L(nt, mp.outputs[0], lumps.inputs["Vector"])
    rim = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 2.4, "Detail": 2.0, "Roughness": 0.5})
    L(nt, mp.outputs[0], rim.inputs["Vector"])
    geo = N(nt, "ShaderNodeNewGeometry"); nsep = N(nt, "ShaderNodeSeparateXYZ"); L(nt, geo.outputs["True Normal"], nsep.inputs[0])
    nz = nsep.outputs["Z"]
    rollfade = keyed_value(nt, "RollFade", ROLL_KEYS)
    # leading edge (top rim, nz -> 1): soft lumpy erosion, +-~10 cm; on the backwash the erosion eats the whole roll into a ragged line
    erode = M(nt, "ADD", 0.78, M(nt, "MULTIPLY", 1.1, M(nt, "SUBTRACT", 1.0, rollfade)))
    edge = smoothstep(nt, M(nt, "ADD", nz, M(nt, "MULTIPLY", M(nt, "SUBTRACT", rim.outputs["Fac"], 0.5), 0.5)), erode, M(nt, "ADD", erode, 0.21))
    alpha = M(nt, "SUBTRACT", 1.0, edge)
    bsdf = foam_base(nt, 0.10)
    bump = N(nt, "ShaderNodeBump", inputs={"Strength": 0.8})
    L(nt, lumps.outputs["Fac"], bump.inputs["Height"]); L(nt, bump.outputs[0], bsdf.inputs["Normal"])
    tr = N(nt, "ShaderNodeBsdfTransparent"); mix = N(nt, "ShaderNodeMixShader")
    L(nt, alpha, mix.inputs["Fac"]); L(nt, tr.outputs[0], mix.inputs[1]); L(nt, bsdf.outputs[0], mix.inputs[2]); L(nt, mix.outputs[0], out.inputs[0])
    return m

def gradient_mat(name, rgba, a_top, a_bottom, noise_amt=0.0, fade_keys=None):
    """Emission with alpha = lerp(a_bottom, a_top, v) (optionally noise-modulated)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    m.surface_render_method = "BLENDED"
    nt = m.node_tree; nt.nodes.clear()
    out = N(nt, "ShaderNodeOutputMaterial")
    coord = N(nt, "ShaderNodeTexCoord"); sep = N(nt, "ShaderNodeSeparateXYZ"); L(nt, coord.outputs["UV"], sep.inputs[0])
    v = sep.outputs["Y"]
    a = M(nt, "ADD", a_bottom, M(nt, "MULTIPLY", v, a_top - a_bottom))
    if noise_amt:
        mp = N(nt, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1, 1, 3.0); L(nt, coord.outputs["Object"], mp.inputs["Vector"])
        nz = N(nt, "ShaderNodeTexNoise", inputs={"Scale": 3.0, "Detail": 2.0}); L(nt, mp.outputs[0], nz.inputs["Vector"])
        a = M(nt, "MULTIPLY", a, M(nt, "ADD", 1.0 - noise_amt, M(nt, "MULTIPLY", nz.outputs["Fac"], 2 * noise_amt)))
    if fade_keys:
        a = M(nt, "MULTIPLY", a, keyed_value(nt, "Fade", fade_keys))
    em = N(nt, "ShaderNodeEmission", inputs={"Color": rgba})
    tr = N(nt, "ShaderNodeBsdfTransparent"); mix = N(nt, "ShaderNodeMixShader")
    L(nt, a, mix.inputs["Fac"]); L(nt, tr.outputs[0], mix.inputs[1]); L(nt, em.outputs[0], mix.inputs[2]); L(nt, mix.outputs[0], out.inputs[0])
    return m

def png_mat(name, img):
    m = bpy.data.materials.new(name); m.use_nodes = True
    m.surface_render_method = "BLENDED"
    nt = m.node_tree; nt.nodes.clear()
    out = N(nt, "ShaderNodeOutputMaterial")
    tex = N(nt, "ShaderNodeTexImage"); tex.image = img; tex.interpolation = "Cubic"
    img.alpha_mode = "STRAIGHT"
    em = N(nt, "ShaderNodeEmission"); tr = N(nt, "ShaderNodeBsdfTransparent"); mix = N(nt, "ShaderNodeMixShader")
    L(nt, tex.outputs["Color"], em.inputs["Color"]); L(nt, tex.outputs["Alpha"], mix.inputs["Fac"])
    L(nt, tr.outputs[0], mix.inputs[1]); L(nt, em.outputs[0], mix.inputs[2]); L(nt, mix.outputs[0], out.inputs[0])
    return m

# ---------------------------------------------------------------- camera + light
if "Camera" not in bpy.data.objects:
    cam_data = bpy.data.cameras.new("Cam"); cam_data.type = "ORTHO"
    cam_data.sensor_fit = "VERTICAL"; cam_data.ortho_scale = H
    cam = link(bpy.data.objects.new("Camera", cam_data))
    cam.location = (0, -30, 0); cam.rotation_euler = (math.radians(90), 0, 0)
sc.camera = bpy.data.objects["Camera"]
if "Sun" not in bpy.data.objects:
    link(bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN")))
sun = bpy.data.objects["Sun"]; sun.data.energy = 2.6; sun.data.use_shadow = False
sun.rotation_euler = Vector((-0.55, 0.35, -0.76)).to_track_quat("-Z", "Y").to_euler()   # light travels down-right and away: lumps shade
world = sc.world or bpy.data.worlds.new("World"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.6, 0.7, 0.85, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.32

# ---------------------------------------------------------------- the field (was: sand)
plane("Field", W * 1.5, H * 1.5, (0, 6, 0), flat_mat("BrandBlueField", BLUE))

# ---------------------------------------------------------------- the wave
wave = link(bpy.data.objects.new("WaveRig", None)); wave.empty_display_type = "PLAIN_AXES"
flow = link(bpy.data.objects.new("FoamFlow", None)); flow.empty_display_type = "ARROWS"   # the foam pattern's frame (keyed below)
SKIRT_LEN = 30.0
plane("WaterFilm", W * 1.5, SKIRT_LEN, (0, 4.8, -0.7), gradient_mat("WaterFilm", (1, 1, 1, 1), 0.12, 0.0, fade_keys=[(CREEP_END, 1.0), (116, 0.3)]), parent=wave, z_anchor="top")

def key_z(o, frame, z, interp="BEZIER", easing="AUTO"):
    o.location.z = z; o.keyframe_insert("location", index=2, frame=frame)
    kp = [k for k in fcurves_of(o.animation_data)[0].keyframe_points if k.co.x == frame][0]
    kp.interpolation = interp; kp.easing = easing
key_z(wave, 1, Z_OFF, "CONSTANT")
key_z(wave, RUN_START, Z_OFF, "CUBIC", "EASE_OUT")       # run-up: arrives fast, decelerates
key_z(wave, RUN_END, Z_PEAK, "SINE", "EASE_OUT")         # last trickle forward
key_z(wave, CREEP_END, Z_CREEP, "QUAD", "EASE_IN")       # backwash: starts slow, accelerates
key_z(wave, PULL_END, Z_OFF, "CONSTANT")
key_z(wave, FRAMES, Z_OFF, "CONSTANT")

def crest_z(frame):
    sc.frame_set(frame); return wave.matrix_world.translation.z
crest_zs = {f: crest_z(f) for f in range(1, FRAMES + 1)}

# the foam pattern rides with the water on the run-up (85 %), mostly stays put on the backwash (20 %)
flow_peak = 0.85 * (crest_zs[CREEP_END] - crest_zs[1])
for f in range(1, FRAMES + 1):
    if f <= CREEP_END: fz = 0.85 * (crest_zs[f] - crest_zs[1])
    else: fz = flow_peak - 0.2 * (crest_zs[CREEP_END] - crest_zs[f])
    flow.location = (0, 0, fz); flow.keyframe_insert("location", frame=f)
for fc in fcurves_of(flow.animation_data):
    for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
# the wave: one world-fixed surface driven by the keyed crest line and its running maximum
reach_zs, hi_r = {}, -1e9
for f in range(1, FRAMES + 1):
    hi_r = max(hi_r, crest_zs[f]); reach_zs[f] = hi_r
plane("Wash", W * 1.5, H * 1.5 + 12, (0, 4.6, 0), wash_mat("Wash", flow, [(f, crest_zs[f]) for f in range(1, FRAMES + 1)], [(f, reach_zs[f]) for f in range(1, FRAMES + 1)]))

# ---------------------------------------------------------------- the card elements
def img_alpha(img):
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32); img.pixels.foreach_get(px)
    return px.reshape(h, w, 4)[:, :, 3]
def load_img(fn):
    p = os.path.join(ASSETS, fn)
    for i in bpy.data.images:
        if os.path.normpath(bpy.path.abspath(i.filepath)) == os.path.normpath(p): return i
    return bpy.data.images.load(p)

def crop_plane(name, img, x0, x1, yt, yb, to_world, y_depth, margin=6):
    """Sub-rectangle of an image as its own quad (exact 1 texel : 1 cm mapping),
    origin at the element's centre so it rotates/settles about itself."""
    w, h = img.size
    x0, x1, yt, yb = max(0, x0 - margin), min(w, x1 + 1 + margin), max(0, yt - margin), min(h, yb + 1 + margin)
    (xl, zt), (xr, zb) = to_world(x0, yt), to_world(x1, yb)
    cx, cz = (xl + xr) / 2, (zt + zb) / 2
    mesh = bpy.data.meshes.new(name)
    verts = [(xl - cx, 0, zb - cz), (xr - cx, 0, zb - cz), (xr - cx, 0, zt - cz), (xl - cx, 0, zt - cz)]
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    uv = mesh.uv_layers.new(name="UVMap")
    u0, u1, v0, v1 = x0 / w, x1 / w, 1 - yb / h, 1 - yt / h
    for li, co in zip(range(4), [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]):
        uv.data[li].uv = co
    o = link(bpy.data.objects.new(name, mesh))
    o.location = (cx, y_depth, cz)
    o.data.materials.append(png_mat(name, img))
    return o

full = lambda px, py: (px_to_x(px), px_to_z(py))
MARK_S = 8.2 / 1024                                  # mark plane: 820 px box, top-left at px (130, 300)
mark_w = lambda px, py: (-4.1 + px * MARK_S, px_to_z(300) - py * MARK_S)

def alpha_bbox(a, xa=0, xb=None):
    ys, xs = np.nonzero(a[:, xa:xb] > 0.02); h = a.shape[0]
    return int(xs.min()) + xa, int(xs.max()) + xa, int(h - 1 - ys.max()), int(h - 1 - ys.min())

imgs = {k: load_img(f) for k, f in {"word": "layer-word.png", "dl": "layer-dlnow.png", "mark": "mark_t.png"}.items()}
shadow_imgs = {k: load_img(f) for k, f in {"word": "layer-word-shadow.png", "dl": "layer-dlnow-shadow.png", "mark": "mark_t-shadow.png"}.items()}
shadow_key = {imgs[k].name: shadow_imgs[k] for k in imgs}

def shadow_mat(name, img):
    """Blurred alpha of the element, near-black, fading out over SHADOW_FADE."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    m.surface_render_method = "BLENDED"
    nt = m.node_tree; nt.nodes.clear()
    out = N(nt, "ShaderNodeOutputMaterial")
    tex = N(nt, "ShaderNodeTexImage"); tex.image = img; tex.interpolation = "Cubic"; img.alpha_mode = "STRAIGHT"
    gain = N(nt, "ShaderNodeValue"); gain.name = "Gain"
    gain.outputs[0].default_value = 0.42; gain.outputs[0].keyframe_insert("default_value", frame=SHADOW_FADE[0])
    gain.outputs[0].default_value = 0.0; gain.outputs[0].keyframe_insert("default_value", frame=SHADOW_FADE[1])
    a = M(nt, "MULTIPLY", tex.outputs["Alpha"], gain.outputs[0])
    em = N(nt, "ShaderNodeEmission", inputs={"Color": (0.0, 0.02, 0.06, 1)})
    tr = N(nt, "ShaderNodeBsdfTransparent"); mix = N(nt, "ShaderNodeMixShader")
    L(nt, a, mix.inputs["Fac"]); L(nt, tr.outputs[0], mix.inputs[1]); L(nt, em.outputs[0], mix.inputs[2]); L(nt, mix.outputs[0], out.inputs[0])
    return m
alphas = {k: img_alpha(i) for k, i in imgs.items()}

# name, image, bbox, mapping, depth, mass, spring pivot (fraction of half-size: (fx, fz))
specs = [
    ("LogoMark",    imgs["mark"],   alpha_bbox(alphas["mark"]),                    mark_w, -0.30, 2.2, (-0.22,  0.30), 0.80, 0.22),
    ("Wordmark",    imgs["word"],   alpha_bbox(alphas["word"]),                    full,   -0.25, 1.3, ( 0.30,  0.20), 1.00, 0.34),
    ("DownloadNow", imgs["dl"],     alpha_bbox(alphas["dl"]),                      full,   -0.20, 0.6, (-0.25, -0.25), 1.30, 0.50),
]

# ---------------------------------------------------------------- simulation rig
with bpy.context.temp_override(scene=sc):
    bpy.ops.rigidbody.world_add()
rbw = sc.rigidbody_world
rbw.substeps_per_frame = 12; rbw.solver_iterations = 24; rbw.time_scale = 1.0
rbw.point_cache.frame_start, rbw.point_cache.frame_end = 1, FRAMES
sc.use_gravity = False; sc.gravity = (0, 0, 0)

rig = link(bpy.data.objects.new("AssetsRig", None)); rig.empty_display_type = "PLAIN_AXES"
# anchors ride the foam front: block top = min(final, crest + offset)
hi = -1e9
for f in range(1, FRAMES + 1):
    hi = max(hi, crest_z(f) + RIDE_OFFSET - BLOCK_TOP_Z)   # running max: once carried up, it stays
    rig.location.z = min(BLOCK_LIFT, hi)
    rig.keyframe_insert("location", index=2, frame=f)
for fc in fcurves_of(rig.animation_data):
    for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
sc.frame_set(1)
rig_z1 = rig.location.z

with bpy.context.temp_override(scene=sc):
    bpy.ops.object.effector_add(type="TURBULENCE", location=(0, 0, 0))
turb = bpy.context.active_object; turb.name = "Jumble"
turb.field.strength = 0.0; turb.field.size = TURB_SIZE; turb.field.flow = 0.0; turb.field.noise = 0.0; turb.field.seed = TURB_SEED
turb.field.use_2d_force = False; turb.field.falloff_power = 0.0
for f, k in TURB_KEYS:
    turb.field.strength = TURB_STRENGTH * k; turb.field.keyframe_insert("strength", frame=f)
for fc in fcurves_of(turb.animation_data):
    for kp in fc.keyframe_points: kp.interpolation = "BEZIER"

lid_mesh = bpy.data.meshes.new("FoamLid")
hx, hy, hz = W * 0.75, 1.0, 0.2
lid_mesh.from_pydata([(sx * hx, sy * hy, sz * hz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)], [],
                     [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)])
lid = link(bpy.data.objects.new("FoamLid", lid_mesh)); lid.parent = wave
lid.location = (0, 0, LID_CLEARANCE + hz)    # bottom face inside the tongues above the mean line
lid.hide_render = True; lid.display_type = "WIRE"
lid.keyframe_insert("location", index=2, frame=CREEP_END)   # the front only pushes on the way in:
lid.location.z = 60.0; lid.keyframe_insert("location", index=2, frame=CREEP_END + 1)   # lifted clear at the peak
for fc in fcurves_of(lid.animation_data):
    for kp in fc.keyframe_points: kp.interpolation = "CONSTANT"

def rb_add(o, kind):
    with bpy.context.temp_override(object=o, selected_objects=[o], active_object=o, scene=sc):
        bpy.ops.rigidbody.object_add(type=kind)
    return o.rigid_body

lrb = rb_add(lid, "PASSIVE"); lrb.kinematic = True; lrb.collision_shape = "BOX"; lrb.friction = 0.2
lrb.collision_collections = [c < len(specs) for c in range(20)]   # collides with every element
assets, homes, dry_frames = [], {}, {}
for i, (name, img, bb, to_world, depth, mass, pivot, wf, drag) in enumerate(specs):
    o = crop_plane(name, img, *bb, to_world, depth)
    homes[name] = Vector(o.location)
    sh = crop_plane(name + "_Shadow", shadow_key[img.name], *bb, to_world, depth + 0.6, margin=28)
    sh.data.materials.clear(); sh.data.materials.append(shadow_mat(name + "_Shadow", shadow_key[img.name]))
    sh.parent = o
    sh.location = (sh.location.x - o.location.x + 0.05, 0.6, sh.location.z - o.location.z - 0.07)
    hw, hh = o.dimensions.x / 2, o.dimensions.z / 2
    # start the sim with the element on its anchor, off the bottom of frame
    o.location.z += rig_z1
    rb = rb_add(o, "ACTIVE")
    rb.collision_shape = "BOX"; rb.mass = mass
    rb.linear_damping = 0.12; rb.angular_damping = 0.18
    rb.collision_collections = [c == i + 1 for c in range(20)]   # nothing collides with anything
    rb.use_deactivation = False
    # anchor: kinematic body that rides the AssetsRig
    am = bpy.data.meshes.new(name + "_anchor"); am.from_pydata([(-.05, 0, -.05), (.05, 0, -.05), (.05, 0, .05), (-.05, 0, .05)], [], [(0, 1, 2, 3)])
    anchor = link(bpy.data.objects.new(name + "_Anchor", am)); anchor.parent = rig
    anchor.location = (homes[name].x + pivot[0] * hw, depth, homes[name].z + pivot[1] * hh)
    anchor.hide_render = True; anchor.display_type = "WIRE"
    base_z, bottom = anchor.location.z, homes[name].z - hh
    dry_frame = next((f for f in range(CREEP_END, FRAMES + 1) if crest_zs[f] + CREST_R < bottom - 0.3), FRAMES)
    try:      # the moment the water starts receding, the element is heavy in the thinning sheet: no more bouncing
        rb.keyframe_insert("linear_damping", frame=CREEP_END - 1); rb.keyframe_insert("angular_damping", frame=CREEP_END - 1)
        rb.linear_damping, rb.angular_damping = 0.4, 0.5
        rb.keyframe_insert("linear_damping", frame=CREEP_END); rb.keyframe_insert("angular_damping", frame=CREEP_END)
    except Exception as e:
        print("damping keys not supported:", e)
    dry_frames[name] = dry_frame
    try:      # friction with the field once dry: damping jumps (rigid-body settings are animatable)
        rb.keyframe_insert("linear_damping", frame=dry_frame - 1); rb.keyframe_insert("angular_damping", frame=dry_frame - 1)
        rb.linear_damping, rb.angular_damping = DRY_DAMPING
        rb.keyframe_insert("linear_damping", frame=dry_frame); rb.keyframe_insert("angular_damping", frame=dry_frame)
    except Exception as e:
        print("damping keys not supported:", e)
    for f in range(1, FRAMES + 1):
        cz = crest_zs[f]
        wet = min(1.0, max(0.0, (cz + CREST_R - bottom) / WET_RAMP)); wet = wet * wet * (3 - 2 * wet)
        # the rig holds the block BLOCK_LIFT above the slot; once the water recedes the anchor sinks to the slot with it
        anchor.location.z = base_z - (0.0 if f < CREEP_END else BLOCK_LIFT * (1.0 - wet))
        anchor.keyframe_insert("location", index=2, frame=f)
    for fc in fcurves_of(anchor.animation_data):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    sc.frame_set(1)
    arb = rb_add(anchor, "PASSIVE"); arb.kinematic = True
    arb.collision_collections = [c == 19 for c in range(20)]
    # damped spring: pulls the pivot point back onto the anchor, and the tilt back to level
    con = link(bpy.data.objects.new(name + "_Spring", None)); con.empty_display_type = "SPHERE"; con.empty_display_size = 0.2
    con.location = (anchor.location.x, depth, anchor.location.z + rig_z1)
    with bpy.context.temp_override(object=con, selected_objects=[con], active_object=con, scene=sc):
        bpy.ops.rigidbody.constraint_add(type="GENERIC_SPRING")
    c = con.rigid_body_constraint
    c.object1, c.object2 = anchor, o
    c.disable_collisions = True; c.spring_type = "SPRING2"
    c.use_limit_lin_y = True; c.limit_lin_y_lower = c.limit_lin_y_upper = 0
    c.use_limit_ang_x = True; c.limit_ang_x_lower = c.limit_ang_x_upper = 0
    c.use_limit_ang_z = True; c.limit_ang_z_lower = c.limit_ang_z_upper = 0
    c.use_limit_ang_y = True; c.limit_ang_y_lower, c.limit_ang_y_upper = math.radians(-TILT_LIMIT), math.radians(TILT_LIMIT)
    w = OMEGA * wf
    k = mass * w ** 2; cd = 2 * DAMP_RATIO * math.sqrt(k * mass)
    inertia = mass * ((2 * hw) ** 2 + (2 * hh) ** 2) / 12
    ka = inertia * (w * 1.6) ** 2; ca = 2 * (DAMP_RATIO + 0.15) * math.sqrt(ka * inertia)
    for ax in "xz":
        setattr(c, f"use_spring_{ax}", True); setattr(c, f"spring_stiffness_{ax}", k); setattr(c, f"spring_damping_{ax}", cd)
    c.use_spring_ang_y = True; c.spring_stiffness_ang_y = ka; c.spring_damping_ang_y = ca
    assets.append(o)

for mat in bpy.data.materials:
    if mat.surface_render_method == "BLENDED":
        try: mat.use_transparent_shadow = True
        except AttributeError: pass

# ---------------------------------------------------------------- run + bake the sim
with bpy.context.temp_override(scene=sc):
    bpy.ops.ptcache.free_bake_all()
baked = {o.name: [] for o in assets}
for f in range(1, FRAMES + 1):
    sc.frame_set(f)                       # steps the rigid-body sim
    for o in assets:
        baked[o.name].append((Vector(o.matrix_world.translation), o.matrix_world.to_euler("XYZ").y))
# turn the simulated transforms into plain keyframes and drop the sim (deterministic headless renders)
springs = [o for o in bpy.data.objects if o.name.endswith("_Spring")]
anchors = [o for o in bpy.data.objects if o.name.endswith("_Anchor")]
for con in springs:                      # constraints first, then bodies, then the world (else Bullet double-frees)
    with bpy.context.temp_override(object=con, selected_objects=[con], active_object=con, scene=sc):
        bpy.ops.rigidbody.constraint_remove()
for o in assets + anchors:
    with bpy.context.temp_override(object=o, selected_objects=[o], active_object=o, scene=sc):
        bpy.ops.rigidbody.object_remove()
with bpy.context.temp_override(scene=sc):
    bpy.ops.rigidbody.world_remove()
for o in springs + anchors:
    bpy.data.objects.remove(o, do_unlink=True)
ratchet_note = {}
for o in assets:
    rows, hz_ = baked[o.name], homes[o.name].z
    above_at_peak = rows[CREEP_END - 1][0].z >= hz_
    ratchet_note[o.name] = "ratchet" if above_at_peak else "BELOW SLOT AT PEAK (rises)"
    if above_at_peak:
        zmin = rows[CREEP_END - 1][0].z
        for i in range(CREEP_END - 1, len(rows)):
            loc, ry = rows[i]
            zmin = max(hz_, min(zmin, loc.z)); loc = Vector((loc.x, loc.y, zmin)); rows[i] = (loc, ry)
for o in assets:
    for f, (loc, ry) in enumerate(baked[o.name], start=1):
        o.location = loc; o.rotation_euler = (0, ry, 0)
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)
    for fc in fcurves_of(o.animation_data):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
# the sim is now plain keyframes; report the residual and blend the last frames to the exact slot
report = {}
for o in assets:
    home = homes[o.name]
    sc.frame_set(FRAMES)
    report[o.name] = (round((Vector(o.location) - home).length * 100, 2), round(math.degrees(o.rotation_euler.y), 2))
    start = min(dry_frames[o.name] + LOCK_AFTER_DRY, FRAMES - LOCK_FRAMES)
    for f in range(start, FRAMES + 1):
        sc.frame_set(f)
        t = min(1.0, (f - start) / LOCK_FRAMES); t = t * t * (3 - 2 * t)
        o.location = Vector(o.location).lerp(home, t)
        o.rotation_euler.y *= (1 - t)
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)
    report[o.name] += (dry_frames[o.name], start, ratchet_note[o.name])
OUTRO_REPORT = report
print("RESIDUAL at last sim frame (cm, deg):", report)
sc.frame_set(1)

# ---------------------------------------------------------------- save + render
blend = os.path.join(HERE, "outro.blend")
if MODE != "live":
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    print("saved", blend)
if MODE == "test":
    sc.render.image_settings.file_format = "PNG"
    for f in [int(x) for x in os.environ.get("OUTRO_TEST_FRAMES", "30,60,80,100").split(",")]:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(HERE, f"test_{f:03d}.png")
        bpy.ops.render.render(write_still=True)
        print("wrote", sc.render.filepath)
elif MODE == "full":
    # PNG sequence (Blender 5.x moved video output; ffmpeg encodes it afterwards, see README)
    sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"
    sc.render.filepath = os.path.join(HERE, "frames", "f_")
    bpy.ops.render.render(animation=True)
    print("rendered", sc.render.filepath)
