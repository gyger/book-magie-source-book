"""Figure 42: Carnot's cylinder and piston abcd with heat reservoirs A and B."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5

    # Cylinder walls (slight natural lean: left 245->240, right 520->516)
    y_top = 212.0
    y_bot = 1213.0
    lx_top, lx_bot = 246.0, 240.0
    rx_top, rx_bot = 521.0, 516.0

    def wall_x(y: float) -> tuple[float, float]:
        t = (y - y_top) / (y_bot - y_top)
        return lx_top + (lx_bot - lx_top) * t, rx_top + (rx_bot - rx_top) * t

    # Cylinder left, right, and bottom a-b
    s.line(lx_top, y_top, lx_bot, y_bot, stroke_width=sw)
    s.line(rx_top, y_top, rx_bot, y_bot, stroke_width=sw)
    s.line(lx_bot, y_bot, rx_bot, y_bot, stroke_width=sw)

    # Piston rod (top y=132 down to dashed piston top y=884)
    rod_top = 132.0
    rod_bot = 884.0
    rl_top, rr_top = 372.0, 390.0
    rl_bot, rr_bot = 368.0, 385.0
    s.line(rl_top, rod_top, rr_top, rod_top, stroke_width=5.5)
    s.line(rl_top, rod_top, rl_bot, rod_bot, stroke_width=5.5)
    s.line(rr_top, rod_top, rr_bot, rod_bot, stroke_width=5.5)

    # Horizontal dashed lines: g-h (y=441), e-f (y=656), piston upper face (y=884), i-k (y=1035)
    for y_dash in (441.5, 656.5, 884.5, 1035.5):
        lx, rx = wall_x(y_dash)
        s.line(lx, y_dash, rx, y_dash, stroke_width=5.5, dash="24,14")

    # Solid piston lower face c-d (y=938)
    lx_cd, rx_cd = wall_x(938.0)
    s.line(lx_cd, 938.0, rx_cd, 938.0, stroke_width=sw)

    # Reservoirs A (left) and B (right) with 45-degree hatching along top and inner vertical walls
    y_res_top = 1379.0
    y_res_bot = 1582.0
    a_x0, a_x1 = 44.0, 283.0
    b_x0, b_x1 = 450.0, 682.0

    # Reservoir A outer boundary (top + right wall)
    s.line(a_x0, y_res_top, a_x1, y_res_top, stroke_width=sw)
    s.line(a_x1, y_res_top, a_x1, y_res_bot, stroke_width=sw)
    # Reservoir B outer boundary (top + left wall)
    s.line(b_x0, y_res_top, b_x1, y_res_top, stroke_width=sw)
    s.line(b_x0, y_res_top, b_x0, y_res_bot, stroke_width=sw)

    # Hatching inside A (below top edge and left of right wall)
    hatch_w = 26.0
    step_h = 20.0
    # Top band of A
    x = a_x0 + 16.0
    while x <= a_x1 + 2.0:
        x_end = max(a_x0, x - hatch_w)
        y_end = y_res_top + (x - x_end)
        s.line(x, y_res_top, x_end, y_end, stroke_width=4.0)
        x += step_h
    # Right wall of A
    y = y_res_top + 16.0
    while y <= y_res_bot - 4.0:
        y_end = min(y_res_bot + 6.0, y + hatch_w)
        x_end = a_x1 - (y_end - y)
        s.line(a_x1, y, x_end, y_end, stroke_width=4.0)
        y += 15.5

    # Hatching inside B (below top edge and right of left wall)
    x = b_x0 + 18.0
    while x <= b_x1 + 2.0:
        x_end = max(b_x0, x - hatch_w)
        y_end = y_res_top + (x - x_end)
        s.line(x, y_res_top, x_end, y_end, stroke_width=4.0)
        x += 21.0
    # Left wall of B
    y = y_res_top + 18.0
    while y <= y_res_bot:
        s.line(b_x0 + hatch_w, y - hatch_w, b_x0, y, stroke_width=4.0)
        y += 17.5

    # Labels
    lib.label(s, 196.0, 440.0, "g", size=58.0, italic=True, bold=True)
    lib.label(s, 556.0, 437.0, "h", size=58.0, italic=True, bold=True)
    lib.label(s, 197.0, 646.0, "e", size=58.0, italic=True, bold=True)
    lib.label(s, 556.0, 645.0, "f", size=58.0, italic=True, bold=True)
    lib.label(s, 194.0, 932.0, "c", size=58.0, italic=True, bold=True)
    lib.label(s, 554.0, 928.0, "d", size=58.0, italic=True, bold=True)
    lib.label(s, 203.0, 1025.0, "i", size=58.0, italic=True, bold=True)
    lib.label(s, 550.0, 1027.0, "k", size=58.0, italic=True, bold=True)
    lib.label(s, 240.0, 1242.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 507.0, 1243.0, "b", size=58.0, italic=True, bold=True)
    lib.label(s, 174.0, 1460.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 551.0, 1458.0, "B", size=58.0, italic=False, bold=True)

    s.save(out_svg)
