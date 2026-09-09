#!/usr/bin/env python3
"""Paint Ossein — anatomical chart skeletons on ruled paper.

Language: ivory bone, hairline ink, leader ticks, tea stain. Not a leather
puppet, not a charcoal doodle, not a sticker cutout, not an egg.
The specimen stays on one sheet. The step is the dance.
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

GIF_COLORS = 80
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "ossein-traits"
PREVIEW_DIR = ROOT / "public" / "ossein-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

SLUG = "ossein"
NAME = "Ossein"
SYMBOL = "OSSN"
TOKEN = "Chart"

SHEETS = ("cream", "ledger", "night", "slate", "aged", "blush", "vellum", "mint")
RULES = ("hair", "dot", "cross", "double")
SPECIMENS = ("cortical", "avian", "feline", "equine", "frog", "ape", "fish", "serpent")
JOINTS = ("ring", "dot", "cross", "tick")
LEADERS = ("none", "one", "pair")
STAINS = ("none", "tea", "foxing", "coffee")
CHALKS = ("none", "mote", "smear", "dust")

SHEET = {
    "cream": ((244, 236, 214), (92, 118, 156)),
    "ledger": ((228, 236, 214), (86, 122, 78)),
    "night": ((28, 32, 40), (168, 196, 214)),
    "slate": ((196, 206, 214), (72, 86, 102)),
    "aged": ((232, 214, 176), (132, 86, 48)),
    "blush": ((244, 220, 214), (156, 86, 98)),
    "vellum": ((236, 224, 196), (112, 92, 64)),
    "mint": ((220, 236, 226), (64, 122, 112)),
}
IVORY = (236, 226, 206)
INK = (62, 48, 38)


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def pose(frame: int) -> dict[str, int]:
    turn = frame / FRAMES * math.tau
    return {
        "bob": int(round(math.sin(turn) * 10)),
        "lean": int(round(math.sin(turn) * 12)),
        "larm": int(round(math.sin(turn) * 42)),
        "rarm": int(round(math.sin(turn + math.pi) * 42)),
        "step": int(round(math.sin(turn) * 20)),
    }


def anchors(frame: int) -> dict[str, tuple[int, int]]:
    step = pose(frame)
    bob, lean = step["bob"], step["lean"]
    skull = (256 + lean, 128 + bob)
    neck = (256 + lean, 168 + bob)
    shoulder_l = (198 + lean, 188 + bob)
    shoulder_r = (314 + lean, 188 + bob)
    hip_l = (220 + lean, 318 + bob)
    hip_r = (292 + lean, 318 + bob)
    return {
        "skull": skull,
        "neck": neck,
        "shoulder_l": shoulder_l,
        "shoulder_r": shoulder_r,
        "elbow_l": (168 + lean, 236 + bob - step["larm"] // 2),
        "elbow_r": (344 + lean, 236 + bob - step["rarm"] // 2),
        "hand_l": (150 + lean, 286 + bob - step["larm"]),
        "hand_r": (362 + lean, 286 + bob - step["rarm"]),
        "hip_l": hip_l,
        "hip_r": hip_r,
        "knee_l": (206 + lean - step["step"] // 2, 382 + bob),
        "knee_r": (306 + lean + step["step"] // 2, 382 + bob),
        "foot_l": (188 + lean - step["step"], 448 + bob),
        "foot_r": (324 + lean + step["step"], 448 + bob),
    }


def bone(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], thick: int = 12) -> None:
    draw.line((start, end), fill=IVORY, width=thick)
    radius = thick // 2 + 2
    for point in (start, end):
        draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), fill=IVORY, outline=INK)


def paint_sheet(kind: str, _frame: int) -> Image.Image:
    paper, _rule = SHEET[kind]
    image = Image.new("RGBA", (SIZE, SIZE), (*paper, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((28, 28, SIZE - 29, SIZE - 29), outline=shift_ink(kind), width=2)
    return image


def shift_ink(kind: str) -> tuple[int, int, int, int]:
    return (*SHEET[kind][1], 90)


def paint_rule(kind: str, _frame: int) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    ink = (72, 96, 132, 110)
    if kind == "hair":
        for y in range(48, SIZE - 40, 16):
            draw.line((40, y, SIZE - 40, y), fill=ink, width=1)
    elif kind == "dot":
        for y in range(56, SIZE - 40, 22):
            for x in range(56, SIZE - 40, 22):
                draw.ellipse((x, y, x + 2, y + 2), fill=ink)
    elif kind == "cross":
        for y in range(52, SIZE - 40, 28):
            draw.line((40, y, SIZE - 40, y), fill=ink, width=1)
        for x in range(52, SIZE - 40, 28):
            draw.line((x, 40, x, SIZE - 40), fill=ink, width=1)
    else:
        for y in range(48, SIZE - 40, 24):
            draw.line((40, y, SIZE - 40, y), fill=ink, width=1)
            draw.line((40, y + 4, SIZE - 40, y + 4), fill=ink, width=1)
    return image


def paint_specimen(kind: str, frame: int) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    points = anchors(frame)
    bone(draw, points["skull"], points["neck"], 10)
    bone(draw, points["neck"], ((points["hip_l"][0] + points["hip_r"][0]) // 2, points["hip_l"][1]), 11)
    bone(draw, points["shoulder_l"], points["shoulder_r"], 8)
    bone(draw, points["shoulder_l"], points["elbow_l"], 10)
    bone(draw, points["elbow_l"], points["hand_l"], 8)
    bone(draw, points["shoulder_r"], points["elbow_r"], 10)
    bone(draw, points["elbow_r"], points["hand_r"], 8)
    bone(draw, points["hip_l"], points["hip_r"], 8)
    bone(draw, points["hip_l"], points["knee_l"], 11)
    bone(draw, points["knee_l"], points["foot_l"], 10)
    bone(draw, points["hip_r"], points["knee_r"], 11)
    bone(draw, points["knee_r"], points["foot_r"], 10)
    skull(draw, kind, points["skull"])
    ribs(draw, points["neck"], points["hip_l"])
    return image


def skull(draw: ImageDraw.ImageDraw, kind: str, center: tuple[int, int]) -> None:
    cx, cy = center
    if kind == "cortical":
        draw.ellipse((cx - 36, cy - 40, cx + 36, cy + 28), fill=IVORY, outline=INK)
        draw.arc((cx - 22, cy + 6, cx + 22, cy + 34), 10, 170, fill=INK, width=2)
    elif kind == "avian":
        draw.ellipse((cx - 28, cy - 28, cx + 18, cy + 22), fill=IVORY, outline=INK)
        draw.polygon([(cx + 10, cy - 4), (cx + 62, cy + 4), (cx + 8, cy + 16)], fill=IVORY, outline=INK)
    elif kind == "feline":
        draw.ellipse((cx - 32, cy - 30, cx + 32, cy + 24), fill=IVORY, outline=INK)
        draw.polygon([(cx - 8, cy + 8), (cx + 8, cy + 8), (cx, cy + 36)], fill=IVORY, outline=INK)
        draw.polygon([(cx - 28, cy - 24), (cx - 16, cy - 46), (cx - 8, cy - 20)], fill=IVORY, outline=INK)
        draw.polygon([(cx + 28, cy - 24), (cx + 16, cy - 46), (cx + 8, cy - 20)], fill=IVORY, outline=INK)
    elif kind == "equine":
        draw.ellipse((cx - 26, cy - 28, cx + 26, cy + 20), fill=IVORY, outline=INK)
        draw.polygon([(cx - 6, cy + 4), (cx + 18, cy + 8), (cx + 48, cy + 28), (cx - 4, cy + 22)], fill=IVORY, outline=INK)
    elif kind == "frog":
        draw.ellipse((cx - 48, cy - 22, cx + 48, cy + 22), fill=IVORY, outline=INK)
        draw.ellipse((cx - 36, cy - 28, cx - 8, cy - 4), fill=IVORY, outline=INK)
        draw.ellipse((cx + 8, cy - 28, cx + 36, cy - 4), fill=IVORY, outline=INK)
    elif kind == "ape":
        draw.ellipse((cx - 40, cy - 36, cx + 40, cy + 32), fill=IVORY, outline=INK)
        draw.arc((cx - 18, cy + 4, cx + 18, cy + 28), 20, 160, fill=INK, width=2)
    elif kind == "fish":
        draw.ellipse((cx - 30, cy - 22, cx + 34, cy + 22), fill=IVORY, outline=INK)
        draw.polygon([(cx - 28, cy), (cx - 58, cy - 18), (cx - 58, cy + 18)], fill=IVORY, outline=INK)
    else:
        draw.ellipse((cx - 24, cy - 22, cx + 24, cy + 18), fill=IVORY, outline=INK)
        draw.arc((cx - 70, cy - 10, cx + 10, cy + 70), 200, 340, fill=IVORY, width=10)


def ribs(draw: ImageDraw.ImageDraw, neck: tuple[int, int], hip: tuple[int, int]) -> None:
    top = neck[1] + 16
    for index in range(5):
        y = top + index * 16
        span = 28 + index * 4
        draw.arc((256 - span, y, 256 + span, y + 22), 10, 170, fill=INK, width=2)


def paint_joint(kind: str, frame: int) -> Image.Image:
    image = blank()
    draw = ImageDraw.Draw(image)
    ink = (122, 48, 42, 230)
    keys = ("shoulder_l", "shoulder_r", "elbow_l", "elbow_r", "hip_l", "hip_r", "knee_l", "knee_r")
    for key in keys:
        x, y = anchors(frame)[key]
        if kind == "ring":
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), outline=ink, width=2)
        elif kind == "dot":
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=ink)
        elif kind == "cross":
            draw.line((x - 6, y, x + 6, y), fill=ink, width=2)
            draw.line((x, y - 6, x, y + 6), fill=ink, width=2)
        else:
            draw.line((x - 5, y - 5, x + 5, y + 5), fill=ink, width=2)
    return image


def paint_leader(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    image = blank()
    draw = ImageDraw.Draw(image)
    skull = anchors(frame)["skull"]
    ink = (72, 64, 52, 220)
    draw.line((skull[0] + 36, skull[1] - 8, 430, 72), fill=ink, width=1)
    draw.line((418, 72, 452, 72), fill=ink, width=2)
    if kind == "pair":
        hip = anchors(frame)["hip_r"]
        draw.line((hip[0] + 8, hip[1], 430, 420), fill=ink, width=1)
        draw.line((418, 420, 452, 420), fill=ink, width=2)
    return image


def paint_stain(kind: str, _frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    image = blank()
    draw = ImageDraw.Draw(image)
    if kind == "tea":
        draw.ellipse((70, 360, 190, 470), fill=(168, 112, 62, 70))
    elif kind == "foxing":
        for x, y, r in ((90, 90, 8), (400, 120, 5), (120, 400, 6), (380, 390, 7), (300, 80, 4)):
            draw.ellipse((x, y, x + r, y + r), fill=(132, 78, 48, 90))
    else:
        draw.ellipse((300, 330, 460, 490), fill=(92, 58, 36, 80))
    return image


def paint_chalk(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    image = blank()
    draw = ImageDraw.Draw(image)
    turn = frame / FRAMES * math.tau
    dust = (236, 226, 206, 160)
    if kind == "mote":
        for index in range(10):
            x = 60 + index * 40
            y = 48 + int(math.sin(turn + index) * 8)
            draw.ellipse((x, y, x + 3, y + 3), fill=dust)
    elif kind == "smear":
        draw.arc((80, 70, 220, 180), 20, 200, fill=dust, width=4)
    else:
        for index in range(14):
            x = 40 + (index * 37) % 420
            y = 40 + int((index * 53 + math.sin(turn) * 6) % 430)
            draw.point((x, y), fill=dust)
    return image


PAINTERS = {
    "sheet": {kind: (lambda frame, kind=kind: paint_sheet(kind, frame)) for kind in SHEETS},
    "rule": {kind: (lambda frame, kind=kind: paint_rule(kind, frame)) for kind in RULES},
    "specimen": {kind: (lambda frame, kind=kind: paint_specimen(kind, frame)) for kind in SPECIMENS},
    "joint": {kind: (lambda frame, kind=kind: paint_joint(kind, frame)) for kind in JOINTS},
    "leader": {kind: (lambda frame, kind=kind: paint_leader(kind, frame)) for kind in LEADERS if kind != "none"},
    "stain": {kind: (lambda frame, kind=kind: paint_stain(kind, frame)) for kind in STAINS if kind != "none"},
    "chalk": {kind: (lambda frame, kind=kind: paint_chalk(kind, frame)) for kind in CHALKS if kind != "none"},
}

STACK = ("sheet", "rule", "specimen", "joint", "leader", "stain", "chalk")
TRAIT_LABELS = (
    ("sheet", "Sheet"),
    ("rule", "Rule"),
    ("specimen", "Specimen"),
    ("joint", "Joint"),
    ("leader", "Leader"),
    ("stain", "Stain"),
    ("chalk", "Chalk"),
)
TRAIT_SPEC = {
    "sheet": [
        ("cream", "Cream Sheet", 18),
        ("ledger", "Ledger Sheet", 16),
        ("night", "Night Sheet", 14),
        ("slate", "Slate Sheet", 14),
        ("aged", "Aged Sheet", 12),
        ("blush", "Blush Sheet", 10),
        ("vellum", "Vellum Sheet", 8),
        ("mint", "Mint Sheet", 8),
    ],
    "rule": [
        ("hair", "Hair Rule", 32),
        ("dot", "Dot Rule", 26),
        ("cross", "Cross Rule", 22),
        ("double", "Double Rule", 20),
    ],
    "specimen": [
        ("cortical", "Cortical", 16),
        ("avian", "Avian", 14),
        ("feline", "Feline", 14),
        ("equine", "Equine", 12),
        ("frog", "Frog", 12),
        ("ape", "Ape", 12),
        ("fish", "Fish", 10),
        ("serpent", "Serpent", 10),
    ],
    "joint": [
        ("ring", "Ring Joint", 30),
        ("dot", "Dot Joint", 28),
        ("cross", "Cross Joint", 22),
        ("tick", "Tick Joint", 20),
    ],
    "leader": [
        ("none", "No Leader", 36),
        ("one", "One Leader", 36),
        ("pair", "Pair Leader", 28),
    ],
    "stain": [
        ("none", "Clean Sheet", 36),
        ("tea", "Tea Stain", 26),
        ("foxing", "Foxing", 22),
        ("coffee", "Coffee Stain", 18),
    ],
    "chalk": [
        ("none", "Clear Air", 36),
        ("mote", "Chalk Motes", 26),
        ("smear", "Chalk Smear", 20),
        ("dust", "Chalk Dust", 18),
    ],
}
SIGNATURES = [
    {"sheet": "cream", "rule": "hair", "specimen": "cortical", "joint": "ring", "leader": "one", "stain": "none", "chalk": "mote"},
    {"sheet": "night", "rule": "cross", "specimen": "avian", "joint": "dot", "leader": "pair", "stain": "tea", "chalk": "none"},
    {"sheet": "ledger", "rule": "dot", "specimen": "feline", "joint": "cross", "leader": "none", "stain": "foxing", "chalk": "smear"},
    {"sheet": "aged", "rule": "double", "specimen": "equine", "joint": "tick", "leader": "one", "stain": "coffee", "chalk": "dust"},
    {"sheet": "slate", "rule": "hair", "specimen": "frog", "joint": "ring", "leader": "pair", "stain": "none", "chalk": "mote"},
    {"sheet": "blush", "rule": "cross", "specimen": "ape", "joint": "dot", "leader": "none", "stain": "tea", "chalk": "none"},
    {"sheet": "mint", "rule": "dot", "specimen": "fish", "joint": "cross", "leader": "one", "stain": "foxing", "chalk": "dust"},
    {"sheet": "vellum", "rule": "double", "specimen": "serpent", "joint": "tick", "leader": "pair", "stain": "tea", "chalk": "smear"},
    {"sheet": "night", "rule": "hair", "specimen": "cortical", "joint": "dot", "leader": "none", "stain": "coffee", "chalk": "mote"},
    {"sheet": "cream", "rule": "cross", "specimen": "feline", "joint": "ring", "leader": "one", "stain": "none", "chalk": "dust"},
    {"sheet": "ledger", "rule": "double", "specimen": "avian", "joint": "tick", "leader": "one", "stain": "foxing", "chalk": "none"},
    {"sheet": "aged", "rule": "hair", "specimen": "ape", "joint": "cross", "leader": "pair", "stain": "tea", "chalk": "smear"},
    {"sheet": "slate", "rule": "dot", "specimen": "equine", "joint": "ring", "leader": "none", "stain": "coffee", "chalk": "mote"},
    {"sheet": "blush", "rule": "hair", "specimen": "fish", "joint": "dot", "leader": "one", "stain": "none", "chalk": "dust"},
    {"sheet": "mint", "rule": "cross", "specimen": "serpent", "joint": "tick", "leader": "none", "stain": "tea", "chalk": "none"},
    {"sheet": "vellum", "rule": "double", "specimen": "frog", "joint": "cross", "leader": "pair", "stain": "foxing", "chalk": "smear"},
]
BLURBS = {
    "sheet": "The chart paper — cream, ledger, night, slate, aged, blush, vellum, mint.",
    "rule": "The printed grid — hair, dot, cross, double.",
    "specimen": "The dancing skeleton. Eight specimens: cortical, avian, feline, equine, frog, ape, fish, serpent.",
    "joint": "Marks at the articulations — ring, dot, cross, tick.",
    "leader": "Callout ticks — one, pair — or an unlabeled plate.",
    "stain": "Age on the sheet — tea, foxing, coffee — or a clean sheet.",
    "chalk": "Dust over the plate — mote, smear, dust — or clear air.",
}
NONE_LABELS = {"leader": "No Leader", "stain": "Clean Sheet", "chalk": "Clear Air"}
DEFAULTS = {key: SIGNATURES[0][key] for key in STACK}
COLLECTION_STORY = (
    "Ossein.\n\n"
    "A 10,000-piece collection of looping anatomical-chart PFP GIFs on Robinhood Chain. "
    "Each plate is stacked from seven plates — sheet, rule, specimen, joint, leader, stain, and chalk — "
    "then flattened onto one 12-frame GIF. Eight dancing specimens: cortical, avian, feline, equine, frog, ape, fish, and serpent. "
    "Ivory bone. Hairline ink. The step is the loop.\n\n"
    "A medical chart, not a leather puppet. Not neon tubing. Not soy-ink blots. "
    "The specimen stays seated on one sheet. The dance is in the joints. One shared clock.\n\n"
    "Minting free on Robinhood Chain (chain ID 4663). Gas is ETH."
)
COLLECTION_DESCRIPTION = (
    "Ossein is a 10,000-piece collection of looping anatomical-chart PFP GIFs. "
    "Each plate is stacked from seven plates — sheet, rule, specimen, joint, leader, stain, and chalk — "
    "then flattened onto one 12-frame GIF. Ivory bone. Hairline ink. A step on the grid."
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
    colors = np.array([[0.93, 0.90, 0.82], [0.72, 0.78, 0.86], [0.18, 0.16, 0.14], [0.55, 0.42, 0.32]], dtype=np.float32)
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    yy = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None]
    xx = np.broadcast_to(x, (height, width))
    t = np.clip(xx * 0.5 + yy * 0.5, 0.0, 0.999) * (len(colors) - 1)
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
    ImageDraw.Draw(rim).rounded_rectangle((12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(92, 118, 156, 255), width=4)
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
        print("Writing Ossein brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Ossein chart skeletons…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
