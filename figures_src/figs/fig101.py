"""Figure 101: Crookes magnetic deflection tube with mica millimeter scales e and d."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # Pear-shaped horizontal glass bulb with upper-left exhaust hook
    d_bulb = (
        "M 654 226 C 850 202, 1020 140, 1220 60 "
        "C 1460 -10, 1740 40, 1940 210 "
        "C 2020 284, 2070 364, 2116 404 "
        "L 2200 416 C 2236 424, 2236 476, 2200 484 "
        "L 2116 498 C 2060 546, 2000 660, 1910 742 "
        "C 1720 874, 1500 894, 1280 822 "
        "C 1080 762, 860 704, 560 652 "
        "C 420 622, 340 540, 340 440 "
        "C 340 314, 412 246, 514 238 "
        "C 554 234, 540 164, 490 156 "
        "L 304 166 Q 236 164, 232 142 Q 254 114, 304 108 "
        "L 540 94 C 600 92, 622 184, 654 226 Z"
    )
    s.path(d_bulb, stroke_width=sw)

    # Left cathode a (-), glass pinch, curved lead wire to c, and horizontal scale e
    s.path("M 412 462 L 420 536 C 424 568, 456 576, 514 584 C 584 592, 650 592, 710 588", stroke_width=sw)
    s.line(480.0, 408.0, 480.0, 502.0, stroke_width=10.0)
    s.line(316.0, 448.0, 466.0, 448.0, stroke_width=sw)
    s.polygon([(334.0, 434.0), (434.0, 440.0), (434.0, 458.0), (334.0, 466.0)], fill="#ffffff", stroke_width=5.5)
    s.rect(484.0, 502.0, 236.0, 46.0, fill="#ffffff", stroke_width=5.5)
    for x in range(494, 718, 12):
        tick_h = 15.0 if (x - 494) % 60 == 0 else 9.0
        s.line(x, 502.0, x, 502.0 + tick_h, stroke_width=3.2)
    for num, x in [("0", 496.0), ("5", 554.0), ("10", 614.0), ("15", 674.0)]:
        lib.label(s, x, 532.0, num, size=27.0, italic=False, bold=True)

    # Vertical mica screen c (oval) and tapered phosphorescent screen f-f to scale d
    s.ellipse(712.0, 456.0, 24.0, 134.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.line(712.0, 322.0, 1736.0, 194.0, stroke_width=sw)
    s.line(712.0, 590.0, 1724.0, 706.0, stroke_width=sw)

    # Graduated vertical glass scale d (curved oval + vertical bar with tick marks)
    s.ellipse(1752.0, 450.0, 46.0, 246.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(1724.0, 204.0, 22.0, 492.0, fill="#ffffff", stroke_width=5.5)
    for y in range(220, 688, 12):
        s.line(1724.0, y, 1746.0, y, stroke_width=3.5)

    # Right inner curved guide to anode ring b (+)
    s.path("M 1768 206 C 1900 206, 1990 310, 2006 410", stroke_width=sw * 0.85)
    s.path("M 1768 694 C 1900 694, 1990 590, 2006 490", stroke_width=sw * 0.85)
    s.rect(2016.0, 412.0, 40.0, 76.0, fill="#ffffff", stroke_width=sw, rx=10.0)
    s.line(2056.0, 450.0, 2248.0, 450.0, stroke_width=sw)
    s.polygon([(2104.0, 434.0), (2216.0, 428.0), (2216.0, 470.0), (2104.0, 464.0)], fill="#ffffff", stroke_width=5.5)

    # Undeflected straight cathode-ray beam (horizontal ribbon)
    s.line(712.0, 436.0, 1724.0, 436.0, stroke_width=sw * 0.85)
    s.line(712.0, 460.0, 1724.0, 460.0, stroke_width=sw * 0.85)

    # Magnetically deflected curved beam curving down to bottom of scale d
    s.path("M 712 436 C 1060 404, 1410 428, 1724 614", stroke_width=sw * 0.85)
    s.path("M 712 460 C 1060 432, 1410 462, 1724 656", stroke_width=sw * 0.85)

    # Horseshoe magnet N-S at bottom-left
    d_mag = (
        "M 562 606 L 106 616 C 4 622, 4 748, 106 756 L 616 742 "
        "L 616 798 L 106 806 C 12 802, 12 732, 18 690 "
        "M 110 666 L 578 666 L 616 742 "
        "M 578 666 L 578 646 "
        "M 578 706 L 112 706 C 92 706, 92 666, 110 666"
    )
    s.path(d_mag, stroke_width=sw)

    # Labels
    lib.label(s, 272.0, 464.0, "−", size=60.0, italic=False, bold=True)
    lib.label(s, 480.0, 384.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 586.0, 474.0, "e", size=56.0, italic=True, bold=True)
    lib.label(s, 672.0, 326.0, "c", size=58.0, italic=True, bold=True)
    lib.label(s, 1254.0, 224.0, "f", size=58.0, italic=True, bold=True)
    lib.label(s, 1208.0, 684.0, "f", size=58.0, italic=True, bold=True)
    lib.label(s, 1800.0, 246.0, "d", size=58.0, italic=True, bold=True)
    lib.label(s, 2036.0, 388.0, "b", size=58.0, italic=True, bold=True)
    lib.label(s, 2286.0, 456.0, "+", size=60.0, italic=False, bold=True)
    lib.label(s, 580.0, 628.0, "N", size=58.0, italic=False, bold=True)
    lib.label(s, 574.0, 738.0, "S", size=58.0, italic=False, bold=True)

    # Scale numbers on d
    for num, y in [("35", 292), ("30", 348), ("25", 404), ("20", 456), ("15", 510), ("10", 564), ("5", 616)]:
        lib.label(s, 1786.0, float(y), num, size=46.0, italic=False, bold=True)

    s.save(out_svg)
