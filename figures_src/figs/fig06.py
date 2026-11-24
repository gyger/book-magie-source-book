"""Figure 6: Inclined planes AB, AD, AE, AF, AC with pulley F and weights G, H (Galileo)."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.5
    sw_dash = 6.5

    # Common vertex A
    ax, ay = 868.5, 835.5

    # Vertical AB and horizontal AC
    scene.line(ax, ay, 870.0, 74.0, stroke_width=sw)
    scene.line(ax, ay, 134.0, 831.0, stroke_width=sw)

    # Inclined rays AD and AE
    scene.line(ax, ay, 614.0, 116.0, stroke_width=sw)
    scene.line(ax, ay, 342.0, 290.0, stroke_width=sw)

    # Circles F (pulley), G (weight on plane), H (hanging weight)
    fx, fy, fr = 141.0, 502.0, 34.0
    gx, gy, gr = 331.0, 577.0, 33.5
    hx, hy, hr = 103.0, 717.0, 33.0

    # Inclined plane AF tangent to underside of G and F
    scene.line(ax, ay, 132.0, 532.0, stroke_width=sw)

    # Dashed cord from top of F to top of G
    scene.line(fx + 16.0, fy - fr + 8.0, gx + 4.0, gy - gr + 13.0, stroke_width=sw_dash, dash="22,14")

    # Dashed cord from left side of F straight down to top of H
    scene.line(105.0, fy + 4.0, 105.0, hy - hr, stroke_width=sw_dash, dash="22,14")

    # Dashed vertical projection from F down to C on AC
    scene.line(150.0, fy + fr, 150.0, 831.0, stroke_width=sw_dash, dash="22,14")

    # Draw circles on top with white fill so lines stop cleanly at rim
    scene.circle(fx, fy, fr, fill="#ffffff", stroke="#000000", stroke_width=sw)
    scene.circle(gx, gy, gr, fill="#ffffff", stroke="#000000", stroke_width=sw)
    scene.circle(hx, hy, hr, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Labels
    lib.label(scene, 862, 46, "B", size=60, italic=False, bold=True)
    lib.label(scene, 575, 90, "D", size=60, italic=False, bold=True)
    lib.label(scene, 302, 260, "E", size=60, italic=False, bold=True)
    lib.label(scene, 98, 442, "F", size=60, italic=False, bold=True)
    lib.label(scene, 396, 576, "G", size=60, italic=False, bold=True)
    lib.label(scene, 32, 710, "H", size=60, italic=False, bold=True)
    lib.label(scene, 142, 874, "C", size=60, italic=False, bold=True)
    lib.label(scene, 900, 842, "A", size=60, italic=False, bold=True)

    scene.save(out_svg)
