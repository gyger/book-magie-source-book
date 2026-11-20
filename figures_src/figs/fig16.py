"""Figure 16: Parallelogram ABCD with dashed curve AE D."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    A = (92.2, 212.5)
    B = (652.0, 23.0)
    C = (97.4, 864.9)
    D = (644.5, 700.3)

    sw = 9.5
    s.polygon([A, B, D, C], stroke_width=sw)

    curve_pts = [
        A,
        (145.0, 198.5),
        (195.0, 195.0),
        (245.0, 199.5),
        (295.0, 210.5),
        (345.0, 230.0),
        (395.0, 263.0),
        (445.0, 306.0),
        (495.0, 359.0),
        (545.0, 428.0),
        (595.0, 528.0),
        (629.0, 615.0),
        D,
    ]
    lib.smooth_curve(s, curve_pts, stroke_width=8.5, dash="30,18")

    lib.label(s, 60, 218, "A", size=56, italic=False, bold=True)
    lib.label(s, 675, 48, "B", size=56, italic=False, bold=True)
    lib.label(s, 62, 864, "C", size=56, italic=False, bold=True)
    lib.label(s, 672, 688, "D", size=56, italic=False, bold=True)
    lib.label(s, 474, 286, "E", size=56, italic=False, bold=True)

    s.save(out_svg)
