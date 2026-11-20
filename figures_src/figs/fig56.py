"""Figure 56: Bartholinus's double refraction through Iceland spar rhomboid PQRS-NOLM."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _hatched_bar(
    s: draw.Scene,
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    n_hatch: int = 12,
    sw: float = 4.5,
) -> None:
    s.polygon([p0, p1, p2, p3], stroke_width=sw)
    for i in range(1, n_hatch):
        t = i / n_hatch
        x0 = p0[0] + (p1[0] - p0[0]) * t
        y0 = p0[1] + (p1[1] - p0[1]) * t
        x1 = p3[0] + (p2[0] - p3[0]) * t
        y1 = p3[1] + (p2[1] - p3[1]) * t
        s.line(x0, y0, x1, y1, stroke_width=3.0)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 5.5

    # Top face P-S-R-Q
    p_pt = (72.0, 96.0)
    s_pt = (743.0, 102.0)
    r_pt = (931.0, 251.0)
    q_pt = (269.0, 250.0)

    # Bottom face N-M-L-O
    n_pt = (264.0, 491.0)
    m_pt = (907.0, 493.0)
    l_pt = (1095.0, 637.0)
    o_pt = (444.0, 636.0)

    s.polygon([p_pt, s_pt, r_pt, q_pt], stroke_width=sw)
    s.polygon([n_pt, m_pt, l_pt, o_pt], stroke_width=sw)
    s.line(*p_pt, *n_pt, stroke_width=sw)
    s.line(*s_pt, *m_pt, stroke_width=sw)
    s.line(*r_pt, *l_pt, stroke_width=sw)
    s.line(*q_pt, *o_pt, stroke_width=sw)

    # Object B (bottom face, hatched vertical bar)
    _hatched_bar(s, (552.0, 509.0), (546.0, 612.0), (571.0, 613.0), (576.0, 510.0), n_hatch=11, sw=4.5)
    # Object A (bottom face, hatched tilted bar)
    _hatched_bar(s, (775.0, 566.0), (944.0, 597.0), (951.0, 623.0), (781.0, 592.0), n_hatch=14, sw=4.5)

    # Double images H and G on top face (open vertical bars)
    s.polygon([(375.0, 118.0), (410.0, 128.0), (400.0, 218.0), (366.0, 209.0)], stroke_width=4.5)
    s.polygon([(446.0, 127.0), (474.0, 136.0), (467.0, 232.0), (438.0, 223.0)], stroke_width=4.5)

    # Double image E-C-F-D on top face (long bar with hatched middle section C-F)
    s.polygon([(540.0, 170.0), (778.0, 202.0), (775.0, 228.0), (538.0, 198.0)], stroke_width=4.5)
    _hatched_bar(s, (614.0, 180.0), (710.0, 193.0), (707.0, 219.0), (611.0, 207.0), n_hatch=9, sw=4.0)

    # Labels
    lib.label(s, 72.0, 58.0, "P", size=46.0, italic=False, bold=True)
    lib.label(s, 390.0, 58.0, "H", size=46.0, italic=False, bold=True)
    lib.label(s, 464.0, 58.0, "G", size=46.0, italic=False, bold=True)
    lib.label(s, 738.0, 60.0, "S", size=46.0, italic=False, bold=True)
    lib.label(s, 272.0, 215.0, "Q", size=46.0, italic=False, bold=True)
    lib.label(s, 540.0, 138.0, "E", size=44.0, italic=False, bold=True)
    lib.label(s, 608.0, 148.0, "C", size=44.0, italic=False, bold=True)
    lib.label(s, 700.0, 160.0, "F", size=44.0, italic=False, bold=True)
    lib.label(s, 760.0, 168.0, "D", size=44.0, italic=False, bold=True)
    lib.label(s, 964.0, 248.0, "R", size=46.0, italic=False, bold=True)
    lib.label(s, 272.0, 448.0, "N", size=46.0, italic=False, bold=True)
    lib.label(s, 862.0, 456.0, "M", size=46.0, italic=False, bold=True)
    lib.label(s, 464.0, 600.0, "O", size=46.0, italic=False, bold=True)
    lib.label(s, 598.0, 560.0, "B", size=46.0, italic=False, bold=True)
    lib.label(s, 768.0, 535.0, "A", size=46.0, italic=False, bold=True)
    lib.label(s, 1126.0, 634.0, "L", size=46.0, italic=False, bold=True)

    s.save(out_svg)
