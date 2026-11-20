"""Render SVG via Typst and produce side-by-side + red/blue overlay diagnostics."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


def render_svg_via_typst(svg_path: Path, target_w: int, target_h: int) -> Image.Image:
    """Render an SVG file through Typst at exact pixel dimensions (target_w, target_h)."""
    # Use 1pt = 1px at 72 ppi so Typst renders directly at target_w x target_h
    root_dir = svg_path.resolve().parent.parent
    tmp_base = root_dir / "figures_src" / "out" / "_tmp"
    tmp_base.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=tmp_base) as tmpdir:
        tmp = Path(tmpdir)
        typ_file = tmp / "render.typ"
        out_png = tmp / "render.png"
        rel_svg = svg_path.resolve().relative_to(root_dir).as_posix()
        typ_code = (
            f"#set page(width: {target_w}pt, height: {target_h}pt, margin: 0pt, fill: white)\n"
            f'#image("/{rel_svg}", width: {target_w}pt, height: {target_h}pt)\n'
        )
        typ_file.write_text(typ_code, encoding="utf-8")
        subprocess.run(
            [
                "typst",
                "compile",
                "--root",
                str(root_dir),
                "--format",
                "png",
                "--ppi",
                "72",
                str(typ_file),
                str(out_png),
            ],
            check=True,
        )
        im = Image.open(out_png).convert("L")
        if im.size != (target_w, target_h):
            im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        return im


def make_diagnostics(
    scan_png: Path,
    svg_path: Path,
    out_dir: Path,
    fig_name: str,
    dark_thresh: int = 180,
) -> dict[str, float]:
    """Generate figXX_cmp.png and figXX_ovl.png and return overlap metrics."""
    out_dir.mkdir(parents=True, exist_ok=True)
    scan_im = Image.open(scan_png).convert("L")
    w, h = scan_im.size
    svg_im = render_svg_via_typst(svg_path, w, h)

    # Side-by-side comparison
    gap = 12
    cmp_im = Image.new("RGB", (w * 2 + gap, h), (220, 220, 220))
    cmp_im.paste(scan_im.convert("RGB"), (0, 0))
    cmp_im.paste(svg_im.convert("RGB"), (w + gap, 0))
    cmp_im.save(out_dir / f"{fig_name}_cmp.png", optimize=True)

    # Red/Blue/Black overlay
    scan_arr = np.asarray(scan_im) < dark_thresh
    svg_arr = np.asarray(svg_im) < dark_thresh
    ovl = np.full((h, w, 3), 255, dtype=np.uint8)
    only_scan = scan_arr & (~svg_arr)
    only_svg = svg_arr & (~scan_arr)
    both = scan_arr & svg_arr
    ovl[only_scan] = (225, 45, 45)    # Red = original scan only
    ovl[only_svg] = (35, 90, 235)     # Blue = generated SVG only
    ovl[both] = (0, 0, 0)             # Black = exact overlap
    Image.fromarray(ovl, mode="RGB").save(out_dir / f"{fig_name}_ovl.png", optimize=True)

    n_both = int(both.sum())
    n_scan = int(scan_arr.sum())
    n_svg = int(svg_arr.sum())
    union = n_scan + n_svg - n_both
    iou = (n_both / union) if union > 0 else 1.0
    return {
        "scan_px": n_scan,
        "svg_px": n_svg,
        "both_px": n_both,
        "iou": round(iou, 3),
    }
