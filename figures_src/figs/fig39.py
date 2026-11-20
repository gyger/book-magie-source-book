"""Figure 39: Joule's inverted receivers immersed in three separate water cans."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _capsule_path(x_left: float, x_right: float, y_top: float, y_bot: float, dome_h: float) -> str:
    rx = 0.5 * (x_right - x_left)
    yt = y_top + dome_h
    yb = y_bot - dome_h
    return (
        f"M {draw._fmt(x_left)} {draw._fmt(yt)} "
        f"A {draw._fmt(rx)} {draw._fmt(dome_h)} 0 0 1 {draw._fmt(x_right)} {draw._fmt(yt)} "
        f"L {draw._fmt(x_right)} {draw._fmt(yb)} "
        f"A {draw._fmt(rx)} {draw._fmt(dome_h)} 0 0 1 {draw._fmt(x_left)} {draw._fmt(yb)} Z"
    )


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.2

    # --- Left water can ---
    # Back rim arc
    s.path("M 30 112 C 30 56, 316 56, 316 112", stroke_width=sw)
    s.line(30.0, 112.0, 24.0, 712.0, stroke_width=sw)
    s.line(316.0, 112.0, 305.0, 712.0, stroke_width=sw)
    s.path("M 24 712 C 62 782, 266 782, 305 712", stroke_width=sw)

    # --- Middle small water can (back rim + walls + bottom) ---
    s.path("M 358 112 C 358 64, 603 64, 603 112", stroke_width=sw)
    s.line(358.0, 112.0, 357.0, 348.0, stroke_width=sw)
    s.line(603.0, 112.0, 602.0, 348.0, stroke_width=sw)
    s.path("M 357 348 C 392 404, 568 404, 602 348", stroke_width=sw)

    # --- Right water can ---
    s.path("M 688 109 C 688 55, 974 55, 974 109", stroke_width=sw)
    s.line(688.0, 109.0, 685.0, 706.0, stroke_width=sw)
    s.line(974.0, 109.0, 964.0, 706.0, stroke_width=sw)
    s.path("M 685 706 C 724 776, 926 776, 964 706", stroke_width=sw)

    # --- Left inverted receiver ---
    s.path(_capsule_path(54.0, 281.0, 106.0, 688.0, 108.0), stroke_width=sw)

    # --- Right inverted receiver ---
    s.path(_capsule_path(718.0, 943.0, 106.0, 668.0, 108.0), stroke_width=sw)
    # Bottom plug on right receiver
    s.path("M 796 663 L 796 697 Q 834 704 872 697 L 872 663", stroke_width=sw)
    lib.filled_dot(s, 810.0, 686.0, r=5.5)
    lib.filled_dot(s, 855.0, 686.0, r=5.5)

    # --- Inverted connecting L-pipes (white fill to cleanly mask back rims behind them) ---
    # Left L-pipe
    s.path(
        "M 135 110 L 135 55 L 420 56 L 420 286 L 386 286 L 386 90 L 188 90 L 188 110 "
        "Q 161 118 135 110 Z",
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )
    s.line(135.0, 63.0, 420.0, 64.0, stroke_width=3.8)

    # Right L-pipe
    s.path(
        "M 854 110 L 854 57 L 540 57 L 540 286 L 578 286 L 578 92 L 798 92 L 798 110 "
        "Q 826 118 854 110 Z",
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )
    s.line(540.0, 65.0, 854.0, 65.0, stroke_width=3.8)

    # Front rim arcs of all 3 cans (drawn in front of receivers & pipes, matching scan)
    s.path("M 30 112 C 62 170, 284 170, 316 112", stroke_width=sw)
    s.path("M 358 112 C 388 172, 574 172, 603 112", stroke_width=sw)
    s.path("M 688 109 C 720 165, 942 165, 974 109", stroke_width=sw)

    # --- Stopcock assembly inside middle can ---
    s.rect(376.0, 287.0, 56.0, 53.0, fill="#ffffff", stroke="#000000", stroke_width=sw)
    s.rect(528.0, 287.0, 59.0, 53.0, fill="#ffffff", stroke="#000000", stroke_width=sw)
    s.rect(463.0, 270.0, 38.0, 90.0, fill="#ffffff", stroke="#000000", stroke_width=sw)
    lib.filled_dot(s, 482.0, 288.0, r=5.0)
    lib.filled_dot(s, 482.0, 340.0, r=5.0)
    s.line(432.0, 299.0, 463.0, 299.0, stroke_width=sw)
    s.line(432.0, 327.0, 463.0, 327.0, stroke_width=sw)
    s.line(501.0, 299.0, 528.0, 299.0, stroke_width=sw)
    s.line(501.0, 327.0, 528.0, 327.0, stroke_width=sw)

    s.save(out_svg)
