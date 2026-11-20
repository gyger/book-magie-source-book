"""Figure 43: Carnot cycle P-V indicator diagram (Clapeyron / Clausius)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw_axis = 9.0
    sw_line = 7.5

    # Coordinate axes intersecting at o = (101, 850)
    ox, oy = 101.0, 850.0
    s.line(ox, 36.0, ox, 933.0, stroke_width=sw_axis)
    s.line(6.0, oy, w - 4.0, oy, stroke_width=sw_axis)

    # Key vertices on the Carnot cycle
    pa = (511.0, 174.0)
    pb = (920.0, 344.0)
    pc = (1124.0, 687.0)
    pd = (680.0, 535.0)

    # Vertical projection lines down to x-axis (e, h, f, g)
    s.line(pa[0], pa[1], pa[0], oy, stroke_width=sw_line)
    s.line(pd[0], pd[1], pd[0], oy, stroke_width=sw_line)
    s.line(pb[0], pb[1], pb[0], oy, stroke_width=sw_line)
    s.line(pc[0], pc[1], pc[0], oy, stroke_width=sw_line)

    # Upper isotherm a -> b (gentle downward-convex curve)
    pts_ab = [
        pa,
        (600.0, 217.5),
        (680.0, 253.5),
        (760.0, 287.5),
        (840.0, 317.5),
        pb,
    ]
    lib.smooth_curve(s, pts_ab, stroke_width=sw_line)

    # Right adiabatic b -> c
    pts_bc = [
        pb,
        (960.0, 437.5),
        (1000.0, 515.5),
        (1040.0, 579.5),
        (1080.0, 635.5),
        pc,
    ]
    lib.smooth_curve(s, pts_bc, stroke_width=sw_line)

    # Left adiabatic a -> d and lower isotherm d -> c
    pts_ad = [
        pa,
        (525.0, 235.5),
        (540.0, 289.5),
        (560.0, 346.5),
        (580.0, 394.5),
        (600.0, 432.5),
        (620.0, 467.5),
        (650.0, 508.5),
        pd,
    ]
    lib.smooth_curve(s, pts_ad, stroke_width=sw_line)

    pts_dc = [
        pd,
        (720.0, 570.5),
        (760.0, 595.5),
        (800.0, 616.5),
        (840.0, 634.5),
        (880.0, 647.5),
        (920.0, 658.5),
        (960.0, 670.5),
        (1000.0, 677.5),
        (1040.0, 681.5),
        (1080.0, 684.5),
        pc,
    ]
    lib.smooth_curve(s, pts_dc, stroke_width=sw_line)

    # Labels (italic bold matching original scan)
    lib.label(s, 61.0, 886.0, "o", size=58.0, italic=True, bold=True)
    lib.label(s, 506.0, 882.0, "e", size=58.0, italic=True, bold=True)
    lib.label(s, 678.0, 882.0, "h", size=58.0, italic=True, bold=True)
    lib.label(s, 912.0, 878.0, "f", size=58.0, italic=True, bold=True)
    lib.label(s, 1126.0, 891.0, "g", size=58.0, italic=True, bold=True)
    lib.label(s, 513.0, 143.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 926.0, 302.0, "b", size=58.0, italic=True, bold=True)
    lib.label(s, 1160.0, 688.0, "c", size=58.0, italic=True, bold=True)
    lib.label(s, 642.0, 577.0, "d", size=58.0, italic=True, bold=True)

    s.save(out_svg)
