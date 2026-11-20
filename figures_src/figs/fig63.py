"""Figure 63: Grimaldi's first diffraction experiment — light cone AB past opaque obstacle FE onto screen CD."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    sw_thin = 4.2

    # Aperture A (left edge) and B (right edge)
    ax, ay = 1692.0, 114.0
    bx, by = 1766.0, 128.0

    # Screen horizontal base C-D
    y_cd = 925.0
    cx, dx = 74.0, 1134.0
    s.line(cx, y_cd, dx, y_cd, stroke_width=sw)

    # Outer cone boundaries A-C and B-D
    s.line(ax, ay, cx, y_cd, stroke_width=sw)
    s.line(bx, by, dx, y_cd, stroke_width=sw)

    # Opaque obstacle F-E (small shaded rectangle)
    f_tl = (1236.0, 428.0)
    f_tr = (1256.0, 422.0)
    e_br = (1278.0, 488.0)
    e_bl = (1256.0, 495.0)
    s.polygon([f_tl, f_tr, e_br, e_bl], fill="#ffffff", stroke="#000000", stroke_width=5.0)
    # Cross-hatching inside obstacle FE
    for i in range(1, 6):
        t = i / 6.0
        p1 = (f_tl[0] + (e_bl[0] - f_tl[0]) * t, f_tl[1] + (e_bl[1] - f_tl[1]) * t)
        p2 = (f_tr[0] + (e_br[0] - f_tr[0]) * t, f_tr[1] + (e_br[1] - f_tr[1]) * t)
        s.line(*p1, *p2, stroke_width=3.5)

    # Geometric shadow rays past F and E onto I, G, H, L
    s.line(ax, ay, 514.0, y_cd, stroke_width=sw_thin)
    s.line(bx, by, 608.0, y_cd, stroke_width=sw_thin)
    s.line(ax, ay, 782.0, y_cd, stroke_width=sw_thin)
    s.line(bx, by, 850.0, y_cd, stroke_width=sw_thin)

    # Diffracted dashed rays from F -> M and from E -> N
    s.line(f_tl[0], f_tl[1], 362.0, y_cd, stroke_width=5.0, dash="18,14")
    s.line(e_bl[0], e_bl[1], 950.0, y_cd, stroke_width=5.0, dash="18,14")

    # Small aperture oval at A-B
    s.line(ax - 22.0, ay + 10.0, bx + 18.0, by - 4.0, stroke_width=3.5)

    # Labels
    lib.label(s, 1660.0, 62.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 1805.0, 88.0, "B", size=54.0, italic=False, bold=True)
    lib.label(s, 1234.0, 386.0, "F", size=50.0, italic=False, bold=True)
    lib.label(s, 1295.0, 542.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 98.0, 882.0, "C", size=54.0, italic=False, bold=True)
    lib.label(s, 1178.0, 922.0, "D", size=54.0, italic=False, bold=True)

    lib.label(s, 316.0, 966.0, "M", size=48.0, italic=False, bold=True)
    lib.label(s, 476.0, 966.0, "I", size=48.0, italic=False, bold=True)
    lib.label(s, 568.0, 966.0, "G", size=48.0, italic=False, bold=True)
    lib.label(s, 725.0, 966.0, "H", size=48.0, italic=False, bold=True)
    lib.label(s, 816.0, 966.0, "L", size=48.0, italic=False, bold=True)
    lib.label(s, 920.0, 966.0, "N", size=48.0, italic=False, bold=True)

    s.save(out_svg)
