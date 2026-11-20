"""Figure 104: Goldstein's canal-ray discharge tubes (Fig. 1 and Fig. 2)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # === Fig. 1 (left tube) ===
    # Upper wide cylinder with semicircular top and flat-rounded bottom meeting neck
    d_up1 = (
        "M 36 818 L 36 200 "
        "A 88 88 0 0 1 212 200 "
        "L 212 818 "
        "Q 212 836, 192 836 L 56 836 Q 36 836, 36 818 Z"
    )
    s.path(d_up1, stroke_width=sw)

    # Lower tube connected via narrow neck
    d_lo1 = (
        "M 98 836 L 98 866 C 98 900, 34 912, 34 974 "
        "L 34 1288 A 89 88 0 0 0 212 1288 "
        "L 212 974 C 212 912, 152 900, 152 866 L 152 836"
    )
    s.path(d_lo1, stroke_width=sw)

    # Perforated cathode plate K inside bottom of upper tube
    s.ellipse(124.0, 810.0, 72.0, 26.0, fill="#ffffff", stroke_width=sw)

    # Cathode lead wire d from top terminal b down to K
    s.circle(122.0, 92.0, 21.0, fill="#ffffff", stroke_width=sw)
    s.path("M 122 113 C 122 250, 138 350, 134 520 C 132 610, 184 710, 174 784", stroke_width=sw)

    # Anode a at bottom of Fig. 1
    s.line(124.0, 1266.0, 124.0, 1378.0, stroke_width=sw)
    s.circle(124.0, 1400.0, 21.0, fill="#ffffff", stroke_width=sw)

    # === Fig. 2 (right tube) ===
    # Upper wide cylinder (rounded top and rounded bottom around neck r)
    d_up2 = (
        "M 536 798 C 492 780, 468 742, 468 690 "
        "L 468 106 A 106 104 0 0 1 680 106 "
        "L 680 690 C 680 742, 654 780, 608 798"
    )
    s.path(d_up2, stroke_width=sw)

    # Lower tube + inner glass tube r rising into upper chamber
    d_lo2 = (
        "M 536 664 L 536 866 C 536 908, 466 922, 466 986 "
        "L 466 1280 A 105 92 0 0 0 676 1280 "
        "L 676 986 C 676 922, 608 908, 608 866 L 608 664"
    )
    s.path(d_lo2, stroke_width=sw)

    # Cylindrical cathode cup K fitted over top of tube r
    s.path("M 522 606 L 522 664 Q 571 682, 620 664 L 620 606", fill="#ffffff", stroke_width=sw)
    s.ellipse(571.0, 606.0, 49.0, 20.0, fill="#ffffff", stroke_width=sw)

    # Side hook and lead wire d to terminal b-
    s.path("M 620 612 L 646 612 Q 658 612, 654 628 L 620 628", fill="#ffffff", stroke_width=sw * 0.85)
    s.path("M 648 628 Q 644 710, 654 766", stroke_width=sw)
    s.circle(662.0, 786.0, 21.0, fill="#ffffff", stroke_width=sw)

    # Anode a at bottom of Fig. 2
    s.line(568.0, 1266.0, 568.0, 1372.0, stroke_width=sw)
    s.circle(568.0, 1394.0, 21.0, fill="#ffffff", stroke_width=sw)

    # Labels
    lib.label(s, 122.0, 46.0, "b", size=64.0, italic=True, bold=True)
    lib.label(s, 102.0, 474.0, "d", size=64.0, italic=True, bold=True)
    lib.label(s, 120.0, 750.0, "K", size=62.0, italic=True, bold=True)
    lib.label(s, 14.0, 808.0, "x", size=58.0, italic=True, bold=True)
    lib.label(s, 74.0, 1406.0, "+", size=58.0, italic=False, bold=True)
    lib.label(s, 128.0, 1450.0, "a", size=64.0, italic=True, bold=True)
    lib.label(s, 116.0, 1516.0, "Fig. 1", size=54.0, italic=False, bold=True)

    lib.label(s, 566.0, 560.0, "K", size=62.0, italic=True, bold=True)
    lib.label(s, 510.0, 718.0, "r", size=64.0, italic=True, bold=True)
    lib.label(s, 678.0, 706.0, "d", size=64.0, italic=True, bold=True)
    lib.label(s, 668.0, 844.0, "b⁻", size=64.0, italic=True, bold=True)
    lib.label(s, 614.0, 1406.0, "+", size=58.0, italic=False, bold=True)
    lib.label(s, 568.0, 1444.0, "a", size=64.0, italic=True, bold=True)
    lib.label(s, 554.0, 1516.0, "Fig. 2", size=54.0, italic=False, bold=True)

    s.save(out_svg)
