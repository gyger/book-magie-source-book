"""Figure 91, 1: Faraday's soft-iron ring with primary (A) and secondary (B) coils."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    # Exposed bare iron ring segments at top and bottom
    s.path("M 378 79 Q 402 76, 424 79", stroke_width=sw)
    s.path("M 384 109 Q 402 106, 420 109", stroke_width=sw)
    s.path("M 376 347 Q 398 350, 418 347", stroke_width=sw)
    s.path("M 366 376 Q 398 380, 424 376", stroke_width=sw)

    # Left coil B (crescent-shaped winding around left half of ring)
    d_coil_b = (
        "M 378 76 "
        "C 312 68, 232 132, 232 226 "
        "C 232 318, 304 382, 368 380 "
        "C 380 374, 384 356, 378 344 "
        "C 334 328, 302 282, 302 226 "
        "C 302 168, 336 126, 382 110 "
        "C 386 98, 386 82, 378 76 Z"
    )
    s.path(d_coil_b, fill="#ffffff", stroke_width=sw)

    # Right coil A (crescent-shaped winding around right half of ring)
    d_coil_a = (
        "M 424 72 "
        "C 502 68, 586 132, 586 228 "
        "C 586 322, 506 388, 426 382 "
        "C 416 374, 414 356, 420 342 "
        "C 480 326, 520 282, 520 228 "
        "C 520 168, 482 126, 422 108 "
        "C 418 96, 418 80, 424 72 Z"
    )
    s.path(d_coil_a, fill="#ffffff", stroke_width=sw)

    # Four connecting lead wires
    s.path("M 372 72 Q 320 42, 250 50 L 12 96", stroke_width=sw)
    s.path("M 362 380 Q 332 414, 240 408 L 28 380", stroke_width=sw)
    s.path("M 438 72 Q 444 26, 524 20 L 684 36", stroke_width=sw)
    s.path("M 432 384 Q 456 446, 524 446 L 684 424", stroke_width=sw)

    # Labels
    lib.label(s, 186.0, 232.0, "B", size=72.0, italic=False, bold=True)
    lib.label(s, 628.0, 236.0, "A", size=72.0, italic=False, bold=True)

    s.save(out_svg)
