"""Figure 21: Isometric wireframe blocks A, (A), B, (B) with dashed reference lines CD and EF."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _draw_subdivided_block(
    s: draw.Scene,
    x0: float,
    y0: float,
    w_front: float,
    h_cell: float,
    dx_step: float,
    dy_step: float,
    *,
    sw: float = 6.5,
    dash: str | None = None,
) -> None:
    """Draw 1x2 front face extruded 2 steps along (dx_step, dy_step)."""
    x1 = x0 + w_front
    ym = y0 + h_cell
    y2 = y0 + 2 * h_cell

    def shift(x: float, y: float, k: int) -> tuple[float, float]:
        return (x + k * dx_step, y + k * dy_step)

    # Front face outline + mid horizontal divider
    s.line(x0, y0, x1, y0, stroke_width=sw, dash=dash)
    s.line(x0, ym, x1, ym, stroke_width=sw, dash=dash)
    s.line(x0, y2, x1, y2, stroke_width=sw, dash=dash)
    s.line(x0, y0, x0, y2, stroke_width=sw, dash=dash)
    s.line(x1, y0, x1, y2, stroke_width=sw, dash=dash)

    # Top face: 3 depth edges + 2 depth cross-lines (k=1, k=2)
    s.line(x0, y0, *shift(x0, y0, 2), stroke_width=sw, dash=dash)
    s.line(x1, y0, *shift(x1, y0, 2), stroke_width=sw, dash=dash)
    for k in (1, 2):
        s.line(*shift(x0, y0, k), *shift(x1, y0, k), stroke_width=sw, dash=dash)

    # Right face: mid & bottom depth edges + vertical dividers (k=1, k=2)
    s.line(x1, ym, *shift(x1, ym, 2), stroke_width=sw, dash=dash)
    s.line(x1, y2, *shift(x1, y2, 2), stroke_width=sw, dash=dash)
    for k in (1, 2):
        s.line(*shift(x1, y0, k), *shift(x1, y2, k), stroke_width=sw, dash=dash)


def _draw_single_cube(
    s: draw.Scene,
    x0: float,
    y0: float,
    w: float,
    h: float,
    dx: float,
    dy: float,
    *,
    sw: float = 6.5,
    dash: str | None = None,
) -> None:
    """Draw a single isometric cube."""
    # Front face
    s.line(x0, y0, x0 + w, y0, stroke_width=sw, dash=dash)
    s.line(x0, y0 + h, x0 + w, y0 + h, stroke_width=sw, dash=dash)
    s.line(x0, y0, x0, y0 + h, stroke_width=sw, dash=dash)
    s.line(x0 + w, y0, x0 + w, y0 + h, stroke_width=sw, dash=dash)
    # Top face
    s.line(x0, y0, x0 + dx, y0 + dy, stroke_width=sw, dash=dash)
    s.line(x0 + w, y0, x0 + w + dx, y0 + dy, stroke_width=sw, dash=dash)
    s.line(x0 + dx, y0 + dy, x0 + w + dx, y0 + dy, stroke_width=sw, dash=dash)
    # Right face
    s.line(x0 + w + dx, y0 + dy, x0 + w + dx, y0 + h + dy, stroke_width=sw, dash=dash)
    s.line(x0 + w, y0 + h, x0 + w + dx, y0 + h + dy, stroke_width=sw, dash=dash)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    dx_off = 3.0
    dy_off = 750.0

    # Left vertical dashed reference line C-D
    s.line(221.0 + dx_off, 108.0, 221.0 + dx_off, 810.0 + dy_off, stroke_width=6.0, dash="22,10")

    # Right vertical dashed reference line E-F
    s.line(1285.0 + dx_off, 180.0 + dy_off, 1285.0 + dx_off, 534.0 + dy_off, stroke_width=6.0, dash="22,12")

    # Block A (solid, single cube at top-left)
    _draw_single_cube(s, 30.0, 134.0, 82.0, 77.0, 73.0, -44.0, sw=6.5, dash=None)

    # Block (A) (dashed, single cube at bottom-left)
    _draw_single_cube(s, 28.0, 777.0 + dy_off, 82.0, 77.0, 75.0, -45.0, sw=6.0, dash="18,10")

    # Block B (solid)
    _draw_subdivided_block(s, 1018.0 + dx_off, 171.0 + dy_off, 82.0, 85.0, 77.0, -41.5, sw=6.5, dash=None)

    # Block (B) (dashed)
    _draw_subdivided_block(s, 1018.0 + dx_off, 546.0 + dy_off, 82.0, 84.0, 77.0, -43.5, sw=6.0, dash="18,10")

    # Labels
    lib.label(s, 138, 54, "A", size=52, italic=False, bold=True)
    lib.label(s, 258, 128, "C", size=52, italic=False, bold=True)
    lib.label(s, 966 + dx_off, 251 + dy_off, "B", size=52, italic=False, bold=True)
    lib.label(s, 953 + dx_off, 630 + dy_off, "(B)", size=52, italic=False, bold=True)
    lib.label(s, 133 + dx_off, 694 + dy_off, "(A)", size=52, italic=False, bold=True)
    lib.label(s, 254 + dx_off, 787 + dy_off, "D", size=52, italic=False, bold=True)
    lib.label(s, 1313 + dx_off, 217 + dy_off, "E", size=52, italic=False, bold=True)
    lib.label(s, 1314 + dx_off, 506 + dy_off, "F", size=52, italic=False, bold=True)

    s.save(out_svg)
