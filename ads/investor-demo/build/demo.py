"""Investor demo "One trip, both sides": the 3D layer. Blender 5.3, EEVEE, 1920 x 1080, 24 fps.

A paper map of Southeast Asia on a table. Lantern Trips' laptop sits on Krabi, the
traveller's phone on Singapore. One trip goes back and forth along an azure arc and
every hop lands as a real WanderBuddy screen. Captions, the lockup, the model lines
and the end card are the HTML overlay (overlay.html), not this file.

  B=/Applications/Blender.app/Contents/MacOS/Blender
  $B -b --factory-startup -P build/demo.py -- stills 3,9,13.5,25.5   # times in seconds (WB_QUICK=1: half size)
  $B -b --factory-startup -P build/demo.py -- anim                   # frames 0..END to render/3d (WB_FROM/WB_TO/WB_RESUME)

Shared helpers come from ../../b2b-cinematic/build/film.py. Every moving thing is a
pure function of t, keyed on every frame, so motion blur and any re-render agree.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Quaternion, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
sys.path.insert(0, os.path.normpath(os.path.join(AD, "../b2b-cinematic/build")))
import film  # noqa: E402
from film import (box, clamp, emit, empty, key_val, lerp, lin, link, out_cubic, plane, principled,  # noqa: E402
                  prog, rad, ring, slab, smooth, smoother, sun)

film.W, film.H = 1920, 1080
FPS = 24
SCR = os.path.join(AD, "screens")
END_T = 80.0                  # the end card covers everything after this (old timeline, before the friends' act)
# WB_ACT=1 renders only the friends' act (the B2C flow), which is inserted into the timeline at
# 7.0 s; the agency film after it keeps its frames, shifted by ACT_LEN (see compose.sh).
ACT = os.environ.get("WB_ACT") == "1"
ACT_T0, ACT_LEN = 7.0, 33.0
NF = int(END_T * FPS) + 1     # frames 0..1920
QUICK = film.QUICK


def S(name):
    return os.path.join(SCR, name)


def F(t):
    return int(round(t * FPS))


def win(t, a, b, fi=0.25, fo=0.25):
    """1 inside [a, b] with smooth ramps."""
    return min(smooth(prog(t, a, a + fi)), 1 - smooth(prog(t, b - fo, b)))


V = Vector

# --- geography ----------------------------------------------------------------

MAP = json.load(open(S("map.json")))
KX = math.cos(math.radians(MAP["LATC"]))
M_DEG = 0.1                                       # metres per degree of latitude
MW = (MAP["LON1"] - MAP["LON0"]) * KX * M_DEG
MH = (MAP["LAT1"] - MAP["LAT0"]) * M_DEG


def _geo0(lon, lat):
    return V(((lon - MAP["LON0"]) * KX * M_DEG - MW / 2, (lat - MAP["LAT0"]) * M_DEG - MH / 2, 0))


_k0, _s0 = _geo0(*MAP["cities"]["krabi"]), _geo0(*MAP["cities"]["singapore"])
ORIGIN = (_k0 + _s0) / 2


def geo(lon, lat):
    return _geo0(lon, lat) - ORIGIN


KRABI = geo(*MAP["cities"]["krabi"])
SING = geo(*MAP["cities"]["singapore"])

# --- the timeline (seconds) ---------------------------------------------------

LID = (7.2, 8.8)                 # the laptop opens
WAKE = 7.8                       # the phone wakes
ARC_DRAW = (16.8, 18.6)          # the listing goes out, Krabi -> Singapore
DOTS = [(30.2, 31.8, -1), (45.0, 46.6, 1), (60.0, 61.6, -1)]  # (from, to, direction): +1 Krabi->Singapore
NIGHT = (57.6, 59.4)
DAY = (69.4, 71.2)

# laptop screen: (time it shows, image); phone screen likewise ('market' scrolls)
LAP_SHOTS = [(0.0, "crm-app_dashboard.png"), (11.2, "listings.png"), (31.7, "inboxHold.png"), (38.0, "itinerary.png"),
             (61.7, "crm-inbox_assistant_pickup.png"), (69.6, "listings.png")]
PH_SHOTS = [(0.0, "lockEve.png"), (18.6, "market"), (46.6, "app-home.png"), (50.6, "app-documents.png"),
            (53.6, "app-chat.png"), (58.0, "lock2347.png"), (67.45, "lock2348.png"), (70.4, "app-home.png")]
# the friends' act: the group chat, then the four things the app does for a friend group
PH_SHOTS_ACT = [(0.0, "lockCrew.png"), (10.0, "b2c_dates.png"), (14.6, "b2c_vote.png"),
                (19.0, "b2c_igconnect.png"), (22.8, "igDM.png"), (26.8, "b2c_reels.png"),
                (31.2, "b2c_budget.png"), (35.6, "b2c_live.png")]
LAP_ON = 8.3                     # the laptop screen lights as the lid opens

# --- camera poses -------------------------------------------------------------

LAP_POS = KRABI + V((0.075, 0.175, 0.0))
LAP_YAW = 12.0
LID_OPEN, LID_SHUT = 75.0, 180.0
PH_SCALE = 1.25
PH_POS = SING + V((0.012, 0.072, 0.0))
PH_LEAN = 16.0
PH_YAW = -4.0


def lap_frame(lid=LID_OPEN):
    m_lap = Matrix.Translation(LAP_POS) @ Matrix.Rotation(rad(LAP_YAW), 4, "Z")
    m_h = m_lap @ Matrix.Translation((0, 0.122, 0.011)) @ Matrix.Rotation(rad(lid), 4, "X")
    return m_lap, m_h, m_h @ Matrix.Translation((0, 0.122, -0.0003))


def ph_frame():
    """The phone's world matrix: upright, leaning back PH_LEAN, its bottom edge on the map."""
    half = (2796 * film.PH_PX + 80 * film.PH_PX) / 2 * PH_SCALE
    tilt = rad(90 - PH_LEAN)
    up = V((0, math.cos(tilt), math.sin(tilt)))       # the phone's +Y after the lean (before yaw)
    rz = Matrix.Rotation(rad(PH_YAW), 4, "Z")
    centre = PH_POS + (rz.to_3x3() @ up) * half + V((0, 0, 0.0042 * PH_SCALE))
    return Matrix.Translation(centre) @ rz @ Matrix.Rotation(tilt, 4, "X") @ Matrix.Scale(PH_SCALE, 4)


