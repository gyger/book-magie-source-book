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
    fx, fy = 900.0, 1044.0

    # Opaque screen edge A-G (horizontal at y = 92)
    ax, ay = 482.0, 92.0
    gx, gy = 824.0, 92.0
    s.line(ax, ay, gx, gy, stroke_width=sw)

    # Dashed extension of edge left to B and C
    bx, by = 434.0, 92.0
    cx, cy = 356.0, 92.0
    s.line(cx, cy, ax, ay, stroke_width=sw_thin, dash="18,14")

    # Wavefront curve C'' - C' - C - A
    lib.smooth_curve(
        s,
        [(34.0, 38.0), (156.0, 68.0), (254.0, 84.0), (356.0, 92.0), (482.0, 92.0)],
        stroke_width=sw,
    )

    # Point C' on wavefront
    c1x, c1y = 254.0, 84.0
    # Point E above A on ray F-E
    ex, ey = 456.0, 32.0

    # Rays from F to A, B, C, C', and E (actually F-A extends up-left through E!)
    s.line(fx, fy, ex, ey, stroke_width=sw)       # F -> A -> E
    s.line(fx, fy, bx, by, stroke_width=sw_thin)  # F -> B
    s.line(fx, fy, cx, cy, stroke_width=sw_thin)  # F -> C
    s.line(fx, fy, c1x, c1y, stroke_width=sw_thin)  # F -> C'

    # Circular arc E-C centered at F with radius FC (passing through C and E)
    r_fc = math.hypot(cx - fx, cy - fy)
    ang_c = math.degrees(math.atan2(cy - fy, cx - fx))
    ang_e = math.degrees(math.atan2(ey - fy, ex - fx))
    s.arc(fx, fy, r_fc, ang_c - 6.0, ang_e + 6.0, stroke_width=sw_thin, sweep=1)

    # Dashed chord/arc continuation from C' up-right to (356, 30)
    s.line(c1x, c1y, 356.0, 30.0, stroke_width=sw_thin, dash="16,12")

    # Labels
    lib.label(s, 146.0, 44.0, "C\u2033", size=50.0, italic=False, bold=True)
    lib.label(s, 232.0, 48.0, "C\u2032", size=50.0, italic=False, bold=True)
    lib.label(s, 316.0, 64.0, "C", size=50.0, italic=False, bold=True)
    lib.label(s, 478.0, 46.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 504.0, 74.0, "A", size=50.0, italic=False, bold=True)
    lib.label(s, 384.0, 128.0, "B", size=50.0, italic=False, bold=True)
    lib.label(s, 845.0, 84.0, "G", size=50.0, italic=False, bold=True)
    lib.label(s, 856.0, 1044.0, "F", size=54.0, italic=False, bold=True)

    s.save(out_svg)
