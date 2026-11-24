"""Figure 102: Crookes concave-cathode focus tubes A (straight) and B (magnetically deflected)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _tube(s: draw.Scene, cx: float, top_y: float, bot_y: float, sw: float) -> None:
    """Draw one vertical Crookes focus tube with exhaust hook and concave cathode a."""
    hw = 124.0
    d_outer = (
        f"M {cx - hw} {bot_y - 365} L {cx - hw} {top_y + 112} "
        f"A {hw} 112 0 0 1 {cx + hw} {top_y + 112} "
        f"L {cx + hw} {bot_y - 120} "
        f"A {hw} 120 0 0 1 {cx - hw} {bot_y - 120} "
        f"L {cx - hw} {bot_y - 255} "
        f"C {cx - hw} {bot_y - 285}, {cx - hw - 52} {bot_y - 290}, {cx - hw - 52} {bot_y - 245} "
        f"L {cx - hw - 52} {bot_y - 108} "
        f"Q {cx - hw - 54} {bot_y - 72}, {cx - hw - 78} {bot_y - 44} "
        f"Q {cx - hw - 102} {bot_y - 72}, {cx - hw - 104} {bot_y - 108} "
        f"L {cx - hw - 104} {bot_y - 260} "
        f"C {cx - hw - 104} {bot_y - 332}, {cx - hw - 52} {bot_y - 336}, {cx - hw - 24} {bot_y - 336} "
        f"C {cx - hw - 4} {bot_y - 336}, {cx - hw} {bot_y - 346}, {cx - hw} {bot_y - 365} Z"
    )
    s.path(d_outer, stroke_width=sw)

    # Top anode disk + pinch seal
    s.circle(cx, top_y - 10.0, 12.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.polygon([
        (cx - 16.0, top_y + 4.0), (cx + 16.0, top_y + 4.0),
        (cx + 10.0, top_y + 74.0), (cx - 10.0, top_y + 74.0),
    ], fill="#ffffff", stroke_width=5.5)
    s.line(cx, top_y + 74.0, cx, top_y + 92.0, stroke_width=sw)
    s.line(cx - 26.0, top_y + 92.0, cx + 26.0, top_y + 92.0, stroke_width=sw * 1.1)

    # Concave hemispherical cup cathode a
    cup_y = 874.0 if cx < 500 else 860.0
    s.path(f"M {cx - 94} {cup_y - 90} A 94 90 0 0 0 {cx + 94} {cup_y - 90}", stroke_width=sw * 1.25)

    # Supporting glass stem down to bottom pinch seal
    s.rect(cx - 9.0, cup_y - 2.0, 18.0, bot_y - cup_y - 44.0, fill="#000000", stroke="none")
    s.polygon([
        (cx - 10.0, bot_y - 50.0), (cx + 10.0, bot_y - 50.0),
        (cx + 26.0, bot_y - 2.0), (cx - 26.0, bot_y - 2.0),
    ], fill="#ffffff", stroke_width=5.5)
    s.circle(cx, bot_y + 10.0, 12.0, fill="#ffffff", stroke_width=sw * 0.85)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # Left tube A
    _tube(s, 242.0, 152.0, 1484.0, sw)
    # Straight dashed focus rays converging at (242, 650)
    s.line(169.0, 836.0, 366.0, 336.0, stroke_width=sw * 0.85, dash="22,16")
    s.line(315.0, 836.0, 118.0, 354.0, stroke_width=sw * 0.85, dash="22,16")
    s.line(242.0, 870.0, 242.0, 248.0, stroke_width=sw * 0.85, dash="26,18")

    # Right tube B
    _tube(s, 742.0, 134.0, 1456.0, sw)
    # Magnetically deflected curved rays converging near (684, 636)
    s.path("M 678 826 Q 730 740, 684 636 Q 664 606, 636 602", stroke_width=sw * 0.85, dash="18,14")
    s.path("M 742 856 Q 740 730, 684 636 Q 662 612, 636 616", stroke_width=sw * 0.85, dash="18,14")
    s.path("M 796 782 Q 750 690, 684 636 Q 666 618, 638 626", stroke_width=sw * 0.85, dash="18,14")

    # Labels
    lib.label(s, 248.0, 102.0, "A", size=68.0, italic=False, bold=True)
    lib.label(s, 176.0, 892.0, "a", size=64.0, italic=True, bold=True)
    lib.label(s, 740.0, 82.0, "B", size=68.0, italic=False, bold=True)
    lib.label(s, 672.0, 868.0, "a", size=64.0, italic=True, bold=True)

    s.save(out_svg)
