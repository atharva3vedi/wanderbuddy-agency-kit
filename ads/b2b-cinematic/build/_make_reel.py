"""One-off: writes build/reel.py from build/opened.py (same office and phone sets, new screens,
a new set for the itinerary pages, new timing). Edit reel.py directly afterwards."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "opened.py")).read()


def cut(a, b, new):
    global s
    i = s.index(a)
    j = s.index(b, i)
    s = s[:i] + new + s[j:]


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


cut('"""Second pass, film 3', 'import math', '''"""Second pass, film 6, The Reel: the itinerary maker and the assistant.

  Blender -b --factory-startup -P build/reel.py -- [still f f ...]

23:40: a traveller sends Lantern Trips a reel and one question (her phone: set dressing,
screens/reel/reel_dm.png). In the office the real CRM (build/reel_capture.mjs): the
conversation with "Turn into a proposal", then its panel reading the reel, pricing from
past trips and writing the plan. Then the plan itself: the fourteen real pages of the
itinerary (build/reel_pages.mjs) sliding out across a dark desk. Then Home: she picked an
option and tapped Book. Then the inbox on the trip: her question answered from the trip
plan at 23:48. Last, the pages squared in a stack at dawn.
Frames: render/reel/3d/####.png, 0..767.
"""
''')
cut('N = 650', 'LAP = Vector(', '''N = 768                                 # 32 s
OUT = os.path.join(AD, "render", "reel", "3d")
SCRA = os.path.join(SCR, "reel")
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
RB, RB2, RC, RD, RE, RF = 96, 156, 240, 432, 552, 672   # her phone | the chat | the panel | the pages | Home | on the trip | dawn
F_DONE, F_REPLY = 184, 580              # the panel finishes, the assistant's answer arrives
R1, R2, R3, R4 = RB + 16, 196, RD + 20, 596   # the four rings: the button, the plan, Book, the answer
P1, P2 = (-100, -90), (-100, -90)
F_WIN = 10 ** 6                         # no street shot in this film
HOSTEL = Vector((0.0, 60.0, 0.5))       # her bunk
PG = Vector((0.0, 90.0, 0.75))          # the desk the plan is laid out on
PGW = 0.297
PGH = 0.297 * 1860 / 2616
''')
# her phone: the reel and her question
cut('    la_m = emit("list_a"', '    area("bunk_window"', '''    la_m = emit("list_a", image=os.path.join(SCRA, "reel_dm.png"))
    la = slab("list_a", PW, PH, 165 * PH_PX, 0.00002, la_m, la_m, la_m, parent=pht)
    la.location = (0, 0, 0.0039 + 0.00012)
''')
rep('duvet.data.materials.append(principled("duvet", "#263A33", rough=0.95, bump=(380, 0.35, 2)))   # a sofa, not the bunk',
    'duvet.data.materials.append(principled("duvet", "#1F3048", rough=0.95, bump=(380, 0.35, 2)))')
# the laptop: five screens, four rings
cut('    scr_m = emit("screen"', '    glow = area("screen_light"', '''    scr_m = emit("screen", image=os.path.join(SCRA, "thread.png"))
    scr = plane("lap_screen", SW, SH, scr_m, hinge)
    scr.location = (0, 0.1075 + 0.006, -0.0004)
    scr.rotation_euler = (0, math.pi, 0)
    later = []                                                # (material, from frame, fade frames)
    for k, (nm, f0, fd) in enumerate((("proposal_run", RB2, 0), ("proposal_done", F_DONE, 0), ("home_book", RD, 0), ("inbox_q", RE, 0), ("inbox_qa", F_REPLY, 9))):
        m_ = emit(nm, image=os.path.join(SCRA, nm + ".png"), alpha=0.0)
        pl_ = plane(nm, SW, SH, m_, scr)
        pl_.location = (0, 0, 0.0003 + 0.00006 * k)
        later.append((m_, f0, fd))
    rings = []
    for k, ((x, y, w, h), f_in, f_out, rad_) in enumerate((((1068, 782, 166, 30), R1, RB2, 0.0028), ((1065, 471, 511, 240), R2, RC, 0.004),
                                                         ((305, 414, 687, 60), R3, RE, 0.003), ((796, 277, 451, 118), R4, RF, 0.0042))):
        rm_ = emit(f"ring{k}", AZURE, alpha=0.0)
        rh_ = empty(f"ring{k}_h", scr, (*px(x + w / 2, y + h / 2), 0.0009))
        ring(f"ring{k}", w / 1600 * SW + 0.003, h / 1000 * SH + 0.003, rad_, 0.0011, rm_, rh_)
        ring_in(rh_, rm_, f_in, 10)
        fade_mat(rm_, f_out - 1, 1.0)                           # gone on the cut
        fade_mat(rm_, f_out, 0.0)
        rings.append(rm_)