_, _, M_LSCR = lap_frame()
M_PH = ph_frame()
LS_W, LS_H = 0.334, 0.2088
PS_W, PS_H = film.PW * PH_SCALE, film.PH * PH_SCALE


def screen_basis(m, z_off=0.0):
    r = m.to_3x3().normalized()
    c = m @ V((0, 0, z_off))
    return c, (r @ V((1, 0, 0))).normalized(), (r @ V((0, 1, 0))).normalized(), (r @ V((0, 0, 1))).normalized()


def pose_on(m, z_off, dist, lens, shift_x=0.0, shift_y=0.0, lift=0.0):
    c, rx, ry, nz = screen_basis(m, z_off)
    tgt = c - rx * shift_x - ry * shift_y
    loc = tgt + nz * dist + V((0, 0, lift))
    return (loc, tgt, lens)


P = {
    "top0": (V((0.62, 0.0, 4.2)), V((0.62, 0.05, 0.0)), 42.0),
    "top1": (V((0.12, -0.75, 2.2)), V((0.02, -0.15, 0.0)), 34.0),
    "wide": (V((0.30, -1.50, 0.50)), V((-0.01, 0.03, 0.07)), 38.0),
    "wide2": (V((0.26, -1.30, 0.44)), V((-0.02, 0.04, 0.08)), 38.0),
    "lap": pose_on(M_LSCR, 0.0, 0.56, 40.0, shift_x=0.072, shift_y=0.004),
    "lapw": None,
    "ph": pose_on(M_PH, 0.0045, 0.53, 45.0, shift_x=0.090, shift_y=0.004),
    "phc": pose_on(M_PH, 0.0045, 0.36, 45.0, shift_x=0.050, shift_y=-0.030),   # the 23:48 notification
    "night": (V((0.24, -1.36, 0.42)), V((-0.02, 0.04, 0.08)), 38.0),
    "rise": (V((0.04, -1.05, 1.50)), V((0.0, -0.02, 0.0)), 34.0),
    "rise2": (V((0.02, -0.92, 1.62)), V((0.0, -0.02, 0.0)), 34.0),
}
# medium on the laptop, the map in front of it showing (the pages land there)
_c, _rx, _ry, _nz = screen_basis(M_LSCR)
P["lapw"] = (_c + V((0.08, -0.95, 0.30)), _c + V((-0.10, -0.24, -0.08)), 36.0)

CAM_KEYS = [
    (0.0, "top0"), (3.8, "top1"), (7.0, "wide"), (10.0, "wide2"),
    (11.6, "lap"), (16.4, "lap"), (18.0, "wide"), (19.6, "ph"), (29.2, "ph"), (30.8, "wide"), (31.6, "wide"),
    (33.0, "lap"), (37.6, "lap"), (38.9, "lapw"), (43.8, "lapw"), (45.4, "wide"), (46.4, "wide"),
    (48.0, "ph"), (57.4, "ph"), (59.2, "night"), (61.4, "night"), (62.8, "lap"), (65.0, "lap"),
    (66.2, "night"), (67.4, "night"), (68.6, "phc"), (69.6, "phc"), (73.2, "rise"), (END_T, "rise2"),
]


