"""Figure 67: Fresnel's wave-front construction for diffraction into the geometrical shadow of edge AG."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    sw_thin = 5.0

    # Observation point F inside shadow
    fx, fy = 913.0, 1040.0

    # Opaque screen edge A-G (horizontal solid line at y = 93)
    ax, ay = 487.0, 93.0
    gx, gy = 828.0, 93.0
    s.line(ax, ay, gx, gy, stroke_width=sw)

    # Wavefront curve C'' - C' - C - B - A (dashed)
    c1x, c1y = 246.0, 88.0
    cx, cy = 338.5, 92.0
    bx, by = 419.5, 93.0
    lib.smooth_curve(
        s,
        [(32.0, 50.0), (100.0, 69.0), (175.0, 81.0), (c1x, c1y), (cx, cy), (bx, by), (ax, ay)],
        stroke_width=sw,
        dash="20,12",
    )

    # Unit vector along F -> A (extending above A to top edge y = 0)
    fa_len = math.hypot(ax - fx, ay - fy)
    ux, uy = (ax - fx) / fa_len, (ay - fy) / fa_len

    # Point E on dashed extension of FA at distance FC from F
    r_fc = math.hypot(cx - fx, cy - fy)
    ex, ey = fx + ux * r_fc, fy + uy * r_fc

    # Top of dashed extension of FA at y = 2
    t_top = (2.0 - fy) / uy
    top_x, top_y = fx + ux * t_top, 2.0

    # Solid rays from F to A, B, C, C'
    s.line(fx, fy, ax, ay, stroke_width=sw)         # F -> A
    s.line(fx, fy, bx, by, stroke_width=sw_thin)    # F -> B
    s.line(fx, fy, cx, cy, stroke_width=sw_thin)    # F -> C
    s.line(fx, fy, c1x, c1y, stroke_width=sw_thin)  # F -> C'

    # Dashed extension of FA above A through E to top edge
    s.line(ax, ay, top_x, top_y, stroke_width=sw_thin, dash="16,10")

    # Dashed circular arc C-E centered at F with radius FC, terminating cleanly at C and E
    ang_c = math.degrees(math.atan2(cy - fy, cx - fx))
    ang_e = math.degrees(math.atan2(ey - fy, ex - fx))
    s.arc(fx, fy, r_fc, ang_c, ang_e, stroke_width=sw_thin, dash="16,10", sweep=1)

    # Dashed construction arc/line from C' up-right to top edge
    lib.smooth_curve(
        s,
        [(c1x, c1y), (294.0, 52.0), (332.0, 26.0), (368.0, 2.0)],
        stroke_width=sw_thin,
        dash="16,10",
    )

    # Labels
    lib.label(s, 162.0, 44.0, "C\u2033", size=50.0, italic=False, bold=True)
    lib.label(s, 236.0, 56.0, "C\u2032", size=50.0, italic=False, bold=True)
    lib.label(s, 322.0, 62.0, "C", size=50.0, italic=False, bold=True)
    lib.label(s, 494.0, 26.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 514.0, 68.0, "A", size=50.0, italic=False, bold=True)
    lib.label(s, 398.0, 128.0, "B", size=50.0, italic=False, bold=True)
    lib.label(s, 866.0, 86.0, "G", size=50.0, italic=False, bold=True)
    lib.label(s, 866.0, 1036.0, "F", size=54.0, italic=False, bold=True)

    s.save(out_svg)
