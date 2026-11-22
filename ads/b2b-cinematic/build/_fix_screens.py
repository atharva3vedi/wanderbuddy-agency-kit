"""One-off (2026-11-12): fixes three rendering faults in the second-pass film scripts.

1. Phone screen images were square planes: their corners stuck out past the rounded glass.
   They are now rounded slabs, the same shape as the phone's own screen.
2. The laptop's change of screen was a crossfade during a camera pan: with two motion-blur
   steps it ghosted. It is now a cut (camera and screen change on the same frame).
3. Opened 3 Times: her phone went black between opens. It now shows her lock screen, later
   each time, with the other agency's quotation still unread on it.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(name, pairs):
    p = os.path.join(HERE, name)
    s = open(p).read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w").write(s)
    print("patched", name)


ROUND = "slab({n}, PW, PH, 165 * PH_PX, 0.00002, {m}, {m}, {m}, parent={p})"

patch("agencies2.py", [
    ('lp = plane(f"lockp{k}", PW, PH, m, ph1)', "lp = " + ROUND.format(n='f"lockp{k}"', m="m", p="ph1")),
    ('la = plane("list_a", PW, PH, la_m, pht)', "la = " + ROUND.format(n='"list_a"', m="la_m", p="pht")),
    ('lb = plane("list_b", PW, PH, lb_m, pht)', "lb = " + ROUND.format(n='"list_b"', m="lb_m", p="pht")),
])

patch("monsoon.py", [
    ('lp = plane(f"mlockp{k}", PW, PH, m, phl)', "lp = " + ROUND.format(n='f"mlockp{k}"', m="m", p="phl")),
    ('''    for f in range(F_SWAP - 8, F_SWAP + 1):
        fade_mat(ring_m, f, 1 - prog(f, F_SWAP - 8, F_SWAP))''',
     '''    fade_mat(ring_m, F_SWAP - 1, 1.0)                          # gone on the cut to Home
    fade_mat(ring_m, F_SWAP, 0.0)'''),
    ("        fade_mat(home_m, f, smooth(prog(f, F_SWAP, F_SWAP + 8)))", "        fade_mat(home_m, f, 1.0 if f >= F_SWAP else 0.0)      # a cut, with the camera"),
    ('''        (F_SWAP - 4, board_c + nrm * 0.39, board_c, 50, 2.8, board_c),
        (F_SWAP + 18, home_c + nrm * 0.4, home_c, 50, 2.8, home_c),''',
     '''        (F_SWAP - 1, board_c + nrm * 0.39, board_c, 50, 2.8, board_c),
        (F_SWAP, home_c + nrm * 0.4, home_c, 50, 2.8, home_c),'''),
    ("    MOVES = (346, F_SWAP - 4)", "    MOVES = (346,)"),
    ("bpy.context.scene.render.use_motion_blur = (f + 1) not in (MB, MC, MD, ME)", "bpy.context.scene.render.use_motion_blur = (f + 1) not in (MB, MC, MD, F_SWAP, ME)"),
])

patch("opened.py", [
    ('lp = plane(f"lockp{k}", PW, PH, m, ph1)', "lp = " + ROUND.format(n='f"lockp{k}"', m="m", p="ph1")),
    ('la = plane("list_a", PW, PH, la_m, pht)', "la = " + ROUND.format(n='"list_a"', m="la_m", p="pht")),
    ('''    lb = plane("list_b", PW, PH, lb_m, pht)
    lb.location = (0, 0, 0.0039 + 0.00018)''',
     '''    lb = ''' + ROUND.format(n='"list_b"', m="lb_m", p="pht") + '''
    lb.location = (0, 0, 0.0039 + 0.00022)
    later_m = []                                              # her lock screen the next morning, and the next night
    for k in (1, 2):
        lm_ = emit(f"lock_t{k}", image=os.path.join(SCRA, f"lockT{k}.png"), alpha=0.0)
        lo_ = ''' + ROUND.format(n='f"lock_t{k}"', m="lm_", p="pht") + '''
        lo_.location = (0, 0, 0.0039 + 0.00012 + 0.00003 * k)
        later_m.append(lm_)'''),
    ('''        key_val(la_m.node_tree.nodes["em"].inputs["Strength"], f, 1 - smooth(prog(f, OPENS[0][0] - 4, OPENS[0][0] + 2)))
        fade_mat(board_m, f, smooth(prog(f, F_SWAP, F_SWAP + 8)))''',
     '''        for k, lm_ in enumerate(later_m):                     # swapped in while the plan covers the screen
            fade_mat(lm_, f, 1.0 if f >= OPENS[k][0] + 12 else 0.0)
        fade_mat(board_m, f, 1.0 if f >= F_SWAP else 0.0)      # a cut, with the camera'''),
    ('''    for f in range(F_SWAP - 8, F_SWAP + 1):
        fade_mat(ring_m, f, 1 - prog(f, F_SWAP - 8, F_SWAP))''',
     '''    fade_mat(ring_m, F_SWAP - 1, 1.0)                          # gone on the cut to the board
    fade_mat(ring_m, F_SWAP, 0.0)'''),
    ('''        (F_SWAP - 4, hold_c + nrm * 0.49, hold_c, 50, 2.8, hold_c),
        (F_SWAP + 18, card_c + nrm * 0.4, card_c, 50, 2.8, card_c),''',
     '''        (F_SWAP - 1, hold_c + nrm * 0.49, hold_c, 50, 2.8, hold_c),
        (F_SWAP, card_c + nrm * 0.4, card_c, 50, 2.8, card_c),'''),
    ("    MOVES = (262, F_SWAP - 4)", "    MOVES = (262,)"),
    ("bpy.context.scene.render.use_motion_blur = (f + 1) not in (TD, TE, TF)", "bpy.context.scene.render.use_motion_blur = (f + 1) not in (TD, F_SWAP, TE, TF)"),
])
