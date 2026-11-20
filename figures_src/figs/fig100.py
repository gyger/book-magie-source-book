"""Figure 100: Crookes magnetic deflection tube (Plan) and schematic diagram A."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    # === Left: Plan view of tube ===
    d_plan = (
        "M 110 318 L 194 314 C 310 214, 520 76, 756 76 "
        "C 990 76, 1180 206, 1296 312 "
        "L 1378 320 C 1424 326, 1424 402, 1378 408 "
        "L 1296 416 C 1180 524, 990 644, 756 644 "
        "C 520 644, 310 510, 194 410 "
        "L 110 404 C 66 398, 66 324, 110 318 Z"
    )
    s.path(d_plan, stroke_width=sw)

    # Magnet pole rectangle S (dashed inside tube, hatched outside left)
    s.rect(36.0, 300.0, 440.0, 128.0, fill="none", stroke_width=sw * 0.8, dash="20,12")
    for x in range(42, 194, 12):
        s.line(x, 300.0, x, 326.0, stroke_width=3.5)
        s.line(x, 398.0, x, 428.0, stroke_width=3.5)

    # Left electrode a (+), right electrode b (-)
    s.line(184.0, 322.0, 184.0, 396.0, stroke_width=sw)
    s.rect(86.0, 346.0, 88.0, 26.0, fill="#ffffff", stroke_width=4.5, rx=8.0)
    s.line(1292.0, 330.0, 1292.0, 404.0, stroke_width=sw)
    s.rect(1312.0, 354.0, 88.0, 26.0, fill="#ffffff", stroke_width=4.5, rx=8.0)

    # Horizontal axis a-g-e
    s.line(184.0, 366.0, 858.0, 366.0, stroke_width=sw * 0.85, dash="36,12,8,12")

    # Screen e
    s.line(858.0, 282.0, 858.0, 370.0, stroke_width=sw * 1.1)

    # Hatched shadow band from screen e to wall f-l
    poly_shadow = [(858.0, 282.0), (858.0, 370.0), (296.0, 224.0), (364.0, 180.0)]
    s.add_def(
        '<clipPath id="clip_sh100">'
        '<polygon points="858,282 858,370 296,224 364,180"/>'
        '</clipPath>'
    )
    hatch = []
    for x in range(280, 960, 22):
        hatch.append(f'<line x1="{x}" y1="160" x2="{x - 130}" y2="390" stroke="#000000" stroke-width="4"/>')
    s.raw('<g clip-path="url(#clip_sh100)">' + "".join(hatch) + "</g>")
    s.polygon(poly_shadow, fill="none", stroke_width=sw * 0.85)

    # Deflected shadow curves m and o
    s.path("M 858 282 Q 620 242, 456 144", stroke_width=sw * 0.8, dash="18,12")
    s.path("M 858 282 Q 670 228, 528 116", stroke_width=sw * 0.8, dash="18,12")

    # Circled markers k, q, h, i, J
    for cx, cy, txt in [
        (680.0, 220.0, "k"), (588.0, 284.0, "q"),
        (660.0, 300.0, "h"), (708.0, 386.0, "i"), (598.0, 412.0, "J"),
    ]:
        s.circle(cx, cy, 30.0, fill="#ffffff", stroke_width=5.0)
        lib.label(s, cx, cy, txt, size=48.0, italic=True, bold=True)

    # Small side ring c
    s.ellipse(1214.0, 336.0, 16.0, 10.0, fill="#ffffff", stroke_width=4.5)

    # === Right: Diagram A ===
    # Bulb wall arc
    s.path("M 1508 668 C 1490 618, 1502 578, 1554 570 C 1640 554, 1730 480, 1810 434 C 1900 386, 1990 374, 2070 368", stroke_width=sw)
    # Axis g-e
    s.line(1594.0, 626.0, 2264.0, 626.0, stroke_width=sw * 0.85, dash="36,12,8,12")
    s.line(1598.0, 598.0, 1598.0, 646.0, stroke_width=sw)
    s.rect(1504.0, 614.0, 74.0, 22.0, fill="#ffffff", stroke_width=4.5, rx=8.0)
    # Vertical screen e
    s.line(2264.0, 544.0, 2264.0, 626.0, stroke_width=sw * 1.1)
    # Fan of dashed deflection curves from top of e to o, 1, 2, 3, 4, 5
    s.line(2264.0, 544.0, 1768.0, 464.0, stroke_width=sw * 0.8, dash="28,12")
    for tx, ty in [(1850, 416), (1894, 400), (1936, 390), (1976, 380)]:
        s.path(f"M 2264 544 Q {(2264 + tx) * 0.5 - 40:.1f} {(544 + ty) * 0.5 + 30:.1f}, {tx} {ty}", stroke_width=sw * 0.75, dash="16,10")
    # Lower curved ray to p
    s.path("M 2036 626 Q 1860 600, 1698 514", stroke_width=sw * 0.8, dash="22,12")

    # Labels
    lib.label(s, 18.0, 360.0, "+", size=54.0, italic=False, bold=True)
    lib.label(s, 210.0, 386.0, "a", size=54.0, italic=True, bold=True)
    lib.label(s, 336.0, 386.0, "g", size=54.0, italic=True, bold=True)
    lib.label(s, 448.0, 398.0, "S", size=54.0, italic=True, bold=True)
    lib.label(s, 286.0, 214.0, "l", size=52.0, italic=True, bold=True)
    lib.label(s, 356.0, 168.0, "f", size=52.0, italic=True, bold=True)
    lib.label(s, 428.0, 128.0, "m", size=52.0, italic=True, bold=True)
    lib.label(s, 460.0, 92.0, "n", size=52.0, italic=True, bold=True)
    lib.label(s, 536.0, 92.0, "o", size=52.0, italic=True, bold=True)
    lib.label(s, 882.0, 330.0, "e", size=54.0, italic=True, bold=True)
    lib.label(s, 1152.0, 300.0, "c", size=54.0, italic=True, bold=True)
    lib.label(s, 1264.0, 376.0, "b", size=54.0, italic=True, bold=True)
    lib.label(s, 1464.0, 374.0, "−", size=54.0, italic=False, bold=True)
    lib.label(s, 760.0, 686.0, "Plan", size=58.0, italic=True, bold=True)

    lib.label(s, 1866.0, 314.0, "A", size=60.0, italic=False, bold=True)
    lib.label(s, 1468.0, 628.0, "g", size=54.0, italic=True, bold=True)
    lib.label(s, 1696.0, 548.0, "p", size=52.0, italic=True, bold=True)
    lib.label(s, 1750.0, 444.0, "o", size=52.0, italic=True, bold=True)
    lib.label(s, 1854.0, 510.0, "f", size=52.0, italic=True, bold=True)
    lib.label(s, 1844.0, 394.0, "1", size=44.0, italic=True, bold=True)
    lib.label(s, 1878.0, 382.0, "2", size=44.0, italic=True, bold=True)
    lib.label(s, 1916.0, 374.0, "3", size=44.0, italic=True, bold=True)
    lib.label(s, 1952.0, 366.0, "4", size=44.0, italic=True, bold=True)
    lib.label(s, 1984.0, 360.0, "5", size=44.0, italic=True, bold=True)
    lib.label(s, 2292.0, 588.0, "e", size=54.0, italic=True, bold=True)

    s.save(out_svg)
