"""Figure 76: Michelson-Morley apparatus vertical cross-section showing stone a, wooden float bb, mercury trough cc, pin d, guides g, lever f, and brick piers."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _draw_brick_pier(
    s: draw.Scene,
    x0: float,
    x1: float,
    row_ys: list[float],
    joint_xs_even: list[float],
    joint_xs_odd: list[float],
    sw: float = 6.0,
) -> None:
    y0, y1 = row_ys[0], row_ys[-1]
    s.rect(x0, y0, x1 - x0, y1 - y0, stroke_width=sw)
    for y in row_ys[1:-1]:
        s.line(x0, y, x1, y, stroke_width=5.0)
    for i in range(len(row_ys) - 1):
        ya, yb = row_ys[i], row_ys[i + 1]
        jxs = joint_xs_even if (i % 2 == 0) else joint_xs_odd
        for jx in jxs:
            s.line(jx, ya, jx, yb, stroke_width=5.0)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    sw_thick = 12.0

    # --- 1. Stone slab a (top) and continuous wooden annular float bb ---
    # Outer vertical sides of stone slab a descending from top to float shoulder y=212
    s.line(81.0, 4.0, 81.0, 212.0, stroke_width=sw)
    s.line(1295.0, 4.0, 1295.0, 212.0, stroke_width=sw)
    # Bottom of stone slab a (left and right of label e)
    s.line(81.0, 170.0, 616.0, 170.0, stroke_width=sw)
    s.line(684.0, 170.0, 1295.0, 170.0, stroke_width=sw)

    # Continuous stepped profile of wooden annular float bb (open at top, continuous with upper structure)
    s.polyline(
        [
            (81.0, 212.0),
            (103.0, 212.0),
            (103.0, 382.0),
            (358.0, 382.0),
            (358.0, 212.0),
            (1010.0, 212.0),
            (1010.0, 382.0),
            (1273.0, 382.0),
            (1273.0, 212.0),
            (1295.0, 212.0),
        ],
        stroke_width=sw,
    )
    # Inner horizontal guide/bridge lines between left and right troughs
    s.line(376.0, 240.0, 992.0, 240.0, stroke_width=sw)
    s.line(376.0, 378.0, 992.0, 378.0, stroke_width=sw)

    # --- 2. Cast-iron mercury trough cc (thick black U-profiles on left & right) ---
    # Left trough U-channel (starts slightly below y=212 shoulder)
    s.polyline(
        [(85.0, 228.0), (85.0, 396.0), (376.0, 396.0), (376.0, 224.0)],
        stroke_width=sw_thick,
    )
    # Right trough U-channel
    s.polyline(
        [(992.0, 224.0), (992.0, 396.0), (1293.0, 396.0), (1293.0, 228.0)],
        stroke_width=sw_thick,
    )

    # --- 3. Central pin d, top flange/plate, socket e, lever f ---
    px = 688.0
    # Thick horizontal flange/plate at the top of central pin d
    s.line(632.0, 214.0, 742.0, 214.0, stroke_width=11.0)
    # Central vertical pin d
    s.line(px, 196.0, px, 396.0, stroke_width=sw)
    # Pivot lever f below pin
    s.circle(px, 396.0, 11.5, fill="#ffffff", stroke="#000000", stroke_width=4.8)
    s.line(px + 11.5, 396.0, px + 72.0, 396.0, stroke_width=4.8)
    s.circle(px + 82.0, 396.0, 10.0, fill="#ffffff", stroke="#000000", stroke_width=4.8)

    # --- 4. Cement cap course and two brick piers below trough ---
    # Left pier cap course (y=400..451) with mortar joint + 8 brick courses (y=451..861)
    s.rect(81.0, 400.0, 298.0, 51.0, stroke_width=sw)
    s.line(247.0, 400.0, 247.0, 451.0, stroke_width=5.0)
    left_rows = [451.0, 505.0, 555.0, 607.0, 657.0, 708.0, 758.0, 811.0, 861.0]
    _draw_brick_pier(s, 81.0, 319.0, left_rows, [162.0], [244.0], sw=sw)

    # Right pier cap course (y=398..446) with mortar joint + 8 brick courses (y=446..858)
    s.rect(999.0, 398.0, 302.0, 48.0, stroke_width=sw)
    s.line(1140.0, 398.0, 1140.0, 446.0, stroke_width=5.0)
    right_rows = [446.0, 498.0, 549.0, 601.0, 653.0, 704.0, 754.0, 806.0, 858.0]
    _draw_brick_pier(s, 1062.0, 1301.0, right_rows, [1226.0], [1140.0], sw=sw)

    # Labels
    lib.label(s, 686.0, 56.0, "a", size=54.0, italic=True, bold=True)
    lib.label(s, 650.0, 168.0, "e", size=46.0, italic=True, bold=True)
    lib.label(s, 48.0, 314.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 224.0, 306.0, "b", size=52.0, italic=True, bold=True)
    lib.label(s, 406.0, 310.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 536.0, 310.0, "g", size=50.0, italic=True, bold=True)
    lib.label(s, 656.0, 304.0, "d", size=52.0, italic=True, bold=True)
    lib.label(s, 816.0, 310.0, "g", size=50.0, italic=True, bold=True)
    lib.label(s, 956.0, 310.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 1136.0, 306.0, "b", size=52.0, italic=True, bold=True)
    lib.label(s, 1324.0, 314.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 536.0, 416.0, "g", size=50.0, italic=True, bold=True)
    lib.label(s, 682.0, 434.0, "f", size=50.0, italic=True, bold=True)
    lib.label(s, 812.0, 416.0, "g", size=50.0, italic=True, bold=True)

    s.save(out_svg)
