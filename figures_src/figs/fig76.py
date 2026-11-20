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
    y0: float,
    y1: float,
    n_rows: int = 8,
    sw: float = 5.5,
) -> None:
    s.rect(x0, y0, x1 - x0, y1 - y0, stroke_width=sw)
    row_h = (y1 - y0) / n_rows
    for i in range(1, n_rows):
        y = y0 + i * row_h
        s.line(x0, y, x1, y, stroke_width=4.5)
    # Alternating vertical brick joints
    for i in range(n_rows):
        ya = y0 + i * row_h
        yb = y0 + (i + 1) * row_h
        if i % 2 == 0:
            for frac in (0.35, 0.70):
                jx = x0 + (x1 - x0) * frac
                s.line(jx, ya, jx, yb, stroke_width=4.0)
        else:
            for frac in (0.18, 0.52, 0.85):
                jx = x0 + (x1 - x0) * frac
                s.line(jx, ya, jx, yb, stroke_width=4.0)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    sw_thick = 11.0

    # --- 1. Stone slab a (top) ---
    # Open top sides descending from y=4 down to y=170, with central socket recess e
    s.line(82.0, 4.0, 82.0, 212.0, stroke_width=sw)
    s.line(1292.0, 4.0, 1292.0, 212.0, stroke_width=sw)
    # Bottom of stone slab a (left and right of label e)
    s.line(82.0, 170.0, 614.0, 170.0, stroke_width=sw)
    s.line(688.0, 170.0, 1292.0, 170.0, stroke_width=sw)

    # --- 2. Wooden annular float bb (left and right blocks) ---
    # Left float b: x = 108..366, y = 218..380
    s.rect(108.0, 218.0, 258.0, 162.0, stroke_width=sw)
    # Right float b: x = 1004..1262, y = 218..380
    s.rect(1004.0, 218.0, 258.0, 162.0, stroke_width=sw)
    # Inner connecting bridge/plate above guides g
    s.line(366.0, 218.0, 1004.0, 218.0, stroke_width=sw)
    s.line(382.0, 240.0, 988.0, 240.0, stroke_width=sw)
    s.line(382.0, 378.0, 988.0, 378.0, stroke_width=sw)

    # --- 3. Cast-iron mercury trough cc (thick black U-profiles on left & right) ---
    # Left trough U-channel
    s.polyline(
        [(82.0, 212.0), (82.0, 396.0), (382.0, 396.0), (382.0, 212.0)],
        stroke_width=sw_thick,
    )
    # Right trough U-channel
    s.polyline(
        [(988.0, 212.0), (988.0, 396.0), (1292.0, 396.0), (1292.0, 212.0)],
        stroke_width=sw_thick,
    )

    # --- 4. Central pin d, socket e, lever f ---
    px = 684.0
    s.line(px, 200.0, px, 412.0, stroke_width=sw)
    # Pivot lever f below pin
    s.circle(px, 396.0, 12.0, fill="#ffffff", stroke="#000000", stroke_width=4.5)
    s.line(px + 12.0, 396.0, px + 76.0, 396.0, stroke_width=4.5)
    s.circle(px + 86.0, 396.0, 10.0, fill="#ffffff", stroke="#000000", stroke_width=4.5)

    # --- 5. Cement cap and two brick piers below trough ---
    # Left pier cement cap (y=402..446) + brick pier (x=82..324, y=446..852)
    s.rect(82.0, 402.0, 300.0, 44.0, stroke_width=sw)
    _draw_brick_pier(s, 82.0, 324.0, 446.0, 852.0, n_rows=8, sw=sw)

    # Right pier cement cap (y=402..446) + brick pier (x=1052..1292, y=446..852)
    s.rect(988.0, 402.0, 304.0, 44.0, stroke_width=sw)
    _draw_brick_pier(s, 1052.0, 1292.0, 446.0, 852.0, n_rows=8, sw=sw)

    # Labels
    lib.label(s, 686.0, 56.0, "a", size=54.0, italic=True, bold=True)
    lib.label(s, 654.0, 168.0, "e", size=46.0, italic=True, bold=True)
    lib.label(s, 48.0, 314.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 224.0, 306.0, "b", size=52.0, italic=True, bold=True)
    lib.label(s, 412.0, 314.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 536.0, 314.0, "g", size=50.0, italic=True, bold=True)
    lib.label(s, 654.0, 306.0, "d", size=52.0, italic=True, bold=True)
    lib.label(s, 816.0, 314.0, "g", size=50.0, italic=True, bold=True)
    lib.label(s, 954.0, 314.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 1136.0, 306.0, "b", size=52.0, italic=True, bold=True)
    lib.label(s, 1326.0, 314.0, "c", size=48.0, italic=True, bold=True)
    lib.label(s, 536.0, 418.0, "g", size=50.0, italic=True, bold=True)
    lib.label(s, 678.0, 434.0, "f", size=50.0, italic=True, bold=True)
    lib.label(s, 814.0, 418.0, "g", size=50.0, italic=True, bold=True)

    s.save(out_svg)
