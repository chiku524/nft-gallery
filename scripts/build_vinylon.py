#!/usr/bin/env python3
"""Paint Vinylon — twisted balloon characters in a party booth.

Language: inflated latex tubes, knots, specular shine. Not neon tubing,
not a leather puppet, not a soy-ink blot, not a sticker cutout, not an egg.
The twist stays in one envelope. The bob is the dance.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402
from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

GIF_COLORS = 96
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "vinylon-traits"
PREVIEW_DIR = ROOT / "public" / "vinylon-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

SLUG = "vinylon"
NAME = "Vinylon"
SYMBOL = "VNYL"
TOKEN = "Twist"

BOOTHS = ("curtain", "tile", "night", "circus", "stripe", "dusk", "paper", "plaid")
LATEXES = ("red", "yellow", "blue", "pink", "green", "orange", "white", "purple")
TWISTS = ("hound", "hare", "steed", "swan", "monkey", "dino", "poodle", "figure")
KNOTS = ("ear", "waist", "nose", "none")
VALVES = ("silver", "gold", "black", "none")
GLEAMS = ("tight", "wide", "none")
CONFETTI = ("none", "dots", "stream", "mix")

LATEX = {
    "red": (214, 48, 58),
    "yellow": (236, 196, 48),
    "blue": (48, 112, 214),
    "pink": (236, 112, 168),
    "green": (48, 168, 92),
    "orange": (232, 122, 42),
    "white": (236, 232, 224),
    "purple": (132, 64, 196),
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def shift(rgb: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    return tuple(max(0, min(255, channel + amount)) for channel in rgb)  # type: ignore[return-value]


def pose(frame: int) -> dict[str, int]:
    turn = frame / FRAMES * math.tau
    return {
        "bob": int(round(math.sin(turn) * 14)),
        "lean": int(round(math.sin(turn) * 8)),
        "larm": int(round(math.sin(turn) * 40)),
        "rarm": int(round(math.sin(turn + math.pi) * 40)),
        "step": int(round(math.sin(turn) * 16)),
    }


def tube(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], radius: int, fill: tuple[int, int, int]) -> None:
    draw.line((start, end), fill=fill, width=radius * 2)
    draw.ellipse((start[0] - radius, start[1] - radius, start[0] + radius, start[1] + radius), fill=fill)
    draw.ellipse((end[0] - radius, end[1] - radius, end[0] + radius, end[1] + radius), fill=fill)


def paint_booth(kind: str, _frame: int) -> Image.Image:
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
    draw = ImageDraw.Draw(image)
    if kind == "curtain":
        image.paste((92, 28, 48, 255), (0, 0, SIZE, SIZE))
        for x in range(0, SIZE, 36):
            draw.polygon([(x, 0), (x + 18, 0), (x + 28, SIZE), (x + 8, SIZE)], fill=(122, 42, 68, 255))
    elif kind == "tile":
        image.paste((214, 196, 176, 255), (0, 0, SIZE, SIZE))
        for y in range(0, SIZE, 48):
            draw.line((0, y, SIZE, y), fill=(168, 148, 128, 255), width=2)
        for x in range(0, SIZE, 48):
            draw.line((x, 0, x, SIZE), fill=(168, 148, 128, 255), width=2)
    elif kind == "night":
        image.paste((18, 16, 32, 255), (0, 0, SIZE, SIZE))
        for x, y in ((80, 70), (180, 40), (320, 90), (420, 60), (140, 160), (380, 150)):
            draw.ellipse((x, y, x + 4, y + 4), fill=(236, 220, 180, 255))
    elif kind == "circus":
        image.paste((28, 36, 92, 255), (0, 0, SIZE, SIZE))
        draw.pieslice((40, -80, 472, 280), 0, 180, fill=(214, 48, 58, 255))
        draw.pieslice((80, -40, 432, 220), 0, 180, fill=(236, 196, 48, 255))
    elif kind == "stripe":
        for y in range(0, SIZE, 32):
            draw.rectangle((0, y, SIZE, y + 16), fill=(214, 72, 92, 255) if (y // 32) % 2 == 0 else (244, 214, 176, 255))
    elif kind == "dusk":
        image.paste((72, 48, 92, 255), (0, 0, SIZE, SIZE))
        draw.rectangle((0, 300, SIZE, SIZE), fill=(42, 32, 48, 255))
    elif kind == "paper":
        image.paste((236, 220, 196, 255), (0, 0, SIZE, SIZE))
        for x in range(24, SIZE, 40):
            draw.line((x, 0, x - 20, SIZE), fill=(196, 168, 132, 255), width=2)
    else:
        for y in range(0, SIZE, 40):
            for x in range(0, SIZE, 40):
                fill = (48, 92, 72, 255) if ((x // 40) + (y // 40)) % 2 == 0 else (196, 168, 92, 255)
                draw.rectangle((x, y, x + 40, y + 40), fill=fill)
    return image


def paint_latex(kind: str, frame: int) -> Image.Image:
    step = pose(frame)
    bob, lean = step["bob"], step["lean"]
    color = LATEX[kind]
    image = blank()
    draw = ImageDraw.Draw(image)
    dark = shift(color, -36)
    head = (256 + lean, 132 + bob)
    neck = (256 + lean, 188 + bob)
    hip = (256 + lean, 332 + bob)
    tube(draw, (hip[0] - 28, hip[1]), (220 + lean - step["step"], 448 + bob), 18, dark)
    tube(draw, (hip[0] + 28, hip[1]), (292 + lean + step["step"], 448 + bob), 18, dark)
    tube(draw, neck, hip, 28, color)
    tube(draw, (214 + lean, 214 + bob), (156 + lean, 250 + bob - step["larm"]), 16, color)
    tube(draw, (298 + lean, 214 + bob), (356 + lean, 250 + bob - step["rarm"]), 16, color)
    draw.ellipse((head[0] - 42, head[1] - 42, head[0] + 42, head[1] + 42), fill=color)
    draw.ellipse((head[0] - 18, head[1] - 22, head[0] - 4, head[1] - 8), fill=shift(color, 50))
    return image


def paint_twist(kind: str, frame: int) -> Image.Image:
    step = pose(frame)
    bob, lean = step["bob"], step["lean"]
    image = blank()
    draw = ImageDraw.Draw(image)
    rubber = (236, 228, 214)
    dark = (42, 32, 36)
    head = (256 + lean, 132 + bob)
    if kind == "hound":
        tube(draw, (head[0] - 18, head[1] - 8), (head[0] - 62, head[1] + 28), 12, rubber)
        tube(draw, (head[0] + 10, head[1] + 8), (head[0] + 48, head[1] + 36), 10, dark)
        draw.ellipse((148 + lean, 360 + bob, 176 + lean, 388 + bob), fill=rubber)
    elif kind == "hare":
        tube(draw, (head[0] - 18, head[1] - 8), (head[0] - 28, head[1] - 72), 10, rubber)
        tube(draw, (head[0] + 18, head[1] - 8), (head[0] + 28, head[1] - 72), 10, rubber)
    elif kind == "steed":
        tube(draw, (head[0] + 8, head[1] + 6), (head[0] + 78, head[1] + 18), 12, rubber)
        draw.polygon([(head[0] + 10, head[1] - 20), (head[0] + 28, head[1] - 48), (head[0] + 36, head[1] - 8)], fill=rubber)
    elif kind == "swan":
        tube(draw, (head[0] + 6, head[1] + 10), (head[0] + 70, head[1] - 18), 11, rubber)
        draw.ellipse((head[0] + 58, head[1] - 32, head[0] + 86, head[1] - 4), fill=rubber)
    elif kind == "monkey":
        tube(draw, (156 + lean, 250 + bob - step["larm"]), (128 + lean, 320 + bob), 12, rubber)
        tube(draw, (356 + lean, 250 + bob - step["rarm"]), (384 + lean, 210 + bob), 12, rubber)
        draw.ellipse((head[0] - 16, head[1] + 18, head[0] + 16, head[1] + 42), fill=dark)
    elif kind == "dino":
        draw.polygon([(head[0] + 20, head[1] - 8), (head[0] + 72, head[1] + 8), (head[0] + 18, head[1] + 22)], fill=rubber)
        draw.polygon([(292 + lean, 300 + bob), (360 + lean, 250 + bob), (348 + lean, 330 + bob)], fill=rubber)
    elif kind == "poodle":
        for cx, cy in ((head[0] - 24, head[1] - 8), (head[0] + 22, head[1] - 4), (head[0], head[1] + 16)):
            draw.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=rubber)
        draw.ellipse((256 + lean - 18, 300 + bob, 256 + lean + 18, 300 + bob + 36), fill=rubber)
    else:
        draw.ellipse((head[0] - 14, head[1] - 8, head[0] - 4, head[1] + 2), fill=dark)
        draw.ellipse((head[0] + 4, head[1] - 8, head[0] + 14, head[1] + 2), fill=dark)
        draw.arc((head[0] - 12, head[1] + 4, head[0] + 12, head[1] + 22), 20, 160, fill=dark, width=2)
    return image


def paint_knot(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    step = pose(frame)
    image = blank()
    draw = ImageDraw.Draw(image)
    ink = (28, 22, 26, 230)
    bob, lean = step["bob"], step["lean"]
    points = {
        "ear": [(236 + lean, 118 + bob), (276 + lean, 118 + bob)],
        "waist": [(256 + lean, 286 + bob)],
        "nose": [(256 + lean, 154 + bob)],
    }[kind]
    for x, y in points:
        draw.ellipse((x - 8, y - 6, x + 8, y + 6), fill=ink)
        draw.arc((x - 12, y - 10, x + 12, y + 10), 200, 40, fill=(236, 220, 200, 255), width=2)
    return image


def paint_valve(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    step = pose(frame)
    image = blank()
    draw = ImageDraw.Draw(image)
    color = {"silver": (196, 202, 208), "gold": (214, 168, 64), "black": (28, 24, 28)}[kind]
    x, y = 214 + step["lean"], 188 + step["bob"]
    draw.rounded_rectangle((x - 8, y, x + 8, y + 22), radius=3, fill=(*color, 255))
    draw.rectangle((x - 5, y + 18, x + 5, y + 28), fill=(244, 236, 220, 255))
    return image


def paint_gleam(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    step = pose(frame)
    image = blank()
    draw = ImageDraw.Draw(image)
    bob, lean = step["bob"], step["lean"]
    width = 6 if kind == "tight" else 12
    shine = (255, 250, 240, 200)
    draw.line((236 + lean, 118 + bob, 236 + lean, 300 + bob), fill=shine, width=width)
    draw.line((214 + lean, 214 + bob, 168 + lean, 236 + bob - step["larm"] // 2), fill=shine, width=max(3, width // 2))
    return image


def paint_confetti(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    image = blank()
    draw = ImageDraw.Draw(image)
    turn = frame / FRAMES * math.tau
    colors = [(236, 72, 72, 220), (236, 196, 48, 220), (48, 168, 214, 220), (132, 64, 196, 220)]
    if kind in ("dots", "mix"):
        for index in range(12):
            x = 40 + index * 38
            y = 36 + int(math.sin(turn + index * 0.6) * 12)
            color = colors[index % len(colors)]
            draw.ellipse((x, y, x + 7, y + 7), fill=color)
    if kind in ("stream", "mix"):
        for index, color in enumerate(colors):
            x = 70 + index * 90
            y = 50 + int(math.sin(turn + index) * 8)
            draw.line((x, y, x + 18, y + 22), fill=color, width=3)
    return image


PAINTERS = {
    "booth": {kind: (lambda frame, kind=kind: paint_booth(kind, frame)) for kind in BOOTHS},
    "latex": {kind: (lambda frame, kind=kind: paint_latex(kind, frame)) for kind in LATEXES},
    "twist": {kind: (lambda frame, kind=kind: paint_twist(kind, frame)) for kind in TWISTS},
    "knot": {kind: (lambda frame, kind=kind: paint_knot(kind, frame)) for kind in KNOTS if kind != "none"},
    "valve": {kind: (lambda frame, kind=kind: paint_valve(kind, frame)) for kind in VALVES if kind != "none"},
    "gleam": {kind: (lambda frame, kind=kind: paint_gleam(kind, frame)) for kind in GLEAMS if kind != "none"},
    "confetti": {kind: (lambda frame, kind=kind: paint_confetti(kind, frame)) for kind in CONFETTI if kind != "none"},
}

STACK = ("booth", "latex", "twist", "knot", "valve", "gleam", "confetti")
TRAIT_LABELS = (
    ("booth", "Booth"),
    ("latex", "Latex"),
    ("twist", "Twist"),
    ("knot", "Knot"),
    ("valve", "Valve"),
    ("gleam", "Gleam"),
    ("confetti", "Confetti"),
)
TRAIT_SPEC = {
    "booth": [
        ("curtain", "Curtain Booth", 16),
        ("tile", "Tile Booth", 14),
        ("night", "Night Booth", 14),
        ("circus", "Circus Booth", 14),
        ("stripe", "Stripe Booth", 12),
        ("dusk", "Dusk Booth", 12),
        ("paper", "Paper Booth", 10),
        ("plaid", "Plaid Booth", 8),
    ],
    "latex": [
        ("red", "Red Latex", 16),
        ("yellow", "Yellow Latex", 14),
        ("blue", "Blue Latex", 14),
        ("pink", "Pink Latex", 14),
        ("green", "Green Latex", 12),
        ("orange", "Orange Latex", 12),
        ("white", "White Latex", 10),
        ("purple", "Purple Latex", 8),
    ],
    "twist": [
        ("hound", "Hound Twist", 16),
        ("hare", "Hare Twist", 14),
        ("steed", "Steed Twist", 14),
        ("swan", "Swan Twist", 12),
        ("monkey", "Monkey Twist", 12),
        ("dino", "Dino Twist", 12),
        ("poodle", "Poodle Twist", 10),
        ("figure", "Figure Twist", 10),
    ],
    "knot": [
        ("none", "No Knot", 24),
        ("ear", "Ear Knot", 28),
        ("waist", "Waist Knot", 26),
        ("nose", "Nose Knot", 22),
    ],
    "valve": [
        ("none", "No Valve", 28),
        ("silver", "Silver Valve", 28),
        ("gold", "Gold Valve", 24),
        ("black", "Black Valve", 20),
    ],
    "gleam": [
        ("none", "Matte", 28),
        ("tight", "Tight Gleam", 40),
        ("wide", "Wide Gleam", 32),
    ],
    "confetti": [
        ("none", "Clear Air", 34),
        ("dots", "Dot Confetti", 26),
        ("stream", "Stream Confetti", 22),
        ("mix", "Mix Confetti", 18),
    ],
}
SIGNATURES = [
    {"booth": "curtain", "latex": "red", "twist": "hound", "knot": "ear", "valve": "silver", "gleam": "tight", "confetti": "dots"},
    {"booth": "circus", "latex": "yellow", "twist": "hare", "knot": "nose", "valve": "gold", "gleam": "wide", "confetti": "stream"},
    {"booth": "night", "latex": "blue", "twist": "steed", "knot": "waist", "valve": "black", "gleam": "tight", "confetti": "none"},
    {"booth": "stripe", "latex": "pink", "twist": "swan", "knot": "ear", "valve": "silver", "gleam": "wide", "confetti": "mix"},
    {"booth": "tile", "latex": "green", "twist": "monkey", "knot": "none", "valve": "gold", "gleam": "tight", "confetti": "dots"},
    {"booth": "dusk", "latex": "orange", "twist": "dino", "knot": "waist", "valve": "black", "gleam": "none", "confetti": "stream"},
    {"booth": "paper", "latex": "white", "twist": "poodle", "knot": "nose", "valve": "silver", "gleam": "wide", "confetti": "mix"},
    {"booth": "plaid", "latex": "purple", "twist": "figure", "knot": "ear", "valve": "gold", "gleam": "tight", "confetti": "dots"},
    {"booth": "night", "latex": "red", "twist": "swan", "knot": "waist", "valve": "none", "gleam": "wide", "confetti": "stream"},
    {"booth": "curtain", "latex": "blue", "twist": "hare", "knot": "nose", "valve": "silver", "gleam": "none", "confetti": "mix"},
    {"booth": "circus", "latex": "green", "twist": "hound", "knot": "ear", "valve": "black", "gleam": "tight", "confetti": "none"},
    {"booth": "stripe", "latex": "purple", "twist": "dino", "knot": "waist", "valve": "gold", "gleam": "wide", "confetti": "dots"},
    {"booth": "tile", "latex": "orange", "twist": "poodle", "knot": "none", "valve": "silver", "gleam": "tight", "confetti": "stream"},
    {"booth": "dusk", "latex": "pink", "twist": "figure", "knot": "nose", "valve": "none", "gleam": "wide", "confetti": "mix"},
    {"booth": "paper", "latex": "yellow", "twist": "monkey", "knot": "ear", "valve": "black", "gleam": "none", "confetti": "dots"},
    {"booth": "plaid", "latex": "white", "twist": "steed", "knot": "waist", "valve": "gold", "gleam": "tight", "confetti": "stream"},
]
BLURBS = {
    "booth": "The party wall — curtain, tile, night, circus, stripe, dusk, paper, plaid.",
    "latex": "The inflated body — red, yellow, blue, pink, green, orange, white, purple.",
    "twist": "The dancing balloon. Eight twists: hound, hare, steed, swan, monkey, dino, poodle, figure.",
    "knot": "A tied pinch — ear, waist, nose — or an untied tube.",
    "valve": "The inflation nozzle — silver, gold, black — or a sealed end.",
    "gleam": "Specular shine on the latex — tight, wide — or matte.",
    "confetti": "Air in the booth — dots, stream, mix — or clear air.",
}
NONE_LABELS = {"knot": "No Knot", "valve": "No Valve", "gleam": "Matte", "confetti": "Clear Air"}
DEFAULTS = {key: SIGNATURES[0][key] for key in STACK}
COLLECTION_STORY = (
    "Vinylon.\n\n"
    "A 10,000-piece collection of looping balloon-animal PFP GIFs on Robinhood Chain. "
    "Each twist is stacked from seven plates — booth, latex, twist, knot, valve, gleam, and confetti — "
    "then flattened onto one 12-frame GIF. Eight dancing twists: hound, hare, steed, swan, monkey, dino, poodle, and figure. "
    "Inflated tubes. Knots at the joints. The bob is the loop.\n\n"
    "Latex in a booth. Not neon tubing. Not a leather puppet. Not soy-ink blots. "
    "The twist stays seated in one envelope. The dance is the squeeze. One shared clock.\n\n"
    "Minting free on Robinhood Chain (chain ID 4663). Gas is ETH."
)
COLLECTION_DESCRIPTION = (
    "Vinylon is a 10,000-piece collection of looping balloon-animal PFP GIFs. "
    "Each twist is stacked from seven plates — booth, latex, twist, knot, valve, gleam, and confetti — "
    "then flattened onto one 12-frame GIF. Inflated tubes. Knots. Specular shine."
)


def trait_path(category: str, trait_id: str) -> Path:
    return TRAIT_DIR / category / f"{trait_id}.png"


def render_trait_frames(category: str, trait_id: str) -> list[Image.Image]:
    return [PAINTERS[category][trait_id](frame) for frame in range(FRAMES)]


def compose_selection(selection: dict[str, str]) -> list[Image.Image]:
    layers: list[list[Image.Image]] = []
    for category in STACK:
        trait_id = selection[category]
        if trait_id == "none":
            continue
        path = trait_path(category, trait_id)
        if path.exists():
            with Image.open(path) as im:
                im.load()
                frames = []
                for i in range(getattr(im, "n_frames", 1)):
                    im.seek(i)
                    frames.append(im.convert("RGBA").copy())
                layers.append(frames)
        else:
            layers.append(render_trait_frames(category, trait_id))
    out = []
    for i in range(FRAMES):
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        for frames in layers:
            canvas = Image.alpha_composite(canvas, frames[i % len(frames)])
        out.append(canvas)
    return out


def name_of(category: str, trait_id: str) -> str:
    for item_id, name, _rarity in TRAIT_SPEC[category]:
        if item_id == trait_id:
            return name
    return trait_id


def build_traits() -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    (TRAIT_DIR / "manifest.json").write_text(
        json.dumps({"name": NAME, "size": SIZE, "frames": FRAMES, "durationMs": DURATION_MS, "format": "apng", "loop": 0, "order": list(STACK)}, indent=2) + "\n",
        encoding="utf-8",
    )


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS, colors=GIF_COLORS, dither=GIF_DITHER, palette_picks=FRAMES)
        samples.append(
            {
                "id": index,
                "name": f"{TOKEN} #{index}",
                "image": f"/{SLUG}-preview/{index}.gif",
                "attributes": [{"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")
    write_ts(samples)


def write_ts(samples: list[dict]) -> None:
    rows = []
    for sample in samples:
        attrs = ",\n      ".join(f'{{ trait_type: "{a["trait_type"]}", value: "{a["value"]}" }}' for a in sample["attributes"])
        rows.append(f'  {{\n    id: {sample["id"]},\n    name: "{sample["name"]}",\n    image: "{sample["image"]}?v=1",\n    attributes: [\n      {attrs},\n    ],\n  }}')
    (SRC_DATA / f"{SLUG}-gallery.ts").write_text(
        f"export type {NAME}Sample = {{\n  id: number;\n  name: string;\n  image: string;\n  attributes: {{ trait_type: string; value: string }}[];\n}};\n\n"
        f"export const {SLUG}Samples: {NAME}Sample[] = [\n" + ",\n".join(rows) + "\n];\n",
        encoding="utf-8",
    )
    cats = []
    for key, label in TRAIT_LABELS:
        traits = [
            f'      {{ id: "{trait_id}", name: "{name}", image: "/{SLUG}-traits/{key}/{trait_id}.png", rarity: {rarity} }}'
            for trait_id, name, rarity in TRAIT_SPEC[key]
            if trait_id != "none"
        ]
        none = NONE_LABELS.get(key)
        none_line = f'\n    noneLabel: "{none}",' if none else ""
        cats.append(f'  {{\n    id: "{key}",\n    label: "{label}",\n    blurb: "{BLURBS[key]}",{none_line}\n    traits: [\n' + ",\n".join(traits) + ",\n    ],\n  }")
    ids = " | ".join(f'"{key}"' for key, _label in TRAIT_LABELS)
    picks = ",\n".join(f'    {key}: pick({SLUG}CategoryById("{key}"))' for key, _label in TRAIT_LABELS)
    defaults = ",\n".join(f'  {key}: "{DEFAULTS[key]}"' for key in STACK)
    (SRC_DATA / f"{SLUG}-traits.ts").write_text(
        f"export type {NAME}Trait = {{\n  id: string;\n  name: string;\n  image?: string;\n  rarity: number;\n}};\n\n"
        f"export type {NAME}TraitCategory = {{\n  id: {ids};\n  label: string;\n  blurb: string;\n  noneLabel?: string;\n  traits: {NAME}Trait[];\n}};\n\n"
        f'export const {SYMBOL}_ART_VERSION = "{SLUG}-v1";\n\nexport const {SYMBOL}_FRAMES = 12;\nexport const {SYMBOL}_DURATION_MS = 90;\n\n'
        f"export function {SLUG}TraitSrc(path?: string) {{\n  if (!path) return \"\";\n  return `${{path}}?v=${{{SYMBOL}_ART_VERSION}}`;\n}}\n\n"
        f"export const {SLUG}TraitCategories: {NAME}TraitCategory[] = [\n" + ",\n".join(cats) + "\n];\n\n"
        f'export const none{NAME}Trait: {NAME}Trait = {{ id: "none", name: "None", rarity: 0 }};\n\n'
        f"export function {SLUG}CategoryById(id: {NAME}TraitCategory[\"id\"]) {{\n"
        f"  const category = {SLUG}TraitCategories.find((item) => item.id === id);\n"
        f"  if (!category) throw new Error(`Unknown {NAME} trait category: ${{id}}`);\n  return category;\n}}\n\n"
        f"export function find{NAME}Trait(categoryId: {NAME}TraitCategory[\"id\"], traitId: string) {{\n"
        f"  if (traitId === \"none\") return none{NAME}Trait;\n  return {SLUG}CategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n}}\n\n"
        f"export const default{NAME}Selection = {{\n{defaults},\n}} as const;\n\nexport type {NAME}Selection = Record<{NAME}TraitCategory[\"id\"], string>;\n\n"
        f"export function random{NAME}Selection(): {NAME}Selection {{\n  const pick = (category: {NAME}TraitCategory) => {{\n"
        f"    const pool: {NAME}Trait[] = category.noneLabel ? [{{ id: \"none\", name: category.noneLabel, rarity: 22 }}, ...category.traits] : category.traits;\n"
        "    const total = pool.reduce((sum, trait) => sum + Math.max(trait.rarity, 1), 0);\n    let roll = Math.random() * total;\n"
        "    for (const trait of pool) {\n      roll -= Math.max(trait.rarity, 1);\n      if (roll <= 0) return trait.id;\n    }\n    return pool[0].id;\n  };\n"
        "  return {\n" + picks + ",\n  };\n}\n\n"
        f"export function {SLUG}CombinationCount() {{\n  return {SLUG}TraitCategories.reduce((product, category) => {{\n"
        "    const extra = category.noneLabel ? 1 : 0;\n    return product * (category.traits.length + extra);\n  }, 1);\n}\n\n"
        f"export function {SLUG}SelectionToLayers(selection: {NAME}Selection) {{\n"
        f"  return ({json.dumps(list(STACK))} as const)\n    .map((id) => find{NAME}Trait(id, selection[id]))\n"
        f"    .filter((trait): trait is {NAME}Trait => Boolean(trait?.image))\n    .map((trait) => {SLUG}TraitSrc(trait.image));\n}}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array([[0.86, 0.22, 0.32], [0.95, 0.78, 0.28], [0.16, 0.18, 0.36], [0.42, 0.62, 0.92]], dtype=np.float32)
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    yy = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None]
    xx = np.broadcast_to(x, (height, width))
    t = np.clip(xx * 0.7 + yy * 0.3, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    frac = (t - i0)[..., None]
    rgb_out = colors[i0] * (1.0 - frac) + colors[np.clip(i0 + 1, 0, len(colors) - 1)] * frac
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / f"{SLUG}-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / f"{SLUG}.json").write_text(
        json.dumps(
            {
                "name": NAME,
                "symbol": SYMBOL,
                "description": COLLECTION_DESCRIPTION,
                "image": f"/brand/collection-{SLUG}.gif",
                "featured_image": f"/brand/featured-{SLUG}.jpg",
                "banner_image": f"/brand/banner-{SLUG}.png",
                "opensea_banner_image": f"/brand/banner-{SLUG}-opensea.jpg",
                "external_link": f"/{SLUG}",
                "seller_fee_basis_points": 500,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_brand() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    portraits = [compose_selection(selection)[0] for selection in SIGNATURES[:7]]
    logo_frames = compose_selection(SIGNATURES[0])
    logo = logo_frames[0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle((16, 16, SIZE - 17, SIZE - 17), radius=36, fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    rim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle((12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(236, 72, 72, 255), width=4)
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / f"logo-{SLUG}.png")
    save_apng([frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames], BRAND_DIR / f"logo-{SLUG}-loop.png")

    def lineup(width: int, height: int, faces: list[Image.Image]) -> Image.Image:
        canvas = panoramic_wash(width, height)
        count = len(faces)
        size = int(height * 0.82)
        overlap = size // 5
        total = size * count - overlap * (count - 1)
        start_x = (width - total) // 2
        y = (height - size) // 2 + int(height * 0.03)
        for index, portrait in enumerate(faces):
            place_portrait(canvas, portrait, start_x + index * (size - overlap), y, size, radius=max(20, size // 16))
        return canvas

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / f"banner-{SLUG}.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / f"banner-{SLUG}-opensea.jpg", quality=90)
    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / f"featured-{SLUG}.jpg", quality=90)
    save_loop_gif(
        [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / f"collection-{SLUG}.gif",
        DURATION_MS,
        colors=GIF_COLORS,
        dither=GIF_DITHER,
        palette_picks=FRAMES,
    )
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Vinylon brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Vinylon balloon twists…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
