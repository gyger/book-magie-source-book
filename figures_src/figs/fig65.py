"""Figure 65: Grimaldi's second diffraction experiment with two successive apertures CD and GH."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    sw_thin = 5.5

    # Upper opaque plate A-C and D-B (y = 220..244)
    y_u0, y_u1 = 220.0, 244.0
    s.rect(322.0, y_u0, 174.0, y_u1 - y_u0, stroke_width=sw_thin)
    s.rect(579.0, y_u0, 160.0, y_u1 - y_u0, stroke_width=sw_thin)

    # Lower opaque plate E-G and H-F (y = 584..608)
    y_l0, y_l1 = 584.0, 608.0
    s.rect(348.0, y_l0, 120.0, y_l1 - y_l0, stroke_width=sw_thin)
    s.rect(598.0, y_l0, 110.0, y_l1 - y_l0, stroke_width=sw_thin)

    # Screen horizontal base at y = 1218
    y_base = 1218.0
    s.line(62.0, y_base, 974.0, y_base, stroke_width=sw)

    # Direct rays through aperture CD and GH
    s.line(520.0, 34.0, 424.0, y_base, stroke_width=sw_thin)   # -> L
    s.line(638.0, 34.0, 316.0, y_base, stroke_width=sw_thin)   # -> N
    s.line(458.0, 34.0, 742.0, y_base, stroke_width=sw_thin)   # -> O
    s.line(564.0, 34.0, 656.0, y_base, stroke_width=sw_thin)   # -> M

    # Diffracted dashed rays: from G to I, and from H to K
    s.line(476.0, 596.0, 178.0, y_base, stroke_width=sw_thin, dash="22,18")
    s.line(604.0, 596.0, 896.0, y_base, stroke_width=sw_thin, dash="22,18")

    # Labels
    lib.label(s, 282.0, 234.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 780.0, 234.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 456.0, 294.0, "C", size=54.0, italic=False, bold=True)
    lib.label(s, 622.0, 294.0, "D", size=54.0, italic=False, bold=True)
    lib.label(s, 424.0, 544.0, "G", size=54.0, italic=False, bold=True)
    lib.label(s, 636.0, 544.0, "H", size=54.0, italic=False, bold=True)
    lib.label(s, 314.0, 600.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, 744.0, 600.0, "F", size=58.0, italic=False, bold=True)

    lib.label(s, 146.0, 1172.0, "I", size=54.0, italic=False, bold=True)
    lib.label(s, 268.0, 1172.0, "N", size=54.0, italic=False, bold=True)
    lib.label(s, 452.0, 1172.0, "L", size=54.0, italic=False, bold=True)
    lib.label(s, 584.0, 1172.0, "M", size=54.0, italic=False, bold=True)
    lib.label(s, 764.0, 1172.0, "O", size=54.0, italic=False, bold=True)
    lib.label(s, 916.0, 1172.0, "K", size=54.0, italic=False, bold=True)

    s.save(out_svg)
