#!/usr/bin/env python3
"""Paint the Robin Banx static trait kit from a blank drawing language.

The collection uses sharp dossier collage geometry: torn files, masked human
figures, halftone shadow, evidence ink, and multichain contraband.  Only the
style-neutral size and image writer come from paint_kit.
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from paint_kit import SIZE, save_image  # noqa: E402

NAME = "Robin Banx"
SYMBOL = "RBX"
SLUG = "robinbanx"
TOKEN = "Robin Banx"
CHAIN = "Base"
CHAIN_ID = 8453
SUPPLY = 10_000
MINT = "Free"
ART_VERSION = "robinbanx-v1"
TRAIT_DIR = ROOT / "public" / f"{SLUG}-traits"
PREVIEW_DIR = ROOT / "public" / f"{SLUG}-preview"
BRAND_DIR = ROOT / "public" / "brand"
METADATA_DIR = ROOT / "public" / "metadata"
DATA_DIR = ROOT / "src" / "data"

INK = "#111216"
PAPER = "#ded7c6"
BONE = "#eee8d9"
SMOKE = "#282a30"
CRIMSON = "#bc2734"
ACID = "#d7ed52"
CYAN = "#58c8d1"
COBALT = "#3659a8"
AMBER = "#e3a53a"

STACK = (
    "safehouse",
    "chain_trail",
    "alias",
    "getup",
    "disguise",
    "headpiece",
    "instrument",
    "evidence_mark",
)

TRAIT_LABELS = (
    ("safehouse", "Safehouse"),
    ("alias", "Alias"),
    ("getup", "Getup"),
    ("disguise", "Disguise"),
    ("headpiece", "Headpiece"),
    ("instrument", "Instrument"),
    ("chain_trail", "Chain Trail"),
    ("evidence_mark", "Evidence Mark"),
)

# id, display name, weight. Eight categories × ten files = 80 PNG traits.
TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "safehouse": [
        ("ledger-room", "Ledger Room", 18), ("night-vault", "Night Vault", 16),
        ("rail-archive", "Rail Archive", 14), ("concrete-cellar", "Concrete Cellar", 13),
        ("redacted-office", "Redacted Office", 12), ("signal-attic", "Signal Attic", 10),
        ("canal-depot", "Canal Depot", 8), ("embassy-basement", "Embassy Basement", 5),
        ("offshore-bunker", "Offshore Bunker", 3), ("black-site", "Black Site", 1),
    ],
    "alias": [
        ("rook", "Rook", 16), ("vesper", "Vesper", 15), ("cutlass", "Cutlass", 14),
        ("cipher", "Cipher", 13), ("morrow", "Morrow", 12), ("switch", "Switch", 10),
        ("locke", "Locke", 8), ("parallax", "Parallax", 6), ("zero-day", "Zero Day", 4),
        ("ghost-key", "Ghost Key", 2),
    ],
    "getup": [
        ("pinstripe-rig", "Pinstripe Rig", 17), ("courier-coat", "Courier Coat", 16),
        ("night-vest", "Night Vest", 14), ("heist-knit", "Heist Knit", 13),
        ("archive-suit", "Archive Suit", 12), ("armored-shirt", "Armored Shirt", 10),
        ("signal-parka", "Signal Parka", 8), ("embassy-tux", "Embassy Tux", 5),
        ("hazmat-tailoring", "Hazmat Tailoring", 3), ("carbon-mail", "Carbon Mail", 2),
    ],
    "disguise": [
        ("none", "Unmasked", 24), ("bandit-cloth", "Bandit Cloth", 18),
        ("ledger-blind", "Ledger Blind", 14), ("mirror-specs", "Mirror Specs", 13),
        ("half-respirator", "Half Respirator", 10), ("paper-visage", "Paper Visage", 8),
        ("cipher-goggles", "Cipher Goggles", 6), ("full-respirator", "Full Respirator", 4),
        ("holo-scrambler", "Holo Scrambler", 2), ("blank-plate", "Blank Plate", 1),
    ],
    "headpiece": [
        ("none", "Bareheaded", 30), ("watch-cap", "Watch Cap", 18),
        ("creased-fedora", "Creased Fedora", 14), ("courier-hood", "Courier Hood", 12),
        ("radio-phones", "Radio Phones", 10), ("night-beret", "Night Beret", 7),
        ("breach-helmet", "Breach Helmet", 4), ("crown-of-keys", "Crown of Keys", 2),
        ("validator-halo", "Validator Halo", 2), ("burner-aureole", "Burner Aureole", 1),
    ],
    "instrument": [
        ("none", "Empty Hands", 22), ("bolt-cutters", "Bolt Cutters", 17),
        ("burner-phone", "Burner Phone", 15), ("cold-wallet", "Cold Wallet", 13),
        ("glass-key", "Glass Key", 10), ("signal-jammer", "Signal Jammer", 8),
        ("bridge-case", "Bridge Case", 6), ("validator-drill", "Validator Drill", 4),
        ("genesis-charge", "Genesis Charge", 3), ("sequencer-override", "Sequencer Override", 2),
    ],
    "chain_trail": [
        ("none", "No Trail", 28), ("base-blueprint", "Base Blueprint", 18),
        ("ethereum-rubric", "Ethereum Rubric", 14), ("bitcoin-ransom", "Bitcoin Ransom", 12),
        ("solana-transit", "Solana Transit", 9), ("arbitrum-route", "Arbitrum Route", 7),
        ("optimism-signal", "Optimism Signal", 5), ("polygon-grid", "Polygon Grid", 4),
        ("zora-negative", "Zora Negative", 2), ("multichain-crossing", "Multichain Crossing", 1),
    ],
    "evidence_mark": [
        ("none", "Clean File", 26), ("case-open", "Case Open", 18),
        ("seized", "Seized", 14), ("classified", "Classified", 12),
        ("redacted", "Redacted", 10), ("base-8453", "Base 8453", 8),
        ("wanted", "Wanted", 6), ("chain-of-custody", "Chain of Custody", 3),
        ("inside-job", "Inside Job", 2), ("case-000", "Case 000", 1),
    ],
}

# Explicitly exported so the generator and UI can apply the same constraints.
INCOMPATIBLE = (
    (("disguise", "full-respirator"), ("headpiece", "courier-hood")),
    (("disguise", "blank-plate"), ("headpiece", "radio-phones")),
    (("disguise", "holo-scrambler"), ("headpiece", "breach-helmet")),
    (("getup", "hazmat-tailoring"), ("disguise", "bandit-cloth")),
    (("getup", "carbon-mail"), ("instrument", "bolt-cutters")),
    (("headpiece", "crown-of-keys"), ("instrument", "validator-drill")),
    (("chain_trail", "bitcoin-ransom"), ("instrument", "sequencer-override")),
)

SIGNATURES = [
    dict(zip(STACK, values))
    for values in [
        ("ledger-room", "base-blueprint", "rook", "pinstripe-rig", "bandit-cloth", "creased-fedora", "bolt-cutters", "case-open"),
        ("night-vault", "ethereum-rubric", "vesper", "courier-coat", "mirror-specs", "watch-cap", "burner-phone", "seized"),
        ("rail-archive", "bitcoin-ransom", "cutlass", "night-vest", "ledger-blind", "night-beret", "cold-wallet", "classified"),
        ("concrete-cellar", "solana-transit", "cipher", "heist-knit", "half-respirator", "radio-phones", "glass-key", "redacted"),
        ("redacted-office", "arbitrum-route", "morrow", "archive-suit", "paper-visage", "courier-hood", "signal-jammer", "base-8453"),
        ("signal-attic", "optimism-signal", "switch", "armored-shirt", "cipher-goggles", "watch-cap", "bridge-case", "wanted"),
        ("canal-depot", "polygon-grid", "locke", "signal-parka", "none", "breach-helmet", "validator-drill", "chain-of-custody"),
        ("embassy-basement", "zora-negative", "parallax", "embassy-tux", "full-respirator", "night-beret", "genesis-charge", "inside-job"),
        ("offshore-bunker", "multichain-crossing", "zero-day", "hazmat-tailoring", "blank-plate", "validator-halo", "sequencer-override", "case-000"),
        ("black-site", "base-blueprint", "ghost-key", "carbon-mail", "holo-scrambler", "burner-aureole", "cold-wallet", "classified"),
        ("ledger-room", "none", "cipher", "courier-coat", "none", "none", "burner-phone", "case-open"),
        ("night-vault", "optimism-signal", "rook", "archive-suit", "mirror-specs", "crown-of-keys", "glass-key", "base-8453"),
        ("rail-archive", "polygon-grid", "morrow", "armored-shirt", "bandit-cloth", "radio-phones", "signal-jammer", "wanted"),
        ("concrete-cellar", "ethereum-rubric", "locke", "embassy-tux", "paper-visage", "creased-fedora", "bridge-case", "seized"),
        ("signal-attic", "solana-transit", "vesper", "night-vest", "ledger-blind", "validator-halo", "genesis-charge", "redacted"),
        ("canal-depot", "arbitrum-route", "cutlass", "heist-knit", "cipher-goggles", "courier-hood", "sequencer-override", "chain-of-custody"),
    ]
]

COLLECTION_STORY = (
    "Robin Banx is a 10,000-piece noir security dossier assembled on Base. "
    "Angular masked operators move through torn case files, halftone shadow, "
    "evidence ink, and multichain contraband. Every RBX is a deterministic "
    "eight-layer static collage. The mint is free; the file is never closed."
)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def canvas() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def jittered_polygon(points: list[tuple[int, int]], seed: str, spread: int = 4) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    return [(x + rng.randint(-spread, spread), y + rng.randint(-spread, spread)) for x, y in points]


def halftone(im: Image.Image, box: tuple[int, int, int, int], color: str, step: int, seed: str) -> None:
    draw = ImageDraw.Draw(im)
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            if (x // step + y // step) % 2 == 0 and rng.random() > .16:
                r = max(1, step // 5)
                draw.ellipse((x-r, y-r, x+r, y+r), fill=color)


def torn_sheet(draw: ImageDraw.ImageDraw, inset: int, fill: str, seed: str) -> None:
    rng = random.Random(seed)
    points = []
    for x in range(inset, SIZE - inset + 1, 28):
        points.append((x, inset + rng.randint(-8, 8)))
    for y in range(inset + 28, SIZE - inset + 1, 28):
        points.append((SIZE - inset + rng.randint(-8, 8), y))
    for x in range(SIZE - inset - 28, inset - 1, -28):
        points.append((x, SIZE - inset + rng.randint(-8, 8)))
    for y in range(SIZE - inset - 28, inset, -28):
        points.append((inset + rng.randint(-8, 8), y))
    draw.polygon(points, fill=fill)


def paint_safehouse(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    palettes = [
        (INK, PAPER, CRIMSON), (SMOKE, BONE, COBALT), ("#15171b", "#c9c1ad", AMBER),
        ("#1d1b20", "#d4cfbf", CYAN), ("#18191e", "#c6bdad", CRIMSON),
    ]
    dark, paper, accent = palettes[index % len(palettes)]
    d.rectangle((0, 0, SIZE, SIZE), fill=dark)
    torn_sheet(d, 22 + index % 3 * 5, paper, trait_id)
    d.polygon(jittered_polygon([(52, 70), (460, 45), (442, 451), (66, 466)], trait_id, 6), fill=dark)
    d.line((72, 126, 438, 102), fill=accent, width=4)
    d.line((80, 408, 430, 432), fill=accent, width=3)
    for y in range(144, 390, 42):
        d.line((65, y, 448, y - 18), fill=(230, 225, 211, 26), width=2)
    halftone(im, (48, 52, 470, 470), (*ImageColor_getrgb(accent), 95), 13 + index % 3, trait_id)
    d.text((65, 82), f"FILE / {index+1:02d}", font=font(19), fill=paper)
    d.text((330, 416), "RBX", font=font(28), fill=accent)
    return im


def ImageColor_getrgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


def paint_alias(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    skin = ["#8f604c", "#bb8060", "#68483f", "#d1a078", "#78513f"][index % 5]
    shadow = ["#322b31", "#29313a", "#332825"][index % 3]
    # Broad angular human shoulders and a faceted head; intentionally no ovals.
    d.polygon(jittered_polygon([(112, 474), (142, 340), (206, 304), (308, 302), (379, 346), (410, 474)], trait_id), fill=shadow)
    d.polygon([(196, 307), (184, 191), (221, 127), (309, 140), (337, 213), (312, 304), (257, 332)], fill=skin)
    d.polygon([(184, 191), (221, 127), (256, 119), (244, 208), (202, 254)], fill="#211f24")
    d.polygon([(244, 208), (337, 213), (312, 304), (257, 332)], fill="#16171b")
    d.line((221, 127, 309, 140, 337, 213, 312, 304, 257, 332, 196, 307, 184, 191, 221, 127), fill=BONE, width=5)
    d.polygon([(206, 248), (244, 236), (253, 258), (214, 265)], fill=INK)
    d.polygon([(274, 239), (315, 247), (307, 266), (268, 257)], fill=INK)
    d.line((252, 282, 294, 286), fill=CRIMSON, width=5)
    d.text((184, 354), trait_id.replace("-", " ").upper(), font=font(16), fill=(235, 229, 214, 140))
    return im


def paint_getup(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    colors = [COBALT, "#31343b", "#6e2831", "#625e52", "#1c4a4b", "#463b59", "#263c31", "#24262c", "#b4aa83", "#202b35"]
    c = colors[index]
    d.polygon([(110, 477), (142, 342), (205, 307), (257, 336), (309, 307), (380, 344), (411, 477)], fill=c)
    d.polygon([(205, 307), (257, 336), (224, 476), (159, 476)], fill="#18191d")
    d.polygon([(309, 307), (257, 336), (286, 476), (354, 476)], fill="#25262b")
    d.line((257, 337, 257, 476), fill=BONE, width=4)
    if index % 3 == 0:
        for y in range(356, 470, 20):
            d.line((151, y, 221, y+8), fill=(224, 214, 190, 80), width=2)
            d.line((292, y+8, 368, y), fill=(224, 214, 190, 80), width=2)
    if index in (2, 5, 6, 8, 9):
        d.polygon([(137, 350), (190, 318), (220, 475), (164, 475)], outline=CRIMSON, width=5)
    d.rectangle((231, 404, 283, 424), fill=INK, outline=AMBER, width=3)
    return im


def paint_disguise(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    if trait_id == "none":
        return im
    d = ImageDraw.Draw(im)
    if trait_id in ("mirror-specs", "ledger-blind", "cipher-goggles"):
        color = CYAN if index % 2 else CRIMSON
        d.polygon([(191, 220), (250, 210), (251, 249), (202, 262)], fill=INK, outline=color, width=5)
        d.polygon([(262, 210), (329, 222), (316, 262), (263, 249)], fill=INK, outline=color, width=5)
        d.line((250, 224, 264, 224), fill=color, width=5)
        if trait_id == "ledger-blind":
            d.rectangle((192, 207, 329, 255), fill=(20, 20, 24, 225))
            for x in range(200, 326, 12):
                d.line((x, 211, x-13, 252), fill=(220, 214, 194, 90), width=2)
    elif trait_id in ("bandit-cloth", "paper-visage"):
        fill = "#292a2e" if trait_id == "bandit-cloth" else PAPER
        d.polygon([(187, 250), (249, 229), (328, 249), (312, 307), (257, 327), (198, 304)], fill=fill, outline=CRIMSON, width=4)
        d.line((219, 270, 298, 270), fill=INK, width=5)
    else:
        fill = {"half-respirator": "#343941", "full-respirator": "#23282e", "holo-scrambler": COBALT, "blank-plate": BONE}[trait_id]
        top = 226 if trait_id == "half-respirator" else 183
        d.polygon([(196, top), (255, 203), (324, top), (317, 304), (258, 331), (199, 303)], fill=fill, outline=INK, width=5)
        d.polygon([(222, 252), (253, 239), (288, 253), (277, 294), (241, 296)], fill=INK)
        for x in (231, 252, 273):
            d.line((x, 260, x-2, 286), fill=CYAN, width=3)
    return im


def paint_headpiece(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    if trait_id == "none":
        return im
    d = ImageDraw.Draw(im)
    if trait_id in ("validator-halo", "burner-aureole"):
        color = CYAN if trait_id == "validator-halo" else CRIMSON
        d.arc((164, 76, 350, 238), 192, 347, fill=color, width=12)
        d.line((184, 139, 326, 107), fill=BONE, width=3)
    elif trait_id == "crown-of-keys":
        d.polygon([(185, 170), (196, 91), (237, 146), (270, 70), (295, 145), (337, 92), (326, 178)], fill=AMBER, outline=INK, width=5)
    elif trait_id in ("radio-phones",):
        d.arc((174, 101, 340, 250), 190, 350, fill=INK, width=16)
        d.rectangle((173, 180, 204, 245), fill=COBALT, outline=BONE, width=4)
        d.rectangle((315, 180, 344, 245), fill=COBALT, outline=BONE, width=4)
    elif trait_id == "breach-helmet":
        d.polygon([(181, 191), (198, 120), (245, 96), (309, 111), (340, 190)], fill="#343943", outline=BONE, width=5)
        d.rectangle((238, 104, 260, 184), fill=CRIMSON)
    elif trait_id == "courier-hood":
        d.polygon([(170, 212), (190, 123), (256, 91), (326, 126), (347, 218), (316, 182), (255, 144), (201, 185)], fill="#272a31", outline=CRIMSON, width=5)
    else:
        color = "#26282e" if index % 2 else "#542a31"
        if trait_id == "creased-fedora":
            d.polygon([(162, 174), (203, 145), (319, 148), (356, 182), (264, 191)], fill=color, outline=BONE, width=4)
            d.polygon([(205, 147), (220, 101), (300, 106), (319, 148)], fill=color)
        else:
            d.polygon([(187, 178), (201, 120), (292, 105), (329, 173)], fill=color, outline=BONE, width=4)
    return im


def paint_instrument(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    if trait_id == "none":
        return im
    d = ImageDraw.Draw(im)
    color = [CRIMSON, CYAN, AMBER, COBALT][index % 4]
    if trait_id == "bolt-cutters":
        d.line((332, 442, 428, 273), fill=INK, width=18)
        d.line((371, 443, 396, 281), fill=INK, width=18)
        d.polygon([(415, 290), (449, 240), (459, 254), (432, 315)], fill=color)
        d.polygon([(383, 289), (370, 237), (389, 229), (408, 306)], fill=color)
    elif trait_id in ("burner-phone", "cold-wallet", "glass-key"):
        d.polygon([(347, 355), (416, 333), (433, 419), (361, 441)], fill=INK, outline=color, width=6)
        d.rectangle((367, 357, 410, 403), fill="#d8ddc4")
        d.text((377, 365), "8453", font=font(12), fill=INK)
    elif trait_id in ("bridge-case", "genesis-charge"):
        d.polygon([(321, 361), (438, 337), (458, 431), (337, 456)], fill="#202228", outline=color, width=6)
        d.rectangle((365, 345, 405, 369), outline=BONE, width=4)
        d.text((354, 390), "RBX", font=font(22), fill=color)
    else:
        d.polygon([(333, 344), (398, 312), (447, 390), (374, 438)], fill="#282c34", outline=color, width=6)
        d.circle((390, 364), 16, fill=INK, outline=BONE, width=3)
        d.line((361, 355, 414, 410), fill=color, width=5)
        d.text((374, 375), "///", font=font(16), fill=BONE)
    return im


def paint_chain_trail(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    if trait_id == "none":
        return im
    d = ImageDraw.Draw(im)
    colors = [COBALT, "#6978a8", AMBER, "#62c5bb", "#5f7dd5", CRIMSON, "#9b60c5", "#7862aa", "#d9d2be"]
    color = colors[(index - 1) % len(colors)]
    rng = random.Random(trait_id)
    for lane in range(3):
        pts = []
        for x in range(-20, 550, 46):
            y = 95 + lane * 130 + int(math.sin(x / 52 + lane) * 30) + rng.randint(-6, 6)
            pts.append((x, y))
        d.line(pts, fill=(*ImageColor_getrgb(color), 150), width=5)
        for x, y in pts[1::2]:
            d.polygon([(x, y-10), (x+10, y), (x, y+10), (x-10, y)], outline=(*ImageColor_getrgb(color), 180), width=3)
    d.text((54, 448), trait_id.replace("-", " / ").upper(), font=font(15), fill=(*ImageColor_getrgb(color), 165))
    return im


def paint_evidence_mark(trait_id: str, index: int) -> Image.Image:
    im = canvas()
    if trait_id == "none":
        return im
    stamp = Image.new("RGBA", (280, 100), (0, 0, 0, 0))
    d = ImageDraw.Draw(stamp)
    color = CRIMSON if index % 2 else AMBER
    d.rectangle((5, 8, 274, 92), outline=color, width=7)
    label = trait_id.replace("-", " ").upper()
    bbox = d.textbbox((0, 0), label, font=font(27))
    d.text(((280-(bbox[2]-bbox[0]))/2, 32), label, font=font(27), fill=color)
    stamp = stamp.rotate([-12, 8, -5, 14][index % 4], resample=Image.Resampling.BICUBIC, expand=True)
    im.alpha_composite(stamp, (12 + index % 3 * 52, 34 + index % 4 * 90))
    if trait_id == "redacted":
        dd = ImageDraw.Draw(im)
        for y in (110, 151, 387):
            dd.rectangle((58, y, 455, y + 17), fill=(14, 15, 18, 225))
    return im


PAINTERS = {
    "safehouse": paint_safehouse, "alias": paint_alias, "getup": paint_getup,
    "disguise": paint_disguise, "headpiece": paint_headpiece,
    "instrument": paint_instrument, "chain_trail": paint_chain_trail,
    "evidence_mark": paint_evidence_mark,
}


def trait_path(category: str, trait_id: str) -> Path:
    return TRAIT_DIR / category.replace("_", "-") / f"{trait_id}.png"


def name_of(category: str, trait_id: str) -> str:
    return next(name for item_id, name, _weight in TRAIT_SPEC[category] if item_id == trait_id)


def compatible(selection: dict[str, str]) -> bool:
    return not any(selection.get(a) == av and selection.get(b) == bv for (a, av), (b, bv) in INCOMPATIBLE)


def compose(selection: dict[str, str]) -> Image.Image:
    out = canvas()
    for category in STACK:
        with Image.open(trait_path(category, selection[category])) as layer:
            out = Image.alpha_composite(out, layer.convert("RGBA"))
    return out


def write_traits() -> None:
    for category, traits in TRAIT_SPEC.items():
        for index, (trait_id, _name, _weight) in enumerate(traits):
            save_image(PAINTERS[category](trait_id, index), trait_path(category, trait_id), compress_level=7)


def write_manifest() -> None:
    manifest = {
        "name": NAME, "symbol": SYMBOL, "version": ART_VERSION, "size": SIZE,
        "static": True, "chain": CHAIN, "chainId": CHAIN_ID, "supply": SUPPLY,
        "mint": MINT, "stack": list(STACK),
        "traits": {
            category: [
                {"id": trait_id, "name": name, "weight": weight,
                 "image": f"/{SLUG}-traits/{category.replace('_', '-')}/{trait_id}.png"}
                for trait_id, name, weight in traits
            ] for category, traits in TRAIT_SPEC.items()
        },
        "incompatible": [
            {"left": {"category": a, "trait": av}, "right": {"category": b, "trait": bv}}
            for (a, av), (b, bv) in INCOMPATIBLE
        ],
        "signatures": SIGNATURES,
    }
    save_text(TRAIT_DIR / "manifest.json", json.dumps(manifest, indent=2) + "\n")


def write_previews_and_brand() -> None:
    previews = []
    for token_id, selection in enumerate(SIGNATURES, 1):
        art = compose(selection)
        save_image(art, PREVIEW_DIR / f"{token_id}.png", compress_level=7)
        previews.append(art)

    logo = previews[0].copy()
    ld = ImageDraw.Draw(logo)
    ld.polygon([(18, 18), (220, 18), (178, 86), (18, 110)], fill=CRIMSON)
    ld.text((36, 30), "RBX", font=font(43), fill=BONE)
    save_image(logo, BRAND_DIR / f"logo-{SLUG}.png", compress_level=7)

    def montage(width: int, height: int, count: int) -> Image.Image:
        out = Image.new("RGB", (width, height), INK)
        tile = max(height, width // count)
        for i in range(count):
            crop = previews[i].convert("RGB").resize((tile, tile), Image.Resampling.LANCZOS)
            x = int((width - tile) * i / max(count - 1, 1))
            out.paste(crop, (x, (height - tile) // 2))
        d = ImageDraw.Draw(out, "RGBA")
        d.polygon([(0, 0), (width * .42, 0), (width * .28, height), (0, height)], fill=(12, 13, 16, 210))
        d.text((width * .035, height * .25), "ROBIN", font=font(max(36, height // 8)), fill=BONE)
        d.text((width * .035, height * .42), "BANX", font=font(max(52, height // 6)), fill=CRIMSON)
        d.text((width * .04, height * .66), "BASE / 8453 / FREE MINT", font=font(max(18, height // 28)), fill=ACID)
        return out

    save_image(montage(1200, 800, 4), BRAND_DIR / f"featured-{SLUG}.jpg", quality=92)
    save_image(montage(2800, 700, 7), BRAND_DIR / f"banner-{SLUG}-opensea.jpg", quality=92)
    save_image(montage(1500, 560, 5).convert("RGBA"), BRAND_DIR / f"banner-{SLUG}.png", compress_level=7)
    save_image(previews[8], BRAND_DIR / f"collection-{SLUG}.png", compress_level=7)


def save_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_metadata() -> None:
    metadata = {
        "name": NAME, "symbol": SYMBOL, "description": COLLECTION_STORY,
        "image": f"/brand/collection-{SLUG}.png",
        "featured_image": f"/brand/featured-{SLUG}.jpg",
        "banner_image": f"/brand/banner-{SLUG}.png",
        "opensea_banner_image": f"/brand/banner-{SLUG}-opensea.jpg",
        "external_link": f"/{SLUG}", "chain": CHAIN, "chain_id": CHAIN_ID,
        "supply": SUPPLY, "mint_price": MINT, "seller_fee_basis_points": 500,
        "fee_recipient": "0x0000000000000000000000000000000000000000",
    }
    save_text(METADATA_DIR / f"{SLUG}.json", json.dumps(metadata, indent=2) + "\n")
    save_text(METADATA_DIR / f"{SLUG}-description.txt", COLLECTION_STORY + "\n")


def ts_quote(value: str) -> str:
    return json.dumps(value)


def write_ts_catalogs() -> None:
    ids = " | ".join(ts_quote(key) for key in STACK)
    incompatible = [
        {
            "left": {"category": a, "trait": av},
            "right": {"category": b, "trait": bv},
        }
        for (a, av), (b, bv) in INCOMPATIBLE
    ]
    lines = [
        "export type RobinBanxTrait = { id: string; name: string; image: string; rarity: number };",
        f"export type RobinBanxCategoryId = {ids};",
        "export type RobinBanxTraitCategory = { id: RobinBanxCategoryId; label: string; optional: boolean; traits: RobinBanxTrait[] };",
        f'export const ROBINBANX_ART_VERSION = "{ART_VERSION}";',
        "export const robinBanxTraitCategories: RobinBanxTraitCategory[] = [",
    ]
    labels = dict(TRAIT_LABELS)
    for category in STACK:
        lines.append(f"  {{ id: {ts_quote(category)}, label: {ts_quote(labels[category])}, optional: {str(any(t[0] == 'none' for t in TRAIT_SPEC[category])).lower()}, traits: [")
        for trait_id, name, weight in TRAIT_SPEC[category]:
            image = f"/{SLUG}-traits/{category.replace('_', '-')}/{trait_id}.png"
            lines.append(f"    {{ id: {ts_quote(trait_id)}, name: {ts_quote(name)}, image: {ts_quote(image)}, rarity: {weight} }},")
        lines.append("  ] },")
    lines += [
        "];",
        "export type RobinBanxSelection = Record<RobinBanxCategoryId, string>;",
        "export const defaultRobinBanxSelection: RobinBanxSelection = " + json.dumps(SIGNATURES[0]) + ";",
        "export const robinBanxIncompatiblePairs = " + json.dumps(incompatible) + " as const;",
        "export function isRobinBanxSelectionCompatible(selection: RobinBanxSelection) {",
        "  return !robinBanxIncompatiblePairs.some(({ left, right }) =>",
        "    selection[left.category] === left.trait && selection[right.category] === right.trait,",
        "  );",
        "}",
        "export function robinBanxTraitSrc(path: string) { return `${path}?v=${ROBINBANX_ART_VERSION}`; }",
        "export function robinBanxSelectionToLayers(selection: RobinBanxSelection) {",
        "  return robinBanxTraitCategories.map((category) => category.traits.find((trait) => trait.id === selection[category.id]))",
        "    .filter((trait): trait is RobinBanxTrait => Boolean(trait)).map((trait) => robinBanxTraitSrc(trait.image));",
        "}",
        "",
    ]
    save_text(DATA_DIR / f"{SLUG}-traits.ts", "\n".join(lines))

    gallery = [
        "export type RobinBanxSample = { id: number; name: string; image: string; attributes: { trait_type: string; value: string }[] };",
        "export const robinBanxSamples: RobinBanxSample[] = [",
    ]
    labels = dict(TRAIT_LABELS)
    for token_id, selection in enumerate(SIGNATURES, 1):
        attrs = [{"trait_type": labels[key], "value": name_of(key, selection[key])} for key in STACK]
        gallery.append(f"  {{ id: {token_id}, name: {ts_quote(f'{TOKEN} #{token_id}')}, image: {ts_quote(f'/{SLUG}-preview/{token_id}.png?v=1')}, attributes: {json.dumps(attrs)} }},")
    gallery += ["];", ""]
    save_text(DATA_DIR / f"{SLUG}-gallery.ts", "\n".join(gallery))


def main() -> None:
    print(f"Painting {sum(map(len, TRAIT_SPEC.values()))} {NAME} static traits...")
    write_traits()
    write_manifest()
    write_previews_and_brand()
    write_metadata()
    write_ts_catalogs()
    print(f"Wrote trait kit, 16 previews, brand art, metadata, and TypeScript catalogs for {NAME}.")


if __name__ == "__main__":
    main()
