# WanderBuddy India still ads: one Blender scene per spec, rendered in Cycles.
# Run: blender -b --factory-startup --python build_ad.py -- spec.json
# The spec holds a list of shots; each shot is a photo backdrop (or a studio backdrop with
# floating trip cards) and a modelled phone that shows a fresh capture of the live site.
import bpy, bmesh, json, math, sys, os
from mathutils import Vector, Euler

args = sys.argv[sys.argv.index('--') + 1:]
SPEC = json.load(open(args[0]))
ONLY = args[1].split(',') if len(args) > 1 else None

# ---------------------------------------------------------------- helpers
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def rounded_rect(w, h, r, seg=12):
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(seg + 1):
            a = math.radians(a0 + 90 * i / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def ngon_obj(name, pts, z=0.0, uv=True):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((x, y, z)) for x, y in pts]
    f = bm.faces.new(vs)
    if uv:
        lay = bm.loops.layers.uv.new('UVMap')
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        for loop in f.loops:
            co = loop.vert.co
            loop[lay].uv = ((co.x - x0) / (x1 - x0), (co.y - y0) / (y1 - y0))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    return ob

def principled(mat):
    return next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')

def set_in(node, names, value):
    for n in names:
        if n in node.inputs:
            node.inputs[n].default_value = value; return
    raise KeyError(names)

