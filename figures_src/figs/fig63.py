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
    ax, ay = 1696.0, 106.0
    bx, by = 1770.0, 114.0

    # Screen horizontal base C-D
    y_cd = 912.0
    cx, dx = 113.0, 1131.0
    s.line(74.0, y_cd, 1148.0, y_cd, stroke_width=sw)

    # Outer cone boundaries A-C and B-D
    s.line(ax, ay, cx, y_cd, stroke_width=sw)
    s.line(bx, by, dx, y_cd, stroke_width=sw)

    # Geometric shadow rays past F and E onto I, G, H, L:
    # From B through F -> I, from A through F -> G,
    # from B through E -> H, from A through E -> L
    s.line(bx, by, 482.0, y_cd, stroke_width=sw_thin)
    s.line(ax, ay, 584.0, y_cd, stroke_width=sw_thin)
    s.line(bx, by, 754.0, y_cd, stroke_width=sw_thin)
    s.line(ax, ay, 829.0, y_cd, stroke_width=sw_thin)

    # Opaque obstacle F-E (small hatched rectangle, drawn on top of rays)
    f_tl = (1244.0, 426.0)
    f_tr = (1264.0, 420.0)
    e_br = (1286.0, 486.0)
    e_bl = (1264.0, 493.0)
    s.polygon([f_tl, f_tr, e_br, e_bl], fill="#ffffff", stroke="#000000", stroke_width=5.0)
    # Cross-hatching inside obstacle FE
    for i in range(1, 6):
        t = i / 6.0
        p1 = (f_tl[0] + (e_bl[0] - f_tl[0]) * t, f_tl[1] + (e_bl[1] - f_tl[1]) * t)
        p2 = (f_tr[0] + (e_br[0] - f_tr[0]) * t, f_tr[1] + (e_br[1] - f_tr[1]) * t)
        s.line(*p1, *p2, stroke_width=3.5)

    # Diffracted dashed rays from F -> M and from E -> N
    s.line(f_tl[0], f_tl[1], 324.0, y_cd, stroke_width=5.0, dash="18,14")
    s.line(e_bl[0], e_bl[1], 932.0, y_cd, stroke_width=5.0, dash="18,14")

    # Labels
    lib.label(s, 1668.0, 60.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 1812.0, 82.0, "B", size=54.0, italic=False, bold=True)
    lib.label(s, 1236.0, 386.0, "F", size=50.0, italic=False, bold=True)
    lib.label(s, 1298.0, 545.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 96.0, 868.0, "C", size=54.0, italic=False, bold=True)
    lib.label(s, 1198.0, 912.0, "D", size=54.0, italic=False, bold=True)

    lib.label(s, 316.0, 962.0, "M", size=48.0, italic=False, bold=True)
    lib.label(s, 476.0, 962.0, "I", size=48.0, italic=False, bold=True)
    lib.label(s, 580.0, 962.0, "G", size=48.0, italic=False, bold=True)
    lib.label(s, 738.0, 962.0, "H", size=48.0, italic=False, bold=True)
    lib.label(s, 826.0, 962.0, "L", size=48.0, italic=False, bold=True)
    lib.label(s, 926.0, 962.0, "N", size=48.0, italic=False, bold=True)

    s.save(out_svg)
