"""One-off (2026-11-12): the blue (azure ring, brand-blue end card) alignment fixes.

1. The ring on the Lantern Trips sign was taller than the gap under the balcony, so its top edge was
   hidden and it read as a lopsided U. It now hugs the sign and stops just under the balcony.
2. The ring on a Home row sat on the next row's border. It is 4 px shorter and centred on its own row.
3. End cards: the mark and wordmark sat 14.5 px right of centre (measured on the final frame) while
   the lines under them were centred. The lockup moves 14.5 px left.
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


SIGN = [
    ('wh_ = empty("win_ring_h", None, (0.5 * (WX0 + DX1), -0.17, 3.3))', 'wh_ = empty("win_ring_h", None, (0.5 * (WX0 + DX1), -0.17, 3.23))   # its top stays under the balcony'),
    ('ring("win_ring", 4.1, 1.0, 0.14, 0.11, win_m, wh_)', 'ring("win_ring", 3.98, 0.63, 0.12, 0.085, win_m, wh_)'),
]
patch("agencies2.py", SIGN)
patch("opened.py", SIGN + [
    ('rh = empty("ring_h", scr, (*px(305 + 687 / 2, 159 + 63 / 2), 0.0006))', 'rh = empty("ring_h", scr, (*px(305 + 687 / 2, 161 + 59 / 2), 0.0006))'),
    ('ring("ring", 687 / 1600 * SW + 0.004, 63 / 1000 * SH + 0.004, 0.003, 0.0012, ring_m, rh)', 'ring("ring", 687 / 1600 * SW + 0.004, 59 / 1000 * SH + 0.002, 0.003, 0.0012, ring_m, rh)'),
])
patch("monsoon.py", SIGN + [
    ('rh2 = empty("ring2_h", scr, (*px(336 + 470 / 2, 159 + 63 / 2), 0.0009))', 'rh2 = empty("ring2_h", scr, (*px(336 + 470 / 2, 161 + 59 / 2), 0.0009))'),
    ('ring("ring2", 470 / 1600 * SW + 0.004, 63 / 1000 * SH + 0.004, 0.003, 0.0011, ring2_m, rh2)', 'ring("ring2", 470 / 1600 * SW + 0.004, 59 / 1000 * SH + 0.002, 0.003, 0.0011, ring2_m, rh2)'),
])
CARD = [('    mx, my = -total / 2 + MM / 2, E["y"]', '    mx, my = -total / 2 + MM / 2 - 14.5, E["y"]      # the wordmark estimate runs 29 px wide: centre the lockup on the lines')]
patch("endcard_v2.py", CARD)
patch("endcard_v3.py", CARD)
patch("day2_compose_v2.py", [('os.path.join(R, "endcard", "%04d.png")', 'os.path.join(R, "endcard_v2", "%04d.png")')])
