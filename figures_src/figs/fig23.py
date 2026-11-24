"""Figure 23: Poinsot's couple (S, -S) acting on a rigid body with resultant force AR and axis AD."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    ox, oy = 28.0, 16.0

    # Closed free-form rigid body outline
    raw_pts = [
        (1178.0, 122.0), (1151.5, 98.5), (1075.3, 65.6), (1011.5, 33.5),
        (926.7, 32.8), (853.9, 35.5), (797.5, 28.6), (741.8, 31.6),
        (690.4, 38.7), (643.7, 46.3), (600.5, 54.6), (560.0, 69.5),
        (522.4, 82.5), (486.5, 94.2), (452.3, 108.6), (419.1, 123.5),
        (386.5, 139.5), (355.5, 158.5), (326.5, 180.6), (294.7, 201.1),
        (260.3, 222.2), (232.2, 250.8), (201.9, 280.6), (173.4, 314.4),
        (128.6, 348.3), (75.2, 389.0), (39.5, 440.0), (15.5, 497.2),
        (4.0, 558.7), (4.0, 621.5), (8.2, 685.7), (20.5, 751.5),
        (58.0, 804.7), (120.4, 835.8), (196.1, 844.1), (270.5, 838.4),
        (335.0, 829.7), (388.8, 824.6), (437.3, 817.6), (481.1, 811.2),
        (521.5, 806.5), (560.0, 798.5), (596.4, 786.6), (630.9, 773.5),
        (664.1, 760.5), (699.5, 753.3), (733.0, 739.6), (760.4, 715.9),
        (792.5, 698.2), (826.4, 679.9), (857.3, 656.0), (891.7, 631.5),
        (925.7, 602.8), (961.3, 570.4), (1012.0, 515.0), (1068.5, 440.0),
        (1104.5, 382.8), (1143.9, 315.9), (1178.0, 260.0),
        (1203.0, 214.0), (1213.0, 174.0), (1200.0, 144.0),
    ]
    blob_pts = [(x + ox, y + oy) for (x, y) in raw_pts]
    blob_pts.append(blob_pts[0])
    lib.smooth_curve(s, blob_pts, stroke_width=7.5)

    # L-shaped axes at A-D and resultant force arrow A -> R
    A = (258.3 + ox, 615.1 + oy)
    D = (624.0 + ox, 615.1 + oy)
    lib.arrow(s, A[0], A[1], A[0], 1062.0, stroke_width=10.0, head_len=38.0, head_w=22.0)
    s.line(A[0], A[1], D[0], D[1], stroke_width=10.0)

    # Couple arm B-C and anti-parallel forces B -> -S and C -> S
    B = (728.6 + ox, 431.3 + oy)
    C = (925.0 + ox, 310.7 + oy)
    dx, dy = -186.6, -278.6
    s.line(*B, *C, stroke_width=10.0)
    lib.arrow(s, B[0], B[1], B[0] + dx, B[1] + dy, stroke_width=10.0, head_len=38.0, head_w=22.0)
    lib.arrow(s, C[0], C[1], C[0] - dx, C[1] - dy, stroke_width=10.0, head_len=38.0, head_w=22.0)

    # Labels
    lib.label(s, 502 + ox, 162 + oy, "-S", size=54, italic=True, bold=True)
    lib.label(s, 932 + ox, 270 + oy, "C", size=52, italic=False, bold=True)
    lib.label(s, 725 + ox, 466 + oy, "B", size=52, italic=False, bold=True)
    lib.label(s, 1120 + ox, 588 + oy, "S", size=54, italic=True, bold=True)
    lib.label(s, 226 + ox, 576 + oy, "A", size=52, italic=False, bold=True)
    lib.label(s, 602 + ox, 644 + oy, "D", size=52, italic=False, bold=True)
    lib.label(s, 244, 1036, "R", size=52, italic=False, bold=True)

    s.save(out_svg)
