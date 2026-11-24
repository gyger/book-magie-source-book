"""Figure 24: Torricelli's barometer experiment — straight tube (B) and bulb tube (A) in mercury basin (C, D)."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _hatch_stroke(
    s: draw.Scene,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    w_base: float = 5.5,
) -> None:
    """Draw a tapered woodcut hatching stroke from (x1, y1) (wide) to (x2, y2) (pointed)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 1.0:
        return
    nx, ny = -dy / L, dx / L
    hw = w_base * 0.5
    pts = [
        (x1 - nx * hw, y1 - ny * hw),
        (x1 + nx * hw, y1 + ny * hw),
        (x2, y2),
    ]
    s.polygon(pts, fill="#000000", stroke="none")


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # --- Basin / Dish at bottom (y=1715..2322) ---
    # 1) Pedestal foot (outer ellipse + hatched shadow under stem)
    s.ellipse(308.0, 2258.0, 211.0, 63.0, fill="#ffffff", stroke="#000000", stroke_width=14.0)
    # Dark shadow core under stem on top of foot
    s.path(
        "M 134 2204 C 195 2180, 415 2180, 476 2204 "
        "C 476 2246, 392 2266, 308 2266 "
        "C 224 2266, 134 2246, 134 2204 Z",
        fill="#000000",
        stroke="none",
    )
    # Downward woodcut hatching along lower edge of pedestal stem shadow
    foot_hatch_lengths = [
        14, 20, 18, 24, 22, 26, 20, 28, 24, 30, 22, 28, 26,
        30, 24, 28, 22, 26, 20, 24, 18, 22, 16, 18, 14,
    ]
    for i, hl in enumerate(foot_hatch_lengths):
        t = i / (len(foot_hatch_lengths) - 1)
        x = 144.0 + t * 324.0
        u = (t - 0.5) * 2.0  # -1..1
        y_base = 2258.0 - 24.0 * (u * u)
        _hatch_stroke(s, x, y_base - 8.0, x - u * 4.0, y_base + hl, w_base=8.2)

    # 2) Outer basin body (filled black, then carve out white inner surfaces cleanly)
    basin_outer = (
        "M 6 1815 "
        "C 6 1750, 140 1715, 296 1715 "
        "C 452 1715, 588 1750, 588 1815 "
        "C 588 1850, 540 1890, 515 1935 "
        "C 515 1965, 593 2000, 593 2050 "
        "C 593 2135, 480 2185, 310 2185 "
        "C 140 2185, 12 2135, 12 2050 "
        "C 12 2000, 76 1965, 76 1935 "
        "C 54 1890, 6 1850, 6 1815 Z"
    )
    s.path(basin_outer, fill="#000000", stroke="#000000", stroke_width=6.0)

    # 3) White upper opening of basin (mercury surface / open top D)
    s.path(
        "M 16 1815 "
        "C 16 1758, 142 1726, 296 1726 "
        "C 450 1726, 576 1758, 576 1815 "
        "C 576 1868, 450 1906, 296 1906 "
        "C 142 1906, 16 1868, 16 1815 Z",
        fill="#ffffff",
        stroke="none",
    )

    # 4) White belly reflection of basin (around C)
    s.path(
        "M 46 2050 "
        "C 46 2004, 94 1960, 114 1926 "
        "C 188 1914, 408 1914, 484 1926 "
        "C 502 1962, 552 2004, 552 2050 "
        "C 552 2102, 442 2120, 302 2120 "
        "C 162 2120, 46 2102, 46 2050 Z",
        fill="#ffffff",
        stroke="none",
    )

    # 5) Woodcut vertical hatching under the liquid surface / neck of basin
    # Left of left tube
    neck_left_lens = [24, 34, 28, 38, 32, 36]
    for i, hl in enumerate(neck_left_lens):
        x = 80.0 + i * 10.5
        y0 = 1938.0 - i * 3.5
        _hatch_stroke(s, x, y0 - 10.0, x - 2.0, y0 + hl, w_base=7.6)

    # Between the two tubes (prominent vertical hatching fringe below liquid surface)
    neck_mid_lens = [32, 44, 34, 48, 38, 50, 42, 46, 36, 48, 40, 46, 38, 44, 34, 40]
    for i, hl in enumerate(neck_mid_lens):
        x = 222.0 + i * 9.8
        y0 = 1916.0
        _hatch_stroke(s, x, y0 - 10.0, x, y0 + hl, w_base=7.8)

    # Right of right tube
    neck_right_lens = [34, 42, 32, 38, 30, 24]
    for i, hl in enumerate(neck_right_lens):
        x = 460.0 + i * 10.2
        y0 = 1920.0 + i * 3.5
        _hatch_stroke(s, x, y0 - 10.0, x + 2.0, y0 + hl, w_base=7.6)

    # 6) Woodcut upward hatching along the lower belly of basin
    belly_lens = [
        18, 24, 20, 28, 22, 30, 26, 32, 24, 30,
        28, 34, 26, 32, 28, 36, 30, 34, 28, 36,
        32, 34, 28, 36, 30, 34, 28, 32, 26, 34,
        28, 30, 24, 32, 26, 30, 22, 28, 20, 24,
        18, 22, 16, 20, 16,
    ]
    n_b = len(belly_lens)
    for i, hl in enumerate(belly_lens):
        t = i / (n_b - 1)
        u = (t - 0.5) * 2.0  # -1..1
        x = 52.0 + t * 496.0
        # Follow lower belly contour from y≈2050 at edges to y≈2118 at center
        y_base = 2118.0 - 66.0 * (u * u) * (0.35 + 0.65 * abs(u))
        dx_tip = -u * 8.0  # gentle inward tilt near the curved sides
        _hatch_stroke(s, x, y_base + 12.0, x + dx_tip, y_base - hl, w_base=8.0)

    # --- Horizontal mercury-level line B-A ---
    s.line(66.0, 337.0, 530.0, 333.0, stroke_width=13.0)

    # --- Left Tube (straight, rounded top) ---
    # Upper vacuum part (white fill, black walls)
    s.path(
        "M 131 337 L 131 104 C 131 58, 207 58, 207 104 L 207 337 Z",
        fill="#ffffff",
        stroke="#000000",
        stroke_width=12.0,
    )
    # Filled mercury column inside left tube (slight rightward tilt matching scan)
    s.path(
        "M 125 337 L 213 337 L 220 2036 "
        "C 220 2070, 136 2070, 136 2036 Z",
        fill="#000000",
        stroke="none",
    )

    # --- Right Tube (spherical bulb at top) ---
    # Upper vacuum neck below bulb
    s.path(
        "M 374 335 L 374 176 L 448 176 L 448 335 Z",
        fill="#ffffff",
        stroke="#000000",
        stroke_width=12.0,
    )
    # Filled mercury column inside right tube
    s.path(
        "M 368 335 L 454 335 L 458 2028 "
        "C 458 2062, 374 2062, 374 2028 Z",
        fill="#000000",
        stroke="none",
    )
    # Spherical glass bulb at top (black silhouette + white upper highlight + woodcut hatching)
    s.ellipse(410.0, 108.0, 91.0, 87.0, fill="#000000", stroke="#000000", stroke_width=6.0)
    hl_cx, hl_cy, hl_rx, hl_ry = 401.0, 74.0, 56.0, 44.0
    s.ellipse(hl_cx, hl_cy, hl_rx, hl_ry, fill="#ffffff", stroke="none")
    # Radial/vertical-ish woodcut hatching ticks concentrated along right & lower edge of bulb highlight
    bulb_angles_deg = [-32, -20, -8, 4, 16, 28, 40, 52, 64, 76, 88, 100, 114, 128]
    bulb_lens = [14, 18, 22, 18, 24, 18, 22, 16, 18, 14, 16, 12, 12, 10]
    for ang_deg, hl in zip(bulb_angles_deg, bulb_lens):
        rad = math.radians(ang_deg)
        ca, sa = math.cos(rad), math.sin(rad)
        x1 = hl_cx + (hl_rx + 6.0) * ca
        y1 = hl_cy + (hl_ry + 6.0) * sa
        x2 = hl_cx + (hl_rx - hl) * ca
        y2 = hl_cy + (hl_ry - hl) * sa - 2.0
        _hatch_stroke(s, x1, y1, x2, y2, w_base=6.8)

    # Labels
    lib.label(s, 62.0, 304.0, "B", size=54.0, italic=False, bold=True)
    lib.label(s, 508.0, 302.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 326.0, 1812.0, "D", size=56.0, italic=False, bold=True)
    lib.label(s, 255.0, 2042.0, "C", size=56.0, italic=False, bold=True)

    s.save(out_svg)
