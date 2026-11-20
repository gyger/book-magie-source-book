"""Figure 40: Cagniard de la Tour's broken siphon-barometer tube for critical-point vapor pressure."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.2

    # --- Upper broken section (sealed tip a down to jagged break at y~1570) ---
    # Left wall: tip (116, 62) -> shoulder (80, 356) -> straight down to (82, 1558)
    # Right wall: tip (116, 62) -> shoulder (136, 356) -> straight down to (143, 1545)
    upper_pts = [
        (116.0, 62.0),
        (98.0, 200.0),
        (80.0, 356.0),
        (76.0, 500.0),
        (78.0, 1000.0),
        (82.0, 1558.0),
        # Jagged break along bottom of upper section
        (95.0, 1582.0),
        (106.0, 1546.0),
        (116.0, 1572.0),
        (127.0, 1538.0),
        (143.0, 1552.0),
        # Right wall going back up
        (139.0, 1000.0),
        (137.0, 500.0),
        (136.0, 356.0),
        (130.0, 200.0),
        (116.0, 62.0),
    ]
    s.polyline(upper_pts, stroke_width=sw)

    # Dashed mercury levels g' and g in upper section
    s.line(82.0, 356.0, 136.0, 356.0, stroke_width=5.5, dash="10,7")
    s.line(77.0, 618.5, 138.0, 618.5, stroke_width=5.5, dash="10,7")

    # --- Lower broken section (left narrow limb + U-bend c + right wider limb to tip f) ---
    # Left outer wall: jagged top break -> straight down to U-bend outer start (82, 3480)
    left_outer_and_break = [
        (82.0, 3480.0),
        (82.0, 2810.0),
        (80.0, 2250.0),
        (82.0, 1858.0),
        # Jagged top break
        (95.0, 1834.0),
        (102.0, 1852.0),
        (112.0, 1782.0),
        (124.0, 1800.0),
        (139.0, 1758.0),
        (145.0, 1785.0),
        # Left inner wall going down
        (146.0, 2250.0),
        (148.0, 2810.0),
        (148.0, 3420.0),
    ]
    s.polyline(left_outer_and_break, stroke_width=sw)

    # Inner U-bend + constriction neck + inner wall of right wider limb up to tip f
    inner_right = [
        (148.0, 3420.0),
        (136.0, 3468.0),
        (146.0, 3504.0),
        (174.0, 3516.0),
        (206.0, 3494.0),
        (225.0, 3440.0),
        (226.0, 3395.0),
        (210.0, 3330.0),
        (212.0, 3280.0),
        (227.0, 3100.0),
        (253.0, 2810.0),
        (269.0, 2630.0),
        (278.0, 2500.0),
        (308.0, 2250.0),
        (350.0, 2060.0),
        (376.0, 1930.0),
    ]
    lib.smooth_curve(s, inner_right, stroke_width=sw)

    # Outer U-bend + outer wall of right wider limb up to tip f
    outer_right = [
        (82.0, 3480.0),
        (96.0, 3538.0),
        (140.0, 3568.0),
        (195.0, 3566.0),
        (246.0, 3530.0),
        (276.0, 3465.0),
        (296.0, 3390.0),
        (312.0, 3280.0),
        (328.0, 3100.0),
        (354.0, 2810.0),
        (371.0, 2630.0),
        (383.0, 2500.0),
        (403.0, 2250.0),
        (392.0, 2080.0),
        (376.0, 1930.0),
    ]
    lib.smooth_curve(s, outer_right, stroke_width=sw)

    # Dashed level lines b', b, e', e, d
    s.line(82.0, 2590.0, 148.0, 2590.0, stroke_width=5.5, dash="10,7")
    s.line(82.0, 2758.0, 148.0, 2758.0, stroke_width=5.5, dash="10,7")
    s.line(271.0, 2594.0, 374.0, 2600.0, stroke_width=5.5, dash="12,7")
    s.line(256.0, 2762.0, 357.0, 2768.0, stroke_width=5.5, dash="12,7")
    s.line(212.0, 3280.0, 312.0, 3286.0, stroke_width=5.5, dash="12,7")

    # Labels
    lib.label(s, 117.0, 36.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 44.0, 348.0, "g′", size=58.0, italic=True, bold=True)
    lib.label(s, 44.0, 608.0, "g", size=58.0, italic=True, bold=True)
    lib.label(s, 346.0, 1945.0, "f", size=58.0, italic=True, bold=True)
    lib.label(s, 46.0, 2588.0, "b′", size=58.0, italic=True, bold=True)
    lib.label(s, 44.0, 2756.0, "b", size=58.0, italic=True, bold=True)
    lib.label(s, 412.0, 2588.0, "e′", size=58.0, italic=True, bold=True)
    lib.label(s, 392.0, 2762.0, "e", size=58.0, italic=True, bold=True)
    lib.label(s, 356.0, 3266.0, "d", size=58.0, italic=True, bold=True)
    lib.label(s, 265.0, 3538.0, "c", size=58.0, italic=True, bold=True)

    s.save(out_svg)
