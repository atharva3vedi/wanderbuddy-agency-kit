"""One-off: writes build/opened.py from build/agencies2.py (same sets, new screens and timing)."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "agencies2.py")).read()


def cut(a, b, new):
    global s
    i = s.index(a)
    j = s.index(b, i)
    s = s[:i] + new + s[j:]


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


cut('"""Second pass, film 1', 'import math', '''"""Second pass, film 3, Opened 3 Times: the follow-up.

  Blender -b --factory-startup -P build/opened.py -- [still f f ...]

Monday: two agencies send the same couple a quote for Komodo (her lock screen,
set dressing). She opens the Lantern Trips plan, then again, then again (the real
itinerary cover in a plain viewer, screens/opened/cover_phone.png). In Lantern
Trips the real CRM says so (build/opened_capture.mjs): Home's "Opened quote v2 3
times since yesterday. Call while it is fresh", then her card under Booked.
Next door the other phone is still waiting on Wednesday morning. At dawn the
azure ring lands on the Lantern Trips sign.
Frames: render/opened/3d/####.png, 0..649. The dawn street (516..649) is the same
picture as agencies2.py frames 564..697.
"""
''')
cut('N = sec(29.1)', 'LAP = Vector(', '''N = 650                                 # 27.1 s
OUT = os.path.join(AD, "render", "opened", "3d")
SCRA = os.path.join(SCR, "opened")
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
TB, TC, TD, TE, TF = 0, 0, 240, 420, 516   # her phone | Lantern Trips, at night | next door, till morning | dawn
P1, P2 = (-100, -90), (-100, -90)       # no phones behind the shutters in this film
OPENS = [(76, 122), (140, 180), (196, 234)]   # she opens the plan: on, off
F_WAKE, F_RING, F_SWAP, F_RING2 = -20, 326, 356, 384   # ring on the call prompt, the board comes up, ring on her card under Booked
LOCK = [TE - 5, 472]                    # the phone next door: Tuesday, Wednesday
UP1, UP2 = (TF + 18, TF + 72), (TF + 40, TF + 94)
F_WIN = TF + 64
HOSTEL = Vector((0.0, 60.0, 0.5))       # her sofa, far behind the street
''')
# laptop: Home's call prompt, then the board with her card under Booked
cut('    scr_m = emit("screen"', '    glow = area("screen_light"', '''    scr_m = emit("screen", image=os.path.join(SCRA, "home_hot.png"))
    scr = plane("lap_screen", SW, SH, scr_m, hinge)
    scr.location = (0, 0.1075 + 0.006, -0.0004)
    scr.rotation_euler = (0, math.pi, 0)
    board_m = emit("board", image=os.path.join(SCRA, "board_booked.png"), alpha=0.0)
    bp = plane("board", SW, SH, board_m, scr)
    bp.location = (0, 0, 0.0003)
    ring_m = emit("ring", AZURE, alpha=0.0)                    # "Opened quote v2 3 times since yesterday. Call while it is fresh"
    rh = empty("ring_h", scr, (*px(305 + 687 / 2, 159 + 63 / 2), 0.0006))
    ring("ring", 687 / 1600 * SW + 0.004, 63 / 1000 * SH + 0.004, 0.003, 0.0012, ring_m, rh)
    ring_in(rh, ring_m, F_RING, 10)
    for f in range(F_SWAP - 8, F_SWAP + 1):
        fade_mat(ring_m, f, 1 - prog(f, F_SWAP - 8, F_SWAP))
    ring2_m = emit("ring2", AZURE, alpha=0.0)                  # her card, under Booked
    rh2 = empty("ring2_h", scr, (*px(1072 + 224 / 2, 301 + 149 / 2), 0.0009))
    ring("ring2", 224 / 1600 * SW + 0.003, 149 / 1000 * SH + 0.003, 0.004, 0.0011, ring2_m, rh2)
    ring_in(rh2, ring2_m, F_RING2, 10)
