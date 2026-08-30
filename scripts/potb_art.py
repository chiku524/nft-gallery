#!/usr/bin/env python3
"""In-place SVG + PNG trait art for Pugs On The Block.

Every trait is drawn on a 1024×1024 canvas already seated on the pug.
No crop/fit pass. Studio and the generator just stack the layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from PIL import Image, ImageDraw

SIZE = 1024
WALL_TOP = 648
INK = "#1a120e"


def _hex(color: str | tuple[int, int, int]) -> str:
    if isinstance(color, tuple):
        return "#{:02x}{:02x}{:02x}".format(*color)
    return color


def _rgb(color: str | tuple[int, int, int]) -> tuple[int, int, int]:
    if isinstance(color, tuple):
        return color
    h = color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


@dataclass
class Drawing:
    ops: list[tuple] = field(default_factory=list)

    def ellipse(self, xy, fill, stroke=INK, sw=7):
        self.ops.append(("ellipse", xy, fill, stroke, sw))

    def rect(self, xy, fill, stroke=None, sw=0, radius=0):
        self.ops.append(("rect", xy, fill, stroke, sw, radius))

    def polygon(self, pts, fill, stroke=INK, sw=6):
        self.ops.append(("polygon", pts, fill, stroke, sw))

    def line(self, a, b, stroke=INK, sw=6):
        self.ops.append(("line", a, b, stroke, sw))

    def to_png(self) -> Image.Image:
        im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for op in self.ops:
            kind = op[0]
            if kind == "ellipse":
                _, xy, fill, stroke, sw = op
                if fill:
                    d.ellipse(xy, fill=_rgb(fill))
                if stroke and sw:
                    d.ellipse(xy, outline=_rgb(stroke), width=int(sw))
            elif kind == "rect":
                _, xy, fill, stroke, sw, radius = op
                if radius:
                    d.rounded_rectangle(xy, radius=radius, fill=_rgb(fill) if fill else None, outline=_rgb(stroke) if stroke else None, width=int(sw or 0))
                else:
                    d.rectangle(xy, fill=_rgb(fill) if fill else None, outline=_rgb(stroke) if stroke else None, width=int(sw or 0))
            elif kind == "polygon":
                _, pts, fill, stroke, sw = op
                d.polygon(pts, fill=_rgb(fill) if fill else None)
                if stroke and sw:
                    closed = list(pts) + [pts[0]]
                    d.line(closed, fill=_rgb(stroke), width=int(sw), joint="curve")
            elif kind == "line":
                _, a, b, stroke, sw = op
                d.line([a, b], fill=_rgb(stroke), width=int(sw))
        return im

    def to_svg(self) -> str:
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}">',
            "<g fill-rule=\"evenodd\" stroke-linejoin=\"round\" stroke-linecap=\"round\">",
        ]
        for op in self.ops:
            kind = op[0]
            if kind == "ellipse":
                _, xy, fill, stroke, sw = op
                x0, y0, x1, y1 = xy
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
                parts.append(
                    f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                    f'fill="{_hex(fill) if fill else "none"}" stroke="{_hex(stroke) if stroke else "none"}" '
                    f'stroke-width="{sw}"/>'
                )
            elif kind == "rect":
                _, xy, fill, stroke, sw, radius = op
                x0, y0, x1, y1 = xy
                rr = f' rx="{radius}" ry="{radius}"' if radius else ""
                parts.append(
                    f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"{rr} '
                    f'fill="{_hex(fill) if fill else "none"}" stroke="{_hex(stroke) if stroke else "none"}" '
                    f'stroke-width="{sw or 0}"/>'
                )
            elif kind == "polygon":
                _, pts, fill, stroke, sw = op
                points = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                parts.append(
                    f'<polygon points="{points}" fill="{_hex(fill) if fill else "none"}" '
                    f'stroke="{_hex(stroke) if stroke else "none"}" stroke-width="{sw}"/>'
                )
            elif kind == "line":
                _, a, b, stroke, sw = op
                parts.append(
                    f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" '
                    f'stroke="{_hex(stroke)}" stroke-width="{sw}"/>'
                )
        parts.append("</g></svg>")
        return "\n".join(parts)


COATS = {
    "fawn": {"fur": "#e8b482", "shade": "#c88958", "mask": "#2b211c", "paw": "#f3d2b0"},
    "cream": {"fur": "#f3d7b3", "shade": "#d4b48a", "mask": "#3a2c24", "paw": "#fff1dc"},
    "black": {"fur": "#3a3538", "shade": "#2a2628", "mask": "#1a1618", "paw": "#d9c4a8"},
}


def draw_background(kind: str) -> Drawing:
    g = Drawing()
    palettes = {
        "brownstone": ("#c45a28", "#8a2f12", "#f0b06a"),
        "stoop-day": ("#6ec4f2", "#f2c98a", "#f7e7c4"),
        "cream-brick": ("#f0c9a0", "#e0a878", "#f8e2c4"),
        "rooftop": ("#f08a2a", "#c44a12", "#ffd07a"),
        "subway": ("#3d2a55", "#1c1428", "#7a5a9a"),
        "court": ("#5a3a78", "#241428", "#c47a3a"),
        "neon": ("#1a1030", "#0a0618", "#ff4d8d"),
        "chain-green": ("#1f5a3a", "#0d2e1c", "#7dce6a"),
    }
    mid, dark, accent = palettes[kind]
    g.rect((0, 0, SIZE, SIZE), mid)
    if kind in {"brownstone", "cream-brick", "stoop-day"}:
        for y in range(0, SIZE, 48):
            offset = 28 if (y // 48) % 2 else 0
            for x in range(-40 + offset, SIZE, 92):
                g.rect((x + 3, y + 3, x + 86, y + 42), dark, None, 0, 4)
        if kind == "stoop-day":
            g.ellipse((620, 40, 780, 200), accent, None, 0)
        g.rect((80, 220, 280, 640), "#2a1a14", INK, 6, 8)
        g.rect((120, 280, 240, 400), "#7ec8e8", INK, 5, 4)
    elif kind == "rooftop":
        g.rect((0, 0, SIZE, 360), "#2a1848")
        g.ellipse((680, 60, 860, 240), accent, None, 0)
        g.rect((0, 360, SIZE, SIZE), mid)
        for i in range(6):
            g.rect((40 + i * 170, 420, 150 + i * 170, 640), dark, INK, 5, 6)
    elif kind == "subway":
        g.rect((0, 0, SIZE, 280), "#12101c")
        for x in range(0, SIZE, 80):
            g.rect((x + 8, 300, x + 72, 620), "#c4b49a", INK, 4, 4)
        g.rect((0, 200, SIZE, 260), accent, None, 0)
    elif kind == "court":
        g.ellipse((-80, 80, 420, 520), dark, None, 0)
        g.rect((0, 520, SIZE, 640), "#2a1a14")
    elif kind == "neon":
        g.rect((40, 80, 220, 640), "#ff4d8d", None, 0, 10)
        g.rect((760, 140, 980, 400), "#3df0ff", None, 0, 10)
        g.rect((300, 40, 700, 160), "#b24dff", None, 0, 8)
    else:  # chain-green
        for y in range(0, SIZE, 64):
            g.line((0, y), (SIZE, y), accent, 3)
        for x in range(0, SIZE, 64):
            g.line((x, 0), (x, SIZE), accent, 3)
        g.rect((0, 0, SIZE, SIZE), None, dark, 18)
    return g


def draw_wall(kind: str) -> Drawing:
    g = Drawing()
    fills = {
        "default": "#9aa0a6",
        "concrete": "#8b9096",
        "brownstone-ledge": "#a44a28",
        "crate": "#8a5a28",
        "gold": "#e6b423",
    }
    shade = {
        "default": "#7c8288",
        "concrete": "#6e747a",
        "brownstone-ledge": "#7a3018",
        "crate": "#6a4018",
        "gold": "#c49210",
    }
    fill = fills[kind]
    g.rect((0, WALL_TOP, SIZE, SIZE), fill, INK, 8)
    g.rect((0, WALL_TOP, SIZE, WALL_TOP + 22), shade[kind], INK, 5)
    if kind == "crate":
        for x in (80, 360, 640, 900):
            g.line((x, WALL_TOP + 8), (x, SIZE), INK, 5)
        g.line((0, 820), (SIZE, 820), INK, 5)
    elif kind == "gold":
        for x in range(40, SIZE, 160):
            g.rect((x, WALL_TOP + 40, x + 120, 980), "#f2d056", INK, 5, 8)
    elif kind == "concrete":
        for x in range(0, SIZE, 220):
            g.line((x, WALL_TOP), (x, SIZE), INK, 4)
        g.line((0, 840), (SIZE, 840), INK, 4)
    elif kind == "brownstone-ledge":
        for y in range(WALL_TOP + 28, SIZE, 46):
            off = 20 if ((y // 46) % 2) else 0
            for x in range(-20 + off, SIZE, 110):
                g.rect((x, y, x + 100, y + 38), "#8a381c", INK, 3, 3)
    return g


def _head(g: Drawing, coat: dict) -> None:
    # Ears
    g.ellipse((250, 210, 400, 430), coat["mask"], INK, 8)
    g.ellipse((624, 210, 774, 430), coat["mask"], INK, 8)
    # Head
    g.ellipse((268, 188, 756, 640), coat["fur"], INK, 9)
    g.ellipse((300, 250, 500, 520), coat["shade"], None, 0)
    # Mask
    g.ellipse((330, 330, 694, 620), coat["mask"], INK, 7)
    # Eyes
    g.ellipse((360, 360, 478, 478), "#111111", INK, 6)
    g.ellipse((546, 360, 664, 478), "#111111", INK, 6)
    g.ellipse((392, 388, 428, 424), "#ffffff", None, 0)
    g.ellipse((578, 388, 614, 424), "#ffffff", None, 0)
    # Snout + tongue
    g.ellipse((430, 470, 594, 600), "#2a211c", INK, 6)
    g.ellipse((468, 530, 556, 612), "#f28a96", INK, 5)
    g.line((512, 548), (512, 598), "#c45a68", 4)
    # Wrinkles
    g.line((470, 330), (554, 330), INK, 5)
    g.line((456, 348), (568, 348), INK, 4)


def draw_base(color: str) -> Drawing:
    g = Drawing()
    _head(g, COATS[color])
    return g


def draw_paws(color: str) -> Drawing:
    g = Drawing()
    coat = COATS[color]
    g.ellipse((300, 600, 455, 720), coat["paw"], INK, 8)
    g.ellipse((569, 600, 724, 720), coat["paw"], INK, 8)
    for x0 in (318, 352, 386, 587, 621, 655):
        g.ellipse((x0, 628, x0 + 28, 662), coat["mask"], INK, 4)
    return g


def draw_hat(kind: str) -> Drawing:
    g = Drawing()
    if kind == "beanie":
        g.ellipse((318, 70, 706, 230), "#2f7a3a", INK, 8)  # pom
        g.polygon(
            [(300, 300), (340, 150), (512, 118), (684, 150), (724, 300), (690, 348), (334, 348)],
            "#3d8f48",
            INK,
            8,
        )
        g.rect((320, 300, 704, 368), "#2f7a3a", INK, 7, 18)
        for x in range(360, 680, 36):
            g.line((x, 160), (x, 300), "#2a6a34", 4)
    elif kind == "newsie":
        g.ellipse((290, 200, 734, 360), "#6b4224", INK, 8)
        g.ellipse((310, 188, 714, 300), "#8a5a32", INK, 7)
        g.ellipse((490, 200, 534, 236), "#4a2c16", INK, 5)
        g.rect((268, 328, 756, 378), "#5a361c", INK, 7, 16)
    elif kind == "snapback":
        g.polygon(
            [(320, 320), (360, 190), (512, 168), (664, 190), (704, 320), (680, 348), (344, 348)],
            "#c4282a",
            INK,
            8,
        )
        g.rect((390, 200, 634, 330), "#3a3532", INK, 6, 16)
        g.polygon([(300, 340), (724, 340), (780, 390), (244, 390)], "#e03a3c", INK, 7)
        g.ellipse((494, 168, 530, 202), "#c4282a", INK, 5)
    elif kind == "hardhat":
        g.ellipse((340, 168, 684, 360), "#f2c20a", INK, 8)
        g.rect((300, 300, 724, 372), "#e0a800", INK, 7, 20)
        g.rect((494, 188, 530, 300), "#d4a000", INK, 5, 6)
    elif kind == "crown":
        pts = [(360, 330), (390, 200), (448, 280), (512, 168), (576, 280), (634, 200), (664, 330)]
        g.polygon(pts, "#f0c01a", INK, 8)
        g.rect((360, 318, 664, 368), "#d8a010", INK, 7, 8)
        for x in (400, 512, 624):
            g.ellipse((x - 16, 184, x + 16, 216), "#f2d056", INK, 4)
        for x in (430, 512, 594):
            g.ellipse((x - 18, 328, x + 18, 364), "#d4282a", INK, 4)
    return g


def draw_body(kind: str) -> Drawing:
    g = Drawing()
    # Clothes sit on the neck above the wall so the ledge does not hide them.
    if kind == "bandana":
        g.polygon(
            [
                (318, 575),
                (390, 548),
                (512, 582),
                (634, 548),
                (706, 575),
                (688, WALL_TOP),
                (336, WALL_TOP),
            ],
            "#2f7a3a",
            INK,
            8,
        )
        g.ellipse((668, 530, 778, 622), "#3d8f48", INK, 7)
        g.ellipse((718, 500, 798, 572), "#2f7a3a", INK, 6)
        g.ellipse((688, 488, 758, 548), "#3d8f48", INK, 6)
    elif kind == "collar":
        g.polygon(
            [(338, 575), (400, 548), (512, 572), (624, 548), (686, 575), (662, WALL_TOP), (362, WALL_TOP)],
            "#d4242e",
            INK,
            8,
        )
        g.rect((474, 558, 550, 618), "#f0c01a", INK, 6, 8)
        g.polygon(
            [(492, 608), (478, 638), (498, 628), (512, 646), (526, 628), (546, 638), (532, 608)],
            "#f0c01a",
            INK,
            5,
        )
    elif kind == "hoodie":
        g.polygon(
            [
                (278, 548),
                (368, 518),
                (512, 558),
                (656, 518),
                (746, 548),
                (716, WALL_TOP),
                (308, WALL_TOP),
            ],
            "#e8c9a4",
            INK,
            8,
        )
        g.ellipse((428, 568, 468, 606), "#6a4a28", INK, 4)
        g.ellipse((556, 568, 596, 606), "#6a4a28", INK, 4)
        g.rect((440, 598, 458, WALL_TOP - 4), "#8a5a32", INK, 5, 6)
        g.rect((566, 598, 584, WALL_TOP - 4), "#8a5a32", INK, 5, 6)
    elif kind == "gold-chain":
        for x, y in (
            (392, 548),
            (424, 572),
            (458, 592),
            (492, 608),
            (532, 608),
            (566, 592),
            (600, 572),
            (632, 548),
        ):
            g.ellipse((x - 26, y - 18, x + 26, y + 20), "#f0c01a", INK, 5)
        g.ellipse((474, 600, 550, 646), "#e6b423", INK, 6)
        g.ellipse((490, 612, 534, 640), "#c49210", INK, 4)
    return g


def draw_accessory(kind: str) -> Drawing:
    g = Drawing()
    if kind == "sunglasses":
        g.ellipse((348, 368, 490, 488), "#1a1a1a", INK, 8)
        g.ellipse((534, 368, 676, 488), "#1a1a1a", INK, 8)
        g.rect((478, 410, 546, 438), "#c4282a", INK, 5, 6)
        g.line((348, 410), (300, 390), INK, 7)
        g.line((676, 410), (724, 390), INK, 7)
    elif kind == "monocle":
        g.ellipse((338, 350, 488, 500), None, "#f0c01a", 10)
        g.ellipse((354, 366, 472, 484), "#d6eef2", "#f0c01a", 4)
        g.line((412, 500), (400, 640), "#f0c01a", 5)
        g.ellipse((392, 636, 420, 664), "#f0c01a", INK, 4)
    elif kind == "bone":
        g.ellipse((700, 600, 760, 660), "#f0e0c0", INK, 6)
        g.ellipse((820, 600, 880, 660), "#f0e0c0", INK, 6)
        g.ellipse((700, 680, 760, 740), "#f0e0c0", INK, 6)
        g.ellipse((820, 680, 880, 740), "#f0e0c0", INK, 6)
        g.rect((730, 628, 850, 712), "#e8d2a8", INK, 6, 10)
    elif kind == "coffee":
        g.rect((720, 560, 860, 720), "#6a3a18", INK, 7, 12)
        g.rect((708, 540, 872, 580), "#efe6dc", INK, 6, 10)
        g.ellipse((740, 500, 840, 560), "#efe6dc", INK, 6)
        g.rect((790, 470, 810, 520), "#3a2a18", INK, 4, 3)
    elif kind == "blocks":
        g.rect((80, 560, 200, 680), "#e03a3c", INK, 6, 8)
        g.rect((150, 500, 270, 620), "#3a7ad9", INK, 6, 8)
        g.rect((70, 620, 190, 740), "#f0c01a", INK, 6, 8)
    return g


TRAIT_BUILDERS: dict[tuple[str, str], callable] = {}


def _register():
    for kind in ("brownstone", "stoop-day", "cream-brick", "rooftop", "subway", "court", "neon", "chain-green"):
        TRAIT_BUILDERS[("background", kind)] = lambda k=kind: draw_background(k)
    for color in COATS:
        TRAIT_BUILDERS[("base", color)] = lambda c=color: draw_base(c)
        TRAIT_BUILDERS[("paws", color)] = lambda c=color: draw_paws(c)
    for kind in ("default", "concrete", "brownstone-ledge", "crate", "gold"):
        TRAIT_BUILDERS[("block", kind)] = lambda k=kind: draw_wall(k)
    for kind in ("beanie", "newsie", "snapback", "hardhat", "crown"):
        TRAIT_BUILDERS[("hat", kind)] = lambda k=kind: draw_hat(k)
    for kind in ("bandana", "collar", "hoodie", "gold-chain"):
        TRAIT_BUILDERS[("body", kind)] = lambda k=kind: draw_body(k)
    for kind in ("sunglasses", "monocle", "bone", "coffee", "blocks"):
        TRAIT_BUILDERS[("accessory", kind)] = lambda k=kind: draw_accessory(k)


_register()


FILES = {
    ("background", "brownstone"): "background/bg-brownstone",
    ("background", "stoop-day"): "background/bg-stoop-day",
    ("background", "cream-brick"): "background/bg-cream-brick",
    ("background", "rooftop"): "background/bg-rooftop-sunset",
    ("background", "subway"): "background/bg-subway",
    ("background", "court"): "background/bg-court-dusk",
    ("background", "neon"): "background/bg-neon-night",
    ("background", "chain-green"): "background/bg-chain-green",
    ("base", "fawn"): "base/base-fawn-peek",
    ("base", "cream"): "base/base-cream-peek",
    ("base", "black"): "base/base-black-peek",
    ("paws", "fawn"): "base/front-paws-fawn",
    ("paws", "cream"): "base/front-paws-cream",
    ("paws", "black"): "base/front-paws-black",
    ("block", "default"): "base/wall-default",
    ("block", "concrete"): "block/block-concrete",
    ("block", "brownstone-ledge"): "block/block-brownstone",
    ("block", "crate"): "block/block-crate",
    ("block", "gold"): "block/block-gold",
    ("hat", "beanie"): "hat/hat-beanie",
    ("hat", "newsie"): "hat/hat-newsie",
    ("hat", "snapback"): "hat/hat-snapback",
    ("hat", "hardhat"): "hat/hat-hardhat",
    ("hat", "crown"): "hat/hat-crown",
    ("body", "bandana"): "body/body-bandana",
    ("body", "collar"): "body/body-collar",
    ("body", "hoodie"): "body/body-hoodie",
    ("body", "gold-chain"): "body/body-gold-chain",
    ("accessory", "sunglasses"): "accessory/acc-sunglasses",
    ("accessory", "monocle"): "accessory/acc-monocle",
    ("accessory", "bone"): "accessory/acc-bone",
    ("accessory", "coffee"): "accessory/acc-coffee",
    ("accessory", "blocks"): "accessory/acc-blocks",
}


def write_all(root: Path) -> None:
    traits = root / "public" / "traits"
    for key, rel in FILES.items():
        drawing = TRAIT_BUILDERS[key]()
        dest = traits / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        drawing.to_png().save(dest.with_suffix(".png"))
        dest.with_suffix(".svg").write_text(drawing.to_svg() + "\n", encoding="utf-8")
        print(f"wrote {rel}.svg + .png")