ACT_CAM = [(ACT_T0, "wide"), (ACT_T0 + 2.4, "ph"), (37.4, "ph"), (ACT_T0 + ACT_LEN, "wide")]


def _breath(t):
    return V((0.002 * math.sin(t * 0.7), 0.0015 * math.sin(t * 0.53 + 1), 0.0015 * math.sin(t * 0.61 + 2)))


def cam_act(t):
    """The friends' act: wide, in on the phone, back to the old shot at 7.0 s exactly."""
    for (t0, a), (t1, b) in zip(ACT_CAM, ACT_CAM[1:]):
        if t0 <= t <= t1:
            u = smoother(prog(t, t0, t1))
            pa, pb = P[a], P[b]
            loc, tgt, lens = pa[0].lerp(pb[0], u), pa[1].lerp(pb[1], u), lerp(pa[2], pb[2], u)
            w = smooth(prog(t, ACT_T0, ACT_T0 + 2.4)) * (1 - smooth(prog(t, 37.4, ACT_T0 + ACT_LEN)))
            b0 = _breath(ACT_T0)
            return loc + b0 + (_breath(t) - b0) * w, tgt, lens
    p = P["wide"]
    return p[0] + _breath(ACT_T0), p[1], p[2]


def cam_at(t):
    if ACT:
        return cam_act(t)
    return _cam_old(t)


def _cam_old(t):
    for (t0, a), (t1, b) in zip(CAM_KEYS, CAM_KEYS[1:]):
        if t0 <= t <= t1:
            u = smoother(prog(t, t0, t1))
            pa, pb = P[a], P[b]
            loc = pa[0].lerp(pb[0], u)
            tgt = pa[1].lerp(pb[1], u)
            lens = lerp(pa[2], pb[2], u)
            # a slow breath on the holds, a few millimetres
            loc = loc + V((0.002 * math.sin(t * 0.7), 0.0015 * math.sin(t * 0.53 + 1), 0.0015 * math.sin(t * 0.61 + 2)))
            return loc, tgt, lens
    p = P[CAM_KEYS[-1][1]]
    return p[0], p[1], p[2]


def cam_matrix(t):
    loc, tgt, lens = cam_at(t)
    q = (tgt - loc).to_track_quat("-Z", "Y")
    return Matrix.Translation(loc) @ q.to_matrix().to_4x4(), lens


# --- the lifting cards ----------------------------------------------------------

def present_matrix(t, x_frac, y_frac, dist, width_frac, card_w):
    """A card facing the camera at time t: centre at (x_frac, y_frac) of the frame
    (0 = centre, +0.5 = right/top edge), width_frac of the frame wide."""
    m, lens = cam_matrix(t)
    fh = dist * 24.0 / lens
    fw = fh * 16 / 9
    pos = m @ V((x_frac * fw, y_frac * fh, -dist))
    k = width_frac * fw / card_w
    return pos, m.to_quaternion(), k


