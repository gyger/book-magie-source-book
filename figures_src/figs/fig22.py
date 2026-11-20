"""Figure 22: Poinsot's couple / parallel force translation on a rigid body."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _closed_smooth_path(s: draw.Scene, pts: list[tuple[float, float]], stroke_width: float = 7.0) -> None:
    """Closed Catmull-Rom cubic Bezier curve through pts."""
    n = len(pts)
    d_parts = [f"M {draw._fmt(pts[0][0])} {draw._fmt(pts[0][1])}"]
    for i in range(n):
        p0 = pts[(i - 1) % n]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n]
        c1x = p1[0] + (p2[0] - p0[0]) / 6.0
        c1y = p1[1] + (p2[1] - p0[1]) / 6.0
        c2x = p2[0] - (p3[0] - p1[0]) / 6.0
        c2y = p2[1] - (p3[1] - p1[1]) / 6.0
        d_parts.append(
            f"C {draw._fmt(c1x)} {draw._fmt(c1y)}, {draw._fmt(c2x)} {draw._fmt(c2y)}, {draw._fmt(p2[0])} {draw._fmt(p2[1])}"
        )
    d_parts.append("Z")
    s.path(" ".join(d_parts), stroke_width=stroke_width)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # Free-form rigid body outline (measured from scan)
    blob_pts = [
        (607.5, 460.0), (608.6, 493.1), (608.5, 527.0), (604.3, 561.2),
        (594.3, 594.5), (584.3, 629.2), (568.3, 662.0), (545.5, 690.5),
        (510.0, 725.0), (459.3, 759.6), (432.4, 795.6), (400.6, 834.9),
        (361.0, 867.9), (315.0, 876.5), (267.2, 883.8), (221.4, 870.0),
        (175.0, 855.0), (133.6, 836.6), (99.8, 802.5), (71.5, 765.3),
        (55.5, 719.5), (41.7, 677.9), (33.9, 636.6), (23.5, 600.4),
        (21.5, 562.7), (18.6, 527.6), (19.4, 493.3), (26.5, 460.0),
        (37.3, 428.7), (42.5, 397.8), (49.3, 367.0), (58.2, 336.3),
        (74.1, 308.6), (95.7, 285.1), (117.4, 262.4), (137.3, 237.2),
        (158.0, 200.0), (176.2, 171.7), (204.5, 144.3), (235.2, 110.5),
        (270.0, 60.5), (315.0, 24.5), (364.8, 18.3), (406.8, 57.8),
        (446.5, 84.3), (490.0, 105.0), (527.0, 122.6), (563.5, 148.4),
        (576.6, 198.4), (582.0, 247.1), (584.7, 290.5), (582.6, 331.1),
        (580.7, 367.0), (590.4, 397.1), (598.7, 428.0),
    ]
    _closed_smooth_path(s, blob_pts, stroke_width=6.5)

    # Vertical force P on left (starts at body boundary y=200, arrow down to y=1100)
    xL = 157.2
    lib.arrow(s, xL, 200.0, xL, 1102.0, stroke_width=9.5, head_len=36.0, head_w=20.0)

    # Vertical double-arrow -P' / P' on right (from y=16 to y=972)
    xR = 507.9
    lib.arrow(s, xR, 16.0, xR, 974.0, stroke_width=9.5, head_len=36.0, head_w=20.0, double=True)

    # Horizontal segment IA and diagonal BA
    yI = 492.2
    yB = 676.8
    s.line(xL, yI, xR, yI, stroke_width=8.5)
    s.line(xL, yB, xR, yI, stroke_width=8.5)

    # Labels
    lib.label(s, 558, 62, "-P'", size=56, italic=False, bold=True)
    lib.label(s, 132, 484, "I", size=54, italic=False, bold=True)
    lib.label(s, 470, 460, "A", size=54, italic=False, bold=True)
    lib.label(s, 126, 668, "B", size=54, italic=False, bold=True)
    lib.label(s, 550, 942, "P'", size=56, italic=False, bold=True)
    lib.label(s, 196, 1066, "P", size=56, italic=False, bold=True)

    s.save(out_svg)
