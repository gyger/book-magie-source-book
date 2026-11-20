"""Fig. 68: Fresnel's diffraction through a narrow slit AB with effective rays CF, DF."""

from pathlib import Path
from PIL import Image
import draw
import library


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    bar_y = 82.0
    fx, fy = 62.0, 1035.0
    ax, cx, dx, bx = 457.0, 511.0, 589.0, 635.0

    # Left and right opaque screen edges (slit opening between A and B)
    scene.line(260.0, bar_y, ax, bar_y, stroke_width=10.0)
    scene.line(bx, bar_y, 791.0, bar_y, stroke_width=10.0)
    # Thin line across the slit opening connecting A, C, D, B
    scene.line(ax, bar_y, bx, bar_y, stroke_width=4.0)

    # Four rays from A, C, D, B converging to F
    for x in (ax, cx, dx, bx):
        scene.line(x, bar_y, fx, fy, stroke_width=5.5)

    # Labels A, C, D, B above bar, and F near bottom vertex
    library.label(scene, ax - 8, bar_y - 36, "A", size=54, italic=False, bold=True)
    library.label(scene, cx - 2, bar_y - 36, "C", size=54, italic=False, bold=True)
    library.label(scene, dx - 2, bar_y - 36, "D", size=54, italic=False, bold=True)
    library.label(scene, bx + 8, bar_y - 36, "B", size=54, italic=False, bold=True)
    library.label(scene, fx + 44, fy - 24, "F", size=54, italic=False, bold=True)

    scene.save(out_svg)
