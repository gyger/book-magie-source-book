"""Figure 108: J.J. Thomson's electrostatic deflection cathode-ray tube."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.0
    # Upper glass envelope: left nose -> upper side-arm (+) -> neck -> main tube -> upper plate side-arm -> spherical bulb
    d_top = (
        "M 0 330 Q 48 290, 96 248 Q 140 218, 190 198 "
        "L 190 100 Q 190 76, 218 76 Q 248 76, 256 122 "
        "L 266 196 Q 320 226, 400 298 "
        "L 764 296 Q 820 220, 916 202 "
        "L 1300 202 Q 1344 198, 1348 150 "
        "L 1348 64 Q 1348 36, 1380 36 Q 1412 36, 1412 64 "
        "L 1412 150 Q 1416 198, 1460 202 "
        "L 1978 202 Q 2070 84, 2212 78 "
        "C 2310 78, 2380 116, 2420 166"
    )
    s.path(d_top, stroke_width=sw)

    # Lower glass envelope
    d_bot = (
        "M 0 392 Q 52 444, 118 486 Q 178 514, 252 508 "
        "Q 332 496, 386 420 Q 402 412, 424 412 "
        "L 764 412 Q 824 486, 916 498 "
        "L 1300 498 Q 1344 504, 1348 548 "
        "L 1348 640 Q 1348 672, 1380 672 Q 1412 672, 1412 640 "
        "L 1412 548 Q 1416 504, 1460 498 "
        "L 1978 498 Q 2070 618, 2212 630 "
        "Q 2338 634, 2420 554"
    )
    s.path(d_bot, stroke_width=sw)

    # Cathode C (horizontal lead + vertical elliptical disk)
    s.line(0.0, 355.0, 216.0, 355.0, stroke_width=sw)
    s.ellipse(226.0, 355.0, 9.0, 42.0, fill="#ffffff", stroke_width=sw)

    # Anode lead wire from top side-arm (+) down to plug A
    s.path("M 212 46 L 216 156 Q 222 214, 274 246 L 398 302", stroke_width=sw)

    # Collimating metal plug A with slit
    s.path("M 434 296 A 20 58 0 0 0 434 412 L 502 412 A 20 58 0 0 0 502 296 Z", fill="#ffffff", stroke_width=sw)
    s.ellipse(502.0, 354.0, 20.0, 58.0, fill="#ffffff", stroke_width=sw)
    s.polygon([(488.0, 356.0), (512.0, 336.0), (518.0, 354.0), (492.0, 374.0)], fill="#ffffff", stroke_width=sw * 0.8)

    # Collimating metal plug B with slit
    s.path("M 692 296 A 20 58 0 0 0 692 412 L 750 412 A 20 58 0 0 0 750 296 Z", fill="#ffffff", stroke_width=sw)
    s.ellipse(750.0, 354.0, 20.0, 58.0, fill="#ffffff", stroke_width=sw)
    s.polygon([(736.0, 356.0), (762.0, 336.0), (768.0, 354.0), (740.0, 374.0)], fill="#ffffff", stroke_width=sw * 0.8)

    # Electrostatic deflection plates D (top) and E (bottom)
    s.polygon([(1150.0, 276.0), (1522.0, 276.0), (1600.0, 224.0), (1248.0, 224.0)], fill="#ffffff", stroke_width=sw)
    s.line(1380.0, 20.0, 1380.0, 248.0, stroke_width=sw)

    s.polygon([(1150.0, 444.0), (1522.0, 444.0), (1596.0, 398.0), (1248.0, 398.0)], fill="#ffffff", stroke_width=sw)
    s.line(1380.0, 444.0, 1380.0, 674.0, stroke_width=sw)

    # Graduated phosphorescent scale strip on far right bulb wall (upper end with ticks + lower end)
    s.polyline([(2392.0, 140.0), (2368.0, 162.0), (2420.0, 214.0)], stroke_width=sw * 0.85)
    s.line(2401.0, 149.0, 2391.0, 158.0, stroke_width=sw * 0.7)
    s.line(2409.0, 157.0, 2399.0, 166.0, stroke_width=sw * 0.7)
    s.line(2417.0, 166.0, 2404.0, 178.0, stroke_width=sw * 0.7)
    s.polyline([(2420.0, 502.0), (2402.0, 526.0), (2420.0, 526.0)], stroke_width=sw * 0.85)

    # Labels
    lib.label(s, 254.0, 40.0, "+", size=66.0, italic=False, bold=True)
    lib.label(s, 226.0, 294.0, "c", size=58.0, italic=True, bold=True)
    lib.label(s, 456.0, 260.0, "A", size=64.0, italic=False, bold=True)
    lib.label(s, 716.0, 260.0, "B", size=64.0, italic=False, bold=True)
    lib.label(s, 1154.0, 242.0, "D", size=64.0, italic=False, bold=True)
    lib.label(s, 1152.0, 412.0, "E", size=64.0, italic=False, bold=True)

    s.save(out_svg)
