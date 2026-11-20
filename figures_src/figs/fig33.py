"""Figure 33: Division of vibrating strings (octave, fifth, fourth, etc.) with Greek node labels."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _draw_string(
    s: draw.Scene,
    x1: float,
    x2: float,
    y: float,
    *,
    left_label: str,
    right_label: str,
    left_italic: bool = False,
    right_italic: bool = False,
    ticks: list[tuple[float, str, str]] | None = None,
) -> None:
    """Draw a horizontal string with end-ticks, interior division ticks, and labels.

    ticks: list of (x, label_text, placement) where placement is 'below' or 'above'.
    """
    sw = 8.5
    s.line(x1, y, x2, y, stroke_width=sw)
    # End ticks
    s.line(x1, y - 16.0, x1, y + 16.0, stroke_width=7.0)
    s.line(x2, y - 16.0, x2, y + 16.0, stroke_width=7.0)

    # Left & right labels
    lib.label(s, x1 - 32.0, y - 2.0, left_label, size=62.0, italic=left_italic, bold=True)
    lib.label(s, x2 + 40.0, y - 2.0, right_label, size=62.0, italic=right_italic, bold=True)

    if ticks:
        for tx, txt, pos in ticks:
            s.line(tx, y - 13.0, tx, y + 13.0, stroke_width=6.0)
            if pos == "above":
                lib.label(s, tx, y - 42.0, txt, size=54.0, italic=False, bold=True)
            else:
                lib.label(s, tx, y + 48.0, txt, size=60.0, italic=True, bold=True)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # 1: A - C
    _draw_string(s, 187.0, 1446.0, 50.5, left_label="A", right_label="C")

    # 2: a - gamma (midpoint beta)
    _draw_string(
        s, 194.0, 1450.0, 183.5,
        left_label="a", right_label="γ",
        left_italic=True, right_italic=True,
        ticks=[(824.5, "β", "below")],
    )

    # 3: A - D
    _draw_string(s, 200.0, 1456.0, 355.5, left_label="A", right_label="D")

    # 4: a - delta (thirds beta, gamma)
    _draw_string(
        s, 204.0, 1458.0, 497.5,
        left_label="a", right_label="δ",
        left_italic=True, right_italic=True,
        ticks=[(622.0, "β", "below"), (1046.5, "γ", "below")],
    )

    # 5: A - E
    _draw_string(s, 204.0, 1458.0, 666.5, left_label="A", right_label="E")

    # 6: a - epsilon (quarters beta, gamma, delta)
    _draw_string(
        s, 208.0, 1458.0, 808.5,
        left_label="a", right_label="ε",
        left_italic=True, right_italic=True,
        ticks=[(522.5, "β", "below"), (833.5, "γ", "below"), (1148.5, "δ", "below")],
    )

    # 7: A - G (midpoint D above)
    _draw_string(
        s, 208.0, 1458.0, 977.5,
        left_label="A", right_label="G",
        ticks=[(833.0, "D", "above")],
    )

    # 8: a - eta (thirds gamma, epsilon)
    _draw_string(
        s, 209.0, 1460.0, 1118.5,
        left_label="a", right_label="η",
        left_italic=True, right_italic=True,
        ticks=[(630.5, "γ", "below"), (1051.5, "ε", "below")],
    )

    s.save(out_svg)
