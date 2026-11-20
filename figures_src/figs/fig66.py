"""Figure 66: Thomas Young's interference pattern of two coherent circular wave trains from A and B."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # Rectangular wave tank frame
    x0, y0 = 106.0, 40.0
    x1, y1 = 2289.0, 1044.0
    fw, fh = x1 - x0, y1 - y0

    s.add_def(
        f'<clipPath id="tank"><rect x="{x0:.1f}" y="{y0:.1f}" width="{fw:.1f}" height="{fh:.1f}"/></clipPath>'
    )

    # Two point sources A and B on left edge
    ax, ay = x0, 268.0
    bx, by = x0, 778.0

    # Wavelength spacing ~ 53.5 px (thick concentric circular crests)
    lam = 53.5
    r_max = 2400.0
    ring_sw = 14.5

    s.raw('<g clip-path="url(#tank)">')
    r = lam
    while r <= r_max:
        s.circle(ax, ay, r, fill="none", stroke="#000000", stroke_width=ring_sw)
        s.circle(bx, by, r, fill="none", stroke="#000000", stroke_width=ring_sw)
        r += lam
    s.raw("</g>")

    # Frame border
    s.rect(x0, y0, fw, fh, stroke_width=6.0)

    # Labels A, B (left) and C, D, E, F (right, marking destructive interference nodes)
    lib.label(s, 54.0, ay, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 54.0, by, "B", size=54.0, italic=False, bold=True)
    lib.label(s, 2340.0, 168.0, "C", size=54.0, italic=False, bold=True)
    lib.label(s, 2340.0, 392.0, "D", size=54.0, italic=False, bold=True)
    lib.label(s, 2340.0, 694.0, "E", size=54.0, italic=False, bold=True)
    lib.label(s, 2340.0, 916.0, "F", size=54.0, italic=False, bold=True)

    s.save(out_svg)
