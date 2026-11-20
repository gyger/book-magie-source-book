"""Figure 2: Galileo's pendulum and peg experiment (arcs DBC, GB, IB)."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _arc_from_y_to_bottom(
    scene: draw.Scene,
    cx: float,
    cy: float,
    r: float,
    y_start: float,
    stroke_width: float,
) -> tuple[float, float]:
    """Draw circular arc from left intersection with y=y_start down to bottom (cx, cy+r)."""
    dy = y_start - cy
    dx = math.sqrt(max(0.0, r * r - dy * dy))
    sx, sy = cx - dx, y_start
    ang_start = math.degrees(math.atan2(sy - cy, sx - cx))
    ang_end = 90.0
    scene.arc(cx, cy, r, ang_start, ang_end, stroke_width=stroke_width, sweep=0)
    return sx, sy


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.5

    # Vertical axis AB and horizontal level DC
    x_ab = 864.5
    y_dc = 815.5
    y_top = 74.0
    y_bot = 1150.0

    # Pivot A and outer arc D-B-C
    r_a = y_bot - y_top  # 1076
    dy_dc = y_dc - y_top
    dx_dc = math.sqrt(r_a * r_a - dy_dc * dy_dc)
    x_d = x_ab - dx_dc
    x_c = x_ab + dx_dc

    # Horizontal line DC (with slight margins past D and C as in scan)
    scene.line(22.0, y_dc, 1705.0, y_dc, stroke_width=sw)
    # Vertical line AB
    scene.line(x_ab, y_top, x_ab, y_bot, stroke_width=sw)

    # Pendulum strings AD and AC (with tiny extension past A as in woodcut)
    scene.line(x_d, y_dc, x_ab + 30.0, y_top - 30.0 * (y_dc - y_top) / dx_dc, stroke_width=sw)
    scene.line(x_c, y_dc, x_ab, y_top, stroke_width=sw)

    # Outer circular arc D-B-C centered at A
    ang_d = math.degrees(math.atan2(y_dc - y_top, x_d - x_ab))
    ang_c = math.degrees(math.atan2(y_dc - y_top, x_c - x_ab))
    scene.arc(x_ab, y_top, r_a, ang_d, ang_c, stroke_width=sw, sweep=0)

    # Peg E and arc G-B
    # Peg is at y_e=548; woodcut arc G-B passes through G=(350, 815.5) and B=(864.5, 1150)
    y_e = 548.0
    y_arc_g = 587.0
    r_arc_g = y_bot - y_arc_g  # 563.0
    x_g, _ = _arc_from_y_to_bottom(scene, x_ab, y_arc_g, r_arc_g, y_dc, stroke_width=sw)
    # String EG
    scene.line(x_g, y_dc, x_ab, y_e, stroke_width=sw)
    # Peg nail at E sticking up-right
    scene.polygon(
        [(x_ab, y_e), (934.0, 504.0), (942.0, 518.0)],
        fill="#000000",
        stroke="#000000",
        stroke_width=2.0,
    )

    # Peg F and arc I-B
    y_f = 895.0
    r_f = y_bot - y_f  # 255
    x_i, _ = _arc_from_y_to_bottom(scene, x_ab, y_f, r_f, y_dc, stroke_width=sw)
    # String IF
    scene.line(x_i, y_dc, x_ab, y_f, stroke_width=sw)
    # Peg nail at F sticking up-right
    scene.polygon(
        [(x_ab, y_f), (948.0, 854.0), (956.0, 868.0)],
        fill="#000000",
        stroke="#000000",
        stroke_width=2.0,
    )

    # Labels
    lib.label(scene, 842, 46, "A", size=68, italic=False, bold=True)
    lib.label(scene, 822, 522, "E", size=68, italic=False, bold=True)
    lib.label(scene, 56, 774, "D", size=68, italic=False, bold=True)
    lib.label(scene, 332, 772, "G", size=68, italic=False, bold=True)
    lib.label(scene, 615, 774, "I", size=68, italic=False, bold=True)
    lib.label(scene, 1656, 776, "C", size=68, italic=False, bold=True)
    lib.label(scene, 892, 920, "F", size=68, italic=False, bold=True)
    lib.label(scene, 890, 1106, "B", size=68, italic=False, bold=True)

    scene.save(out_svg)
