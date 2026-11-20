"""Figure 38: Joule's free-expansion apparatus — copper receivers R and E in a single water vessel."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _capsule_path(x_left: float, x_right: float, y_top: float, y_bot: float, dome_h: float) -> str:
    """Rounded-end vertical cylinder (capsule) path."""
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
    sw_thin = 4.6

    # --- Outer double-lobed tin water vessel ---
    # Outer vertical walls and middle seam verticals
    s.line(25.0, 82.0, 30.0, 862.0, stroke_width=sw)
    s.line(333.0, 102.0, 335.0, 858.0, stroke_width=sw)
    s.line(691.0, 102.0, 693.0, 855.0, stroke_width=sw)
    s.line(995.0, 82.0, 1002.0, 856.0, stroke_width=sw)

    # Bottom contour of tin vessel
    s.path(
        "M 30 862 C 85 934, 255 936, 335 858",
        stroke_width=sw,
    )
    s.line(335.0, 857.0, 693.0, 855.0, stroke_width=sw)
    s.path(
        "M 693 855 C 765 924, 925 924, 1002 856",
        stroke_width=sw,
    )

    # Top double-walled peanut-shaped rim
    # Back outer rim
    s.path(
        "M 25 82 C 25 18, 250 8, 326 68 L 696 70 C 772 10, 995 22, 995 82",
        stroke_width=sw,
    )
    # Back inner rim
    s.path(
        "M 39 82 C 39 32, 245 22, 324 79 L 698 80 C 776 24, 982 34, 982 82",
        stroke_width=sw_thin,
    )
    # Front inner rim
    s.path(
        "M 39 82 C 39 148, 248 158, 328 98 L 694 99 C 776 160, 982 150, 982 82",
        stroke_width=sw_thin,
    )
    # Front outer rim
    s.path(
        "M 25 82 C 25 160, 250 172, 333 108 L 691 109 C 774 174, 995 162, 995 82",
        stroke_width=sw,
    )

    # --- Left copper receiver R ---
    s.path(_capsule_path(64.0, 284.0, 162.0, 778.0, 105.0), stroke_width=sw)
    # Small boss/plug at top of R (partially behind front rim)
    s.path("M 146 168 L 146 154 C 146 146, 206 146, 206 154 L 206 168 C 206 177, 146 177, 146 168 Z", stroke_width=sw_thin)
    s.path("M 150 142 C 154 116, 198 116, 202 142", stroke_width=sw_thin)
    lib.filled_dot(s, 162.0, 162.0, r=4.5)
    lib.filled_dot(s, 187.0, 162.0, r=4.5)

    # --- Right copper receiver E ---
    s.path(_capsule_path(737.0, 958.0, 162.0, 764.0, 105.0), stroke_width=sw)

    # --- Connecting tubes and stopcocks ---
    # Left L-shaped pipe from bottom of R to left stopcock
    s.polyline(
        [(147.0, 778.0), (147.0, 800.0), (458.0, 798.0), (458.0, 616.0)],
        stroke_width=sw,
    )
    s.polyline(
        [(235.0, 764.0), (422.0, 761.0), (422.0, 616.0)],
        stroke_width=sw,
    )
    # Double line accent along top of left horizontal pipe
    s.line(230.0, 769.0, 422.0, 766.0, stroke_width=3.0)

    # Right L-shaped pipe from bottom of E to right stopcock
    s.polyline(
        [(870.0, 764.0), (870.0, 793.0), (562.0, 795.0), (562.0, 616.0)],
        stroke_width=sw,
    )
    s.polyline(
        [(786.0, 754.0), (598.0, 756.0), (598.0, 616.0)],
        stroke_width=sw,
    )
    # Double line accent along top of right horizontal pipe
    s.line(792.0, 760.0, 598.0, 762.0, stroke_width=3.0)

    # Left stopcock square housing + diamond key
    s.rect(414.0, 548.0, 58.0, 60.0, stroke_width=sw)
    s.polygon([(442.0, 563.0), (456.0, 577.0), (442.0, 591.0), (428.0, 577.0)], stroke_width=4.8)

    # Right stopcock square housing + diamond key
    s.rect(547.0, 548.0, 61.0, 60.0, stroke_width=sw)
    s.polygon([(576.0, 563.0), (590.0, 577.0), (576.0, 591.0), (562.0, 577.0)], stroke_width=4.8)

    # Center coupling flange + bolt dots + horizontal necks
    s.rect(491.0, 532.0, 39.0, 94.0, stroke_width=sw)
    lib.filled_dot(s, 510.0, 550.0, r=5.0)
    lib.filled_dot(s, 510.0, 608.0, r=5.0)
    s.line(472.0, 567.0, 491.0, 567.0, stroke_width=sw)
    s.line(472.0, 596.0, 491.0, 596.0, stroke_width=sw)
    s.line(530.0, 567.0, 547.0, 567.0, stroke_width=sw)
    s.line(530.0, 596.0, 547.0, 596.0, stroke_width=sw)

    # Labels
    lib.label(s, 174.0, 452.0, "R", size=64.0, italic=False, bold=True)
    lib.label(s, 846.0, 448.0, "E", size=64.0, italic=False, bold=True)
    lib.label(s, 769.0, 823.0, "D", size=58.0, italic=False, bold=True)

    s.save(out_svg)