def mat_metal(name, color, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = principled(m)
    set_in(b, ['Base Color'], (*color, 1)); set_in(b, ['Metallic'], 1.0); set_in(b, ['Roughness'], rough)
    return m

def mat_glossy_black(name, rough=0.08):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = principled(m)
    set_in(b, ['Base Color'], (0.004, 0.004, 0.005, 1)); set_in(b, ['Roughness'], rough)
    return m

def load_img(path):
    img = bpy.data.images.load(path, check_existing=True)
    return img

def mat_screen(name, path, emit=1.0):
    """Glass over a lit-from-within display: emission = the capture, plus a glossy reflection."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = principled(m)
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = load_img(path); tex.interpolation = 'Cubic'
    tex.image.colorspace_settings.name = 'sRGB'
    set_in(b, ['Base Color'], (0, 0, 0, 1)); set_in(b, ['Roughness'], 0.06)
    nt.links.new(tex.outputs['Color'], b.inputs['Emission Color'])
    set_in(b, ['Emission Strength'], emit)
    return m

def mat_emit_image(name, path, strength=1.0, alpha=False):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = load_img(path); tex.interpolation = 'Cubic'
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
    nt.links.new(tex.outputs['Color'], em.inputs['Color'])
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    return m

def mat_card(name, path, emit=0.55):
    """A printed-looking UI card: lit diffuse + some self light so whites stay white, alpha from the PNG."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = principled(m)
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = load_img(path); tex.interpolation = 'Cubic'
    nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(tex.outputs['Color'], b.inputs['Emission Color'])
    nt.links.new(tex.outputs['Alpha'], b.inputs['Alpha'])
    set_in(b, ['Emission Strength'], emit); set_in(b, ['Roughness'], 0.45)
    return m

def mat_backdrop_studio(name, top, bottom):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = principled(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*bottom, 1); ramp.color_ramp.elements[1].color = (*top, 1)
    nt.links.new(tc.outputs['UV'], sep.inputs[0]); nt.links.new(sep.outputs['Y'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    set_in(b, ['Roughness'], 0.9)
    return m

def world_gradient(top, horizon, strength):
    w = bpy.data.worlds.new('World'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree
    bg = next(n for n in nt.nodes if n.type == 'BACKGROUND')
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = (*horizon, 1)
    ramp.color_ramp.elements[1].color = (*top, 1)
    mp = nt.nodes.new('ShaderNodeMapRange'); mp.inputs['From Min'].default_value = -1; mp.inputs['From Max'].default_value = 1
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], mp.inputs['Value']); nt.links.new(mp.outputs['Result'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = strength

def area_light(name, loc, target, size, power, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, 'AREA'); d.size = size; d.energy = power; d.color = color
    ob = bpy.data.objects.new(name, d); bpy.context.collection.objects.link(ob); ob.location = loc
    look_at(ob, Vector(target)); return ob

def look_at(ob, target):
    direction = target - ob.location
    ob.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# ---------------------------------------------------------------- phone
SCR_W = 0.0650
def build_phone(screen_path, emit):
    aspect = 1170 / 2556
    sw, sh = SCR_W, SCR_W / aspect
    bez = 0.0033; bw, bh, thick = sw + 2 * bez, sh + 2 * bez, 0.0080
    root = bpy.data.objects.new('Phone', None); bpy.context.collection.objects.link(root)
    # body: rounded slab, bevelled edges, black glass front, titanium sides
    me = bpy.data.meshes.new('Body'); bm = bmesh.new()
    pts = rounded_rect(bw, bh, 0.0118, 14)
    vs = [bm.verts.new((x, y, -thick)) for x, y in pts]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [g for g in ext['geom'] if isinstance(g, bmesh.types.BMVert)]: v.co.z = 0.0
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    body = bpy.data.objects.new('Body', me); bpy.context.collection.objects.link(body); body.parent = root
    body.data.materials.append(mat_metal('Titanium', (0.16, 0.17, 0.19), 0.28))
    body.data.materials.append(mat_glossy_black('Bezel', 0.05))
    for poly in body.data.polygons:
        poly.use_smooth = True
        if poly.normal.z > 0.9: poly.material_index = 1
    bev = body.modifiers.new('Bevel', 'BEVEL'); bev.width = 0.0016; bev.segments = 8; bev.limit_method = 'ANGLE'
    try: bev.harden_normals = True
    except Exception: pass
    # screen
    scr = ngon_obj('Screen', rounded_rect(sw, sh, 0.0088, 14), z=0.00006); scr.parent = root
    scr.data.materials.append(mat_screen('ScreenMat', screen_path, emit))
    # dynamic island
    isl = ngon_obj('Island', rounded_rect(0.0206, 0.0060, 0.0030, 10), z=0.00012, uv=False); isl.parent = root
    isl.location.y = sh / 2 - 0.0049
    isl.data.materials.append(mat_glossy_black('Island', 0.15))
    # side buttons
    for (y, l) in ((0.030, 0.006), (0.012, 0.011), (-0.004, 0.011)):
        b = ngon_obj('Btn', rounded_rect(0.0010, l, 0.0005, 4), z=0, uv=False); b.parent = root
        b.location = (-bw / 2 - 0.0003, y, -thick / 2); b.rotation_euler = (0, math.radians(90), 0)
        b.data.materials.append(body.data.materials[0])
    return root, (bw, bh)

# ---------------------------------------------------------------- shot
def build_shot(shot):
    reset()
    sc = bpy.context.scene
    W, H = shot['res']
    sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
    try: sc.render.engine = 'CYCLES'
    except TypeError as e: print('engine', e)
    cy = sc.cycles; cy.samples = shot.get('samples', 160); cy.use_denoising = True
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for kind in ('OPTIX', 'CUDA'):
            try:
                prefs.compute_device_type = kind; prefs.get_devices()
                for d in prefs.devices: d.use = d.type != 'CPU'
                if any(d.use for d in prefs.devices): break
            except TypeError: continue
        cy.device = 'GPU'
    except Exception as e: print('gpu', e)
    try: sc.view_settings.view_transform = 'Standard'
    except TypeError as e: print('view', e)
    sc.view_settings.look = 'None'
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'

    # camera looks along +Y from -D
    D = shot.get('cam_dist', 0.32)
    cam_d = bpy.data.cameras.new('Cam'); cam_d.lens = shot.get('lens', 50); cam_d.sensor_fit = 'AUTO'; cam_d.sensor_width = 36
    cam = bpy.data.objects.new('Cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (0, -D, 0); cam.rotation_euler = (math.radians(90), 0, 0)
    cam_d.dof.use_dof = True; cam_d.dof.focus_distance = D + shot.get('focus_off', 0.0); cam_d.dof.aperture_fstop = shot.get('fstop', 22)
    vfov_h = 36 / cam_d.lens  # frame height per metre of distance (portrait: height is the long side)
    aspect = W / H

    if shot['mode'] == 'photo':
        Bd = shot.get('backdrop_dist', 3.0)
        dist = D + Bd
        fh = vfov_h * dist * 1.06; fw = fh * aspect
        pl = ngon_obj('Backdrop', [(-fw / 2, -fh / 2), (fw / 2, -fh / 2), (fw / 2, fh / 2), (-fw / 2, fh / 2)])
        pl.rotation_euler = (math.radians(90), 0, 0); pl.location = (0, Bd, 0)
        pl.data.materials.append(mat_emit_image('Photo', shot['photo_crop'], shot.get('photo_gain', 1.0)))
        world_gradient((0.9, 0.95, 1.0), (0.35, 0.38, 0.40), 0.6)
        area_light('Key', (-0.35, -0.45, 0.45), (0, 0, 0), 0.6, shot.get('key', 18), (1.0, 0.97, 0.93))
        area_light('Rim', (0.40, 0.35, 0.25), (0, 0, 0), 0.3, shot.get('rim', 10), (0.95, 0.97, 1.0))
    else:
        Bd = shot.get('backdrop_dist', 0.22)
        dist = D + Bd
        fh = vfov_h * dist * 1.25; fw = fh * aspect
        pl = ngon_obj('Backdrop', [(-fw / 2, -fh / 2), (fw / 2, -fh / 2), (fw / 2, fh / 2), (-fw / 2, fh / 2)])
        pl.rotation_euler = (math.radians(90), 0, 0); pl.location = (0, Bd, 0)
        pl.data.materials.append(mat_backdrop_studio('Studio', shot.get('bg_top', (0.93, 0.96, 0.99)), shot.get('bg_bottom', (0.80, 0.88, 0.95))))
        world_gradient((1, 1, 1), (0.85, 0.9, 0.95), shot.get('world', 0.5))
        area_light('Key', (-0.25, -0.35, 0.40), (0, 0.1, 0), 0.35, shot.get('key', 22), (1.0, 0.98, 0.95))
        area_light('Fill', (0.35, -0.30, -0.05), (0, 0.1, 0), 0.5, shot.get('fill', 6), (0.92, 0.96, 1.0))
        # cards (sizes from the texture aspect)
        for i, c in enumerate(shot.get('cards', [])):
            img = load_img(c['tex']); iw, ih = img.size
            cw = c.get('w', 0.075); ch = cw * ih / iw
            ob = ngon_obj(f'Card{i}', rounded_rect(cw, ch, 0.0001, 1))
            ob.data.materials.append(mat_card(f'CardMat{i}', c['tex'], c.get('emit', 0.55)))
            ob.location = c['loc']; ob.rotation_euler = Euler([math.radians(90 + c.get('rx', 0)), math.radians(c.get('ry', 0)), math.radians(c.get('rz', 0))], 'XYZ')

    phone, _ = build_phone(shot['screen'], shot.get('screen_emit', 1.0))
    p = shot.get('phone', {})
    phone.location = p.get('loc', (0, 0, 0))
    s = p.get('scale', 1.0); phone.scale = (s, s, s)
    # base: face the camera; then lean back (x), turn (z), roll (y)
    phone.rotation_mode = 'XYZ'
    phone.rotation_euler = (math.radians(90 + p.get('lean', 0)), math.radians(p.get('roll', 0)), math.radians(p.get('turn', 0)))
    sc.render.filepath = shot['out']
    os.makedirs(os.path.dirname(shot['out']), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    print('RENDERED', shot['out'])

for shot in SPEC['shots']:
    if ONLY and shot['name'] not in ONLY: continue
    build_shot(shot)
