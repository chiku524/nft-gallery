#!/usr/bin/env python3
"""Paint Afterimages — unique 1:1 APNG paintings for an OpenSea Drop.

Each token is a finished looping painting, not a trait stack.
16 frames, 100ms, 640×640. Upload pack + site previews land together.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from gif_bake import load_apng_frames, save_loop_gif

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "public" / "afterimages"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
OUT = ROOT / "generated" / "afterimages"
IMAGE_DIR = OUT / "images"
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"

SIZE = 640
FRAMES = 16
DURATION_MS = 100
H, W = SIZE, SIZE


def clamp01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = clamp01((x - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def rgb(hex_color: str) -> np.ndarray:
    value = hex_color.lstrip("#")
    return np.array([int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


def mix(a: np.ndarray | float, b: np.ndarray | float, t: float | np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    t = np.asarray(t, dtype=np.float32)
    if t.ndim >= 2 and a.ndim == 1:
        t = t[..., None]
    return a * (1.0 - t) + b * t


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


def grid() -> tuple[np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return xx, yy


def over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


def fill(dst: np.ndarray, color: np.ndarray, opacity: float = 1.0) -> None:
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = opacity
    over(dst, layer)


def vertical_wash(top: np.ndarray, bottom: np.ndarray, power: float = 1.0) -> np.ndarray:
    xx, yy = grid()
    t = (yy / (H - 1)) ** power
    dst = blank()
    dst[..., :3] = mix(top, bottom, t)
    dst[..., 3] = 1.0
    return dst


def glow(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.exp(-0.5 * (d / max(r, 1.0)) ** 2) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def disc(
    dst: np.ndarray,
    cx: float,
    cy: float,
    r: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = 2.0,
) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = smoothstep(r + soft, r - soft, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def ellipse(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = 2.0,
) -> None:
    xx, yy = grid()
    d = np.sqrt(((xx - cx) / max(rx, 1.0)) ** 2 + ((yy - cy) / max(ry, 1.0)) ** 2)
    a = smoothstep(1.0 + soft / max(rx, ry), 1.0 - soft / max(rx, ry), d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def rect(
    dst: np.ndarray,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    color: np.ndarray,
    opacity: float = 1.0,
    radius: float = 0.0,
) -> None:
    xx, yy = grid()
    if radius <= 0:
        mask = (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)
        layer = blank()
        layer[..., :3] = color
        layer[..., 3] = mask.astype(np.float32) * opacity
        over(dst, layer)
        return
    cx = np.clip(xx, x0 + radius, x1 - radius)
    cy = np.clip(yy, y0 + radius, y1 - radius)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = smoothstep(radius + 1.4, radius - 1.4, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def phase(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr * 255.0, 0, 255).astype(np.uint8), "RGBA")


def save_apng(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stamped = []
    for index, frame in enumerate(frames):
        copy = frame.convert("RGBA")
        pixels = copy.load()
        r, g, b, a = pixels[0, 0]
        pixels[0, 0] = (r, g, b, max(a, 1) if a == 0 else a)
        pixels[1, 0] = (index, 0, FRAMES, 1)
        stamped.append(copy)
    stamped[0].save(
        path,
        save_all=True,
        append_images=stamped[1:],
        duration=[DURATION_MS] * len(stamped),
        loop=0,
        format="PNG",
        disposal=1,
        blend=0,
        compress_level=6,
    )


WORKS = [
    {
        "id": 1,
        "slug": "moonrise",
        "title": "Moonrise Over Still Water",
        "description": "A silver moon climbs a indigo inlet. The water holds the climb a beat later.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Indigo Silver",
            "Motion": "Rise",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 2,
        "slug": "stained-glass",
        "title": "Stained Glass Breath",
        "description": "Jewel panes inhale gold. Lead lines hold while the colors keep changing their mind.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Jewel Gold",
            "Motion": "Pulse",
            "Season": "Dusk",
            "Medium": "APNG",
        },
    },
    {
        "id": 3,
        "slug": "petal-storm",
        "title": "Petal Storm",
        "description": "Blush petals fall through cream light and never quite land.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Blush Cream",
            "Motion": "Fall",
            "Season": "Spring",
            "Medium": "APNG",
        },
    },
    {
        "id": 4,
        "slug": "lighthouse",
        "title": "Lighthouse Sweep",
        "description": "An amber beam turns over navy water. Foam remembers the last pass.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Navy Amber",
            "Motion": "Sweep",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 5,
        "slug": "coral-bloom",
        "title": "Coral Bloom",
        "description": "Anemones open under teal water. A gold fish threads the bloom.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Teal Salmon",
            "Motion": "Bloom",
            "Season": "Tide",
            "Medium": "APNG",
        },
    },
    {
        "id": 6,
        "slug": "neon-dusk",
        "title": "Neon Dusk",
        "description": "A city silhouette holds still while magenta and cyan signs keep arguing.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Magenta Cyan",
            "Motion": "Flicker",
            "Season": "Dusk",
            "Medium": "APNG",
        },
    },
    {
        "id": 7,
        "slug": "firefly-grove",
        "title": "Firefly Grove",
        "description": "Dark pines, a wet floor, and gold specks that refuse a single path.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Forest Gold",
            "Motion": "Drift",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 8,
        "slug": "corona",
        "title": "Corona",
        "description": "A black disc covers the sun. The flare keeps finding new edges.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Black Gold",
            "Motion": "Flare",
            "Season": "Eclipse",
            "Medium": "APNG",
        },
    },
    {
        "id": 9,
        "slug": "koi-mirror",
        "title": "Koi Mirror",
        "description": "Orange and white koi turn under a jade surface. The pond is the painting.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Jade Orange",
            "Motion": "Orbit",
            "Season": "Garden",
            "Medium": "APNG",
        },
    },
    {
        "id": 10,
        "slug": "heat-shimmer",
        "title": "Heat Shimmer",
        "description": "Dunes wait. The air above them will not.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Ochre Sky",
            "Motion": "Shimmer",
            "Season": "Noon",
            "Medium": "APNG",
        },
    },
    {
        "id": 11,
        "slug": "ice-fracture",
        "title": "Ice Fracture",
        "description": "A frozen lake splits. Light travels the crack before the ice does.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Ice Navy",
            "Motion": "Crack",
            "Season": "Winter",
            "Medium": "APNG",
        },
    },
    {
        "id": 12,
        "slug": "nave-light",
        "title": "Nave Light",
        "description": "Stone holds. A honey shaft of dust keeps rewriting the aisle.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Stone Honey",
            "Motion": "Motes",
            "Season": "Afternoon",
            "Medium": "APNG",
        },
    },
    {
        "id": 13,
        "slug": "lantern-rain",
        "title": "Paper Lantern Rain",
        "description": "Warm paper suns hang in a wet street. The rain keeps missing them on purpose.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Cinnabar Night",
            "Motion": "Rain",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 14,
        "slug": "comet-wake",
        "title": "Comet Wake",
        "description": "A pale ember crosses black silk. The wake is longer than the night.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Ice Ember",
            "Motion": "Trail",
            "Season": "Void",
            "Medium": "APNG",
        },
    },
    {
        "id": 15,
        "slug": "tide-pool",
        "title": "Tide Pool",
        "description": "Stone bowls hold the sea for a minute. Starfish keep the minute.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Kelp Sand",
            "Motion": "Ripple",
            "Season": "Tide",
            "Medium": "APNG",
        },
    },
    {
        "id": 16,
        "slug": "aurora-spine",
        "title": "Aurora Spine",
        "description": "A green vertebra of sky. Violet keeps trying the same thought.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Green Violet",
            "Motion": "Curtain",
            "Season": "Winter",
            "Medium": "APNG",
        },
    },
    {
        "id": 17,
        "slug": "candle-window",
        "title": "Candle Window",
        "description": "One room is awake. Moths write circles the house cannot read.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Umber Flame",
            "Motion": "Flicker",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 18,
        "slug": "fog-bell",
        "title": "Fog Bell",
        "description": "A buoy speaks in rings. The fog answers by getting thicker.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Pewter Sage",
            "Motion": "Ring",
            "Season": "Fog",
            "Medium": "APNG",
        },
    },
    {
        "id": 19,
        "slug": "greenhouse-rain",
        "title": "Greenhouse Rain",
        "description": "Glass keeps a summer. Outside, the rain is trying to get in.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Leaf Glass",
            "Motion": "Streak",
            "Season": "Rain",
            "Medium": "APNG",
        },
    },
    {
        "id": 20,
        "slug": "red-giant",
        "title": "Red Giant",
        "description": "An old star takes up the room. The dark around it is patient.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Crimson Coal",
            "Motion": "Breathe",
            "Season": "Void",
            "Medium": "APNG",
        },
    },
    {
        "id": 21,
        "slug": "salt-flats",
        "title": "Salt Flats",
        "description": "The ground is a sky that forgot to stand up. Puddles keep the secret.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Bone Sky",
            "Motion": "Gleam",
            "Season": "Noon",
            "Medium": "APNG",
        },
    },
    {
        "id": 22,
        "slug": "subway-glow",
        "title": "Subway Glow",
        "description": "A tunnel recedes on purpose. Amber lights keep count.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Amber Black",
            "Motion": "Recede",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 23,
        "slug": "whale-breach",
        "title": "Whale Breach",
        "description": "A dark continent of water lifts. Spray writes the return.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Deep Silver",
            "Motion": "Breach",
            "Season": "Tide",
            "Medium": "APNG",
        },
    },
    {
        "id": 24,
        "slug": "harvest-field",
        "title": "Harvest Field",
        "description": "Wheat takes the wind in rows. The sun stays low so the gold can work.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Wheat Dusk",
            "Motion": "Wave",
            "Season": "Harvest",
            "Medium": "APNG",
        },
    },
    {
        "id": 25,
        "slug": "thunderhead",
        "title": "Thunderhead",
        "description": "A bruise of cloud holds the spark. The field waits for the same flash twice.",
        "attributes": {"Series": "Afterimages", "Palette": "Storm Brass", "Motion": "Flash", "Season": "Storm", "Medium": "APNG"},
    },
    {
        "id": 26,
        "slug": "moon-gate",
        "title": "Moon Gate",
        "description": "A round door frames a rounder moon. Stone pretends not to notice.",
        "attributes": {"Series": "Afterimages", "Palette": "Ink Silver", "Motion": "Rise", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 27,
        "slug": "ember-forge",
        "title": "Ember Forge",
        "description": "Coals keep a private sun. Sparks leave without asking.",
        "attributes": {"Series": "Afterimages", "Palette": "Coal Orange", "Motion": "Spark", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 28,
        "slug": "lotus-night",
        "title": "Lotus Night",
        "description": "A pale flower opens on black water. The pond keeps the petals’ secret.",
        "attributes": {"Series": "Afterimages", "Palette": "Pearl Ink", "Motion": "Open", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 29,
        "slug": "clockwork-sky",
        "title": "Clockwork Sky",
        "description": "Orbits pretending to be hours. The sky is late on purpose.",
        "attributes": {"Series": "Afterimages", "Palette": "Brass Night", "Motion": "Turn", "Season": "Void", "Medium": "APNG"},
    },
    {
        "id": 30,
        "slug": "snowbound-cabin",
        "title": "Snowbound Cabin",
        "description": "One chimney writes in white. The rest of the hill is listening.",
        "attributes": {"Series": "Afterimages", "Palette": "Pine Snow", "Motion": "Fall", "Season": "Winter", "Medium": "APNG"},
    },
    {
        "id": 31,
        "slug": "magma-vein",
        "title": "Magma Vein",
        "description": "The rock remembers fire. A crack keeps the memory warm.",
        "attributes": {"Series": "Afterimages", "Palette": "Obsidian Ember", "Motion": "Pulse", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 32,
        "slug": "bamboo-wind",
        "title": "Bamboo Wind",
        "description": "Green columns take the wind in shifts. None of them finish first.",
        "attributes": {"Series": "Afterimages", "Palette": "Jade Mist", "Motion": "Sway", "Season": "Spring", "Medium": "APNG"},
    },
    {
        "id": 33,
        "slug": "harbor-cranes",
        "title": "Harbor Cranes",
        "description": "Steel birds sleep standing. Their eyes blink in amber anyway.",
        "attributes": {"Series": "Afterimages", "Palette": "Rust Sodium", "Motion": "Blink", "Season": "Dusk", "Medium": "APNG"},
    },
    {
        "id": 34,
        "slug": "prism-fall",
        "title": "Prism Fall",
        "description": "White light forgets itself into color. The floor catches every name.",
        "attributes": {"Series": "Afterimages", "Palette": "Spectrum Stone", "Motion": "Fall", "Season": "Afternoon", "Medium": "APNG"},
    },
    {
        "id": 35,
        "slug": "owl-hollow",
        "title": "Owl Hollow",
        "description": "A tree keeps two coins of gold. They open only for the dark.",
        "attributes": {"Series": "Afterimages", "Palette": "Bark Gold", "Motion": "Blink", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 36,
        "slug": "mirage-well",
        "title": "Mirage Well",
        "description": "A circle of water that may not be water. The air argues both ways.",
        "attributes": {"Series": "Afterimages", "Palette": "Sand Cyan", "Motion": "Wobble", "Season": "Noon", "Medium": "APNG"},
    },
    {
        "id": 37,
        "slug": "vinyl-groove",
        "title": "Vinyl Groove",
        "description": "A black sun with a silver path. It turns so the quiet can last.",
        "attributes": {"Series": "Afterimages", "Palette": "Obsidian Chrome", "Motion": "Spin", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 38,
        "slug": "bridge-fog",
        "title": "Bridge Fog",
        "description": "Cables hold a city that the fog has borrowed. Lights remain as IOUs.",
        "attributes": {"Series": "Afterimages", "Palette": "Pearl Steel", "Motion": "Drift", "Season": "Fog", "Medium": "APNG"},
    },
    {
        "id": 39,
        "slug": "radio-tower",
        "title": "Radio Tower",
        "description": "A thin needle talks to nowhere. The blink is the whole sentence.",
        "attributes": {"Series": "Afterimages", "Palette": "Night Red", "Motion": "Beacon", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 40,
        "slug": "glacier-blue",
        "title": "Glacier Blue",
        "description": "A wall of old weather. Melt writes a slow signature.",
        "attributes": {"Series": "Afterimages", "Palette": "Ice Teal", "Motion": "Drip", "Season": "Winter", "Medium": "APNG"},
    },
    {
        "id": 41,
        "slug": "sunflower-tilt",
        "title": "Sunflower Tilt",
        "description": "Heads follow a sun that already left. They keep the habit anyway.",
        "attributes": {"Series": "Afterimages", "Palette": "Gold Leaf", "Motion": "Nod", "Season": "Harvest", "Medium": "APNG"},
    },
    {
        "id": 42,
        "slug": "ink-bloom",
        "title": "Ink Bloom",
        "description": "A drop decides to become a garden. Paper has no vote.",
        "attributes": {"Series": "Afterimages", "Palette": "Sumi Cream", "Motion": "Bloom", "Season": "Afternoon", "Medium": "APNG"},
    },
    {
        "id": 43,
        "slug": "terrace-lights",
        "title": "Terrace Lights",
        "description": "A hillside of small gold rooms. Each one keeps a different hour.",
        "attributes": {"Series": "Afterimages", "Palette": "Umber Gold", "Motion": "Twinkle", "Season": "Dusk", "Medium": "APNG"},
    },
    {
        "id": 44,
        "slug": "meteor-choir",
        "title": "Meteor Choir",
        "description": "Many brief lines share one sky. None of them stay for the encore.",
        "attributes": {"Series": "Afterimages", "Palette": "Ash White", "Motion": "Streak", "Season": "Void", "Medium": "APNG"},
    },
    {
        "id": 45,
        "slug": "orchid-house",
        "title": "Orchid House",
        "description": "A magenta thought in still air. The glass around it fogs on the beat.",
        "attributes": {"Series": "Afterimages", "Palette": "Magenta Fog", "Motion": "Breathe", "Season": "Garden", "Medium": "APNG"},
    },
    {
        "id": 46,
        "slug": "night-pier",
        "title": "Night Pier",
        "description": "Planks walk out over black glass. Lamps practice being moons.",
        "attributes": {"Series": "Afterimages", "Palette": "Teak Gold", "Motion": "Shimmer", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 47,
        "slug": "copper-storm",
        "title": "Copper Storm",
        "description": "Clouds rust in place. Lightning is only a rumor they keep repeating.",
        "attributes": {"Series": "Afterimages", "Palette": "Verdigris Copper", "Motion": "Rumble", "Season": "Storm", "Medium": "APNG"},
    },
    {
        "id": 48,
        "slug": "quiet-orbit",
        "title": "Quiet Orbit",
        "description": "A small moon keeps a larger promise. The dark is the agreement.",
        "attributes": {"Series": "Afterimages", "Palette": "Slate Gold", "Motion": "Orbit", "Season": "Void", "Medium": "APNG"},
    },
    {
        "id": 49,
        "slug": "train-signal",
        "title": "Train Signal",
        "description": "Red and green take turns at being the future. The rails do not care.",
        "attributes": {"Series": "Afterimages", "Palette": "Signal Night", "Motion": "Switch", "Season": "Night", "Medium": "APNG"},
    },
    {
        "id": 50,
        "slug": "last-firefly",
        "title": "Last Firefly",
        "description": "One gold thought left in a dark meadow. It refuses to land.",
        "attributes": {"Series": "Afterimages", "Palette": "Meadow Gold", "Motion": "Drift", "Season": "Night", "Medium": "APNG"},
    },
]


def paint_moonrise(frame: int) -> np.ndarray:
    t = phase(frame)
    moon_y = 168.0 - 22.0 * math.sin(t)
    dst = vertical_wash(rgb("#0b1028"), rgb("#1a2748"), 0.85)
    glow(dst, 320, moon_y, 140, rgb("#c9d7ff"), 0.28)
    disc(dst, 320, moon_y, 54, rgb("#f4f1ff"), 0.96, soft=3)
    disc(dst, 308, moon_y - 8, 16, rgb("#d7deef"), 0.35, soft=4)
    xx, yy = grid()
    horizon = 390.0 + 4.0 * np.sin(xx / 40.0 + t)
    water = blank()
    water[..., :3] = mix(rgb("#10243a"), rgb("#0a1628"), (yy - 390) / 250)
    water[..., 3] = smoothstep(horizon - 8, horizon + 4, yy)
    over(dst, water)
    for i in range(18):
        ripple_y = 430 + i * 12 + 3 * math.sin(t + i * 0.4)
        ellipse(dst, 320, ripple_y, 90 + i * 12, 5 + i * 0.4, rgb("#c9d7ff"), 0.07 + 0.02 * math.sin(t + i))
    glow(dst, 320, 430, 90, rgb("#e8eeff"), 0.18 + 0.06 * math.sin(t))
    return dst


def paint_stained_glass(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a1020"), rgb("#0d0a12"))
    rect(dst, 90, 40, 550, 600, rgb("#2a1c14"), 1.0, radius=18)
    panes = [
        (140, 90, 300, 250, "#7a1f4a"),
        (320, 90, 500, 250, "#1d4e89"),
        (140, 270, 300, 430, "#c9a227"),
        (320, 270, 500, 430, "#2f6b4f"),
        (140, 450, 300, 580, "#8b3d1b"),
        (320, 450, 500, 580, "#5c2d8a"),
    ]
    for i, (x0, y0, x1, y1, color) in enumerate(panes):
        pulse = 0.72 + 0.22 * math.sin(t + i * 0.9)
        rect(dst, x0, y0, x1, y1, rgb(color), pulse, radius=8)
        glow(dst, (x0 + x1) / 2, (y0 + y1) / 2, 70, rgb(color), 0.16 * pulse)
    for x in (140, 300, 320, 500):
        rect(dst, x - 6, 80, x + 6, 590, rgb("#3a2a1c"), 0.95)
    for y in (90, 250, 270, 430, 450, 580):
        rect(dst, 130, y - 6, 510, y + 6, rgb("#3a2a1c"), 0.95)
    glow(dst, 320, 300, 180, rgb("#f0d48a"), 0.12 + 0.08 * math.sin(t))
    return dst


def paint_petal_storm(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#f7e6d8"), rgb("#e8b8b0"), 0.7)
    glow(dst, 480, 90, 180, rgb("#fff6ea"), 0.45)
    disc(dst, 500, 70, 46, rgb("#fff4d8"), 0.9)
    rng = np.random.default_rng(31)
    for i in range(42):
        seed = rng.random(4)
        x = (seed[0] * W + 90 * math.sin(t + i) + 40 * i) % (W + 80) - 40
        y = (seed[1] * H + (frame * 18 + i * 21)) % (H + 60) - 30
        rot = 10 + 8 * math.sin(t + i)
        ellipse(dst, x, y, rot, rot * 0.45, mix(rgb("#e37a8a"), rgb("#f4c4b0"), seed[2]), 0.55 + 0.25 * seed[3])
    glow(dst, 200, 520, 160, rgb("#f0c8c0"), 0.2)
    return dst


def paint_lighthouse(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#07101f"), rgb("#15243a"))
    angle = t
    xx, yy = grid()
    beam_x = 430 + math.cos(angle) * 220
    beam_y = 250 + math.sin(angle) * 40
    glow(dst, beam_x, beam_y, 160, rgb("#f2c15a"), 0.22)
    # cliff
    cliff = blank()
    cliff_edge = 430 + 18 * np.sin(xx / 50.0)
    cliff[..., :3] = rgb("#1b2230")
    cliff[..., 3] = smoothstep(cliff_edge - 10, cliff_edge + 20, yy) * (xx < 280).astype(np.float32)
    over(dst, cliff)
    water = blank()
    water[..., :3] = mix(rgb("#10263d"), rgb("#08141f"), (yy - 420) / 220)
    water[..., 3] = smoothstep(470, 500, yy)
    over(dst, water)
    rect(dst, 168, 210, 232, 470, rgb("#d8d2c4"), 1.0, radius=6)
    rect(dst, 156, 188, 244, 230, rgb("#efe6d2"), 1.0, radius=8)
    glow(dst, 200, 208, 36, rgb("#ffe39a"), 0.7 + 0.2 * math.sin(t * 2))
    disc(dst, 200, 208, 10, rgb("#fff6d2"), 0.95)
    for i in range(10):
        ellipse(dst, 360 + i * 28, 520 + 6 * math.sin(t + i), 22, 5, rgb("#e8f0ff"), 0.12)
    return dst


def paint_coral_bloom(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#083246"), rgb("#0b1c28"), 0.6)
    glow(dst, 320, 80, 200, rgb("#3aa7b8"), 0.18)
    for i, (cx, cy, color) in enumerate(
        ((180, 470, "#e07a5f"), (260, 510, "#f2a65a"), (400, 490, "#d66853"), (480, 450, "#f4b183"))
    ):
        open_amt = 18 + 10 * (0.5 + 0.5 * math.sin(t + i))
        glow(dst, cx, cy, 70, rgb(color), 0.22)
        for k in range(7):
            ang = k * (math.pi / 6) - math.pi / 2 + 0.15 * math.sin(t)
            ellipse(dst, cx + math.cos(ang) * open_amt, cy + math.sin(ang) * open_amt * 0.7, 16, 28, rgb(color), 0.8)
        disc(dst, cx, cy + 8, 14, rgb("#f6d7b0"), 0.85)
    fish_x = 200 + 180 * math.sin(t)
    fish_y = 240 + 30 * math.cos(t * 2)
    ellipse(dst, fish_x, fish_y, 22, 10, rgb("#f0c14a"), 0.95)
    ellipse(dst, fish_x - 18, fish_y, 8, 8, rgb("#f0c14a"), 0.8)
    # bubbles
    for i in range(8):
        bx = 140 + i * 50
        by = (520 - (frame * 8 + i * 37) % 420)
        disc(dst, bx, by, 4 + i % 3, rgb("#d7f3f6"), 0.28)
    return dst


def paint_neon_dusk(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a0a24"), rgb("#0a0612"), 0.9)
    glow(dst, 320, 180, 220, rgb("#ff4d8d"), 0.16 + 0.06 * math.sin(t))
    glow(dst, 480, 220, 160, rgb("#3ee0ff"), 0.14 + 0.06 * math.cos(t))
    heights = [220, 280, 190, 310, 240, 200, 270, 230]
    x = 40
    for i, h in enumerate(heights):
        rect(dst, x, 640 - h, x + 70, 620, rgb("#120c18"), 0.96)
        window_on = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(t * 2 + i * 1.3))
        for wy in range(640 - h + 16, 600, 22):
            rect(dst, x + 12, wy, x + 28, wy + 10, rgb("#3ee0ff"), 0.15 + 0.45 * window_on)
            rect(dst, x + 40, wy, x + 56, wy + 10, rgb("#ff4d8d"), 0.12 + 0.4 * (1 - window_on * 0.5))
        x += 76
    rect(dst, 0, 610, 640, 640, rgb("#08060c"), 1.0)
    rect(dst, 210, 300, 250, 318, rgb("#ff4d8d"), 0.55 + 0.4 * (0.5 + 0.5 * math.sin(t * 4)))
    rect(dst, 400, 340, 470, 356, rgb("#3ee0ff"), 0.5 + 0.4 * (0.5 + 0.5 * math.cos(t * 3)))
    return dst


def paint_firefly_grove(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#06140f"), rgb("#0a1c14"))
    for i, x0 in enumerate((40, 160, 300, 430, 540)):
        trunk_x = x0 + 20
        rect(dst, trunk_x, 280, trunk_x + 22, 600, rgb("#1a2a1c"), 0.95)
        glow(dst, trunk_x + 10, 240, 80, rgb("#14301c"), 0.5)
        ellipse(dst, trunk_x + 8, 220, 70 + 8 * math.sin(t + i), 90, rgb("#102418"), 0.7)
    glow(dst, 320, 520, 220, rgb("#0d2618"), 0.35)
    rng = np.random.default_rng(77)
    for i in range(28):
        seed = rng.random(3)
        x = 60 + seed[0] * 520 + 18 * math.sin(t + i * 0.7)
        y = 80 + seed[1] * 460 + 12 * math.cos(t * 1.2 + i)
        pulse = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(t * 2 + i * 0.8))
        glow(dst, x, y, 10 + 6 * pulse, rgb("#f4e07a"), 0.55 * pulse)
        disc(dst, x, y, 2.4, rgb("#fff6b0"), 0.9 * pulse)
    return dst


def paint_corona(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#07060a"), rgb("#120c14"))
    xx, yy = grid()
    ang = np.arctan2(yy - 320, xx - 320)
    dist = np.sqrt((xx - 320) ** 2 + (yy - 320) ** 2)
    rays = 0.5 + 0.5 * np.cos(ang * 14 + t)
    flare = np.exp(-0.5 * ((dist - 110) / 70) ** 2) * (0.35 + 0.25 * rays)
    layer = blank()
    layer[..., :3] = mix(rgb("#f6d27a"), rgb("#c084fc"), 0.5 + 0.5 * np.sin(ang * 3 + t))
    layer[..., 3] = flare
    over(dst, layer)
    glow(dst, 320, 320, 160, rgb("#ffe9a8"), 0.28 + 0.08 * math.sin(t))
    disc(dst, 320, 320, 92, rgb("#050406"), 1.0, soft=2)
    disc(dst, 320, 320, 88, rgb("#0a0810"), 0.9)
    return dst


def paint_koi_mirror(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#12382c"), rgb("#0c241c"))
    glow(dst, 320, 200, 220, rgb("#3d8b6e"), 0.2)
    ellipse(dst, 320, 340, 260, 180, rgb("#0e2f26"), 0.9)
    ellipse(dst, 320, 340, 240, 160, rgb("#164a3a"), 0.55)
    for i, (amp, color, scale) in enumerate(((1.0, "#e76f3c", 1.0), (-1.0, "#f4efe6", 0.82), (0.4, "#d3542c", 0.7))):
        x = 320 + amp * 110 * math.cos(t + i)
        y = 340 + 70 * math.sin(t + i * 1.3)
        ellipse(dst, x, y, 28 * scale, 12 * scale, rgb(color), 0.92)
        ellipse(dst, x - 16 * amp, y, 10 * scale, 8 * scale, rgb(color), 0.7)
        disc(dst, x + 10 * amp, y - 2, 3, rgb("#1a1a1a"), 0.8)
    for i in range(6):
        lily_x = 180 + i * 70
        lily_y = 250 + 20 * math.sin(t + i)
        ellipse(dst, lily_x, lily_y, 22, 10, rgb("#2f6b45"), 0.7)
    glow(dst, 420, 220, 70, rgb("#d7ffe8"), 0.12 + 0.06 * math.sin(t))
    return dst


def paint_heat_shimmer(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#f2d3a2"), rgb("#c9844a"), 0.55)
    glow(dst, 480, 90, 160, rgb("#fff1c8"), 0.5)
    disc(dst, 500, 86, 38, rgb("#fff6d2"), 0.95)
    xx, yy = grid()
    dune = 420 + 28 * np.sin(xx / 70.0 + 0.4) + 10 * np.sin(xx / 28.0)
    sand = blank()
    sand[..., :3] = mix(rgb("#e0a56a"), rgb("#a65b2b"), (yy - 400) / 240)
    sand[..., 3] = smoothstep(dune - 8, dune + 10, yy)
    over(dst, sand)
    dune2 = 500 + 18 * np.sin(xx / 50.0 + 1.2)
    sand2 = blank()
    sand2[..., :3] = rgb("#8d4320")
    sand2[..., 3] = smoothstep(dune2 - 6, dune2 + 12, yy) * 0.85
    over(dst, sand2)
    wave = 0.08 + 0.06 * np.sin(xx / 16.0 + t * 2 + yy / 40.0)
    haze = blank()
    haze[..., :3] = rgb("#fff4d8")
    haze[..., 3] = ((yy > 240) & (yy < 430)).astype(np.float32) * wave
    over(dst, haze)
    return dst


def paint_ice_fracture(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0b1730"), rgb("#16324f"))
    glow(dst, 320, 180, 200, rgb("#9ad4ff"), 0.16)
    ellipse(dst, 320, 400, 280, 150, rgb("#9ec9e6"), 0.55)
    ellipse(dst, 320, 400, 250, 130, rgb("#d7eef8"), 0.35)
    progress = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t))
    xx, yy = grid()
    crack_x = 200 + (yy - 280) * 0.35
    dist = np.abs(xx - crack_x)
    near = (yy > 260) & (yy < 280 + 240 * progress)
    layer = blank()
    layer[..., :3] = rgb("#f4fbff")
    layer[..., 3] = near.astype(np.float32) * smoothstep(10, 1.2, dist) * 0.9
    over(dst, layer)
    glow(dst, 320, 360, 80, rgb("#b9e7ff"), 0.18 * progress)
    for i in range(5):
        bx = 180 + i * 70
        by = 300 + 40 * i
        if by < 280 + 240 * progress:
            glow(dst, bx, by, 18, rgb("#e8f6ff"), 0.35)
    return dst


def paint_nave_light(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#2a241c"), rgb("#16130f"))
    rect(dst, 40, 0, 160, 640, rgb("#3a3328"), 0.7)
    rect(dst, 480, 0, 600, 640, rgb("#3a3328"), 0.7)
    for i, x in enumerate((80, 200, 440, 560)):
        rect(dst, x - 16, 80, x + 16, 620, rgb("#4a4032"), 0.85)
        arch_y = 120
        glow(dst, x, arch_y, 40, rgb("#2a241c"), 0.4)
    shaft_x = 320 + 10 * math.sin(t)
    xx, yy = grid()
    left = shaft_x - 36 - yy * 0.02
    right = shaft_x + 36 + yy * 0.02
    shaft = ((xx > left) & (xx < right) & (yy > 40)).astype(np.float32)
    layer = blank()
    layer[..., :3] = rgb("#f0c878")
    layer[..., 3] = shaft * (0.12 + 0.08 * (1.0 - yy / H))
    over(dst, layer)
    glow(dst, shaft_x, 180, 90, rgb("#f6d48a"), 0.2 + 0.06 * math.sin(t))
    rng = np.random.default_rng(12)
    for i in range(30):
        seed = rng.random(3)
        x = shaft_x - 40 + seed[0] * 80 + 6 * math.sin(t + i)
        y = (40 + seed[1] * 560 + frame * 4 + i * 11) % 600
        disc(dst, x, y, 1.6, rgb("#fff3c8"), 0.35 + 0.35 * seed[2])
    rect(dst, 80, 560, 560, 640, rgb("#1c1812"), 0.9)
    glow(dst, shaft_x, 560, 70, rgb("#f0c878"), 0.16)
    return dst


def paint_lantern_rain(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a0c14"), rgb("#0c0810"))
    rect(dst, 0, 500, 640, 640, rgb("#1a1218"), 0.95)
    lanterns = ((160, 210, "#e85d4c"), (320, 160, "#f0a05a"), (470, 230, "#d94a3a"), (250, 280, "#f4c07a"))
    for i, (cx, cy, color) in enumerate(lanterns):
        bob_y = cy + 6 * math.sin(t + i * 0.8)
        glow(dst, cx, bob_y, 48, rgb(color), 0.28 + 0.08 * math.sin(t + i))
        ellipse(dst, cx, bob_y, 22, 28, rgb(color), 0.92)
        rect(dst, cx - 2, 40, cx + 2, bob_y - 26, rgb("#3a2a22"), 0.7)
        disc(dst, cx, bob_y + 28, 4, rgb("#f6d7a0"), 0.6)
        ellipse(dst, cx, 530, 18, 5, rgb(color), 0.18 + 0.08 * math.sin(t + i))
    rng = np.random.default_rng(19)
    for i in range(40):
        seed = rng.random(2)
        x = seed[0] * W
        y = (seed[1] * H + frame * 22 + i * 13) % (H + 20) - 10
        rect(dst, x, y, x + 1.4, y + 14, rgb("#c8d4e8"), 0.28)
    return dst


def paint_comet_wake(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#07060c"), rgb("#100c18"))
    rng = np.random.default_rng(4)
    for i in range(24):
        seed = rng.random(3)
        disc(dst, 40 + seed[0] * 560, 40 + seed[1] * 400, 1.2 + seed[2] * 1.6, rgb("#e8eef8"), 0.35 + 0.4 * seed[2])
    progress = (frame / FRAMES)
    cx = 80 + progress * 520
    cy = 140 + 80 * math.sin(t * 0.5)
    for k in range(10):
        back = k * 22
        glow(dst, cx - back, cy + back * 0.18, 18 + k * 3, mix(rgb("#9ad4ff"), rgb("#f6b27a"), k / 10), 0.22 - k * 0.015)
    glow(dst, cx, cy, 40, rgb("#fff4d8"), 0.55)
    disc(dst, cx, cy, 8, rgb("#fff8ee"), 0.95)
    return dst


def paint_tide_pool(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#c9b08a"), rgb("#8a6a48"), 0.7)
    glow(dst, 480, 80, 140, rgb("#f4e6c8"), 0.3)
    pools = ((180, 280, 90, 40), (360, 360, 110, 48), (250, 470, 70, 28), (470, 250, 60, 26))
    for i, (cx, cy, rx, ry) in enumerate(pools):
        ellipse(dst, cx, cy, rx, ry, rgb("#1d4a4a"), 0.85)
        pulse = 0.2 + 0.12 * math.sin(t + i)
        ellipse(dst, cx, cy, rx * (0.72 + pulse * 0.1), ry * (0.65 + pulse * 0.1), rgb("#3a8a86"), 0.55)
        ellipse(dst, cx - 10, cy - 6, 12, 5, rgb("#d7f3ee"), 0.25 + 0.1 * math.sin(t + i))
    for i, (cx, cy) in enumerate(((220, 300), (400, 380), (280, 490))):
        ang = t + i
        for k in range(5):
            a = ang + k * (math.pi * 0.4)
            ellipse(dst, cx + math.cos(a) * 16, cy + math.sin(a) * 10, 7, 4, rgb("#d3542c"), 0.85)
        disc(dst, cx, cy, 5, rgb("#f0c14a"), 0.8)
    return dst


def paint_aurora_spine(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#071018"), rgb("#0c1c22"))
    xx, yy = grid()
    for i, color in enumerate(("#49d17c", "#7af0c2", "#c084fc")):
        shift = 40 * math.sin(t + i * 0.9)
        spine = 260 + i * 50 + shift + 18 * np.sin(yy / 28.0 + t + i)
        dist = np.abs(xx - spine)
        width = 28 + 10 * np.sin(yy / 40.0 + t)
        a = np.exp(-0.5 * (dist / np.maximum(width, 6)) ** 2) * (0.22 + 0.1 * (1.0 - yy / H))
        layer = blank()
        layer[..., :3] = rgb(color)
        layer[..., 3] = a * (yy < 520).astype(np.float32)
        over(dst, layer)
    rect(dst, 0, 500, 640, 640, rgb("#0a1418"), 0.9)
    rng = np.random.default_rng(22)
    for i in range(20):
        seed = rng.random(2)
        disc(dst, seed[0] * W, 80 + seed[1] * 380, 1.4, rgb("#e8fff4"), 0.35)
    return dst


def paint_candle_window(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#10182a"), rgb("#0a1018"))
    rect(dst, 180, 220, 460, 560, rgb("#1a1614"), 0.96, radius=6)
    rect(dst, 160, 200, 480, 230, rgb("#241c18"), 0.95)
    flicker = 0.55 + 0.35 * (0.5 + 0.5 * math.sin(t * 3))
    rect(dst, 280, 300, 360, 400, rgb("#f2c15a"), flicker, radius=4)
    glow(dst, 320, 350, 70, rgb("#f6d27a"), 0.25 * flicker)
    disc(dst, 320, 368, 5, rgb("#fff1c0"), flicker)
    for i in range(6):
        ang = t * 2 + i * 1.1
        mx = 320 + math.cos(ang) * (28 + 8 * math.sin(t + i))
        my = 330 + math.sin(ang * 1.3) * 22
        ellipse(dst, mx, my, 5, 2.4, rgb("#d8c8b0"), 0.7)
    rect(dst, 0, 560, 640, 640, rgb("#0c1014"), 1.0)
    return dst


def paint_fog_bell(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#9aa8a4"), rgb("#6a7874"), 0.8)
    glow(dst, 320, 200, 180, rgb("#d7e4de"), 0.25)
    ring = 0.2 + 0.8 * ((frame % FRAMES) / FRAMES)
    for k in range(4):
        r = 40 + (ring * 140 + k * 28) % 180
        ellipse(dst, 320, 300, r, r * 0.35, rgb("#e8f0ea"), 0.12)
    ellipse(dst, 320, 300, 36, 44, rgb("#3a403c"), 0.92)
    ellipse(dst, 320, 292, 22, 16, rgb("#4a524c"), 0.9)
    disc(dst, 320, 348, 6, rgb("#2a302c"), 0.9)
    rect(dst, 314, 348, 326, 430, rgb("#2a302c"), 0.9)
    ellipse(dst, 320, 500, 90, 18, rgb("#5a6864"), 0.5)
    glow(dst, 320, 280, 50, rgb("#f0f6f2"), 0.1 + 0.08 * math.sin(t * 2))
    return dst


def paint_greenhouse_rain(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#d8e8d0"), rgb("#8fb88a"))
    glow(dst, 320, 240, 180, rgb("#f4e8b0"), 0.22)
    rect(dst, 90, 80, 550, 560, rgb("#c5e0c0"), 0.35, radius=8)
    for x in (90, 210, 320, 430, 550):
        rect(dst, x - 3, 80, x + 3, 560, rgb("#d7efe0"), 0.55)
    for y in (80, 220, 360, 560):
        rect(dst, 90, y - 3, 550, y + 3, rgb("#d7efe0"), 0.5)
    for i, (cx, cy) in enumerate(((200, 420), (320, 390), (440, 430))):
        ellipse(dst, cx, cy, 40, 22, rgb("#2f6b45"), 0.7)
        glow(dst, cx, cy - 20, 30, rgb("#49a36a"), 0.25)
        disc(dst, cx, cy - 8, 16 + 3 * math.sin(t + i), rgb("#3d8b6e"), 0.8)
    rng = np.random.default_rng(8)
    for i in range(36):
        seed = rng.random(2)
        x = 100 + seed[0] * 440
        y = (80 + seed[1] * 480 + frame * 16) % 500
        rect(dst, x, y, x + 1.2, y + 16, rgb("#e8f4ee"), 0.4)
    return dst


def paint_red_giant(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#12060a"), rgb("#1a0a0c"))
    scale = 1.0 + 0.06 * math.sin(t)
    glow(dst, 300, 340, 220 * scale, rgb("#e85d4c"), 0.28 + 0.08 * math.sin(t))
    glow(dst, 300, 340, 140 * scale, rgb("#f2a65a"), 0.22)
    disc(dst, 300, 340, 110 * scale, rgb("#c43c2e"), 0.95, soft=6)
    disc(dst, 270, 310, 36, rgb("#e07a5f"), 0.35, soft=10)
    disc(dst, 300, 340, 70 * scale, rgb("#8b1e18"), 0.25)
    rng = np.random.default_rng(2)
    for i in range(16):
        seed = rng.random(3)
        disc(dst, 40 + seed[0] * 560, 40 + seed[1] * 240, 1.3, rgb("#f4d0c8"), 0.25 + 0.3 * seed[2])
    return dst


def paint_salt_flats(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#c9d8e8"), rgb("#e8e0d0"), 0.45)
    glow(dst, 480, 90, 150, rgb("#fff6e0"), 0.4)
    disc(dst, 500, 80, 32, rgb("#fff8e8"), 0.95)
    xx, yy = grid()
    flats = blank()
    flats[..., :3] = mix(rgb("#f4efe6"), rgb("#d8cfc2"), (yy - 280) / 360)
    flats[..., 3] = smoothstep(270, 300, yy)
    over(dst, flats)
    for i in range(8):
        crack_x = 80 + i * 70
        rect(dst, crack_x, 320 + 10 * math.sin(t + i), crack_x + 1.5, 620, rgb("#c4b8a8"), 0.35)
    for i in range(5):
        px = 140 + i * 90
        py = 400 + 20 * math.sin(t * 0.7 + i)
        ellipse(dst, px, py, 36, 8, rgb("#b8cce0"), 0.22 + 0.1 * math.sin(t + i))
        ellipse(dst, px, py, 18, 4, rgb("#f4f8ff"), 0.18)
    return dst


def paint_subway_glow(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0c0a0c"), rgb("#161214"))
    for i in range(9):
        scale = 1.0 - i * 0.08
        w = 520 * scale
        h = 360 * scale
        x0 = 320 - w / 2
        y0 = 80 + i * 28
        rect(dst, x0, y0, x0 + w, y0 + h, rgb("#1a1618"), 0.18)
        pulse = 0.35 + 0.55 * (0.5 + 0.5 * math.sin(t * 2 + i * 0.6))
        rect(dst, x0 + 16, y0 + h * 0.35, x0 + 28, y0 + h * 0.38, rgb("#f2c15a"), pulse)
        rect(dst, x0 + w - 28, y0 + h * 0.35, x0 + w - 16, y0 + h * 0.38, rgb("#f2c15a"), pulse)
    glow(dst, 320, 420, 90, rgb("#f0c878"), 0.12 + 0.06 * math.sin(t))
    rect(dst, 0, 520, 640, 640, rgb("#0a080a"), 0.95)
    return dst


def paint_whale_breach(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#8ec4d8"), rgb("#1a4a62"), 0.7)
    glow(dst, 500, 70, 120, rgb("#fff4d0"), 0.35)
    disc(dst, 520, 70, 28, rgb("#fff6dc"), 0.9)
    lift = 40 * math.sin(t)
    ellipse(dst, 300, 360 - lift, 130, 46, rgb("#1b2a36"), 0.95)
    ellipse(dst, 220, 340 - lift, 36, 22, rgb("#1b2a36"), 0.9)
    disc(dst, 190, 332 - lift, 7, rgb("#0e1620"), 0.85)
    ellipse(dst, 360, 348 - lift, 18, 10, rgb("#3a5164"), 0.5)
    water = blank()
    xx, yy = grid()
    water[..., :3] = mix(rgb("#2a6a82"), rgb("#123848"), (yy - 380) / 260)
    water[..., 3] = smoothstep(400, 430, yy)
    over(dst, water)
    for i in range(12):
        sx = 240 + i * 18 + 8 * math.sin(t + i)
        sy = 390 - lift * 0.4 - (i % 4) * 10
        disc(dst, sx, sy, 3 + i % 3, rgb("#d7eef8"), 0.35)
    return dst


def paint_harvest_field(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#f2c48a"), rgb("#c9844a"), 0.55)
    glow(dst, 120, 90, 140, rgb("#fff1c0"), 0.45)
    disc(dst, 110, 90, 34, rgb("#ffe39a"), 0.95)
    xx, yy = grid()
    for i in range(7):
        band_y = 280 + i * 48
        wave = 10 * np.sin(xx / 36.0 + t + i * 0.4)
        field = blank()
        field[..., :3] = mix(rgb("#e0a54a"), rgb("#8d5a18"), i / 7)
        field[..., 3] = smoothstep(band_y + wave - 16, band_y + wave + 18, yy) * 0.55
        over(dst, field)
    for i in range(3):
        bx = 420 + i * 50
        by = 160 + 12 * math.sin(t * 2 + i)
        ellipse(dst, bx, by, 8, 4, rgb("#2a2018"), 0.8)
    return dst


def paint_thunderhead(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a2438"), rgb("#2a2018"), 0.8)
    xx, yy = grid()
    cloud = blank()
    cloud[..., :3] = rgb("#3a4458")
    cloud[..., 3] = np.exp(-0.5 * (((xx - 320) / 180) ** 2 + ((yy - 180) / 70) ** 2)) * 0.85
    over(dst, cloud)
    flash = 0.15 + 0.75 * max(0.0, math.sin(t * 4))
    glow(dst, 300, 260, 90, rgb("#f4e6a8"), flash)
    rect(dst, 292, 250, 308, 420, rgb("#fff6c8"), flash * 0.8)
    rect(dst, 0, 480, 640, 640, rgb("#1c1810"), 0.95)
    return dst


def paint_moon_gate(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a1020"), rgb("#0c0812"))
    moon_y = 240 - 12 * math.sin(t)
    glow(dst, 320, moon_y, 90, rgb("#d7deef"), 0.3)
    disc(dst, 320, moon_y, 48, rgb("#f4f1ff"), 0.95)
    ellipse(dst, 320, 360, 150, 150, rgb("#2a1c18"), 0.0)
    # gate ring
    xx, yy = grid()
    d = np.sqrt((xx - 320) ** 2 + (yy - 360) ** 2)
    ring = blank()
    ring[..., :3] = rgb("#3a2a22")
    ring[..., 3] = (smoothstep(148, 132, d) * smoothstep(110, 126, d)).astype(np.float32) * 0.95
    over(dst, ring)
    rect(dst, 0, 500, 640, 640, rgb("#161014"), 0.9)
    return dst


def paint_ember_forge(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#140c0a"), rgb("#0a0606"))
    glow(dst, 320, 420, 160, rgb("#e85d4c"), 0.3 + 0.1 * math.sin(t * 2))
    for i in range(8):
        glow(dst, 220 + i * 28, 460 + 8 * math.sin(t + i), 22, rgb("#f2a65a"), 0.4)
        disc(dst, 220 + i * 28, 468, 10, rgb("#c43c2e"), 0.8)
    rng = np.random.default_rng(5)
    for i in range(22):
        seed = rng.random(2)
        x = 180 + seed[0] * 280
        y = (200 + seed[1] * 280 - frame * 10) % 360 + 80
        disc(dst, x, y, 1.8, rgb("#ffe39a"), 0.5)
    return dst


def paint_lotus_night(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0a1420"), rgb("#081018"))
    ellipse(dst, 320, 400, 220, 80, rgb("#0c2430"), 0.8)
    open_amt = 28 + 14 * (0.5 + 0.5 * math.sin(t))
    for k in range(8):
        ang = k * (math.pi / 4) - math.pi / 2
        ellipse(dst, 320 + math.cos(ang) * open_amt, 340 + math.sin(ang) * open_amt * 0.55, 18, 32, rgb("#f4e8e0"), 0.88)
    disc(dst, 320, 340, 16, rgb("#e8c14a"), 0.9)
    glow(dst, 320, 340, 50, rgb("#fff4d8"), 0.18)
    ellipse(dst, 320, 430, 40, 8, rgb("#c9d7ff"), 0.15 + 0.08 * math.sin(t))
    return dst


def paint_clockwork_sky(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0c1018"), rgb("#161018"))
    for i, r in enumerate((90, 140, 190, 250)):
        ang = t * (1.2 - i * 0.2)
        ellipse(dst, 320, 300, r, r, rgb("#c9a227"), 0.08)
        disc(dst, 320 + math.cos(ang) * r, 300 + math.sin(ang) * r, 8, rgb("#f0c878"), 0.85)
    disc(dst, 320, 300, 18, rgb("#f4e6b0"), 0.9)
    return dst


def paint_snowbound_cabin(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a2438"), rgb("#c9d4e0"), 1.4)
    rect(dst, 0, 420, 640, 640, rgb("#d8e4ee"), 0.95)
    rect(dst, 240, 300, 400, 430, rgb("#2a2018"), 0.95)
    rect(dst, 220, 270, 420, 310, rgb("#3a2a1c"), 0.95)
    glow(dst, 280, 350, 24, rgb("#f2c15a"), 0.45 + 0.2 * math.sin(t * 2))
    rect(dst, 268, 338, 292, 362, rgb("#f0c878"), 0.7)
    rect(dst, 330, 250, 348, 300, rgb("#1a1410"), 0.9)
    glow(dst, 339, 230, 16, rgb("#e8eef4"), 0.25)
    rng = np.random.default_rng(9)
    for i in range(36):
        seed = rng.random(2)
        x = seed[0] * W
        y = (seed[1] * H + frame * 8) % H
        disc(dst, x, y, 1.6, rgb("#ffffff"), 0.45)
    return dst


def paint_magma_vein(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#120c0c"), rgb("#1a1010"))
    xx, yy = grid()
    vein_x = 220 + (yy - 80) * 0.25 + 8 * np.sin(yy / 30.0 + t)
    dist = np.abs(xx - vein_x)
    pulse = 0.45 + 0.35 * (0.5 + 0.5 * math.sin(t * 2))
    layer = blank()
    layer[..., :3] = rgb("#e85d4c")
    layer[..., 3] = smoothstep(16, 3, dist) * pulse
    over(dst, layer)
    glow(dst, 320, 360, 80, rgb("#f2a65a"), 0.16 * pulse)
    return dst


def paint_bamboo_wind(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#d7ead0"), rgb("#8fb88a"))
    for i, x0 in enumerate((80, 160, 250, 340, 430, 520)):
        sway = 12 * math.sin(t + i * 0.5)
        rect(dst, x0 + sway, 40, x0 + 18 + sway, 560, rgb("#2f6b45"), 0.85)
        for k in range(5):
            rect(dst, x0 + sway - 4, 80 + k * 90, x0 + 22 + sway, 88 + k * 90, rgb("#3d8b6e"), 0.7)
    glow(dst, 480, 80, 100, rgb("#fff6ea"), 0.2)
    return dst


def paint_harbor_cranes(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#2a2430"), rgb("#1a1820"))
    water = blank()
    xx, yy = grid()
    water[..., :3] = rgb("#1a2430")
    water[..., 3] = smoothstep(430, 460, yy)
    over(dst, water)
    for i, x in enumerate((140, 280, 430)):
        rect(dst, x, 180, x + 16, 460, rgb("#3a3438"), 0.95)
        rect(dst, x - 40, 200, x + 90, 214, rgb("#4a4448"), 0.9)
        on = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(t * 2 + i))
        disc(dst, x + 70, 196, 5, rgb("#f2c15a"), on)
    return dst


def paint_prism_fall(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#f4efe6"), rgb("#d8cfc2"))
    glow(dst, 320, 80, 120, rgb("#ffffff"), 0.45)
    colors = ("#e85d4c", "#f2a65a", "#f0e07a", "#49d17c", "#3aa7b8", "#5c2d8a")
    for i, color in enumerate(colors):
        x = 160 + i * 54 + 6 * math.sin(t + i)
        rect(dst, x, 140, x + 36, 520, rgb(color), 0.55 + 0.2 * math.sin(t + i))
        glow(dst, x + 18, 500, 30, rgb(color), 0.2)
    return dst


def paint_owl_hollow(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0c1410"), rgb("#1a1810"))
    rect(dst, 250, 80, 390, 600, rgb("#2a2218"), 0.95, radius=40)
    blink = 0.2 + 0.8 * (0.5 + 0.5 * math.sin(t * 2))
    disc(dst, 292, 300, 16, rgb("#f0c878"), blink)
    disc(dst, 348, 300, 16, rgb("#f0c878"), blink)
    disc(dst, 292, 300, 6, rgb("#1a1410"), 0.9)
    disc(dst, 348, 300, 6, rgb("#1a1410"), 0.9)
    glow(dst, 320, 300, 50, rgb("#f0c878"), 0.12 * blink)
    return dst


def paint_mirage_well(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#e8d2a8"), rgb("#c9844a"), 0.6)
    wobble = 1.0 + 0.08 * math.sin(t * 2)
    ellipse(dst, 320, 360, 90 * wobble, 28 * wobble, rgb("#3aa7b8"), 0.55)
    ellipse(dst, 320, 360, 60 * wobble, 16, rgb("#d7f3f6"), 0.35 + 0.1 * math.sin(t))
    glow(dst, 320, 340, 70, rgb("#fff4d8"), 0.16)
    for i in range(6):
        ellipse(dst, 320, 330 - i * 12, 40 + i * 8, 6, rgb("#fff6ea"), 0.08)
    return dst


def paint_vinyl_groove(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a1418"), rgb("#0c0a0c"))
    disc(dst, 320, 320, 210, rgb("#1a1a1c"), 0.98)
    for r in (60, 100, 140, 180):
        ellipse(dst, 320, 320, r, r, rgb("#3a3a40"), 0.18)
    ang = t
    disc(dst, 320 + math.cos(ang) * 150, 320 + math.sin(ang) * 150, 6, rgb("#d7deef"), 0.8)
    disc(dst, 320, 320, 22, rgb("#f4efe6"), 0.95)
    disc(dst, 320, 320, 8, rgb("#1a1a1c"), 0.95)
    return dst


def paint_bridge_fog(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#9aa8b4"), rgb("#6a787e"))
    glow(dst, 320, 220, 200, rgb("#e8eef4"), 0.22 + 0.08 * math.sin(t))
    for i, x in enumerate((80, 200, 320, 440, 560)):
        rect(dst, x - 4, 180, x + 4, 480, rgb("#4a5258"), 0.55)
    rect(dst, 40, 240, 600, 256, rgb("#3a4248"), 0.8)
    for i in range(8):
        glow(dst, 80 + i * 70, 248, 10, rgb("#f4e6b0"), 0.25 + 0.2 * math.sin(t + i))
    return dst


def paint_radio_tower(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0c1420"), rgb("#1a1020"))
    rect(dst, 312, 80, 328, 520, rgb("#d8d2c4"), 0.9)
    for y in (140, 240, 340):
        rect(dst, 280, y, 360, y + 6, rgb("#c9c0b0"), 0.8)
    blink = 0.2 + 0.8 * (0.5 + 0.5 * math.sin(t * 3))
    glow(dst, 320, 70, 40, rgb("#e85d4c"), blink)
    disc(dst, 320, 70, 8, rgb("#ff6b5a"), blink)
    rect(dst, 0, 520, 640, 640, rgb("#12141a"), 0.95)
    return dst


def paint_glacier_blue(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#8ec4d8"), rgb("#1a4a62"))
    xx, yy = grid()
    wall = blank()
    wall[..., :3] = mix(rgb("#d7eef8"), rgb("#3aa7b8"), (yy - 80) / 400)
    wall[..., 3] = (xx > 180 + 20 * np.sin(yy / 40.0)).astype(np.float32) * 0.85
    over(dst, wall)
    drip_y = 120 + (frame * 18) % 360
    disc(dst, 260, drip_y, 4, rgb("#e8f6ff"), 0.7)
    glow(dst, 300, 200, 80, rgb("#b9e7ff"), 0.16)
    return dst


def paint_sunflower_tilt(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#8ec4e8"), rgb("#6a9e4a"))
    rect(dst, 0, 380, 640, 640, rgb("#5a8a3a"), 0.9)
    for i, (cx, cy) in enumerate(((160, 300), (320, 250), (480, 310), (240, 360), (400, 340))):
        nod = 10 * math.sin(t + i)
        disc(dst, cx + nod, cy, 28, rgb("#f0c14a"), 0.95)
        disc(dst, cx + nod, cy, 12, rgb("#5c2d14"), 0.9)
        rect(dst, cx - 3, cy + 20, cx + 3, 500, rgb("#2f6b45"), 0.85)
    glow(dst, 500, 80, 100, rgb("#fff4d0"), 0.3)
    return dst


def paint_ink_bloom(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#f4efe6"), rgb("#e8dcc8"))
    scale = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t))
    glow(dst, 320, 320, 160 * scale, rgb("#1a1418"), 0.35)
    disc(dst, 300, 300, 70 * scale, rgb("#1a1a1c"), 0.9, soft=12)
    disc(dst, 360, 340, 40 * scale, rgb("#2a2428"), 0.7, soft=10)
    disc(dst, 250, 360, 28 * scale, rgb("#121014"), 0.6, soft=8)
    return dst


def paint_terrace_lights(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#2a1c28"), rgb("#1a1218"))
    rng = np.random.default_rng(11)
    for i in range(28):
        seed = rng.random(3)
        x = 40 + seed[0] * 560
        y = 80 + seed[1] * 480
        on = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(t * 2 + i * 0.7))
        rect(dst, x, y, x + 10 + seed[2] * 8, y + 7, rgb("#f2c15a"), on)
        glow(dst, x + 6, y + 3, 8, rgb("#f6d27a"), 0.2 * on)
    return dst


def paint_meteor_choir(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#07060c"), rgb("#120c14"))
    rng = np.random.default_rng(3)
    for i in range(10):
        seed = rng.random(3)
        progress = (frame / FRAMES + seed[0]) % 1.0
        x = 40 + progress * 620
        y = 40 + seed[1] * 360 + progress * 80
        glow(dst, x, y, 16, rgb("#f4e6b0"), 0.35)
        rect(dst, x - 28, y - 4, x, y, rgb("#d7deef"), 0.45)
    for i in range(18):
        seed = rng.random(2)
        disc(dst, 30 + seed[0] * 580, 30 + seed[1] * 400, 1.3, rgb("#e8eef8"), 0.4)
    return dst


def paint_orchid_house(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#e8dce8"), rgb("#c8b0c4"))
    rect(dst, 80, 60, 560, 560, rgb("#f4eef4"), 0.35, radius=12)
    scale = 1.0 + 0.08 * math.sin(t)
    glow(dst, 320, 300, 80 * scale, rgb("#c084fc"), 0.22)
    for k in range(5):
        ang = k * (math.pi * 0.4) - math.pi / 2
        ellipse(dst, 320 + math.cos(ang) * 28 * scale, 300 + math.sin(ang) * 22 * scale, 16, 28, rgb("#c43c8e"), 0.85)
    disc(dst, 320, 300, 10, rgb("#f0c14a"), 0.9)
    return dst


def paint_night_pier(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0c1428"), rgb("#08101c"))
    water = blank()
    xx, yy = grid()
    water[..., :3] = rgb("#102030")
    water[..., 3] = smoothstep(360, 390, yy)
    over(dst, water)
    rect(dst, 200, 280, 440, 300, rgb("#3a2a1c"), 0.95)
    for i, x in enumerate((220, 280, 340, 400)):
        rect(dst, x, 300, x + 10, 520, rgb("#2a2018"), 0.85)
        glow(dst, x + 5, 270, 16, rgb("#f2c15a"), 0.3 + 0.15 * math.sin(t + i))
        disc(dst, x + 5, 268, 5, rgb("#ffe39a"), 0.8)
        ellipse(dst, x + 5, 430 + 6 * math.sin(t + i), 10, 4, rgb("#f2c15a"), 0.18)
    return dst


def paint_copper_storm(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#4a2a1c"), rgb("#2a1814"))
    glow(dst, 280, 180, 180, rgb("#c9844a"), 0.28 + 0.1 * math.sin(t))
    glow(dst, 420, 220, 140, rgb("#3d8b6e"), 0.18)
    flash = max(0.0, math.sin(t * 3))
    glow(dst, 360, 260, 70, rgb("#f0c878"), 0.2 * flash)
    rect(dst, 0, 500, 640, 640, rgb("#3a2418"), 0.9)
    return dst


def paint_quiet_orbit(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#080a12"), rgb("#12141c"))
    disc(dst, 320, 340, 110, rgb("#4a525c"), 0.95)
    disc(dst, 290, 310, 36, rgb("#6a727c"), 0.4, soft=10)
    glow(dst, 320, 340, 140, rgb("#c9a227"), 0.12)
    mx = 320 + math.cos(t) * 170
    my = 340 + math.sin(t) * 70
    glow(dst, mx, my, 22, rgb("#f4e6b0"), 0.45)
    disc(dst, mx, my, 10, rgb("#f4efe6"), 0.95)
    return dst


def paint_train_signal(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0c1014"), rgb("#16181c"))
    rect(dst, 300, 80, 340, 520, rgb("#2a2a2c"), 0.95)
    red_on = 0.5 + 0.5 * math.sin(t * 2)
    green_on = 1.0 - red_on
    disc(dst, 320, 160, 28, rgb("#e85d4c"), 0.25 + 0.7 * red_on)
    disc(dst, 320, 250, 28, rgb("#49d17c"), 0.25 + 0.7 * green_on)
    glow(dst, 320, 160, 40, rgb("#e85d4c"), 0.25 * red_on)
    glow(dst, 320, 250, 40, rgb("#49d17c"), 0.25 * green_on)
    rect(dst, 80, 560, 560, 580, rgb("#3a3a40"), 0.8)
    return dst


def paint_last_firefly(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0a140f"), rgb("#06100c"))
    rect(dst, 0, 480, 640, 640, rgb("#102418"), 0.9)
    x = 200 + 180 * math.sin(t)
    y = 220 + 90 * math.cos(t * 1.3)
    glow(dst, x, y, 28, rgb("#f4e07a"), 0.55)
    disc(dst, x, y, 3, rgb("#fff6b0"), 0.95)
    for i, gx in enumerate((80, 180, 400, 520)):
        ellipse(dst, gx, 500, 40, 12, rgb("#14301c"), 0.5)
    return dst


PAINTERS = {
    1: paint_moonrise,
    2: paint_stained_glass,
    3: paint_petal_storm,
    4: paint_lighthouse,
    5: paint_coral_bloom,
    6: paint_neon_dusk,
    7: paint_firefly_grove,
    8: paint_corona,
    9: paint_koi_mirror,
    10: paint_heat_shimmer,
    11: paint_ice_fracture,
    12: paint_nave_light,
    13: paint_lantern_rain,
    14: paint_comet_wake,
    15: paint_tide_pool,
    16: paint_aurora_spine,
    17: paint_candle_window,
    18: paint_fog_bell,
    19: paint_greenhouse_rain,
    20: paint_red_giant,
    21: paint_salt_flats,
    22: paint_subway_glow,
    23: paint_whale_breach,
    24: paint_harvest_field,
    25: paint_thunderhead,
    26: paint_moon_gate,
    27: paint_ember_forge,
    28: paint_lotus_night,
    29: paint_clockwork_sky,
    30: paint_snowbound_cabin,
    31: paint_magma_vein,
    32: paint_bamboo_wind,
    33: paint_harbor_cranes,
    34: paint_prism_fall,
    35: paint_owl_hollow,
    36: paint_mirage_well,
    37: paint_vinyl_groove,
    38: paint_bridge_fog,
    39: paint_radio_tower,
    40: paint_glacier_blue,
    41: paint_sunflower_tilt,
    42: paint_ink_bloom,
    43: paint_terrace_lights,
    44: paint_meteor_choir,
    45: paint_orchid_house,
    46: paint_night_pier,
    47: paint_copper_storm,
    48: paint_quiet_orbit,
    49: paint_train_signal,
    50: paint_last_firefly,
}


def render_work(work_id: int) -> list[Image.Image]:
    painter = PAINTERS[work_id]
    return [to_image(painter(frame)) for frame in range(FRAMES)]


def token_meta(work: dict) -> dict:
    attributes = [{"trait_type": key, "value": value} for key, value in work["attributes"].items()]
    return {
        "name": work["title"],
        "description": work["description"],
        "image": f"{work['id']}.gif",
        "external_url": f"/afterimages/{work['id']}",
        "attributes": attributes,
        "animation_loop": True,
        "compiler": "Afterimages 1:1 APNG",
    }


CSV_FIELDS = [
    "tokenID",
    "name",
    "description",
    "file_name",
    "attributes[Series]",
    "attributes[Palette]",
    "attributes[Motion]",
    "attributes[Season]",
    "attributes[Medium]",
    "attributes[Family]",
    "attributes[Weather]",
]


def drop_csv_row(work: dict, meta: dict) -> dict:
    row = {
        "tokenID": work["id"],
        "name": meta["name"],
        "description": meta["description"],
        "file_name": f"{work['id']}.gif",
    }
    for attr in meta["attributes"]:
        row[f"attributes[{attr['trait_type']}]"] = attr["value"]
    row.setdefault("attributes[Family]", work.get("family", "Signature"))
    row.setdefault("attributes[Weather]", work.get("attributes", {}).get("Weather", "Clear"))
    return row


def build_brand(frames_by_id: dict[int, list[Image.Image]]) -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    first = frames_by_id[1][0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((28, 28, SIZE - 28, SIZE - 28), fill=255)
    logo = first.copy()
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    logo.resize((512, 512), Image.Resampling.LANCZOS).save(BRAND_DIR / "logo-afterimages.png")
    save_apng([frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in frames_by_id[1]], BRAND_DIR / "logo-afterimages-loop.png")

    banner = Image.new("RGBA", (1500, 560), (18, 12, 10, 255))
    picks = (1, 8, 6)
    for i, work_id in enumerate(picks):
        face = frames_by_id[work_id][0].resize((420, 420), Image.Resampling.LANCZOS)
        banner.alpha_composite(face, (40 + i * 480, 90))
    draw = ImageDraw.Draw(banner)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64)
        small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
        small = font
    draw.text((56, 28), "AFTERIMAGES", font=font, fill=(255, 236, 210, 255))
    draw.text((60, 100), "One-of-one APNG paintings that never freeze.", font=small, fill=(232, 198, 160, 255))
    banner.convert("RGB").save(BRAND_DIR / "banner-afterimages.png", quality=94)

    gif_source = frames_by_id[8]
    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS).convert("RGB") for frame in gif_source]
    palette = gif_frames[0].quantize(colors=240, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    gif_q = [frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for frame in gif_frames]
    gif_q[0].save(
        BRAND_DIR / "collection-afterimages.gif",
        save_all=True,
        append_images=gif_q[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )


def write_sidecars(rows: list[dict], supply: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "opensea-metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "README.md").write_text(
        "# Afterimages OpenSea pack\n\n"
        f"{supply:,} unique 1:1 loops at 640×640, 16 frames, 100ms, for an OpenSea Drop on Ink.\n\n"
        f"Upload every file in `gifs/` (1.gif–{supply}.gif) plus `opensea-metadata.csv` to an OpenSea Drop.\n"
        "OpenSea Drops play GIF, not APNG. Tokens 1–50 are the signature APNGs in public/afterimages/.\n"
        "The rest of the drop is baked as GIFs here. The CSV uses OpenSea Studio headers: "
        "`tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.\n",
        encoding="utf-8",
    )
    (META_DIR).mkdir(parents=True, exist_ok=True)
    (META_DIR / "afterimages.json").write_text(
        json.dumps(
            {
                "name": "Afterimages",
                "symbol": "AFTER",
                "description": (
                    f"Afterimages is a {supply:,}-piece OpenSea drop of unique looping paintings on Ink. "
                    "Each token is a finished painting — not stacked traits. One canvas, one clock, one artwork. "
                    "Minting on Ink (chain ID 57073)."
                ),
                "image": "/brand/collection-afterimages.gif",
                "banner_image": "/brand/banner-afterimages.png",
                "external_link": "/afterimages",
                "seller_fee_basis_points": 750,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def write_provenance(supply: int) -> None:
    hashes: list[str] = []
    for token_id in range(1, supply + 1):
        path = GIF_DIR / f"{token_id}.gif"
        if not path.exists():
            continue
        hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
    if not hashes:
        return
    joined = "".join(hashes)
    (OUT / "provenance.json").write_text(
        json.dumps(
            {
                "algorithm": "SHA-256",
                "concatenatedHash": hashlib.sha256(joined.encode("ascii")).hexdigest(),
                "count": len(hashes),
                "hashes": hashes,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    from afterimages_series import SIGNATURE_COUNT, TOTAL, build_generated_roster, paint_generated_job

    parser = argparse.ArgumentParser(description="Paint Afterimages 1:1 loops for an OpenSea Drop on Ink.")
    parser.add_argument("--count", type=int, default=TOTAL, help="How many tokens to include (max 3333)")
    parser.add_argument("--workers", type=int, default=max(1, min(8, cpu_count() or 1)))
    args = parser.parse_args()
    supply = min(max(args.count, 1), TOTAL)

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    signature = [work for work in WORKS if work["id"] <= supply]
    generated = []
    if supply > SIGNATURE_COUNT:
        reserved = {work["title"] for work in WORKS}
        generated = build_generated_roster(supply - SIGNATURE_COUNT, reserved)

    catalog = signature + generated
    rows: list[dict] = []
    print("Writing OpenSea sidecars…")
    for work in catalog:
        meta = token_meta(work)
        (JSON_DIR / f"{work['id']}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        rows.append(drop_csv_row(work, meta))
    write_sidecars(rows, supply)
    families: dict[str, int] = {}
    for work in catalog:
        family = work.get("family") or work.get("attributes", {}).get("Family", "Signature")
        families[family] = families.get(family, 0) + 1
    (OUT / "stats.json").write_text(json.dumps({"supply": supply, "families": families}, indent=2) + "\n", encoding="utf-8")

    print("Painting signature Afterimages 1–50…")
    for work in signature:
        site_path = PUBLIC_DIR / f"{work['id']}.png"
        drop_path = IMAGE_DIR / f"{work['id']}.png"
        gif_path = GIF_DIR / f"{work['id']}.gif"
        if site_path.exists() and site_path.stat().st_size > 0:
            print(f"  #{work['id']} {work['title']} (exists)")
            drop_path.write_bytes(site_path.read_bytes())
            if not gif_path.exists() or gif_path.stat().st_size == 0:
                frames, _duration = load_apng_frames(site_path)
                save_loop_gif(frames, gif_path, DURATION_MS)
        else:
            print(f"  #{work['id']} {work['title']}")
            frames = render_work(work["id"])
            save_apng(frames, site_path)
            drop_path.write_bytes(site_path.read_bytes())
            save_loop_gif(frames, gif_path, DURATION_MS)

    if generated:
        print(f"Painting series Afterimages {SIGNATURE_COUNT + 1}–{supply} with {args.workers} workers…")
        done = 0
        with Pool(processes=args.workers) as pool:
            for token_id, label in pool.imap_unordered(paint_generated_job, generated, chunksize=4):
                done += 1
                if done % 25 == 0 or done == len(generated):
                    print(f"  {done}/{len(generated)}  #{token_id} {label}")

    missing = [token_id for token_id in range(1, supply + 1) if not (GIF_DIR / f"{token_id}.gif").exists()]
    if missing:
        raise SystemExit(f"Missing {len(missing)} GIFs, first: {missing[:8]}")
    print("Hashing provenance…")
    write_provenance(supply)
    print("Done.")


if __name__ == "__main__":
    main()