''')
cut('    # --- the phones behind the shutters', '    tubes = []', '''    # --- the plan: the fourteen real pages, on a dark desk of their own -----------------------
    walnut = principled("walnut", "#2A2019", rough=0.42, bump=(70, 0.04))
    noisy_color(walnut, "#1F1711", "#3A2C22", scale=5.0, detail=10)
    box("plan_desk", (3.6, 3.6, 0.06), (PG.x, PG.y, PG.z - 0.03), walnut)
    pages = []
    rp_ = random.Random(4)
    for k in range(14):
        pm_ = principled(f"page{k}", "#FFFFFF", rough=0.8, image=os.path.join(SCR, "reel", "pages", f"pg{k:02d}.png"))
        bs_ = next(n for n in pm_.node_tree.nodes if n.type == "BSDF_PRINCIPLED")       # keep the page's own colours under a cool light
        tx_ = next(n for n in pm_.node_tree.nodes if n.type == "TEX_IMAGE")
        pm_.node_tree.links.new(tx_.outputs["Color"], bs_.inputs["Emission Color"])
        bs_.inputs["Emission Strength"].default_value = 0.22
        ob_ = plane(f"page{k}", PGW, PGH, pm_)
        col, row = k % 2, k // 2
        z_ = PG.z + 0.0005 * (15 - k)                           # the cover on top of the stack
        slot = Vector((PG.x + (col - 0.5) * (PGW + 0.022), PG.y + (3 - row) * (PGH + 0.016), z_))
        pages.append(dict(ob=ob_, slot=slot, z=z_, tilt=rad(rp_.uniform(-5, 5)), end=Vector((PG.x + rp_.uniform(-0.003, 0.003), PG.y + rp_.uniform(-0.003, 0.003), z_)), yaw=rad(rp_.uniform(-1.6, 1.6))))
    COVER = pages[0]["slot"]
    plan_key = area("plan_key", (PG.x + 1.1, PG.y - 0.9, PG.z + 4.8), PG, 2600, 1.8, color="#E9F0FA")
    plan_dawn = spot("plan_dawn", (PG.x - 2.4, PG.y + 0.9, PG.z + 0.85), PG, 0.0, angle=36, blend=0.6, radius=0.05, color="#FFCFA0")

