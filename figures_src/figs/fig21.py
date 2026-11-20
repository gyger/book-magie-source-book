"""Figure 21: Isometric wireframe blocks (A), B, (B) with dashed reference lines."""

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
    # Front face corners (x0, y0) is top-left of front face
    x1 = x0 + w_front
    ym = y0 + h_cell
    y2 = y0 + 2 * h_cell

    # Depth points (0, 1, 2 steps)
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


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # Left vertical dashed reference line down to D
    s.line(221.0, 10.0, 221.0, 810.0, stroke_width=6.0, dash="22,10")

    # Right vertical dashed reference line E-F
    s.line(1285.0, 180.0, 1285.0, 534.0, stroke_width=6.0, dash="22,12")

    # Block B (solid)
    _draw_subdivided_block(s, 1018.0, 171.0, 82.0, 85.0, 77.0, -41.5, sw=6.5, dash=None)

    # Block (B) (dashed)
    _draw_subdivided_block(s, 1018.0, 546.0, 82.0, 84.0, 77.0, -43.5, sw=6.0, dash="18,10")

    # Block (A) (dashed, single cube at bottom-left)
    ax0, ay0 = 24.0, 777.0
    aw, ah = 82.0, 77.0
    adx, ady = 76.0, -45.0
    d_a = "18,10"
    sw_a = 6.0
    # Front face
    s.line(ax0, ay0, ax0 + aw, ay0, stroke_width=sw_a, dash=d_a)
    s.line(ax0, ay0, ax0, ay0 + ah, stroke_width=sw_a, dash=d_a)
    s.line(ax0 + aw, ay0, ax0 + aw, ay0 + ah, stroke_width=sw_a, dash=d_a)
    # Top face
    s.line(ax0, ay0, ax0 + adx, ay0 + ady, stroke_width=sw_a, dash=d_a)
    s.line(ax0 + aw, ay0, ax0 + aw + adx, ay0 + ady, stroke_width=sw_a, dash=d_a)
    s.line(ax0 + adx, ay0 + ady, ax0 + aw + adx, ay0 + ady, stroke_width=sw_a, dash=d_a)
    # Right face
    s.line(ax0 + aw + adx, ay0 + ady, ax0 + aw + adx, ay0 + ah + ady, stroke_width=sw_a, dash=d_a)
    s.line(ax0 + aw, ay0 + ah, ax0 + aw + adx, ay0 + ah + ady, stroke_width=sw_a, dash=d_a)

    # Labels
    lib.label(s, 966, 251, "B", size=52, italic=False, bold=True)
    lib.label(s, 953, 630, "(B)", size=52, italic=False, bold=True)
    lib.label(s, 133, 694, "(A)", size=52, italic=False, bold=True)
    lib.label(s, 254, 787, "D", size=52, italic=False, bold=True)
    lib.label(s, 1313, 217, "E", size=52, italic=False, bold=True)
    lib.label(s, 1314, 506, "F", size=52, italic=False, bold=True)

    s.save(out_svg)
