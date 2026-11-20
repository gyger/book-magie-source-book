"""Figure 93: Faraday's concentric ice-pails (1, 2, 3, 4) separated by shellac plates."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _hatched_pad(s: draw.Scene, x1: float, x2: float, y1: float, y2: float, rx: float, sw: float) -> None:
    """Draw a rounded insulating pad with diagonal hatching lines."""
    pad_w = x2 - x1
    pad_h = y2 - y1
    clip_id = f"clip_{int(x1)}_{int(y1)}"
    s.add_def(
        f'<clipPath id="{clip_id}">'
        f'<rect x="{x1:.1f}" y="{y1:.1f}" width="{pad_w:.1f}" height="{pad_h:.1f}" rx="{rx:.1f}"/>'
        f'</clipPath>'
    )
    # White fill + diagonal hatch clipped to pad
    s.rect(x1, y1, pad_w, pad_h, fill="#ffffff", stroke="none", rx=rx)
    lines = []
    step = 16.0
    x = x1 - pad_h
    while x < x2 + pad_h:
        lines.append(
            f'<line x1="{x:.1f}" y1="{y2:.1f}" x2="{x + pad_h * 0.62:.1f}" y2="{y1:.1f}" '
            f'stroke="#000000" stroke-width="4.2"/>'
        )
        x += step
    s.raw(f'<g clip-path="url(#{clip_id})">' + "".join(lines) + "</g>")
    s.rect(x1, y1, pad_w, pad_h, fill="none", stroke_width=sw, rx=rx)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.0
    # 4 concentric ice-pail vessels
    # Vessel 1 (outer)
    s.path(
        "M 315 48 L 315 636 Q 315 774, 448 774 L 742 774 Q 868 774, 868 636 L 868 48",
        stroke_width=sw,
    )
    # Vessel 2
    s.path(
        "M 369 90 L 369 612 Q 369 716, 466 716 L 716 716 Q 812 716, 812 612 L 812 76",
        stroke_width=sw,
    )
    # Vessel 3
    s.path(
        "M 423 120 L 423 590 Q 423 664, 492 664 L 686 664 Q 754 664, 754 590 L 754 110",
        stroke_width=sw,
    )
    # Vessel 4 (inner)
    s.path(
        "M 471 148 L 471 574 Q 471 618, 514 618 L 658 618 Q 700 618, 700 574 L 700 144",
        stroke_width=sw,
    )

    # 3 hatched shellac insulating plates between bottoms
    _hatched_pad(s, 394.0, 778.0, 716.0, 774.0, 27.0, sw * 0.9)
    _hatched_pad(s, 426.0, 750.0, 664.0, 716.0, 24.0, sw * 0.9)
    _hatched_pad(s, 464.0, 706.0, 618.0, 664.0, 21.0, sw * 0.9)

    # Carrier sphere C and suspension thread
    s.line(586.0, 0.0, 586.0, 286.0, stroke_width=sw)
    s.circle(586.0, 375.0, 88.0, fill="#ffffff", stroke_width=sw * 0.9)

    # Wire from vessel 1 to electrometer on bottom-left
    s.path("M 315 624 Q 250 660, 200 688 L 82 752", stroke_width=sw)

    # Gold-leaf electrometer on bottom-left
    s.circle(52.0, 770.0, 34.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.line(41.0, 804.0, 41.0, 948.0, stroke_width=6.0)
    s.line(54.0, 804.0, 54.0, 948.0, stroke_width=6.0)
    s.line(41.0, 948.0, 22.0, h - 1.0, stroke_width=6.5)
    s.line(54.0, 948.0, 77.0, h - 1.0, stroke_width=6.5)

    # Labels
    lib.label(s, 314.0, 26.0, "1", size=60.0, italic=False, bold=True)
    lib.label(s, 370.0, 58.0, "2", size=60.0, italic=False, bold=True)
    lib.label(s, 422.0, 92.0, "3", size=60.0, italic=False, bold=True)
    lib.label(s, 470.0, 122.0, "4", size=60.0, italic=False, bold=True)
    lib.label(s, 584.0, 375.0, "C", size=68.0, italic=False, bold=True)

    s.save(out_svg)
