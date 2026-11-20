"""Figure 8: Galileo's parabolic trajectory construction (horizontal ab, vertical bn, parabola bifh)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.5
    sw_grid = 7.0

    # Horizontal levels
    y_ab = 89.5
    y_o = 140.5
    y_g = 245.5
    y_l = 423.5
    y_n = 658.5

    # Vertical columns
    x_left = 92.5
    x_e = 375.5
    x_d = 649.5
    x_c = 921.5
    x_b = 1205.5

    # Top horizontal line a-b extending across entire figure
    scene.line(48.0, y_ab, 1602.0, y_ab, stroke_width=sw)

    # Vertical lines (with slight overhang at top/bottom as in scan)
    scene.line(x_left, 72.0, x_left, 695.0, stroke_width=sw_grid)
    scene.line(x_e, y_ab, x_e, 695.0, stroke_width=sw_grid)
    scene.line(x_d, y_ab, x_d, 695.0, stroke_width=sw_grid)
    scene.line(x_c, y_ab, x_c, 695.0, stroke_width=sw_grid)
    scene.line(x_b, y_ab, x_b, 695.0, stroke_width=sw_grid)

    # Horizontal projection lines from parabola points to vertical b-n
    scene.line(x_c, y_o, x_b, y_o, stroke_width=sw_grid)
    scene.line(x_d, y_g, x_b, y_g, stroke_width=sw_grid)
    scene.line(x_e, y_l, x_b, y_l, stroke_width=sw_grid)
    scene.line(x_left, y_n, x_b, y_n, stroke_width=sw)

    # Smooth parabolic curve through b -> i -> f -> h -> bottom-left
    # Use piecewise cubic Bezier / Catmull-Rom through exact grid intersections
    pts = [
        (x_b, y_ab),
        (x_c, y_o),
        (x_d, y_g),
        (x_e, y_l),
        (x_left, y_n),
    ]
    lib.smooth_curve(scene, pts, stroke_width=sw)

    # Italic lowercase labels matching the original diagram
    lib.label(scene, 376, 48, "e", size=54, italic=True, bold=True)
    lib.label(scene, 650, 44, "d", size=54, italic=True, bold=True)
    lib.label(scene, 920, 48, "c", size=54, italic=True, bold=True)
    lib.label(scene, 1206, 44, "b", size=54, italic=True, bold=True)
    lib.label(scene, 1575, 56, "a", size=54, italic=True, bold=True)

    lib.label(scene, 1230, 138, "o", size=54, italic=True, bold=True)
    lib.label(scene, 892, 168, "i", size=54, italic=True, bold=True)
    lib.label(scene, 620, 218, "f", size=54, italic=True, bold=True)
    lib.label(scene, 1234, 246, "g", size=54, italic=True, bold=True)
    lib.label(scene, 326, 416, "h", size=54, italic=True, bold=True)
    lib.label(scene, 1228, 420, "l", size=54, italic=True, bold=True)
    lib.label(scene, 1230, 656, "n", size=54, italic=True, bold=True)

    scene.save(out_svg)
