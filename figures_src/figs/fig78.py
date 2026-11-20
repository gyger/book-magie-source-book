"""Figure 78: Gilbert's oblong lodestone (whole stone a-d and cut into two halves a-b, c-d)."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _hatch_ellipse_rim(
    s: draw.Scene,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    deg_start: float,
    deg_end: float,
    step_deg: float,
    depth_in: float,
    sw: float = 3.2,
) -> None:
    """Draw woodcut-style radial contour hatching around an elliptical stone rim."""
    deg = deg_start
    while deg <= deg_end + 1e-6:
        a = math.radians(deg)
        ca, sa = math.cos(a), math.sin(a)
        x_out = cx + rx * ca
        y_out = cy + ry * sa
        # Deeper shading on underside (sa > 0) and poles (|ca| large)
        frac = depth_in * (0.55 + 0.45 * max(0.0, sa) + 0.25 * abs(ca))
        x_in = cx + rx * (1.0 - frac) * ca
        y_in = cy + ry * (1.0 - frac) * sa
        s.line(x_out, y_out, x_in, y_in, stroke_width=sw)
        deg += step_deg


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # === Top: whole oblong lodestone a-d ===
    cx1, cy1, rx1, ry1 = 738.0, 248.0, 628.0, 232.0
    s.ellipse(cx1, cy1, rx1, ry1, fill="#ffffff", stroke_width=sw)
    _hatch_ellipse_rim(s, cx1, cy1, rx1, ry1, 0.0, 357.0, 3.0, 0.16, sw=3.2)
    # Extra underside cross-contour line for 3D weight
    s.path("M 156 330 C 340 468, 1140 468, 1320 330", stroke_width=sw * 0.85)

    # === Bottom-left half: a-b ===
    # Left half of ellipse centered at (676, 906), rx=612, ry=218, cut at curved vertical section x~676..724
    cx2, cy2, rx2, ry2 = 676.0, 906.0, 612.0, 218.0
    d_left = (
        f"M {cx2 - 8:.1f} {cy2 - ry2:.1f} "
        f"A {rx2:.1f} {ry2:.1f} 0 0 0 {cx2 - 8:.1f} {cy2 + ry2:.1f} "
        f"Q {cx2 + 86:.1f} {cy2:.1f}, {cx2 - 8:.1f} {cy2 - ry2:.1f} Z"
    )
    s.path(d_left, fill="#ffffff", stroke_width=sw)
    _hatch_ellipse_rim(s, cx2, cy2, rx2, ry2, 92.0, 268.0, 3.2, 0.17, sw=3.2)

    # === Bottom-right half: c-d ===
    cx3, cy3, rx3, ry3 = 854.0, 906.0, 624.0, 218.0
    d_right = (
        f"M {cx3:.1f} {cy3 - ry3:.1f} "
        f"A {rx3:.1f} {ry3:.1f} 0 0 1 {cx3:.1f} {cy3 + ry3:.1f} "
        f"Q {cx3 - 54:.1f} {cy3:.1f}, {cx3:.1f} {cy3 - ry3:.1f} Z"
    )
    s.path(d_right, fill="#ffffff", stroke_width=sw)
    _hatch_ellipse_rim(s, cx3, cy3, rx3, ry3, -88.0, 88.0, 3.2, 0.17, sw=3.2)

    # Elliptical cut cross-section face on left of right half
    s.ellipse(cx3 + 2.0, cy3, 30.0, ry3, fill="#ffffff", stroke_width=sw * 0.85)
    # Diagonal shading inside the cut face
    for y in range(int(cy3 - ry3 + 24), int(cy3 + ry3 - 18), 20):
        dy = (y - cy3) / ry3
        hw = 28.0 * max(0.0, 1.0 - dy * dy) ** 0.5
        s.line(cx3 + 2.0 - hw, y + 10.0, cx3 + 2.0 + hw, y - 10.0, stroke_width=3.2)

    # Labels
    lib.label(s, 78.0, 254.0, "a", size=78.0, italic=True, bold=True)
    lib.label(s, 1402.0, 248.0, "d", size=78.0, italic=True, bold=True)
    lib.label(s, 32.0, 912.0, "a", size=78.0, italic=True, bold=True)
    lib.label(s, 692.0, 912.0, "b", size=76.0, italic=True, bold=True)
    lib.label(s, 910.0, 912.0, "c", size=76.0, italic=True, bold=True)

    s.save(out_svg)
