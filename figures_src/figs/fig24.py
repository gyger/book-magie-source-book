"""Figure 24: Torricelli's barometer experiment — straight tube (B) and bulb tube (A) in mercury basin (C, D)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # --- Basin / Dish at bottom (y=1715..2322) ---
    # 1) Pedestal foot (outer ellipse + inner shadow crescent)
    s.ellipse(310.0, 2258.0, 212.0, 64.0, fill="#ffffff", stroke="#000000", stroke_width=14.0)
    # Dark shadow under stem on top of foot
    s.path(
        "M 156 2205 C 210 2184, 410 2184, 464 2205 "
        "C 476 2248, 390 2274, 310 2274 "
        "C 230 2274, 144 2248, 156 2205 Z",
        fill="#000000",
        stroke="none",
    )

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
        "M 62 2055 "
        "C 62 2008, 106 1962, 120 1930 "
        "C 190 1916, 405 1916, 476 1930 "
        "C 492 1966, 542 2008, 542 2055 "
        "C 542 2106, 440 2124, 302 2124 "
        "C 164 2124, 62 2106, 62 2055 Z",
        fill="#ffffff",
        stroke="none",
    )

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
    # Spherical glass bulb at top (black silhouette + white upper highlight)
    s.ellipse(410.0, 108.0, 91.0, 87.0, fill="#000000", stroke="#000000", stroke_width=6.0)
    s.ellipse(399.0, 74.0, 52.0, 44.0, fill="#ffffff", stroke="none")

    # Labels
    lib.label(s, 62.0, 304.0, "B", size=54.0, italic=False, bold=True)
    lib.label(s, 508.0, 302.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 326.0, 1812.0, "D", size=56.0, italic=False, bold=True)
    lib.label(s, 255.0, 2042.0, "C", size=56.0, italic=False, bold=True)

    s.save(out_svg)