''')
cut('    # --- animation ---', '    all_linear()', '''    # --- animation ----------------------------------------------------------------------
    nsun.data.energy = 0.3
    glow.data.energy = 9.0
    for f in range(N):
        fade_mat(rain_m, f, 0.1)
        rain.location = (0, 0, -((f * 0.44) % TILE))
        rain.keyframe_insert("location", frame=f)
        for m_, f0, fd in later:                                  # the laptop's screens, one after another
            fade_mat(m_, f, (smooth(prog(f, f0, f0 + fd)) if fd else 1.0) if f >= f0 else 0.0)
        # the plan slides out, page by page; at dawn it is one stack
        for k, P in enumerate(pages):
            if f >= RF:
                pos, rz = P["end"], P["yaw"]
            else:
                s_ = RC + 14 + 7 * (k - 1)
                t = out_cubic(prog(f, s_, s_ + 18)) if k else 0.0
                pos = Vector((lerp(COVER.x, P["slot"].x, t), lerp(COVER.y, P["slot"].y, t), P["z"]))
                rz = P["tilt"] * (1 - t)
            key(P["ob"], f, loc=pos, rot=(0.0, 0.0, rz))
        dawn_ = 1.0 if f >= RF else 0.0
        plan_key.data.energy = 2600 * (1 - 0.72 * dawn_)
        plan_key.data.keyframe_insert("energy", frame=f)
        plan_dawn.data.energy = 900.0 * dawn_
        plan_dawn.data.keyframe_insert("energy", frame=f)

    # --- camera --------------------------------------------------------------------------
    bpy.context.view_layer.update()
    marks = {}
    for nm, (x, y) in (("chat", (934, 640)), ("panel", (1320, 300)), ("home", (648, 300)), ("inbox", (934, 302))):
        marks[nm] = empty(nm + "_c", scr, (*px(x, y), 0.0))
    bpy.context.view_layer.update()
    C = {k: v.matrix_world.translation.copy() for k, v in marks.items()}
    nrm = Vector((0, math.sin(rad(OPEN)), -math.cos(rad(OPEN))))
    pc = PT + Vector((0, 0, 0.004))
    up = Vector((0, 0, 1))
    # (frame, position, look at, lens, f-stop, focus point)
    shots = [
        (0, pc + Vector((0.004, 0.115, 0.47)), pc + Vector((0.0, -0.011, 0)), 50, 4.0, pc),
        (RB - 1, pc + Vector((0.003, 0.1, 0.425)), pc + Vector((0.0, -0.010, 0)), 50, 4.0, pc),
        (RB, C["chat"] + nrm * 0.46, C["chat"], 50, 2.8, C["chat"]),
        (RB2 - 1, C["chat"] + nrm * 0.44, C["chat"], 50, 2.8, C["chat"]),
        (RB2, C["panel"] + nrm * 0.41, C["panel"], 50, 2.8, C["panel"]),
        (RC - 1, C["panel"] + nrm * 0.395, C["panel"], 50, 2.8, C["panel"]),
        (RC, COVER + up * 1.33 + Vector((0, -0.0005, 0)), COVER, 50, 8.0, COVER),
        (RC + 160, PG + up * 3.75 + Vector((0, -0.0005, 0)), PG, 50, 8.0, PG),
        (RD - 1, PG + up * 3.86 + Vector((0, -0.0005, 0)), PG, 50, 8.0, PG),
        (RD, C["home"] + nrm * 0.5, C["home"], 50, 2.8, C["home"]),
        (RE - 1, C["home"] + nrm * 0.485, C["home"], 50, 2.8, C["home"]),
        (RE, C["inbox"] + nrm * 0.47, C["inbox"], 50, 2.8, C["inbox"]),
        (RF - 1, C["inbox"] + nrm * 0.445, C["inbox"], 50, 2.8, C["inbox"]),
        (RF, PG + up * 1.3 + Vector((0, -0.0005, 0)), PG + Vector((0, 0.02, 0)), 50, 8.0, PG),
        (N - 1, PG + up * 1.16 + Vector((0, -0.0005, 0)), PG + Vector((0, 0.02, 0)), 50, 8.0, PG),
    ]
    MOVES = (RC,)
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
''')
rep('bpy.context.scene.render.use_motion_blur = (f + 1) not in (TD, F_SWAP, TE, TF)', 'bpy.context.scene.render.use_motion_blur = (f + 1) not in (RB, RB2, RC, RD, RE, RF)')
for bad in ("TB", "TC", "TD", "TE", "TF", "OPENS", "LOCK", "UP1", "UP2", "F_SWAP", "F_RING", "F_RING2", "F_WAKE", "lb_m", "later_m", "board_m", "lock_m", "pl1", "pl2", "ph2_m", "rake", "shutters", "tubes", "hands"):
    hits = [m.start() for m in re.finditer(r"\b" + bad + r"\b", s)]
    if hits:
        print(bad, len(hits), [s[h - 60:h + 50].replace("\n", " ") for h in hits[:2]])
open(os.path.join(HERE, "reel.py"), "w").write(s)
print("wrote reel.py", len(s))
