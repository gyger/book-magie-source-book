"""Fig. 91, 4: Faraday's cylindrical bar magnet thrust into a hollow copper helix."""

from pathlib import Path
from PIL import Image
import draw


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    # Vertical connecting wires going up to galvanometer
    scene.line(48.0, 22.0, 44.0, 140.0, stroke_width=8.0)
    scene.line(418.0, 22.0, 420.0, 140.0, stroke_width=8.0)

    # Hollow helix cylinder body (rounded rectangle / tube)
    scene.rect(42.0, 134.0, 380.0, 78.0, rx=22.0, fill="#ffffff", stroke="#000000", stroke_width=8.0)
    # Left end elliptical opening of the hollow helix
    scene.ellipse(36.0, 173.0, 14.0, 26.0, fill="#ffffff", stroke="#000000", stroke_width=6.0)
    # Right end elliptical opening of the hollow helix
    scene.ellipse(424.0, 173.0, 14.0, 26.0, fill="#ffffff", stroke="#000000", stroke_width=6.0)

    # Cylindrical bar magnet thrust into the right end of the helix
    scene.rect(426.0, 165.0, 342.0, 28.0, rx=10.0, fill="#ffffff", stroke="#000000", stroke_width=7.0)

    scene.save(out_svg)
