"""Fig. 68: Fresnel's diffraction through a narrow slit AB with effective rays CF, DF."""

from pathlib import Path
from PIL import Image
import draw
import library


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    bar_y = 84.0
    fx, fy = 28.0, 1035.0
    ax, cx, dx, bx = 460.0, 513.0, 590.0, 638.0

    # Left and right opaque screen edges (slit opening between A and B)
    scene.line(258.0, bar_y, ax, bar_y, stroke_width=10.0)
    scene.line(bx, bar_y, 791.0, bar_y, stroke_width=10.0)
    # Dashed horizontal line across the slit opening connecting A, C, D, B
    scene.line(ax, bar_y, bx, bar_y, stroke_width=5.5, dash="28,12", linecap="butt")

    # Four rays from A, C, D, B converging to F
    for x in (ax, cx, dx, bx):
        scene.line(x, bar_y, fx, fy, stroke_width=5.5)

    # Labels A, C, D, B above bar, and F near bottom vertex
    library.label(scene, ax + 4, bar_y - 38, "A", size=54, italic=False, bold=True)
    library.label(scene, cx - 2, bar_y - 38, "C", size=54, italic=False, bold=True)
    library.label(scene, dx - 2, bar_y - 38, "D", size=54, italic=False, bold=True)
    library.label(scene, bx + 6, bar_y - 38, "B", size=54, italic=False, bold=True)
    library.label(scene, fx + 52, fy - 24, "F", size=54, italic=False, bold=True)

    scene.save(out_svg)
