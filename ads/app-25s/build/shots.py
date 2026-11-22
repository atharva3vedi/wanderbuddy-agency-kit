"""Build and render one shot of the app-only 25 s ad.

  Blender -b --factory-startup -P build/shots.py -- <shot> [all | still <f> <f> ...]

Shots: panic, panic_ov (its headline layer, rendered without depth of field),
logo, docs, plan, ideas, assist, end. Frames are local to the shot (0 = the
shot's first frame in timeline.json). Output: $WB_OUT/<shot>/####.png
(default: render/ next to build/). RGBA over a transparent film, except the
end card, which is opaque brand blue; edit.py lays them over the grounds.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Euler, Matrix, Vector  # noqa: E402
from wb import *  # noqa: E402,F401,F403

SCALE = float(os.environ.get("WB_SAMPLES_SCALE", "1"))


def shot_len(sid):
    s = next(x for x in TL["shots"] if x["id"] == sid.replace("_ov", ""))
    return s["end"] - s["start"]


# --- headlines ---------------------------------------------------------------

HL = TL.get("layout", {}).get("headline", {"x": -830, "y": 40, "size": 88})


def headline(ov, lines, f_in, x=None, y=None, size=None, color=INK, slide=26):
    """Left-aligned WbSans Bold block, vertically centred on y (px)."""
    x = HL["x"] if x is None else x
    y = HL["y"] if y is None else y
    size = HL["size"] if size is None else size
    m = emit("headline", color, alpha=0.0)
    ob = text("headline", "\n".join(lines), BOLD, size * PX, m, ov, space_line=1.0)
    x0, y0, x1, y1 = local_bounds(ob)
    base_y = y * PX - (y0 + y1) / 2
    for f in range(f_in - 1, f_in + 14):
        t = out_cubic(prog(f, f_in, f_in + 12))
        key_transform(ob, f, loc=(x * PX, base_y - (1 - t) * slide * PX, 0.0))
        key_alpha(m, f, t)
    return ob


# --- the azure ring ----------------------------------------------------------

def add_ring(parent, cx, cy, w, h, r, stroke, f_in, z):
    m = emit("ring", AZURE, alpha=0.0)
    holder = empty("ring_holder", parent, (cx, cy, z))
    ring("ring", w, h, r, stroke, m, holder)
    for f in range(f_in - 1, f_in + 12):
        t = out_cubic(prog(f, f_in, f_in + 10))
        key_transform(holder, f, scale=lerp(1.07, 1.0, t))
        key_alpha(m, f, t)
    return holder


# --- app beats ---------------------------------------------------------------

def beat(bid):
    n = shot_len(bid)
    cfg = TL["beats"][bid]
    sc, cam = new_scene(n, samples=int(56 * SCALE), transparent=True, world=PAGE, world_strength=0.95)
    area("key", (-1.7, 2.0, 2.3), (0.45, -0.35, -0.5), 340, 1.4, "#FFFFFF")
    area("fill", (2.2, -0.6, 2.4), (0.3, 0.0, 0.0), 60, 3.0, "#EAF3FF")
    ov = overlay(cam)
    roots = []
    for i, p in enumerate(cfg["phones"]):
        m = emit(f"scr{i}", None, image=os.path.join(SCR, p["tex"]))
        root = phone(f"phone{i}", m)
        shadow_decal(f"shadow{i}", root, 1.37, 2.876, (0.11, -0.17, -0.42), opacity=0.30)
        roots.append((root, p))
    pop = None
    if "pop" in cfg:
        # The row that matters lifts off the screen into the middle of the frame.
        pc = cfg["pop"]
        pp = cfg["phones"][pc["phone"]]
        pop = empty("pop_root")
        side = solid("pop_side", "#13212F", rough=0.4)
        _, pw, ph = crop_slab("pop", os.path.join(SCR, pp["tex"]), pc["rect"], pc["r"] * PX, 14 * PX, side, pop)
        shadow_decal("pop_shadow", pop, pw * 0.92, ph * 0.85, (0.03, -0.06, -0.16), opacity=0.42)
        x0, y0, x1, y1 = pc["rect"]
        pop_home = on_screen((x0 + x1) / 2, (y0 + y1) / 2, 0.008)
    card = None
    if "card" in cfg:
        c = cfg["card"]
        cm = emit("card", None, image=os.path.join(SCR, c["tex"]))
        side = solid("card_side", "#DCE6EF", rough=0.4)
        card = empty("card_root")
        slab("card", c["w"] * PX, c["h"] * PX, 22 * PX, 10 * PX, cm, side, side, parent=card)
        shadow_decal("card_shadow", card, c["w"] * PX * 0.9, c["h"] * PX * 0.8, (0.02, -0.035, -0.10), opacity=0.22)
    # Every cut lands on a downbeat: the phone arrives with it, then drifts.
    for f in range(n):
        t = f / (n - 1)
        a = out_expo(prog(f, 0, 16))
        for k, (root, p) in enumerate(roots):
            lag = out_expo(prog(f, 2 * k, 16 + 2 * k))
            loc = (p["x"] * PX + lerp(0.010, -0.014, t),
                   p["y"] * PX + lerp(0.0, 0.026, t) - (1 - lag) * 0.11,
                   p["z"] - (1 - lag) * 0.10)
            rot = (rad(lerp(p["rx"][0], p["rx"][1], t)),
                   rad(lerp(p["ry"][0], p["ry"][1], t) + (1 - lag) * 9),
                   rad(lerp(-0.8, 0.6, t)))
            key_transform(root, f, loc=loc, rot=rot, scale=p["s"])
            if pop is not None and k == cfg["pop"]["phone"]:
                pc = cfg["pop"]
                q = out_cubic(prog(f, 8, 24))
                start = Matrix.LocRotScale(Vector(loc), Euler(rot), Vector((p["s"],) * 3)) @ pop_home
                end_ = Vector((pc["to"][0] * PX + lerp(0.0, -0.008, t), pc["to"][1] * PX + lerp(0.0, 0.014, t), pc["lift"]))
                prot = (lerp(rot[0], rad(lerp(5, 3, t)), q), lerp(rot[1], rad(lerp(-5, -2, t)), q), lerp(rot[2], rad(lerp(1.0, -0.5, t)), q))
                key_transform(pop, f, loc=start.lerp(end_, q), rot=prot, scale=lerp(p["s"], p["s"] * pc["s"], q))
        if card is not None:
            c = cfg["card"]
            ca = out_expo(prog(f, 8, 24))
            key_transform(card, f,
                          loc=(c["x"] * PX + (1 - ca) * 0.16 + lerp(0.0, -0.012, t),
                               c["y"] * PX - (1 - ca) * 0.05 + lerp(0.0, 0.016, t),
                               c["z"] + (1 - ca) * 0.06),
                          rot=(rad(lerp(4, 2, t)), rad(lerp(-9, -5, t) - (1 - ca) * 14), rad(lerp(0.6, -0.4, t))),
                          scale=c["s"] * lerp(0.92, 1.0, ca))
        key_transform(cam, f, loc=(lerp(0.0, 0.01, t), 0, D - 0.075 * in_out(t) - 0.03 * (1 - a)))
    headline(ov, cfg["headline"], 3)
    rg = cfg["ring"]
    x0, y0, x1, y1 = rg["rect"]
    if rg.get("pop"):
        cx0, cy0, cx1, cy1 = cfg["pop"]["rect"]
        cw, ch = (cx1 - cx0) * 1290 * PX, (cy1 - cy0) * 2796 * PX
        pad = 10 * PX
        add_ring(pop, (((x0 + x1) / 2 - cx0) / (cx1 - cx0) - 0.5) * cw, (0.5 - ((y0 + y1) / 2 - cy0) / (cy1 - cy0)) * ch,
                 (x1 - x0) / (cx1 - cx0) * cw + pad, (y1 - y0) / (cy1 - cy0) * ch + pad, rg["r"] * PX, 13 * PX,
                 cfg.get("ring_in", 26), 7 * PX + 0.0008)
    elif rg.get("card"):
        c = cfg["card"]
        w, h = c["w"] * PX, c["h"] * PX
        add_ring(card, ((x0 + x1) / 2 - 0.5) * w, (0.5 - (y0 + y1) / 2) * h,
                 (x1 - x0) * w, (y1 - y0) * h, rg["r"] * PX, 7 * PX, 27, 5 * PX + 0.0008)
    else:
        root = roots[rg["phone"]][0]
        a, b = on_screen(x0, y0), on_screen(x1, y1)
        add_ring(root, (a.x + b.x) / 2, (a.y + b.y) / 2, b.x - a.x, a.y - b.y, rg["r"] * PX, 13 * PX, 18, a.z)
    return sc, n


# --- the WanderBuddy logo after the panic ------------------------------------

LG = TL.get("layout", {}).get("logo", {"m0": 250, "m1": 190})
LOGO_M0, LOGO_M1 = LG["m0"], LG["m1"]


def logo():
    n = shot_len("logo")
    sc, cam = new_scene(n, samples=int(24 * SCALE), transparent=True, world=PAGE)
    ov = overlay(cam)
    gap = 0.30 * LOGO_M1
    ww = 0.656 * LOGO_M1 * 134 / 21
    total = LOGO_M1 + gap + ww
    mx = -total / 2 + LOGO_M1 / 2
    lock = empty("lockup", ov)
    holder = empty("mark_holder", lock)
    tile, peaks, wave, _ = mark(holder, LOGO_M1)
    set_mat(tile, emit("tile", FIELD))
    white = emit("white", "#FFFFFF")
    set_mat(peaks, white)
    set_mat(wave, white)
    wm = emit("word", INK, alpha=0.0)
    glyphs, wg, _ = word(lock, LOGO_M1, (mx + LOGO_M1 / 2 + gap) * PX, mat=wm)
    wg.location.z = -0.003  # behind the tile: the word slides out from under it
    for f in range(n):
        t = in_out(prog(f, 2, 16))
        key_transform(holder, f, loc=(lerp(0.0, mx * PX, t), 0, 0), scale=lerp(LOGO_M0 / LOGO_M1, 1.0, t))
        key_alpha(wm, f, out_cubic(prog(f, 7, 19)))
        key_transform(lock, f, scale=lerp(1.0, 1.025, f / (n - 1)))
    base = wg.location.copy()
    for f in range(n):
        w = out_cubic(prog(f, 7, 19))
        key_transform(wg, f, loc=(base.x + (1 - w) * 0.05, base.y, base.z))
    return sc, n


# --- the end card --------------------------------------------------------------

def end():
    n = shot_len("end")
    sc, cam = new_scene(n, samples=int(24 * SCALE), transparent=False, world=FIELD)
    ov = overlay(cam)
    E = TL.get("layout", {}).get("end", {"m": 200, "mm": 236, "y": 40, "lines": [
        {"text": "wanderbuddyapp.com/partners", "font": "semi", "size": 46, "y": -175, "color": "#DCEBFA", "f": [28, 40]}]})
    M = E["m"]       # sets the word, as in brand.css
    MM = E["mm"]     # the white mark alone reads small without its tile
    gap = 0.18 * M
    ww = 0.656 * M * 134 / 21
    total = MM + gap + ww
    mx, my = -total / 2 + MM / 2, E["y"]
    holder = empty("mark_holder", ov, (mx * PX, my * PX, 0))
    _, peaks, wave, _ = mark(holder, MM, tile=False)
    pm, wvm = emit("peaks", "#FFFFFF"), emit("wave", "#FFFFFF", alpha=0.0)
    set_mat(peaks, pm)
    set_mat(wave, wvm)
    # The sea: brand blue in front of the peaks, behind the wave, below the peaks' base.
    # Only as wide as the peaks (x 224-800 of the 1024 tile), so it never covers the word.
    sea = plane("sea", 0.62 * MM * PX, 0.5 * MM * PX, emit("sea", FIELD), holder)
    sea.location = (0, -0.25 * MM * PX, 0.0009)
    wm = emit("word", "#FFFFFF", alpha=0.0)
    glyphs, wg, _ = word(ov, M, (mx + MM / 2 + gap) * PX, my * PX, mat=wm)
    fonts = {"bold": BOLD, "semi": SEMI, "reg": REG}
    lines = []
    for i, ln in enumerate(E["lines"]):
        lm = emit(f"line{i}", ln["color"], alpha=0.0)
        lo = text(f"line{i}", ln["text"], fonts[ln["font"]], ln["size"] * PX, lm, ov, align="CENTER")
        lines.append((lo, lm, ln))
    p0 = peaks.location.copy()
    w0 = wave.location.copy()
    g0 = wg.location.copy()
    k = peaks.parent.scale.x
    for f in range(n):
        a = out_cubic(prog(f, 5, 22))
        key_transform(peaks, f, loc=(p0.x, p0.y - (1 - a) * 0.34 * MM * PX / k, p0.z))
        b = out_cubic(prog(f, 11, 25))
        key_transform(wave, f, loc=(w0.x, w0.y - (1 - b) * 0.05 * MM * PX / k, w0.z))
        key_alpha(wvm, f, b)
        c = out_cubic(prog(f, 17, 31))
        key_transform(wg, f, loc=(g0.x, g0.y - (1 - c) * 0.03, g0.z))
        key_alpha(wm, f, c)
        for lo, lm, ln in lines:
            d = out_cubic(prog(f, ln["f"][0], ln["f"][1]))
            key_transform(lo, f, loc=(0, ln["y"] * PX - (1 - d) * 0.012, 0))
            key_alpha(lm, f, d)
    return sc, n


# --- the panic -------------------------------------------------------------------

AVATAR = {"Maya": "#D96AA7", "Leo": "#2FB5A8", "Priya": "#E8765C", "Sam Reed": "#3FA7E6", "Maya Reed": "#D96AA7", "Ken Walsh": "#4CB782", "Chloe Evans": "#8E7CF0",
          "Ana Costa": "#E8765C", "Leo Martin": "#2FB5A8", "Mia Novak": "#5B8DEF", "Tom Walker": "#7F93A8"}
PP = TL["panic"]
PANIC_SCALE = PP.get("phone_scale", 0.30)
CARD_SCALE = PP.get("card_scale", 1.0)
SPREAD = PP.get("spread", [0.82, 0.46])
MANUAL = [(-0.56, 0.31, 0.06, -6, 9, 3), (0.50, 0.17, 0.13, 4, -11, -2), (-0.52, -0.21, 0.20, -3, 12, 2),
          (0.57, -0.31, 0.03, 5, -9, -3), (0.03, 0.44, -0.30, 6, 3, 1), (-0.13, -0.45, 0.33, -4, 6, -2),
          (0.50, 0.47, -0.52, 3, -6, 2), (-0.82, 0.03, -0.42, -2, 11, -1)]


def panic_card(i, spec, parent, mats):
    root = empty(f"card{i}", parent)
    pad, av, gap = 30, 70, 24
    # A group chat shows as "Group" over "Name: message", like a phone notification.
    group = PP.get("group")
    title = group or spec["who"]
    say = f"{spec['who']}: {spec['say']}" if group else spec["say"]
    nm = text(f"name{i}", title, SEMI, 27 * PX, mats["name"], root)
    tm = text(f"time{i}", spec["at"], REG, 24 * PX, mats["time"], root)
    ms = text(f"msg{i}", say, REG, 38 * PX, mats["msg"], root)
    nw, tw, mw = text_width(nm), text_width(tm), text_width(ms)
    badge = spec.get("badge")
    content = max(nw + 40 * PX + tw, mw + (70 * PX if badge else 0))
    cw = (pad + av + gap + pad) * PX + content
    ch = 150 * PX
    slab(f"face{i}", cw, ch, 34 * PX, 8 * PX, mats["face"], mats["side"], mats["side"], parent=root)
    zf = 4.6 * PX
    left = -cw / 2 + pad * PX
    col = AVATAR.get(spec["who"], "#5B8DEF")
    if col not in mats:
        mats[col] = emit("av" + col, col)
    a = disc(f"av{i}", av / 2 * PX, mats[col], root)
    a.location = (left + av / 2 * PX, 0, zf)
    ini = "".join(w[0] for w in spec["who"].split()[:2])
    it = text(f"ini{i}", ini, BOLD, 26 * PX, mats["white"], root, align="CENTER")
    it.location = (left + av / 2 * PX, -9.5 * PX, zf + 0.3 * PX)
    tx = left + (av + gap) * PX
    nm.location = (tx, ch / 2 - (pad + 24) * PX, zf)
    ms.location = (tx, -ch / 2 + (pad + 10) * PX, zf)
    tm.location = (cw / 2 - pad * PX - tw, ch / 2 - (pad + 24) * PX, zf)
    if badge:
        bx, by = cw / 2 - (pad + 22) * PX, -ch / 2 + (pad + 22) * PX
        b = disc(f"badge{i}", 22 * PX, mats["red"], root)
        b.location = (bx, by, zf)
        bt = text(f"bn{i}", str(badge), BOLD, 26 * PX, mats["white"], root, align="CENTER")
        bt.location = (bx, by - 9.5 * PX, zf + 0.3 * PX)
    return root


def panic():
    P = TL["panic"]
    n = shot_len("panic")
    sc, cam = new_scene(n, samples=int(96 * SCALE), transparent=True, world="#0B141F", world_strength=0.55, mblur=True)
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = P.get("fstop", 2.4)
    area("key", (-1.6, 1.8, 2.2), (0, 0, 0), 90, 1.3, "#DCEBFF")
    area("edge", (1.9, 1.2, -0.6), (0, 0, 0), 140, 1.6, "#9CC9EE")
    scr = emit("lock", "#05080C")
    ph = phone("phone", scr)
    lockm = emit("locktext", D_INK, alpha=1.0)
    datem = emit("date", D_INK2, alpha=1.0)
    p = on_screen(0.5, 0.135)
    lock = P.get("lock", {"date": "Tuesday 11 March", "time": "05:02"})
    dt = text("date", lock["date"], SEMI, 64 * PX, datem, ph, align="CENTER")
    dt.location = p
    p = on_screen(0.5, 0.255)
    tt = text("time", lock["time"], SEMI, 310 * PX, lockm, ph, align="CENTER")
    tt.location = p
    # The app icon the questions collapse into (the real mark, matched to the next shot's first frame).
    holder = empty("icon", ph, on_screen(0.5, 0.5, 0.0012))
    tile, peaks, wave, _ = mark(holder, LOGO_M0 / PANIC_SCALE)
    tm, wm = emit("tile", FIELD, alpha=0.0), emit("iconwhite", "#FFFFFF", alpha=0.0)
    set_mat(tile, tm)
    set_mat(peaks, wm)
    set_mat(wave, wm)
    mats = {"name": emit("name", D_MUTED), "time": emit("time", "#6F8AA3"), "msg": emit("msg", D_INK),
            "face": emit("face", D_SURFACE), "side": solid("side", "#0E1A26", rough=0.5),
            "white": emit("white", "#FFFFFF"), "red": emit("red", "#E0483C")}
    rnd = random.Random(7)
    cards = []
    for i, spec in enumerate(P["cards"]):
        root = panic_card(i, spec, None, mats)
        manual = P.get("manual", MANUAL)
        if i < len(manual):
            x, y, z, rx, ry, rz = manual[i]
        else:
            z = rnd.uniform(0.35, 0.95) if i >= len(P["cards"]) - 6 else rnd.uniform(-1.3, 0.55)
            depth = (D + 0.2 - z) / D
            x = rnd.uniform(-SPREAD[0], SPREAD[0]) * depth
            y = rnd.uniform(-SPREAD[1], SPREAD[1]) * depth
            rx, ry, rz = rnd.uniform(-8, 8), rnd.uniform(-14, 14), rnd.uniform(-5, 5)
        v = Vector((math.copysign(0.0007, x) + rnd.uniform(-0.0003, 0.0003),
                    math.copysign(0.0004, y) + rnd.uniform(-0.0002, 0.0002), rnd.uniform(0.0008, 0.0016)))
        cards.append((root, spec["f"], Vector((x, y, z)), (rad(rx), rad(ry), rad(rz)), v, i))
    c0, c1 = P["collapse"]
    ti0, ti1 = P["tile_in"]
    buzz = [3, 22, 46, 69, 92, 118, 146]
    for f in range(n):
        # Camera: a slow handheld push that settles square on the phone for the cut.
        t = in_out(prog(f, 0, 180))
        s = in_out(prog(f, 176, 204))
        hand = (1 - s)
        cx = lerp(P.get("cam_x0", 0.11), 0.0, t) + hand * (0.006 * math.sin(f * 0.21) + 0.004 * math.sin(f * 0.37 + 1))
        cy = lerp(-0.05, 0.0, t) + hand * (0.005 * math.sin(f * 0.17 + 2) + 0.003 * math.sin(f * 0.43))
        cz = lerp(D + 0.32, D - 0.06, t)
        cz = lerp(cz, D, s)
        cx, cy = lerp(cx, 0.0, s), lerp(cy, 0.0, s)
        roll = rad(lerp(-2.6, 0.8, t) + hand * 0.25 * math.sin(f * 0.15))
        key_transform(cam, f, loc=(cx, cy, cz), rot=(0, 0, lerp(roll, 0.0, s)))
        cam.data.dof.focus_distance = cz - PANIC_SCALE * SCREEN_Z
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        # The phone buzzes with each burst, then squares up.
        jit = 0.0
        for b in buzz:
            if b <= f < b + 9:
                jit = (1 if (f - b) % 2 else -1) * 1.4 * (1 - (f - b) / 9)
        e = in_out(prog(f, 150, 200))
        key_transform(ph, f, loc=(jit * 0.0015, 0, 0),
                      rot=(rad(lerp(-9, 0, e)), rad(lerp(11, 0, e)), rad(lerp(-3, 0, e) + jit)), scale=PANIC_SCALE)
        la = 1 - prog(f, 184, 194)
        key_alpha(lockm, f, la)
        key_alpha(datem, f, la)
        ia = out_cubic(prog(f, ti0, ti1))
        key_alpha(tm, f, ia)
        key_alpha(wm, f, ia)
        # The questions: out of the phone, drifting, then back into it.
        home = Vector((0, 0, 0.02))
        for root, fs, tgt, rot, v, i in cards:
            d0 = c0 + (i * 3) % 7
            d1 = min(c1, d0 + 14)
            if f < fs:
                key_transform(root, f, loc=home, rot=(0, 0, 0), scale=0.0)
                continue
            a = out_expo(prog(f, fs, fs + 13))
            pos = home.lerp(tgt, a) + v * max(0, f - fs)
            r = tuple(c * a + 0.0016 * (f - fs) * (1 if i % 2 else -1) for c in rot)
            sc_ = lerp(0.18, 1.0, a)
            if f >= d0:
                q = in_cubic(prog(f, d0, d1))
                pos = pos.lerp(home, q)
                sc_ = lerp(sc_, 0.04, q)
                if f >= d1:
                    sc_ = 0.0
            key_transform(root, f, loc=pos, rot=r, scale=sc_ * CARD_SCALE)
    return sc, n


def panic_ov():
    """The panic's headline and scrim, sharp (the main pass has depth of field)."""
    P = TL["panic"]
    n = shot_len("panic")
    sc, cam = new_scene(n, samples=int(24 * SCALE), transparent=True, world="#000000", world_strength=0.0)
    ov = overlay(cam)
    sm = emit("scrim", "#03060A", alpha=0.0)
    s = plane("scrim", W / 1000 * 1.2, H / 1000 * 1.2, sm, ov)
    s.location.z = -0.002
    f_in = P["headline_in"]
    hm = emit("hl", "#FFFFFF", alpha=0.0)
    lines = P["headline"]
    if all(isinstance(x, str) for x in lines):       # ["sans part", "serif word"] on one line
        lines = [[lines[0] + " ", lines[1]]]
    sz_a, sz_b = P.get("headline_size", [92, 124])
    lh = sz_a * 1.18 * PX
    hy = P.get("headline_y", 0) * PX
    gap = 22 * PX
    objs = []
    for i, (ta, tb) in enumerate(lines):
        a = text(f"hl_a{i}", ta, BOLD, sz_a * PX, hm, ov) if ta.strip() else None
        b = text(f"hl_b{i}", tb, SERIF, sz_b * PX, hm, ov) if tb.strip() else None
        wa = text_width(a) if a else 0.0
        wb_ = text_width(b) if b else 0.0
        g = gap if (a and b) else 0.0
        x0 = -(wa + g + wb_) / 2
        base = hy + ((len(lines) - 1) / 2 - i) * lh - 0.35 * sz_a * PX
        objs.append((a, b, x0, x0 + wa + g, base))
    for f in range(n):
        sa = 0.66 * (in_out(prog(f, f_in - 6, f_in + 8)) - in_out(prog(f, 180, 192)))
        key_alpha(sm, f, max(0.0, sa))
        h = out_cubic(prog(f, f_in, f_in + 12)) * (1 - in_out(prog(f, 176, 186)))
        dy = (1 - out_cubic(prog(f, f_in, f_in + 12))) * -24 * PX
        key_alpha(hm, f, h)
        for a, b, xa, xb, base in objs:
            if a:
                key_transform(a, f, loc=(xa, base + dy, 0))
            if b:
                key_transform(b, f, loc=(xb, base + dy, 0))
    return sc, n


BUILD = {"panic": panic, "panic_ov": panic_ov, "logo": logo, "end": end}
for _bid in TL["beats"]:
    BUILD[_bid] = (lambda b: (lambda: beat(b)))(_bid)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    sid = argv[0]
    mode = argv[1] if len(argv) > 1 else "all"
    out = os.path.join(os.environ.get("WB_OUT", os.path.join(AD, "render")), TL.get("prefix", "") + sid)
    os.makedirs(out, exist_ok=True)
    sc, n = BUILD[sid]()
    for ob in bpy.data.objects:
        linear_keys(ob)
    if mode == "still":
        for f in [int(x) for x in argv[2:]]:
            sc.frame_set(f)
            sc.render.filepath = os.path.join(out, f"still_{f:04d}.png")
            bpy.ops.render.render(write_still=True)
            print("STILL", sc.render.filepath)
    else:
        sc.render.filepath = os.path.join(out, "")
        bpy.ops.render.render(animation=True)
        print("DONE", sid, n)


main()
