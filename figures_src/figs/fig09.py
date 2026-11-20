"""Figure 9: Stevinus's wreath of spheres (clootcrans) on inclined planes AB, BC."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.5

    # Inner triangle ABC
    ax, ay = 172.0, 514.5
    cx, cy = 1054.0, 514.5
    bx, by = 882.0, 164.0
    scene.polygon([(ax, ay), (bx, by), (cx, cy)], stroke_width=sw)

    # Outer wreath polygon vertices: corners S, T, V and hanging ball centers
    s_pt = (68.0, 516.0)
    t_pt = (905.0, 114.0)
    v_pt = (1120.0, 535.0)

    # 14 ball centers measured from scan
    balls = [
        ("P", 190.0, 466.0, 184, 386),
        ("Q", 392.0, 366.0, 382, 276),
        ("R", 594.0, 265.0, 584, 180),
        ("D", 802.0, 162.0, 760, 108),
        ("E", 962.0, 224.0, 1024, 200),
        ("F", 1068.0, 428.0, 1126, 412),
        ("G", 1115.0, 642.0, 1176, 644),
        ("H", 1034.0, 862.0, 1102, 868),
        ("I", 890.0, 1044.0, 948, 1056),
        ("K", 720.0, 1184.0, 792, 1200),
        ("L", 498.0, 1186.0, 558, 1236),
        ("M", 308.0, 1038.0, 286, 1118),
        ("N", 170.0, 852.0, 118, 898),
        ("O", 102.0, 636.0, 48, 666),
    ]

    # Closed string loop passing through S, T, V and the hanging balls G..O
    loop_pts = [
        s_pt,
        t_pt,
        v_pt,
        (1115.0, 642.0),  # G
        (1034.0, 862.0),  # H
        (890.0, 1044.0),  # I
        (720.0, 1184.0),  # K
        (498.0, 1186.0),  # L
        (308.0, 1038.0),  # M
        (170.0, 852.0),   # N
        (102.0, 636.0),   # O
    ]
    scene.polygon(loop_pts, stroke_width=sw)

    # Draw 14 spheres (unfilled so the string passes visibly through centers as in woodcut)
    r_ball = 34.0
    for name, bx_i, by_i, lx, ly in balls:
        scene.circle(bx_i, by_i, r_ball, fill="none", stroke="#000000", stroke_width=sw)
        lib.label(scene, lx, ly, name, size=66, italic=False, bold=True)

    # Corner labels A, B, C, S, T, V
    lib.label(scene, 192, 578, "A", size=66, italic=False, bold=True)
    lib.label(scene, 870, 224, "B", size=66, italic=False, bold=True)
    lib.label(scene, 1046, 560, "C", size=66, italic=False, bold=True)
    lib.label(scene, 42, 502, "S", size=66, italic=False, bold=True)
    lib.label(scene, 916, 62, "T", size=66, italic=False, bold=True)
    lib.label(scene, 1166, 536, "V", size=66, italic=False, bold=True)

    scene.save(out_svg)
