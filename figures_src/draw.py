"""Low-level SVG primitives and 1:1 pixel-coordinate Scene builder."""

from __future__ import annotations

import math
from html import escape
from pathlib import Path
from typing import Iterable, Sequence


def _fmt(v: float) -> str:
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _attrs(extra: dict[str, object]) -> str:
    parts = []
    for k, v in extra.items():
        if v is None:
            continue
        key = k.replace("_", "-")
        if isinstance(v, float):
            val = _fmt(v)
        else:
            val = str(v)
        parts.append(f'{key}="{escape(val, quote=True)}"')
    return (" " + " ".join(parts)) if parts else ""


class Scene:
    """SVG canvas in 1:1 pixel coordinates matching the reference scan."""

    def __init__(self, w: int, h: int, bg: str | None = None) -> None:
        self.w = int(w)
        self.h = int(h)
        self.defs: list[str] = []
        self.elements: list[str] = []
        if bg:
            self.rect(0, 0, self.w, self.h, fill=bg, stroke="none")

    def add_def(self, raw_svg: str) -> None:
        self.defs.append(raw_svg)

    def raw(self, svg_fragment: str) -> None:
        self.elements.append(svg_fragment)

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        linecap: str = "round",
        **kw: object,
    ) -> None:
        self.elements.append(
            f"<line{_attrs(dict(x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, stroke_linecap=linecap, **kw))}/>"
        )

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: str = "none",
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        rx: float | None = None,
        **kw: object,
    ) -> None:
        self.elements.append(
            f"<rect{_attrs(dict(x=x, y=y, width=w, height=h, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, rx=rx, **kw))}/>"
        )

    def circle(
        self,
        cx: float,
        cy: float,
        r: float,
        *,
        fill: str = "none",
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        **kw: object,
    ) -> None:
        self.elements.append(
            f"<circle{_attrs(dict(cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, **kw))}/>"
        )

    def ellipse(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        *,
        fill: str = "none",
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        rotate: float | None = None,
        **kw: object,
    ) -> None:
        transform = f"rotate({_fmt(rotate)} {_fmt(cx)} {_fmt(cy)})" if rotate else None
        self.elements.append(
            f"<ellipse{_attrs(dict(cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, transform=transform, **kw))}/>"
        )

    def polyline(
        self,
        pts: Sequence[tuple[float, float]],
        *,
        fill: str = "none",
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        linecap: str = "round",
        linejoin: str = "round",
        **kw: object,
    ) -> None:
        pstr = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)
        self.elements.append(
            f"<polyline{_attrs(dict(points=pstr, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, stroke_linecap=linecap, stroke_linejoin=linejoin, **kw))}/>"
        )

    def polygon(
        self,
        pts: Sequence[tuple[float, float]],
        *,
        fill: str = "none",
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        linejoin: str = "round",
        **kw: object,
    ) -> None:
        pstr = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)
        self.elements.append(
            f"<polygon{_attrs(dict(points=pstr, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, stroke_linejoin=linejoin, **kw))}/>"
        )

    def path(
        self,
        d: str,
        *,
        fill: str = "none",
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        linecap: str = "round",
        linejoin: str = "round",
        **kw: object,
    ) -> None:
        self.elements.append(
            f"<path{_attrs(dict(d=d, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, stroke_linecap=linecap, stroke_linejoin=linejoin, **kw))}/>"
        )

    def arc(
        self,
        cx: float,
        cy: float,
        r: float,
        start_deg: float,
        end_deg: float,
        *,
        stroke: str = "#000000",
        stroke_width: float = 4.0,
        dash: str | None = None,
        fill: str = "none",
        sweep: int = 1,
        **kw: object,
    ) -> None:
        """Draw circular arc in SVG coords (deg clockwise from +x axis)."""
        a1 = math.radians(start_deg)
        a2 = math.radians(end_deg)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        delta = (end_deg - start_deg) % 360.0 if sweep == 1 else (start_deg - end_deg) % 360.0
        large = 1 if delta > 180.0 else 0
        d = f"M {_fmt(x1)} {_fmt(y1)} A {_fmt(r)} {_fmt(r)} 0 {large} {sweep} {_fmt(x2)} {_fmt(y2)}"
        self.path(d, fill=fill, stroke=stroke, stroke_width=stroke_width, dash=dash, **kw)

    def text(
        self,
        x: float,
        y: float,
        content: str,
        *,
        size: float = 48.0,
        family: str = "New Computer Modern, Georgia, serif",
        style: str = "normal",
        weight: str = "normal",
        anchor: str = "middle",
        baseline: str = "central",
        fill: str = "#000000",
        rotate: float | None = None,
        **kw: object,
    ) -> None:
        transform = f"rotate({_fmt(rotate)} {_fmt(x)} {_fmt(y)})" if rotate else None
        self.elements.append(
            f"<text{_attrs(dict(x=x, y=y, font_size=size, font_family=family, font_style=style, font_weight=weight, text_anchor=anchor, dominant_baseline=baseline, fill=fill, transform=transform, **kw))}>{escape(content)}</text>"
        )

    def to_svg(self) -> str:
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">',
        ]
        if self.defs:
            lines.append("  <defs>")
            for d in self.defs:
                lines.append("    " + d)
            lines.append("  </defs>")
        for el in self.elements:
            lines.append("  " + el)
        lines.append("</svg>")
        return "\n".join(lines) + "\n"

    def save(self, path: Path | str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_svg(), encoding="utf-8")