''')
rep('lock_m = [emit(f"lock{k}", image=os.path.join(SCRA, f"lock{\'AB\'[k]}.png"), alpha=0.0) for k in range(2)]',
    'lock_m = [emit(f"lock{k}", image=os.path.join(SCRA, f"lockW{k}.png"), alpha=0.0) for k in range(2)]')
# her phone: the lock screen with two quotes, then the plan
rep('duvet.data.materials.append(principled("duvet", "#1F3048", rough=0.95, bump=(380, 0.35, 2)))',
    'duvet.data.materials.append(principled("duvet", "#263A33", rough=0.95, bump=(380, 0.35, 2)))   # a sofa, not the bunk')
rep('la_m = emit("list_a", image=os.path.join(SCRA, "listing_top.png"))', 'la_m = emit("list_a", image=os.path.join(SCRA, "lockT.png"))')
rep('lb_m = emit("list_b", image=os.path.join(SCRA, "listing_hold.png"), alpha=0.0)', 'lb_m = emit("list_b", image=os.path.join(SCRA, "cover_phone.png"), alpha=0.0)')
cut('    hold_m = emit("hold_ring"', '    area("bunk_window"', '')
# animation: her phone and the laptop
rep('''        fade_mat(lb_m, f, smooth(prog(f, SCROLL, SCROLL + 10)))''',
    '''        opened = max(smooth(prog(f, a, a + 6)) * (1 - smooth(prog(f, b, b + 7))) for a, b in OPENS)
        fade_mat(lb_m, f, opened)
        key_val(la_m.node_tree.nodes["em"].inputs["Strength"], f, 1 - smooth(prog(f, OPENS[0][0] - 4, OPENS[0][0] + 2)))
        fade_mat(board_m, f, smooth(prog(f, F_SWAP, F_SWAP + 8)))''')
# camera
cut('    hc = empty("hold_c", scr,', '    nrm = Vector(', '''    hc = empty("call_c", scr, (*px(648, 300), 0.0))
    kc = empty("card_c", scr, (*px(1184, 300), 0.0))
    bpy.context.view_layer.update()
    hold_c = hc.matrix_world.translation.copy()
    card_c = kc.matrix_world.translation.copy()
''')
cut('    shots = [', '    MOVES = (', '''    shots = [
        (0, pc + Vector((0.004, 0.115, 0.47)), pc + Vector((0.0, -0.011, 0)), 50, 4.0, pc),
        (TD - 1, pc + Vector((0.003, 0.1, 0.425)), pc + Vector((0.0, -0.010, 0)), 50, 4.0, pc),
        (TD, Vector((0.55, 3.2, 1.3)), scr_c + Vector((0.02, 0, 0.02)), 35, 3.2, scr_c),
        (262, Vector((0.5, 3.12, 1.29)), scr_c + Vector((0.018, 0, 0.02)), 35, 3.2, scr_c),
        (320, hold_c + nrm * 0.5, hold_c, 50, 2.8, hold_c),
        (F_SWAP - 4, hold_c + nrm * 0.49, hold_c, 50, 2.8, hold_c),
        (F_SWAP + 18, card_c + nrm * 0.4, card_c, 50, 2.8, card_c),
        (TE - 1, card_c + nrm * 0.385, card_c, 50, 2.8, card_c),
        (TE, ph + Vector((0.02, 0.15, 0.37)), ph + Vector((0.0, -0.006, 0)), 50, 4.0, ph),
        (TF - 1, ph + Vector((0.012, 0.135, 0.335)), ph + Vector((0.0, -0.005, 0)), 50, 4.0, ph),
        (TF, Vector((-2.9, -16.4, 1.55)), Vector((-2.9, 0.0, 6.3)), 19, 8.0, Vector((-3.0, 0, 3))),
        (N - 1, Vector((-2.9, -15.6, 1.55)), Vector((-2.9, 0.0, 6.2)), 19.6, 8.0, Vector((-3.0, 0, 3))),
    ]
''')
rep('    MOVES = (110, 152, 372)', '    MOVES = (262, F_SWAP - 4)')
rep('bpy.context.scene.render.use_motion_blur = (f + 1) not in (TB, TC, TD, TE, TF)', 'bpy.context.scene.render.use_motion_blur = (f + 1) not in (TD, TE, TF)')
for bad in ("SCROLL", "F_HOLD", "F_TAP", "hold_m", "sign_c", "front"):
    hits = [m.start() for m in re.finditer(r"\b" + bad + r"\b", s)]
    if hits:
        print(bad, len(hits), [s[h - 50:h + 50].replace("\n", " ") for h in hits[:2]])
open(os.path.join(HERE, "opened.py"), "w").write(s)
print("wrote opened.py", len(s))
