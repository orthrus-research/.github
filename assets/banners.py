"""Draw the Orthrus Research mark and the repository banners as standalone SVG.

usage: python assets/banners.py            writes assets/orthrus-mark.svg and profile/banner.svg
       python assets/banners.py OUT NAME   writes OUT/banner.svg for project NAME

The mark is four identical pieces (vertical bar, fillet, 50-degree band, cut end) related by
reflection and half-turns; the four bands weave around a central diamond, over and under in turn.
Units follow the original 256 px avatar: bands 15 wide, gaps 5, mark 150 x 172.
Text uses the website's system serif stack, so no font file is embedded or licensed.
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARK = "#D6D7D1"  # the avatar's off-white
FIELD = "#000000"
TEXT = "#FFFFFF"
SERIF = "Baskerville, 'Iowan Old Style', 'Palatino Linotype', 'Book Antiqua', Palatino, serif"

WIDTH, GAP, RADIUS = 15.0, 5.0, 15.0
ANGLE = math.radians(50)  # band direction measured from vertical
BAR_X, TOP, CUT_X, OFFSET_X = 67.5, 86.0, 55.0, 29.0
S, C = math.sin(ANGLE), math.cos(ANGLE)
VERTEX_Y = OFFSET_X * C / S  # where the two band families cross on the vertical axis


def f(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def piece(sx: int, sy: int, ident: str) -> str:
    """The piece whose bar is on side sx (-1 left) and end sy (-1 top)."""
    direction = (-sx * S, -sy * C)
    corner_y = sy * (BAR_X - OFFSET_X) / S * C
    t = RADIUS * math.tan(ANGLE / 2)  # fillet tangent length for a 50-degree turn
    p1 = (sx * BAR_X, corner_y + sy * t)
    p2 = (sx * BAR_X + t * direction[0], corner_y + t * direction[1])
    end = (p2[0] + 220 * direction[0], p2[1] + 220 * direction[1])
    sweep = 1 if -sx * sy * S > 0 else 0
    d = (
        f"M{f(sx * BAR_X)} {f(sy * TOP)}L{f(p1[0])} {f(p1[1])}"
        f"A{f(RADIUS)} {f(RADIUS)} 0 0 {sweep} {f(p2[0])} {f(p2[1])}L{f(end[0])} {f(end[1])}"
    )
    # Ends short of the opposite bar; passes under the other family at one diamond vertex.
    clip_x = -200 if sx < 0 else -CUT_X
    clip_w = 200 + CUT_X
    if sx == sy:  # "\" band, under at the vertex on the vertical axis
        vertex, over = (0.0, -sy * VERTEX_Y), (-S, C)
    else:  # "/" band, under at the vertex on the horizontal axis
        vertex, over = (sx * OFFSET_X, 0.0), (S, C)
    a = (vertex[0] - 30 * over[0], vertex[1] - 30 * over[1])
    b = (vertex[0] + 30 * over[0], vertex[1] + 30 * over[1])
    return (
        f'<clipPath id="{ident}c"><rect x="{f(clip_x)}" y="-100" width="{f(clip_w)}" '
        f'height="200"/></clipPath>'
        f'<mask id="{ident}m" maskUnits="userSpaceOnUse" x="-100" y="-100" width="200" '
        f'height="200"><rect x="-100" y="-100" width="200" height="200" fill="#fff"/>'
        f'<path d="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}" stroke="#000" '
        f'stroke-width="{f(WIDTH + 2 * GAP)}"/></mask>'
        f'<g clip-path="url(#{ident}c)"><path d="{d}" fill="none" stroke="{MARK}" '
        f'stroke-width="{f(WIDTH)}" mask="url(#{ident}m)"/></g>'
    )


def mark(prefix: str) -> str:
    """The mark centered on the origin, 150 x 172 units."""
    pieces = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
    return "".join(piece(sx, sy, f"{prefix}{i}") for i, (sx, sy) in enumerate(pieces))


def mark_svg() -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -100 200 200" width="200" '
        f'height="200" role="img" aria-label="Orthrus Research mark"><title>Orthrus Research'
        f"</title>{mark('m')}</svg>\n"
    )


def text_width(text: str, size: float, spacing: float) -> float:
    """Estimated advance of serif capitals; the viewer's font decides the exact width."""
    return len(text) * 0.70 * size + (len(text) - 1) * spacing


def banner_svg(project: str, subtitle: str = "ORTHRUS RESEARCH") -> str:
    """1280 x 320: the mark, then the name in serif capitals over the subtitle, centered."""
    name = project.upper()
    label = f"{project} by Orthrus Research" if project != "Orthrus" else "Orthrus Research"
    words = max(text_width(name, 92, 14), text_width(subtitle, 21, 8.5))
    left = (1280 - (150 + 64 + words)) / 2
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 320" width="1280" '
        f'height="320" role="img" aria-label="{label}"><title>{label}</title>'
        f'<rect width="1280" height="320" fill="{FIELD}"/>'
        f'<g transform="translate({f(left + 75)} 160)">{mark("b")}</g>'
        f'<g font-family="{SERIF}" text-rendering="geometricPrecision">'
        f'<text x="{f(left + 214)}" y="176" font-size="92" letter-spacing="14" '
        f'fill="{TEXT}">{name}</text>'
        f'<text x="{f(left + 218)}" y="228" font-size="21" letter-spacing="8.5" '
        f'fill="{MARK}">{subtitle}</text></g></svg>\n'
    )


def write(path: Path, svg: str) -> None:
    """LF line endings on every platform, so regenerated files compare byte for byte."""
    path.write_bytes(svg.encode("utf-8"))


def main() -> None:
    if len(sys.argv) == 3:
        out = Path(sys.argv[1])
        out.mkdir(parents=True, exist_ok=True)
        write(out / "banner.svg", banner_svg(sys.argv[2]))
        return
    write(HERE / "orthrus-mark.svg", mark_svg())
    write(HERE.parent / "profile/banner.svg", banner_svg("Orthrus", "RESEARCH"))


if __name__ == "__main__":
    main()