CARDS = [
    # the CRM's WanderBuddy page: the app comes with every trip the agency sells (the add-on)
    dict(name="cAddon", img="cardAddon.png", on="lap", src=(300, 95, 1580, 390), size=(1600, 1000),
         up=9.0, back=11.3, x=0.17, y=0.03, dist=0.30, wf=0.56, follow=True),
    # name, image, (laptop|phone, rect px on that screen image, image size), present (t_up, t_hold_end, x, y, dist, width)
    dict(name="cListing", img="cardListing.png", on="lap", src=(548, 1022, 1186, 1740), size=(3200, 2000),
         up=12.0, back=15.3, x=0.02, y=0.02, dist=0.30, wf=0.30),
    dict(name="cFee", img="cardFee.png", on="ph", src=(100, 7050 - 1728 * 3, 1190, 7430 - 1728 * 3), size=(1290, 2796),
         up=24.0, back=28.4, x=0.09, y=0.04, dist=0.28, wf=0.40, ring=24.9),
    dict(name="cHold", img="cardHold.png", on="lap", src=(2560, 210, 3140, 800), size=(3200, 2000),
         up=33.4, back=37.0, x=0.06, y=0.0, dist=0.30, wf=0.28),
    dict(name="cMai", img="cardMai.png", on="ph", src=(150, 1352, 960, 1660), size=(1080, 2341),
         up=54.6, back=57.0, x=0.09, y=0.03, dist=0.28, wf=0.36),
    dict(name="cAnswer", img="cardAnswer.png", on="lap", src=(616, 262, 1290, 478), size=(1600, 1000),
         up=62.9, back=None, x=0.14, y=0.03, dist=0.30, wf=0.52, fly=(65.6, 67.4)),
]
CARDS_ACT = [
    dict(name="bDates", img="cardDates.png", on="ph", src=(26, 1957, 1264, 2276), size=(1290, 2796),
         up=11.0, back=14.2, x=0.10, y=0.03, dist=0.28, wf=0.36),
    dict(name="bVote", img="cardVote.png", on="ph", src=(26, 1831, 1264, 2662), size=(1290, 2796),
         up=15.4, back=18.6, x=0.10, y=0.02, dist=0.28, wf=0.36),
    # a reel goes to our Instagram: the app's steps, then the DM thread
    dict(name="bIgSteps", img="cardIgSteps.png", on="ph", src=(20, 470, 1060, 1250), size=(1080, 2341),
         up=19.8, back=22.4, x=0.10, y=0.02, dist=0.28, wf=0.34),
    dict(name="bIgDm", img="cardIgDm.png", on="ph", src=(40, 520, 1250, 2260), size=(1290, 2796),
         up=23.5, back=26.3, x=0.10, y=0.0, dist=0.28, wf=0.26),
    dict(name="bReel", img="cardReel.png", on="ph", src=(32, 780, 1258, 1048), size=(1290, 2796),
         up=27.6, back=30.6, x=0.10, y=0.03, dist=0.28, wf=0.38),
    dict(name="bSettle", img="cardSettle.png", on="ph", src=(39, 1784, 1251, 2159), size=(1290, 2796),
         up=32.0, back=35.0, x=0.10, y=0.03, dist=0.28, wf=0.36),
    dict(name="bLive", img="cardLive.png", on="ph", src=(24, 1295, 1266, 2290), size=(1290, 2796),
         up=36.0, back=38.7, x=0.10, y=0.02, dist=0.28, wf=0.30),
]
if ACT:
    CARDS = CARDS_ACT
SCROLL = [(0.0, 0.0), (21.0, 0.0), (23.2, 1728.0)]   # css px from the top of the trip page
PAGE_H, VIEW_H = 8586 / 3.0, 932.0


def scroll_css(t):
    for (t0, a), (t1, b) in zip(SCROLL, SCROLL[1:]):
        if t0 <= t <= t1:
            return lerp(a, b, smoother(prog(t, t0, t1)))
    return SCROLL[-1][1]


# --- the arc --------------------------------------------------------------------

# device to device: from the top of the laptop's lid to the top of the phone, so the
# line never crosses a screen in the close-ups
ARC_A = lap_frame()[1] @ V((0, 0.236, -0.0035))
ARC_B = M_PH @ V((0, (2796 + 80) * film.PH_PX / 2 - 0.002, -0.001))
ARC_C = (ARC_A + ARC_B) / 2 + V((0.03, -0.03, 0.42))


def arc_pt(u):
    return ARC_A * (1 - u) ** 2 + ARC_C * 2 * u * (1 - u) + ARC_B * u * u


# --- build ----------------------------------------------------------------------

def screen_chain(name, shots, strength=1.0, market=None):
    """Emission screen that crossfades between images at the given times.
    Returns (material, per-frame updater)."""
    m = bpy.data.materials.new(name)
    nt, out = film._clean(m)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    facs, mapping = [], None
    prev = None
    for i, (_, img) in enumerate(shots):
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.interpolation = "Cubic"
        tex.extension = "EXTEND"
        if img == "market":
            tex.image = bpy.data.images.load(S("marketPhoneFull.png"), check_existing=True)
            tc = nt.nodes.new("ShaderNodeTexCoord")
            mapping = nt.nodes.new("ShaderNodeMapping")
            mapping.inputs["Scale"].default_value = (1.0, VIEW_H / PAGE_H, 1.0)
            nt.links.new(tc.outputs["UV"], mapping.inputs["Vector"])
            nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
        else:
            tex.image = bpy.data.images.load(S(img), check_existing=True)
        if prev is None:
            prev = tex.outputs["Color"]
            facs.append(None)
            continue
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.inputs["Factor"].default_value = 0.0
        nt.links.new(prev, mix.inputs["A"])
        nt.links.new(tex.outputs["Color"], mix.inputs["B"])
        prev = mix.outputs["Result"]
        facs.append(mix.inputs["Factor"])
    nt.links.new(prev, em.inputs["Color"])
    times = [s[0] for s in shots]

    def update(t, f):
        cur = max(i for i, t0 in enumerate(times) if t >= t0 - 1e-6) if t >= times[0] else 0
        # result_i = mix(result_i-1, image_i, f_i): the incoming shot fades in over the one before it
        for i, sock in enumerate(facs):
            if sock is None:
                continue
            v = smooth(prog(t, times[i], times[i] + 0.3)) if i == cur else (1.0 if i == cur - 1 else 0.0)
            key_val(sock, f, v)
        if mapping is not None:
            css = scroll_css(t)
            key_val(mapping.inputs["Location"], f, V((0.0, 1 - (css + VIEW_H) / PAGE_H, 0.0)))
    return m, em, update


