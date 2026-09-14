"""Build the static Street Heirs prototype.

Street Heirs is an original editorial-vector portrait system. This painter is
intentionally self-contained: paint_kit supplies image I/O, while every shape,
palette, layer, trait, and compatibility rule is defined here.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw

from paint_kit import SIZE, save_image


NAME = "Street Heirs"
SYMBOL = "HEIRS"
SLUG = "street-heirs"
SUBJECT = "Editorial-vector streetwear portraits with graphic signals"
CHAIN = "Robinhood Chain"
SUPPLY = 5_555
MINT_PRICE = "0.005 ETH"
ART_VERSION = "prototype-5"
SEED = "street-heirs/clean-cartoon/v5"

ROOT = Path(__file__).resolve().parents[1]
TRAIT_ROOT = ROOT / "public" / f"{SLUG}-traits"
PREVIEW_ROOT = ROOT / "public" / f"{SLUG}-preview"
METADATA_ROOT = ROOT / "public" / "metadata"
DATA_ROOT = ROOT / "src" / "data"

SCALE = 2
INK = "#17223b"
PAPER = "#f4efe5"

TRAIT_ORDER = (
    "atmosphere",
    "complexion",
    "tailoring",
    "coiffure",
    "visage",
    "cadence",
    "adornment",
    "signal",
)

STACK = (
    "atmosphere",
    "tailoring",
    "complexion",
    "coiffure",
    "visage",
    "cadence",
    "adornment",
    "signal",
)

TRAIT_SPEC: dict[str, tuple[tuple[str, str, int], ...]] = {
    "atmosphere": (
        ("midnight-grid", "Midnight Grid", 12),
        ("cobalt-sun", "Cobalt Sun", 13),
        ("amber-blocks", "Amber Blocks", 13),
        ("jade-arc", "Jade Arc", 13),
        ("violet-broadcast", "Violet Broadcast", 12),
        ("crimson-check", "Crimson Check", 12),
        ("paper-blue", "Paper Blue", 13),
        ("acid-window", "Acid Window", 12),
    ),
    "complexion": (
        ("deep-umber", "Deep Umber / Angular", 12),
        ("mahogany", "Mahogany / Broad", 13),
        ("sienna", "Sienna / Soft Jaw", 13),
        ("copper", "Copper / High Cheek", 13),
        ("golden-brown", "Golden Brown / Tapered", 13),
        ("olive", "Olive / Square", 12),
        ("warm-beige", "Warm Beige / Heart", 12),
        ("cool-porcelain", "Cool Porcelain / Long", 12),
    ),
    "tailoring": (
        ("signal-bomber", "Signal Bomber", 11),
        ("varsity-archive", "Varsity Archive", 10),
        ("heavy-hoodie", "Heavy Hoodie", 12),
        ("workwear-blue", "Workwear Blue", 11),
        ("ribbed-turtleneck", "Ribbed Turtleneck", 10),
        ("patched-denim", "Patched Denim", 10),
        ("football-knit", "Football Knit", 9),
        ("track-panel", "Track Panel", 10),
        ("quilted-vest", "Quilted Vest", 9),
        ("longline-coat", "Longline Coat", 8),
    ),
    "coiffure": (
        ("loc-crown", "Loc Crown", 11),
        ("box-braids", "Box Braids", 10),
        ("high-puff", "High Puff", 11),
        ("sculpted-twists", "Sculpted Twists", 10),
        ("wave-crop", "Wave Crop", 11),
        ("temple-fade", "Temple Fade", 11),
        ("buzz-design", "Buzz Design", 10),
        ("bandana-curls", "Bandana Curls", 9),
        ("beanie-coils", "Beanie Coils", 9),
        ("durag-tails", "Durag Tails", 8),
    ),
    "visage": (
        ("steady", "Steady", 14),
        ("side-eye", "Side Eye", 13),
        ("soft-blink", "Soft Blink", 12),
        ("joy-lines", "Joy Lines", 12),
        ("amber-shades", "Amber Shades", 11),
        ("clear-frames", "Clear Frames", 11),
        ("future-visor", "Future Visor", 9),
        ("star-liner", "Star Liner", 8),
    ),
    "cadence": (
        ("calm", "Calm", 16),
        ("half-smile", "Half Smile", 15),
        ("gap-grin", "Gap Grin", 13),
        ("berry-gloss", "Berry Gloss", 12),
        ("silver-tooth", "Silver Tooth", 11),
        ("fine-mustache", "Fine Mustache", 11),
        ("short-beard", "Short Beard", 12),
        ("chin-stripe", "Chin Stripe", 10),
    ),
    "adornment": (
        ("gold-hoops", "Gold Hoops", 14),
        ("silver-studs", "Silver Studs", 14),
        ("curb-chain", "Curb Chain", 13),
        ("pearl-line", "Pearl Line", 11),
        ("nose-ring", "Nose Ring", 12),
        ("ear-cuff", "Ear Cuff", 12),
        ("studio-cans", "Studio Cans", 10),
        ("safety-pin", "Safety Pin", 9),
    ),
    "signal": (
        ("crop-code", "Crop Code", 13),
        ("offset-halo", "Offset Halo", 12),
        ("halftone-veil", "Halftone Veil", 11),
        ("type-bars", "Type Bars", 11),
        ("orbit-lines", "Orbit Lines", 11),
        ("prism-slice", "Prism Slice", 10),
        ("sound-wave", "Sound Wave", 10),
        ("pixel-flare", "Pixel Flare", 9),
        ("double-exposure", "Double Exposure", 8),
        ("corner-stamps", "Corner Stamps", 8),
    ),
}

INCOMPATIBLE = (
    (("coiffure", "beanie-coils"), ("adornment", "studio-cans")),
    (("coiffure", "durag-tails"), ("adornment", "studio-cans")),
    (("visage", "future-visor"), ("adornment", "studio-cans")),
    (("visage", "amber-shades"), ("signal", "halftone-veil")),
    (("tailoring", "heavy-hoodie"), ("adornment", "curb-chain")),
)

SIGNATURES = (
    ("midnight-grid", "deep-umber", "signal-bomber", "loc-crown", "steady", "silver-tooth", "gold-hoops", "offset-halo"),
    ("cobalt-sun", "mahogany", "varsity-archive", "box-braids", "side-eye", "berry-gloss", "nose-ring", "crop-code"),
    ("amber-blocks", "sienna", "heavy-hoodie", "high-puff", "soft-blink", "gap-grin", "pearl-line", "type-bars"),
    ("jade-arc", "copper", "workwear-blue", "sculpted-twists", "joy-lines", "half-smile", "ear-cuff", "orbit-lines"),
    ("violet-broadcast", "golden-brown", "ribbed-turtleneck", "wave-crop", "amber-shades", "calm", "curb-chain", "prism-slice"),
    ("crimson-check", "olive", "patched-denim", "temple-fade", "clear-frames", "fine-mustache", "silver-studs", "sound-wave"),
    ("paper-blue", "warm-beige", "football-knit", "buzz-design", "future-visor", "chin-stripe", "safety-pin", "pixel-flare"),
    ("acid-window", "cool-porcelain", "track-panel", "bandana-curls", "star-liner", "berry-gloss", "gold-hoops", "double-exposure"),
    ("paper-blue", "deep-umber", "quilted-vest", "beanie-coils", "joy-lines", "short-beard", "ear-cuff", "corner-stamps"),
    ("midnight-grid", "mahogany", "longline-coat", "durag-tails", "soft-blink", "silver-tooth", "pearl-line", "prism-slice"),
    ("jade-arc", "sienna", "signal-bomber", "box-braids", "clear-frames", "calm", "studio-cans", "sound-wave"),
    ("amber-blocks", "copper", "varsity-archive", "high-puff", "side-eye", "gap-grin", "nose-ring", "halftone-veil"),
    ("crimson-check", "golden-brown", "workwear-blue", "loc-crown", "star-liner", "half-smile", "safety-pin", "crop-code"),
    ("violet-broadcast", "olive", "track-panel", "sculpted-twists", "steady", "short-beard", "silver-studs", "type-bars"),
    ("acid-window", "warm-beige", "patched-denim", "wave-crop", "amber-shades", "fine-mustache", "curb-chain", "orbit-lines"),
    ("cobalt-sun", "cool-porcelain", "ribbed-turtleneck", "temple-fade", "future-visor", "chin-stripe", "gold-hoops", "offset-halo"),
)


def box(values: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(value * SCALE for value in values)


def points(values: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(x * SCALE, y * SCALE) for x, y in values]


def width(value: int) -> int:
    return value * SCALE


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))


def finish(image: Image.Image) -> Image.Image:
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def line(draw: ImageDraw.ImageDraw, coords: list[tuple[int, int]], fill: str, stroke: int = 4) -> None:
    draw.line(points(coords), fill=fill, width=width(stroke), joint="curve")


def ellipse(draw: ImageDraw.ImageDraw, coords: tuple[int, int, int, int], fill: str, outline: str | None = None, stroke: int = 1) -> None:
    draw.ellipse(box(coords), fill=fill, outline=outline, width=width(stroke))


def polygon(draw: ImageDraw.ImageDraw, coords: list[tuple[int, int]], fill: str, outline: str | None = None, stroke: int = 1) -> None:
    draw.polygon(points(coords), fill=fill)
    if outline:
        draw.line(points(coords + [coords[0]]), fill=outline, width=width(stroke), joint="curve")


def rounded(draw: ImageDraw.ImageDraw, coords: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None, stroke: int = 1) -> None:
    draw.rounded_rectangle(box(coords), radius=radius * SCALE, fill=fill, outline=outline, width=width(stroke))


def paint_atmosphere(trait: str) -> Image.Image:
    palettes = {
        "midnight-grid": ("#202A3D", "#465269", "#D3B36C"),
        "cobalt-sun": ("#496A9A", "#B8C8DA", "#EAD49F"),
        "amber-blocks": ("#D4AE70", "#E7D5AF", "#80564A"),
        "jade-arc": ("#47776E", "#ACC9C1", "#D9C383"),
        "violet-broadcast": ("#685B78", "#B9ADC3", "#D8C99E"),
        "crimson-check": ("#895157", "#AC6C70", "#E5D6C2"),
        "paper-blue": ("#DCE4E6", "#A9BBC7", "#C7816E"),
        "acid-window": ("#B6C3A3", "#718473", "#E8E1D1"),
    }
    base, accent, spark = palettes[trait]
    image = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), base)
    draw = ImageDraw.Draw(image)
    if trait == "midnight-grid":
        line(draw, [(104, 0), (104, 512)], accent, 2)
        line(draw, [(0, 104), (512, 104)], accent, 2)
        ellipse(draw, (390, 54, 448, 112), spark)
    elif trait == "cobalt-sun":
        ellipse(draw, (58, 42, 286, 270), spark)
        rounded(draw, (54, 432, 184, 440), 4, accent)
    elif trait == "amber-blocks":
        rounded(draw, (34, 36, 138, 196), 18, accent)
        rounded(draw, (388, 42, 476, 184), 18, spark)
    elif trait == "jade-arc":
        draw.arc(box((42, 42, 470, 470)), 202, 338, fill=accent, width=width(9))
        ellipse(draw, (400, 70, 430, 100), spark)
    elif trait == "violet-broadcast":
        rounded(draw, (34, 90, 176, 100), 5, accent)
        rounded(draw, (34, 116, 112, 126), 5, spark)
    elif trait == "crimson-check":
        draw.rectangle(box((0, 0, 256, 256)), fill=accent)
        draw.rectangle(box((256, 256, 512, 512)), fill=accent)
        line(draw, [(0, 452), (512, 352)], spark, 8)
    elif trait == "paper-blue":
        polygon(draw, [(0, 0), (146, 0), (74, 512), (0, 512)], accent)
        rounded(draw, (22, 446, 96, 454), 4, spark)
    elif trait == "acid-window":
        rounded(draw, (42, 42, 470, 470), 34, accent)
        rounded(draw, (54, 54, 458, 458), 26, base)
        line(draw, [(82, 58), (82, 454)], spark, 6)
    return finish(image)


COMPLEXIONS = {
    "deep-umber": ("#4b2d2a", "#6e4137", [(170, 166), (342, 158), (376, 264), (344, 388), (274, 436), (194, 396), (150, 286)]),
    "mahogany": ("#6a3b32", "#8a5040", [(156, 176), (354, 176), (380, 294), (344, 402), (256, 438), (164, 394), (132, 286)]),
    "sienna": ("#925844", "#b87359", [(174, 158), (338, 166), (372, 282), (326, 408), (252, 438), (180, 402), (146, 278)]),
    "copper": ("#ae6d4e", "#ca8660", [(164, 174), (346, 160), (384, 272), (334, 396), (258, 432), (178, 394), (134, 270)]),
    "golden-brown": ("#bd8054", "#d39a68", [(180, 154), (336, 166), (368, 278), (318, 414), (256, 444), (190, 402), (152, 270)]),
    "olive": ("#a78261", "#c09c75", [(158, 174), (354, 174), (370, 378), (306, 430), (202, 430), (142, 374)]),
    "warm-beige": ("#d1a17f", "#e1b898", [(176, 160), (338, 164), (378, 278), (330, 394), (256, 442), (182, 394), (138, 278)]),
    "cool-porcelain": ("#e2bba8", "#f0cfbd", [(184, 146), (332, 156), (362, 290), (316, 422), (256, 452), (194, 414), (150, 280)]),
}


def paint_complexion(trait: str) -> Image.Image:
    tone, light, shape = COMPLEXIONS[trait]
    image = blank()
    draw = ImageDraw.Draw(image)
    polygon(draw, [(220, 356), (292, 356), (300, 446), (212, 446)], tone, INK, 6)
    ellipse(draw, (124, 244, 176, 312), tone, INK, 5)
    ellipse(draw, (336, 244, 388, 312), tone, INK, 5)
    polygon(draw, shape, tone, INK, 6)
    ellipse(draw, (304, 284, 344, 322), light)
    ellipse(draw, (144, 266, 160, 286), light)
    ellipse(draw, (352, 266, 368, 286), light)
    line(draw, [(256, 228), (248, 292), (264, 298)], INK, 4)
    return finish(image)


def paint_tailoring(trait: str) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    configs = {
        "signal-bomber": ("#e95745", "#f5c84c"),
        "varsity-archive": ("#173f72", "#eee5d2"),
        "heavy-hoodie": ("#51436f", "#a98ed2"),
        "workwear-blue": ("#286b8e", "#ef9c3d"),
        "ribbed-turtleneck": ("#262938", "#e0bc58"),
        "patched-denim": ("#4776a8", "#f06e62"),
        "football-knit": ("#ece4d7", "#258079"),
        "track-panel": ("#313342", "#d8eb3f"),
        "quilted-vest": ("#6f7b3c", "#efb865"),
        "longline-coat": ("#7d493e", "#69b4aa"),
    }
    main, accent = configs[trait]
    polygon(draw, [(70, 512), (102, 432), (188, 396), (220, 378), (292, 378), (324, 396), (410, 432), (444, 512)], main, INK, 7)
    if trait == "signal-bomber":
        line(draw, [(256, 382), (256, 512)], accent, 9)
        for x in (126, 340):
            rounded(draw, (x, 442, x + 48, 472), 10, accent)
    elif trait == "varsity-archive":
        polygon(draw, [(70, 512), (102, 426), (174, 390), (194, 512)], accent)
        polygon(draw, [(318, 390), (410, 426), (444, 512), (318, 512)], accent)
        line(draw, [(256, 382), (256, 512)], PAPER, 6)
    elif trait == "heavy-hoodie":
        draw.arc(box((158, 352, 354, 482)), 186, 354, fill=accent, width=width(16))
        line(draw, [(218, 398), (208, 484)], PAPER, 4)
        line(draw, [(294, 398), (304, 484)], PAPER, 4)
    elif trait == "workwear-blue":
        line(draw, [(256, 382), (256, 512)], accent, 6)
        for x in (126, 306):
            rounded(draw, (x, 438, x + 80, 494), 8, accent, INK, 4)
    elif trait == "ribbed-turtleneck":
        rounded(draw, (202, 346, 310, 430), 20, main, INK, 6)
        for x in range(216, 306, 18):
            line(draw, [(x, 370), (x, 510)], accent, 3)
    elif trait == "patched-denim":
        for coords in ((118, 430, 182, 476), (326, 444, 390, 492)):
            rounded(draw, coords, 5, accent, PAPER, 3)
        line(draw, [(256, 382), (256, 512)], PAPER, 4)
    elif trait == "football-knit":
        rounded(draw, (220, 416, 292, 498), 10, accent)
        line(draw, [(104, 448), (188, 432)], accent, 8)
        line(draw, [(324, 432), (408, 448)], accent, 8)
    elif trait == "track-panel":
        polygon(draw, [(88, 478), (184, 398), (220, 414), (146, 512)], accent)
        polygon(draw, [(292, 414), (328, 398), (424, 478), (366, 512)], accent)
    elif trait == "quilted-vest":
        for x in range(116, 404, 64):
            for y in range(426, 512, 52):
                polygon(draw, [(x, y + 22), (x + 30, y), (x + 60, y + 22), (x + 30, y + 44)], accent, INK, 2)
    elif trait == "longline-coat":
        polygon(draw, [(194, 388), (246, 430), (208, 512), (94, 512)], accent)
        polygon(draw, [(318, 388), (266, 430), (304, 512), (418, 512)], accent)
    return finish(image)


def paint_coiffure(trait: str) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    hair = "#151b2b"
    shine = "#39415c"
    if trait == "loc-crown":
        polygon(draw, [(158, 194), (170, 130), (218, 100), (294, 100), (344, 136), (354, 204)], hair, INK, 5)
        paths = (
            [(170, 132), (158, 176), (168, 230)],
            [(202, 112), (194, 164), (202, 218)],
            [(234, 102), (228, 152), (234, 202)],
            [(266, 102), (272, 154), (266, 216)],
            [(298, 108), (312, 160), (304, 226)],
            [(330, 132), (348, 178), (338, 240)],
        )
        for index, path in enumerate(paths):
            line(draw, path, hair, 18)
            x, y = path[-1]
            ellipse(draw, (x - 9, y - 9, x + 9, y + 9), hair)
            if index in (1, 4):
                line(draw, [(path[-2][0] - 6, path[-2][1]), (path[-2][0] + 8, path[-2][1])], "#d9a841", 4)
    elif trait == "box-braids":
        polygon(draw, [(164, 196), (176, 132), (220, 100), (296, 100), (340, 132), (350, 198)], hair, INK, 5)
        line(draw, [(256, 100), (256, 176)], "#59617a", 3)
        for offset in (0, 2):
            line(draw, [(194 + offset * 30, 112), (180 + offset * 24, 174)], shine, 3)
            line(draw, [(318 - offset * 30, 112), (332 - offset * 24, 174)], shine, 3)
        braid_paths = (
            [(166, 156), (146, 214), (150, 292), (134, 356)],
            [(194, 142), (176, 218), (184, 300), (170, 376)],
            [(318, 142), (338, 218), (330, 300), (344, 376)],
            [(346, 156), (366, 214), (362, 292), (378, 356)],
        )
        for path in braid_paths:
            line(draw, path, hair, 13)
            for x, y in path[1::2]:
                ellipse(draw, (x - 7, y - 7, x + 7, y + 7), hair)
    elif trait == "high-puff":
        rounded(draw, (176, 166, 338, 206), 20, hair)
        ellipse(draw, (182, 64, 334, 204), hair, INK, 5)
        for x, y, size in ((178, 96, 58), (216, 62, 68), (270, 62, 68), (306, 102, 54), (220, 120, 62), (278, 118, 60)):
            ellipse(draw, (x, y, x + size, y + size), hair)
        line(draw, [(180, 180), (334, 180)], "#b78c48", 6)
    elif trait == "sculpted-twists":
        polygon(draw, [(162, 198), (176, 138), (216, 108), (300, 108), (340, 142), (350, 202)], hair, INK, 5)
        twists = (
            [(180, 146), (166, 118), (186, 84)],
            [(214, 126), (204, 92), (222, 62)],
            [(250, 116), (242, 80), (258, 50)],
            [(286, 120), (298, 84), (286, 54)],
            [(320, 140), (340, 114), (326, 82)],
        )
        for path in twists:
            line(draw, path, hair, 16)
            x, y = path[-1]
            ellipse(draw, (x - 8, y - 8, x + 8, y + 8), hair)
    elif trait == "wave-crop":
        polygon(draw, [(158, 194), (170, 126), (218, 96), (302, 100), (346, 134), (352, 200), (304, 176), (216, 180)], hair, INK, 6)
        draw.arc(box((188, 146, 324, 198)), 194, 342, fill=shine, width=width(3))
    elif trait == "temple-fade":
        polygon(draw, [(160, 206), (174, 132), (224, 106), (312, 110), (350, 154), (348, 210), (318, 172), (202, 174)], hair, INK, 6)
        line(draw, [(316, 124), (278, 174)], "#f1b75c", 5)
    elif trait == "buzz-design":
        polygon(draw, [(168, 202), (180, 138), (220, 110), (304, 112), (342, 146), (348, 202), (306, 174), (210, 176)], "#343a4e", INK, 6)
        line(draw, [(214, 146), (256, 170), (300, 132)], "#d9dcbd", 4)
    elif trait == "bandana-curls":
        for x, y in ((154, 134), (188, 104), (230, 92), (274, 94), (316, 116), (340, 154)):
            ellipse(draw, (x, y, x + 54, y + 58), hair, INK, 3)
        polygon(draw, [(148, 174), (358, 154), (348, 212), (158, 222)], "#e75452", INK, 5)
        for x in (202, 294):
            ellipse(draw, (x, 176, x + 8, 184), PAPER)
    elif trait == "beanie-coils":
        for x in range(166, 342, 34):
            ellipse(draw, (x, 174, x + 42, 226), hair, INK, 3)
        polygon(draw, [(156, 182), (174, 104), (218, 70), (306, 74), (344, 112), (356, 190)], "#d36c43", INK, 6)
        rounded(draw, (150, 166, 360, 214), 16, "#ef9c4b", INK, 5)
    elif trait == "durag-tails":
        polygon(draw, [(154, 194), (174, 124), (226, 92), (310, 98), (350, 142), (356, 208)], "#4453a5", INK, 6)
        line(draw, [(168, 186), (344, 176)], "#8da0f0", 6)
        polygon(draw, [(340, 176), (400, 272), (360, 346), (330, 206)], "#4453a5", INK, 5)
        polygon(draw, [(330, 186), (350, 330), (306, 358), (306, 204)], "#6876c4", INK, 5)
    return finish(image)


def eye_pair(draw: ImageDraw.ImageDraw, pupils: tuple[int, int] = (0, 0), closed: bool = False) -> None:
    if closed:
        draw.arc(box((176, 238, 240, 272)), 14, 166, fill=INK, width=width(5))
        draw.arc(box((272, 238, 336, 272)), 14, 166, fill=INK, width=width(5))
        return
    for center, offset in ((208, pupils[0]), (304, pupils[1])):
        ellipse(draw, (center - 32, 236, center + 32, 278), PAPER, INK, 4)
        ellipse(draw, (center - 7 + offset, 247, center + 7 + offset, 270), INK)


def paint_visage(trait: str) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    if trait == "steady":
        eye_pair(draw)
        line(draw, [(178, 222), (232, 216)], INK, 6)
        line(draw, [(280, 216), (334, 222)], INK, 6)
    elif trait == "side-eye":
        eye_pair(draw, (11, 11))
        line(draw, [(178, 216), (232, 222)], INK, 6)
        line(draw, [(280, 214), (334, 224)], INK, 6)
    elif trait == "soft-blink":
        eye_pair(draw, closed=True)
    elif trait == "joy-lines":
        draw.arc(box((174, 234, 242, 282)), 194, 346, fill=INK, width=width(6))
        draw.arc(box((270, 234, 338, 282)), 194, 346, fill=INK, width=width(6))
    elif trait == "amber-shades":
        rounded(draw, (170, 232, 244, 278), 10, "#f0a83a", INK, 5)
        rounded(draw, (268, 232, 342, 278), 10, "#f0a83a", INK, 5)
        line(draw, [(244, 244), (268, 244)], INK, 6)
        line(draw, [(180, 238), (228, 270)], "#ffe094", 3)
    elif trait == "clear-frames":
        eye_pair(draw)
        rounded(draw, (168, 230, 246, 280), 15, "#d8f3f080", "#376d7c", 5)
        rounded(draw, (266, 230, 344, 280), 15, "#d8f3f080", "#376d7c", 5)
        line(draw, [(246, 244), (266, 244)], "#376d7c", 5)
    elif trait == "future-visor":
        polygon(draw, [(160, 230), (352, 224), (338, 280), (174, 286)], "#71d7dfcc", INK, 5)
        line(draw, [(178, 248), (330, 242)], "#f05c83", 5)
    elif trait == "star-liner":
        eye_pair(draw)
        polygon(draw, [(348, 238), (354, 252), (370, 254), (358, 264), (362, 280), (348, 272), (334, 282), (338, 264), (326, 254), (342, 252)], "#f3c945", INK, 2)
        line(draw, [(176, 236), (236, 246)], "#5140a2", 6)
    return finish(image)


def paint_cadence(trait: str) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    if trait == "calm":
        line(draw, [(228, 346), (284, 346)], INK, 5)
    elif trait == "half-smile":
        draw.arc(box((220, 326, 298, 374)), 12, 160, fill=INK, width=width(6))
    elif trait == "gap-grin":
        rounded(draw, (220, 330, 294, 370), 15, PAPER, INK, 4)
        line(draw, [(256, 334), (256, 350)], INK, 4)
        polygon(draw, [(230, 358), (284, 358), (272, 370), (242, 370)], "#d16f78")
    elif trait == "berry-gloss":
        polygon(draw, [(218, 348), (240, 332), (256, 342), (274, 332), (298, 348), (274, 366), (240, 366)], "#8e3158", INK, 4)
        line(draw, [(236, 350), (278, 350)], "#f3a1b7", 3)
    elif trait == "silver-tooth":
        rounded(draw, (222, 332, 292, 370), 14, PAPER, INK, 4)
        polygon(draw, [(250, 334), (268, 334), (268, 350), (250, 350)], "#a9c5cf", INK, 2)
    elif trait == "fine-mustache":
        polygon(draw, [(218, 338), (252, 330), (256, 342), (260, 330), (294, 338), (264, 350), (256, 344), (248, 350)], INK)
        line(draw, [(226, 362), (286, 362)], INK, 4)
    elif trait == "short-beard":
        polygon(draw, [(198, 334), (216, 390), (256, 416), (298, 390), (316, 334), (292, 374), (256, 392), (220, 374)], "#272a35")
        line(draw, [(224, 350), (288, 350)], PAPER, 4)
    elif trait == "chin-stripe":
        line(draw, [(220, 348), (292, 348)], INK, 5)
        polygon(draw, [(244, 370), (268, 370), (264, 410), (250, 410)], "#272a35")
    return finish(image)


def paint_adornment(trait: str) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    gold = "#f3bd42"
    silver = "#c6d5dc"
    if trait == "gold-hoops":
        for coords in ((126, 270, 170, 334), (342, 270, 386, 334)):
            draw.arc(box(coords), 20, 340, fill=gold, width=width(7))
    elif trait == "silver-studs":
        ellipse(draw, (138, 282, 160, 304), silver, INK, 3)
        ellipse(draw, (352, 282, 374, 304), silver, INK, 3)
    elif trait == "curb-chain":
        for x in range(182, 330, 30):
            draw.arc(box((x, 402 + abs(256 - x) // 8, x + 38, 440 + abs(256 - x) // 8)), 0, 360, fill=gold, width=width(6))
    elif trait == "pearl-line":
        for x in range(184, 338, 28):
            y = 406 + abs(256 - x) // 7
            ellipse(draw, (x, y, x + 19, y + 19), PAPER, INK, 2)
    elif trait == "nose-ring":
        draw.arc(box((260, 288, 292, 330)), 300, 110, fill=gold, width=width(6))
    elif trait == "ear-cuff":
        for y in (264, 282, 300):
            draw.arc(box((346, y, 382, y + 32)), 80, 282, fill=silver, width=width(5))
    elif trait == "studio-cans":
        draw.arc(box((116, 174, 396, 342)), 184, 356, fill=INK, width=width(12))
        rounded(draw, (114, 240, 164, 334), 18, "#ef6b4c", INK, 5)
        rounded(draw, (348, 240, 398, 334), 18, "#ef6b4c", INK, 5)
    elif trait == "safety-pin":
        draw.arc(box((342, 276, 390, 352)), 20, 340, fill=silver, width=width(5))
        line(draw, [(354, 286), (382, 340)], silver, 4)
        ellipse(draw, (344, 278, 360, 294), "#e45757")
    return finish(image)


def paint_signal(trait: str) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    cyan = "#62d7d2"
    coral = "#f15f6d"
    yellow = "#f2cf45"
    if trait == "crop-code":
        for x, y, sx, sy in ((28, 28, 1, 1), (484, 28, -1, 1), (28, 484, 1, -1), (484, 484, -1, -1)):
            line(draw, [(x, y), (x + sx * 38, y)], PAPER, 5)
            line(draw, [(x, y), (x, y + sy * 38)], PAPER, 5)
        for index in range(7):
            draw.rectangle(box((38 + index * 11, 462, 43 + index * 11, 478)), fill=yellow if index % 2 else coral)
    elif trait == "offset-halo":
        draw.arc(box((114, 76, 402, 410)), 190, 354, fill=yellow, width=width(10))
        draw.arc(box((132, 92, 420, 426)), 8, 174, fill=coral, width=width(5))
    elif trait == "halftone-veil":
        for y in range(124, 420, 24):
            for x in range(96, 430, 24):
                if x + y > 370 and x - y < 170:
                    radius = 2 + ((x + y) // 48) % 3
                    ellipse(draw, (x - radius, y - radius, x + radius, y + radius), "#f4efe599")
    elif trait == "type-bars":
        for y, w, color in ((92, 106, yellow), (118, 66, coral), (424, 94, PAPER)):
            rounded(draw, (28, y, 28 + w, y + 14), 7, color)
    elif trait == "orbit-lines":
        draw.arc(box((72, 142, 446, 392)), 196, 342, fill=cyan, width=width(3))
        draw.arc(box((64, 118, 438, 368)), 16, 166, fill=coral, width=width(3))
        ellipse(draw, (398, 174, 420, 196), yellow)
    elif trait == "prism-slice":
        polygon(draw, [(18, 356), (486, 190), (486, 238), (18, 404)], "#64d8d044")
        line(draw, [(18, 356), (486, 190)], cyan, 3)
        line(draw, [(18, 404), (486, 238)], coral, 3)
    elif trait == "sound-wave":
        values = (20, 44, 28, 70, 32, 52, 20)
        for index, h in enumerate(values):
            x = 38 + index * 18
            rounded(draw, (x, 256 - h // 2, x + 8, 256 + h // 2), 4, yellow)
    elif trait == "pixel-flare":
        for x, y, size, color in ((384, 74, 28, yellow), (420, 112, 15, coral), (370, 124, 11, cyan), (446, 84, 7, PAPER)):
            draw.rectangle(box((x, y, x + size, y + size)), fill=color)
    elif trait == "double-exposure":
        polygon(draw, [(74, 90), (190, 90), (142, 454), (24, 454)], "#f15f6d38")
        polygon(draw, [(360, 44), (470, 44), (430, 428), (322, 428)], "#62d7d238")
        line(draw, [(78, 90), (28, 454)], coral, 3)
        line(draw, [(466, 44), (426, 428)], cyan, 3)
    elif trait == "corner-stamps":
        rounded(draw, (22, 24, 108, 64), 6, "#f4efe5dd", INK, 3)
        rounded(draw, (396, 446, 490, 486), 6, "#f2cf45dd", INK, 3)
        for x in range(38, 94, 18):
            line(draw, [(x, 34), (x, 54)], coral, 3)
        for x in range(414, 476, 20):
            ellipse(draw, (x, 458, x + 7, 465), INK)
    return finish(image)


PAINTERS: dict[str, Callable[[str], Image.Image]] = {
    "atmosphere": paint_atmosphere,
    "complexion": paint_complexion,
    "tailoring": paint_tailoring,
    "coiffure": paint_coiffure,
    "visage": paint_visage,
    "cadence": paint_cadence,
    "adornment": paint_adornment,
    "signal": paint_signal,
}


def trait_path(category: str, trait: str) -> Path:
    return TRAIT_ROOT / category / f"{trait}.png"


def combo_from_signature(signature: tuple[str, ...]) -> dict[str, str]:
    return dict(zip(TRAIT_ORDER, signature, strict=True))


def compatible(combo: dict[str, str]) -> bool:
    selected = set(combo.items())
    return all(not ({left, right} <= selected) for left, right in INCOMPATIBLE)


def compose(combo: dict[str, str]) -> Image.Image:
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for category in STACK:
        with Image.open(trait_path(category, combo[category])) as plate:
            canvas.alpha_composite(plate.convert("RGBA"))
    return canvas


def write_manifest() -> None:
    manifest = {
        "collection": {
            "name": NAME,
            "symbol": SYMBOL,
            "slug": SLUG,
            "subject": SUBJECT,
            "chain": CHAIN,
            "planned_supply": SUPPLY,
            "mint_price": MINT_PRICE,
            "art_version": ART_VERSION,
            "seed": SEED,
            "format": "static PNG",
            "size": [SIZE, SIZE],
        },
        "stack": list(STACK),
        "traits": {
            category: [
                {"id": trait_id, "name": name, "weight": weight_value}
                for trait_id, name, weight_value in traits
            ]
            for category, traits in TRAIT_SPEC.items()
        },
        "incompatible": [
            [{"category": left[0], "trait": left[1]}, {"category": right[0], "trait": right[1]}]
            for left, right in INCOMPATIBLE
        ],
        "signatures": [
            {"id": index, "traits": combo_from_signature(signature)}
            for index, signature in enumerate(SIGNATURES, start=1)
        ],
    }
    path = TRAIT_ROOT / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_trait_catalog() -> None:
    payload = json.dumps(
        {
            category: [
                {"id": trait_id, "name": name, "weight": weight_value}
                for trait_id, name, weight_value in traits
            ]
            for category, traits in TRAIT_SPEC.items()
        },
        indent=2,
    )
    source = (
        "// Generated by scripts/build_street_heirs.py. Do not edit by hand.\n\n"
        f"export const streetHeirsStack = {json.dumps(STACK)} as const;\n\n"
        f"export const streetHeirsTraits = {payload} as const;\n\n"
        f"export const streetHeirsPlannedSupply = {SUPPLY};\n"
        f"export const streetHeirsChain = {json.dumps(CHAIN)};\n"
        f"export const streetHeirsMintPrice = {json.dumps(MINT_PRICE)};\n"
    )
    path = DATA_ROOT / f"{SLUG}-traits.ts"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")


def write_metadata() -> None:
    METADATA_ROOT.mkdir(parents=True, exist_ok=True)
    description = (
        "Street Heirs is a static editorial-vector PFP collection celebrating personal style, "
        "neighborhood craft, and the graphic language of the city. Authentic hair, tailoring, "
        "jewelry, and expression meet geometric broadcast signals in 5,555 planned portraits "
        "on Robinhood Chain."
    )
    metadata = {
        "name": NAME,
        "symbol": SYMBOL,
        "description": description,
        "chain": CHAIN,
        "supply": SUPPLY,
        "mint_price": MINT_PRICE,
        "image": f"/{SLUG}-preview/1.png",
        "art_version": ART_VERSION,
        "status": "prototype",
    }
    (METADATA_ROOT / f"{SLUG}.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (METADATA_ROOT / f"{SLUG}-description.txt").write_text(description + "\n", encoding="utf-8")


def render_previews() -> list[str]:
    PREVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    hashes: list[str] = []
    previews: list[Image.Image] = []
    for index, signature in enumerate(SIGNATURES, start=1):
        combo = combo_from_signature(signature)
        if not compatible(combo):
            raise ValueError(f"Signature {index} violates compatibility rules")
        portrait = compose(combo)
        digest = hashlib.sha256(portrait.tobytes()).hexdigest()
        if digest in hashes:
            raise ValueError(f"Signature {index} duplicates a prior rendered portrait")
        hashes.append(digest)
        previews.append(portrait)
        save_image(portrait, PREVIEW_ROOT / f"{index}.png", optimize=True)

    sheet = Image.new("RGB", (SIZE * 4, SIZE * 4), PAPER)
    for index, portrait in enumerate(previews):
        sheet.paste(portrait.convert("RGB"), ((index % 4) * SIZE, (index // 4) * SIZE))
    save_image(sheet, PREVIEW_ROOT / "contact-sheet.jpg", quality=92, optimize=True)
    return hashes


def validate_catalog() -> None:
    if len(SIGNATURES) != 16:
        raise ValueError("The prototype must have exactly 16 signatures")
    valid_by_category = {
        category: {trait_id for trait_id, _, _ in traits}
        for category, traits in TRAIT_SPEC.items()
    }
    seen: set[tuple[str, ...]] = set()
    for index, signature in enumerate(SIGNATURES, start=1):
        if len(signature) != len(TRAIT_ORDER):
            raise ValueError(f"Signature {index} has the wrong number of traits")
        if signature in seen:
            raise ValueError(f"Signature {index} is duplicated")
        seen.add(signature)
        for category, trait in zip(TRAIT_ORDER, signature, strict=True):
            if trait not in valid_by_category[category]:
                raise ValueError(f"Unknown trait {category}/{trait} in signature {index}")
        if not compatible(combo_from_signature(signature)):
            raise ValueError(f"Signature {index} is incompatible")


def paint_traits() -> None:
    for category in STACK:
        painter = PAINTERS[category]
        for trait_id, _, _ in TRAIT_SPEC[category]:
            image = painter(trait_id)
            if image.size != (SIZE, SIZE) or image.mode != "RGBA":
                raise ValueError(f"Invalid plate format for {category}/{trait_id}")
            alpha = image.getchannel("A")
            if alpha.getbbox() is None:
                raise ValueError(f"Empty plate for {category}/{trait_id}")
            save_image(image, trait_path(category, trait_id), optimize=True)


def main() -> None:
    validate_catalog()
    paint_traits()
    write_manifest()
    write_trait_catalog()
    write_metadata()
    hashes = render_previews()
    print(
        f"Built {NAME} {ART_VERSION}: "
        f"{sum(len(traits) for traits in TRAIT_SPEC.values())} plates, "
        f"{len(hashes)} unique signatures."
    )


if __name__ == "__main__":
    main()