def laptop(screen_m):
    alu = principled("alu", "#C9CED5", rough=0.3, metallic=1.0)
    alu_d = principled("alu_d", "#AEB4BC", rough=0.42, metallic=1.0)
    black = principled("bezel", "#06080B", rough=0.1, coat=1.0)
    root = empty("laptop")
    m_lap, _, _ = lap_frame()
    root.matrix_world = m_lap
    base = slab("lap_base", 0.36, 0.25, 0.014, 0.011, alu, alu, alu, bevel=0.002, parent=root)
    base.location.z = 0.0055
    kb = bpy.data.materials.new("keys")
    kb.use_nodes = True
    nt = kb.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Color1"].default_value = lin("#1C2026")
    br.inputs["Color2"].default_value = lin("#22272E")
    br.inputs["Mortar"].default_value = lin("#8E959E")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.012
    br.inputs["Brick Width"].default_value = 0.0667
    br.inputs["Row Height"].default_value = 0.1667
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["UV"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = 0.55
    keys = slab("lap_keys", 0.29, 0.105, 0.004, 0.0012, kb, alu_d, parent=root)
    keys.location = (0, 0.045, 0.0112)
    pad = slab("lap_pad", 0.125, 0.078, 0.006, 0.0008, alu_d, parent=root)
    pad.location = (0, -0.073, 0.0112)
    hinge = empty("lap_hinge", root, (0, 0.122, 0.011))
    hinge.rotation_euler = (rad(LID_SHUT), 0, 0)
    lid = slab("lap_lid", 0.36, 0.238, 0.014, 0.006, black, alu, alu, bevel=0.0015, parent=hinge)
    lid.location = (0, 0.119, -0.0035)
    scr = slab("lap_scr", LS_W, LS_H, 0.004, 0.0003, screen_m, black, black, parent=hinge)
    scr.location = (0, 0.122, -0.0003)
    return hinge


def card_obj(c):
    img = bpy.data.images.load(S(c["img"]), check_existing=True)
    iw, ih = img.size
    x0, y0, x1, y1 = c["src"]
    sw, sh = c["size"]
    if c["on"] == "lap":
        m, W_, H_ = M_LSCR, LS_W, LS_H
    else:
        m, W_, H_ = M_PH, PS_W / PH_SCALE, PS_H / PH_SCALE
    w = (x1 - x0) / sw * W_
    h = (y1 - y0) / sh * H_
    cx = ((x0 + x1) / 2 / sw - 0.5) * W_
    cy = (0.5 - (y0 + y1) / 2 / sh) * H_
    z = 0.0006 if c["on"] == "lap" else 0.0039 + 0.0006
    rest = m @ Matrix.Translation((cx, cy, z))
    front = emit(c["name"] + "_m", image=S(c["img"]))
    edge = principled(c["name"] + "_e", "#D9E1E9", rough=0.5)
    ob = slab(c["name"], w, h, min(w, h) * 0.05, min(w, h) * 0.012, front, edge, edge)
    ob.visible_shadow = False
    ob.rotation_mode = "QUATERNION"
    # the card's mesh is in screen units; on the phone the screen is scaled by PH_SCALE
    rest_scale = PH_SCALE if c["on"] == "ph" else 1.0
    c["obj"], c["w"], c["h"], c["rest"], c["rest_scale"] = ob, w, h, rest, rest_scale
    if c.get("ring"):
        rm = emit(c["name"] + "_ring", "#1E88D6", alpha=0.0)
        rg = ring(c["name"] + "_ring", w * 1.04, h * 1.10, min(w, h) * 0.08, min(w, h) * 0.035, rm, parent=ob)
        rg.location.z = min(w, h) * 0.012
        rg.visible_shadow = False
        c["ring_m"], c["ring_ob"] = rm, rg
    return ob


def card_state(c, t):
    """(location, quaternion, scale) of a card at t, or None when hidden."""
    up, back = c["up"], c["back"]
    if t < up - 0.02:
        return None
    rloc, rq, _ = c["rest"].decompose()
    rs = c["rest_scale"]
    # a card with follow=True is held up in front of the camera while it moves; the others stay put in the room
    tref = t if c.get("follow") else up + 0.6
    ploc, pq, pk = present_matrix(tref, c["x"], c["y"], c["dist"], c["wf"], c["w"])
    # the present pose is taken with the camera where it holds; it stays put in the world
    u = out_cubic(prog(t, up, up + 0.6))
    if c.get("fly") and t > c["fly"][0] - 0.6:
        f0, f1 = c["fly"]
        if t <= f0:
            # shrink toward the start of the arc above Krabi
            v = smoother(prog(t, f0 - 0.6, f0))
            a = arc_pt(0.06)
            small = 0.10 / c["w"]
            q = pq.slerp(cam_matrix(66.8)[0].to_quaternion(), v)
            return ploc.lerp(a, v), q, lerp(pk, small, v)
        if t <= f1:
            v = smoother(prog(t, f0, f1))
            uu = lerp(0.06, 1.0, v)
            small = 0.10 / c["w"]
            k = lerp(small, small * 0.55, v)
            return arc_pt(uu) + V((0, 0, 0.01)), cam_matrix(66.8)[0].to_quaternion(), k
        return None
    if back is not None and t > back:
        v = smoother(prog(t, back, back + 0.5))
        if v >= 1:
            return None
        return ploc.lerp(rloc, v), pq.slerp(rq, v), lerp(pk, rs, v)
    lift = math.sin(math.pi * u) * 0.03
    loc = rloc.lerp(ploc, u)
    cam_loc = cam_matrix(tref)[0].translation
    loc = loc + (cam_loc - loc).normalized() * lift
    return loc, rq.slerp(pq, u), lerp(rs, pk, u)


def focus_at(t):
    loc, tgt, _ = cam_at(t)
    d = (tgt - loc).length
    for c in CARDS:
        st = card_state(c, t)
        if st is None or c.get("fly") and t > c["fly"][0]:
            continue
        w = win(t, c["up"] + 0.15, (c["back"] or c["fly"][0]) + 0.1, 0.45, 0.4)
        if w > 0:
            d = lerp(d, (st[0] - loc).length, w)
    return d


PAGES = ["pg00.png", "pg01.png", "pg02.png", "pg03.png", "pg04.png", "pg05.png"]
PAGE_T0, PAGE_STEP, PAGE_DUR = 39.0, 0.42, 1.0
PAGE_W, PAGE_HH = 0.21, 0.21 * 1860 / 2616
# where each page lands on the map, in front of and to the left of the laptop (over the Andaman Sea)
PAGE_LAND = [(-0.25, -0.02, 14), (-0.20, -0.10, -6), (-0.36, -0.12, 22), (-0.12, -0.19, 4), (-0.30, -0.25, -12), (-0.47, -0.04, 8)]


def page_state(i, t):
    t0 = PAGE_T0 + i * PAGE_STEP
    if t < t0:
        return None
    c, rx, ry, nz = screen_basis(M_LSCR, 0.002)
    start_q = M_LSCR.to_quaternion()
    dx, dy, yaw = PAGE_LAND[i]
    land = KRABI + V((dx, dy, 0.0012 + i * 0.0007))
    land_q = Quaternion((0, 0, 1), rad(LAP_YAW + yaw))
    u = smoother(prog(t, t0, t0 + PAGE_DUR))
    pos = c.lerp(land, u) + V((0, 0, math.sin(math.pi * u) * 0.10))
    return pos, start_q.slerp(land_q, u), lerp(0.30, 1.0, out_cubic(prog(t, t0, t0 + PAGE_DUR * 0.7)))


def build():
    sc, cam = film.new_scene(NF, engine="EEVEE", samples=32, world="#E3EAF1", world_strength=0.85,
                             mblur=True, shutter=0.45)
    sc.frame_start, sc.frame_end = 0, NF - 1
    if ACT:
        sc.frame_start, sc.frame_end = F(ACT_T0), F(ACT_T0 + ACT_LEN) - 1
    cam.data.sensor_fit = "VERTICAL"
    cam.data.sensor_height = 24.0
    cam.data.sensor_width = 24.0 * 16 / 9
    cam.data.clip_start = 0.01
    cam.data.clip_end = 60
    cam.data.dof.aperture_fstop = 4.0
    cam.rotation_mode = "QUATERNION"

    # the table and the map
    floor = principled("floor", "#CDD6DF", rough=0.92)
    fl = plane("floor", 40, 40, floor)
    fl.location.z = -0.0015
    mm = principled("map", "#FFFFFF", rough=0.86, image=S("map.png"), bump=(900, 0.06, 6))
    nt = mm.node_tree
    pb = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    land = nt.nodes.new("ShaderNodeTexImage")
    land.image = bpy.data.images.load(S("map_land.png"), check_existing=True)
    land.image.colorspace_settings.name = "Non-Color"
    land.interpolation = "Cubic"
    lb = nt.nodes.new("ShaderNodeBump")
    lb.inputs["Strength"].default_value = 0.35
    lb.inputs["Distance"].default_value = 0.003
    old = next(n for n in nt.nodes if n.type == "BUMP" and n != lb)
    nt.links.new(land.outputs["Color"], lb.inputs["Height"])
    nt.links.new(lb.outputs["Normal"], old.inputs["Normal"])
    mapo = slab("map", MW, MH, 0.004, 0.0012, mm, principled("map_edge", "#E9EDF1", rough=0.9))
    mapo.location = (-ORIGIN.x, -ORIGIN.y, -0.0006)

    # light: late sun from the west, the sky; a desk lamp for 23:47
    sn = sun("sun", (66, 0, -72), 3.0, angle=1.2, color="#FFF3E6")
    lamp = film.area("lamp", LAP_POS + V((-0.35, -0.10, 0.55)), LAP_POS + V((0.0, -0.10, 0.0)), 0.0, 0.25, color="#FFE7D2")
    bg = next(n for n in sc.world.node_tree.nodes if n.type == "BACKGROUND")

    # the laptop on Krabi
    lap_m, lap_em, lap_upd = screen_chain("lap_screen", LAP_SHOTS, 0.0)
    hinge = laptop(lap_m)
    sheet = principled("rates", "#FFFFFF", rough=0.8, image=S("rate_sheet.png"))
    rs = plane("rates", 0.148, 0.209, sheet)
    rs.location = LAP_POS + V((0.28, 0.06, 0.0009))
    rs.rotation_euler = (0, 0, rad(-18))

    # the phone on Singapore, on a small stand, her passport and boarding pass beside it
    ph_m, ph_em, ph_upd = screen_chain("ph_screen", PH_SHOTS_ACT if ACT else PH_SHOTS, 0.0)
    root, _ = film.phone("phone", ph_m)
    root.matrix_world = M_PH
    standm = principled("stand", "#E8ECF0", rough=0.55)
    st = box("stand", (0.07, 0.025, 0.06), PH_POS + V((0.0, 0.034, 0.03)), standm, bevel=0.004)
    st.rotation_euler = (rad(-PH_LEAN), 0, rad(PH_YAW))
    pp = plane("passport", 0.088, 0.125, principled("passport_m", "#FFFFFF", rough=0.6, image=S("passport.png")))
    pp.location = SING + V((-0.155, 0.02, 0.0016))
    pp.rotation_euler = (0, 0, rad(12))
    bp = plane("boarding", 0.070, 0.166, principled("boarding_m", "#FFFFFF", rough=0.75, image=S("boarding.png")))
    bp.location = SING + V((-0.105, -0.035, 0.0024))
    bp.rotation_euler = (0, 0, rad(-9))

    # the arc and the dot that runs along it
    arc_m = emit("arc", "#1E88D6", strength=1.0)
    cu = bpy.data.curves.new("arc", "CURVE")
    cu.dimensions = "3D"
    spl = cu.splines.new("POLY")
    n = 96
    spl.points.add(n - 1)
    for i in range(n):
        p = arc_pt(i / (n - 1))
        spl.points[i].co = (p.x, p.y, p.z, 1)
    cu.bevel_depth = 0.0017
    cu.bevel_resolution = 3
    cu.use_fill_caps = True
    cu.bevel_factor_start = 0.0
    arc = link(bpy.data.objects.new("arc", cu))
    arc.data.materials.append(arc_m)
    arc.visible_shadow = False
    dot_m = emit("dot", "#1E88D6", strength=1.6)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0065, segments=24, ring_count=12)
    dot = bpy.context.active_object
    dot.name = "dot"
    dot.data.materials.append(dot_m)
    dot.visible_shadow = False
    bpy.ops.object.shade_smooth()

    for c in CARDS:
        card_obj(c)
    pages = []
    for i, pg in enumerate(PAGES):
        m = principled("page%d" % i, "#FFFFFF", rough=0.72, image=S("pages/" + pg))
        ob = slab("page%d" % i, PAGE_W, PAGE_HH, 0.002, 0.0004, m, principled("page_e%d" % i, "#F2EEE6", rough=0.8))
        ob.rotation_mode = "QUATERNION"
        pages.append(ob)

    # --- key every frame -------------------------------------------------------
    hidden = V((0, 0, -5))
    # tu is the film's clock; t is what the agency scene reads. They are the same, except in the
    # friends' act, where the agency scene stays as it is at 7.0 s (laptop shut, nothing drawn).
    for f in (range(F(ACT_T0), F(ACT_T0 + ACT_LEN)) if ACT else range(NF)):
        tu = f / FPS
        t = ACT_T0 if ACT else tu
        m, lens = cam_matrix(tu)
        cam.location = m.translation
        cam.rotation_quaternion = m.to_quaternion()
        cam.data.lens = lens
        cam.data.dof.focus_distance = focus_at(tu)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_quaternion", frame=f)
        cam.data.keyframe_insert("lens", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)

        # lid and screens
        u = smoother(prog(t, *LID))
        hinge.rotation_euler = (rad(lerp(LID_SHUT, LID_OPEN, u)), 0, 0)
        hinge.keyframe_insert("rotation_euler", frame=f)
        key_val(lap_em.inputs["Strength"], f, smooth(prog(t, LAP_ON, LAP_ON + 0.5)))
        if ACT:
            key_val(ph_em.inputs["Strength"], f, smooth(prog(tu, 7.3, 7.65)) * (1 - smooth(prog(tu, 38.9, 39.7))))
        else:
            key_val(ph_em.inputs["Strength"], f, smooth(prog(t, WAKE, WAKE + 0.35)))
        lap_upd(t, f)
        ph_upd(tu, f)

        # day, night, day
        nt_ = smooth(prog(t, *NIGHT)) * (1 - smooth(prog(t, *DAY)))
        sn.data.energy = lerp(3.0, 0.0, nt_)
        sn.data.keyframe_insert("energy", frame=f)
        lamp.data.energy = lerp(0.0, 2.5, nt_)
        lamp.data.keyframe_insert("energy", frame=f)
        key_val(bg.inputs["Color"], f, tuple(lerp(a, b, nt_) for a, b in zip(lin("#E3EAF1"), lin("#0B1320"))))
        key_val(bg.inputs["Strength"], f, lerp(0.85, 0.10, nt_))

        # the arc draws once and stays; the dot runs on each hop
        cu.bevel_factor_end = smoother(prog(t, *ARC_DRAW))
        cu.keyframe_insert("bevel_factor_end", frame=f)
        dpos, dsc = hidden, 0.001
        if ARC_DRAW[0] <= t <= ARC_DRAW[1] + 0.15:
            dpos, dsc = arc_pt(smoother(prog(t, *ARC_DRAW))), 1.0
        for a, b, d in DOTS:
            if a <= t <= b + 0.1:
                v = smoother(prog(t, a, b))
                dpos, dsc = arc_pt(v if d > 0 else 1 - v), 1.0
        dot.location = dpos
        dot.scale = (dsc,) * 3
        dot.keyframe_insert("location", frame=f)
        dot.keyframe_insert("scale", frame=f)

        for c in CARDS:
            st_ = card_state(c, tu)
            ob = c["obj"]
            if st_ is None:
                ob.location, ob.rotation_quaternion, ob.scale = hidden, Quaternion(), (0.001,) * 3
            else:
                ob.location, ob.rotation_quaternion, ob.scale = st_[0], st_[1], (st_[2],) * 3
            ob.keyframe_insert("location", frame=f)
            ob.keyframe_insert("rotation_quaternion", frame=f)
            ob.keyframe_insert("scale", frame=f)
            if c.get("ring_m"):
                film.fade_mat(c["ring_m"], f, out_cubic(prog(t, c["ring"], c["ring"] + 0.4)) * (1 - smooth(prog(t, c["back"], c["back"] + 0.25))))
                rs_ = lerp(1.07, 1.0, out_cubic(prog(t, c["ring"], c["ring"] + 0.4)))
                c["ring_ob"].scale = (rs_, rs_, 1)
                c["ring_ob"].keyframe_insert("scale", frame=f)

        for i, ob in enumerate(pages):
            st_ = page_state(i, t)
            if st_ is None:
                ob.location, ob.rotation_quaternion, ob.scale = hidden, Quaternion(), (0.001,) * 3
            else:
                ob.location, ob.rotation_quaternion, ob.scale = st_[0], st_[1], (st_[2],) * 3
            ob.keyframe_insert("location", frame=f)
            ob.keyframe_insert("rotation_quaternion", frame=f)
            ob.keyframe_insert("scale", frame=f)
    film.all_linear()
    film.set_interp(cu, "LINEAR")
    for sd in bpy.data.lights:
        film.set_interp(sd, "LINEAR")
    return sc


def main():
    argv = film.args()
    mode = argv[0] if argv else "stills"
    sc = build()
    out = os.path.join(AD, "render", "3d_act" if ACT else "3d")
    if mode == "stills":
        ts = [float(x) for x in (argv[1] if len(argv) > 1 else "3,9,13.5,25.5").split(",")]
        film.render(sc, os.path.join(AD, "render", "stills"), stills=[F(t) for t in ts])
    else:
        film.render(sc, out)


main()
