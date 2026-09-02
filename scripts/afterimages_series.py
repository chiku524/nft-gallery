#!/usr/bin/env python3
"""Deterministic Afterimages series painter for tokens 51–3333.

Tokens 1–50 stay the original hand-painted 1:1s. The rest of the drop is a
finished looping painting from a seeded recipe — still not a PFP trait stack.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GIF_DIR = ROOT / "generated" / "afterimages" / "gifs"
IMAGE_DIR = ROOT / "generated" / "afterimages" / "images"
PREVIEW_DIR = ROOT / "public" / "afterimages-preview"

TOTAL = 3333
SIGNATURE_COUNT = 50
PREVIEW_IDS = set(range(51, 67))
SERIES_SEED = 4663_3333

FAMILIES = [
    "Waterline",
    "Stormfield",
    "Grove",
    "Sanctum",
    "Voidlight",
    "Harbor",
    "Emberland",
    "Botanica",
    "Mineral",
    "Nightwork",
    "Paperweather",
    "Orbitwell",
]

MOTIONS = ["Rise", "Pulse", "Fall", "Sweep", "Drift", "Flash", "Spin", "Breath", "Wave", "Trail"]
SEASONS = ["Night", "Dusk", "Dawn", "Storm", "Winter", "Spring", "Harvest", "Void", "Fog", "Noon"]
WEATHERS = ["Clear", "Rain", "Snow", "Sparks", "Petals", "Mist"]

PALETTES: list[tuple[str, str, str, str, str, str]] = [
    ("Indigo Silver", "#0b1028", "#1a2748", "#c9d7ff", "#f4f1ff", "#10243a"),
    ("Jewel Gold", "#1a1020", "#0d0a12", "#c9a227", "#f0d48a", "#2a1c14"),
    ("Blush Cream", "#f7e6d8", "#e8b8b0", "#e37a8a", "#fff4d8", "#f0c8c0"),
    ("Navy Amber", "#07101f", "#15243a", "#f2c15a", "#fff6d2", "#10263d"),
    ("Teal Gold", "#083246", "#0b1c28", "#f0c14a", "#d7f3f6", "#3aa7b8"),
    ("Magenta Cyan", "#1a0820", "#0a0614", "#ff4fd8", "#4df0ff", "#2a1030"),
    ("Pine Gold", "#08140c", "#142418", "#f4e07a", "#fff6b0", "#102418"),
    ("Eclipse Copper", "#140808", "#2a1408", "#f4a05a", "#ffe0a8", "#3a2010"),
    ("Jade Orange", "#0c241c", "#12382c", "#e07a5f", "#f4b183", "#164a3a"),
    ("Sand Heat", "#c9a06a", "#8a4a24", "#fff0c8", "#e0a56a", "#a65b2b"),
    ("Ice Blue", "#d8e8f4", "#8ab0c8", "#ffffff", "#4a88b0", "#b8d4e4"),
    ("Honey Stone", "#2a241c", "#16130f", "#f4e8b0", "#c9a66a", "#3a3428"),
    ("Cinnabar Night", "#1a0a10", "#2a1018", "#e85a3a", "#f4c07a", "#3a1818"),
    ("Ice Ember", "#080c18", "#101828", "#f4b070", "#e8f0ff", "#1a2438"),
    ("Tide Green", "#0a2428", "#16343a", "#7ad0c0", "#d4fff4", "#0c3034"),
    ("Aurora Violet", "#08141c", "#1a2838", "#7dffb0", "#c89cff", "#102030"),
    ("Candle Umber", "#1a1410", "#2a2018", "#f2c15a", "#fff0c4", "#3a2a20"),
    ("Fog Steel", "#8a949c", "#4a545c", "#e8eef4", "#c0c8d0", "#6a747c"),
    ("Glass Summer", "#d8f0d0", "#88b890", "#4a8a58", "#f4ffe8", "#b8d8b0"),
    ("Ember Red", "#2a0808", "#4a1010", "#ff6a3a", "#ffd0a0", "#3a0c0c"),
    ("Salt White", "#e8e4dc", "#c0b8a8", "#ffffff", "#d4cfc4", "#a8a090"),
    ("Sodium Amber", "#121018", "#241c18", "#f4c15a", "#ffe9a8", "#1a1814"),
    ("Deep Marine", "#061018", "#0a1c28", "#3a88c8", "#d0eeff", "#082030"),
    ("Wheat Dusk", "#3a2410", "#c9a050", "#f4d070", "#ffe9b0", "#6a4018"),
    ("Storm Brass", "#1a2438", "#2a2018", "#f2c15a", "#d0d8e8", "#243044"),
    ("Ink Silver", "#0c1018", "#1a2030", "#e8eef8", "#8a9aac", "#141820"),
    ("Coal Orange", "#120a08", "#2a1410", "#ff7a30", "#ffd090", "#1a0c08"),
    ("Pearl Ink", "#0c1420", "#f0e8e0", "#d8c8d8", "#ffffff", "#1a2030"),
    ("Brass Night", "#12141c", "#2a2418", "#d4a84a", "#f4e0a8", "#1a1814"),
    ("Pine Snow", "#1a2438", "#c9d4e0", "#f4f8fc", "#2a2018", "#8aa0b4"),
    ("Obsidian Ember", "#0a0808", "#1a1010", "#ff5a20", "#ffc080", "#140c0c"),
    ("Jade Mist", "#0c2018", "#1a3828", "#9ad0a8", "#e8fff0", "#143024"),
    ("Rust Sodium", "#2a1810", "#4a2a18", "#f4a04a", "#ffd090", "#3a2014"),
    ("Spectrum Stone", "#f4f0e8", "#2a2824", "#7a4ad0", "#f0c04a", "#d8d0c4"),
    ("Bark Gold", "#1a1410", "#2a2018", "#f0c15a", "#c9a060", "#3a2a1c"),
    ("Sand Cyan", "#c8a060", "#e8d0a0", "#3ad0d0", "#ffffff", "#b89050"),
    ("Obsidian Chrome", "#0a0a0c", "#1a1a20", "#c8d0d8", "#ffffff", "#121216"),
    ("Pearl Steel", "#b8c0c8", "#6a747c", "#f4f8fc", "#d0d8e0", "#8a949c"),
    ("Night Red", "#080a12", "#10141c", "#ff3040", "#ffd0d4", "#0c1018"),
    ("Ice Teal", "#d0eef0", "#4a888c", "#e8ffff", "#88c8c8", "#b0d8d8"),
    ("Gold Leaf", "#2a2408", "#4a3a10", "#f4d020", "#fff4a0", "#3a300c"),
    ("Sumi Cream", "#f4ead8", "#1a1410", "#2a2420", "#e8dcc8", "#d8ccb8"),
    ("Umber Gold", "#2a2018", "#1a1410", "#f0c15a", "#ffe0a0", "#3a2a1c"),
    ("Ash White", "#1a1c20", "#0c0e12", "#e8eef4", "#ffffff", "#2a2c30"),
    ("Magenta Fog", "#2a1420", "#f0d8e8", "#d040a0", "#ffe8f4", "#3a1c28"),
    ("Teak Gold", "#1a1410", "#0c1018", "#f0c15a", "#ffe8b0", "#2a2018"),
    ("Verdigris Copper", "#1a2420", "#3a2a18", "#4aa090", "#d4a060", "#243028"),
    ("Slate Gold", "#1a1c24", "#2a2c34", "#d4b05a", "#f4e0a8", "#22242c"),
    ("Signal Night", "#0a0c10", "#14161c", "#ff2030", "#30d050", "#101218"),
    ("Meadow Gold", "#102418", "#0c1810", "#f4e07a", "#fff6b0", "#14301c"),
]

LEFT = [
    "Silent", "Hidden", "Slow", "Pale", "Warm", "Cold", "Soft", "Bright", "Late", "Early",
    "Still", "Wild", "Quiet", "Amber", "Silver", "Copper", "Hollow", "Distant", "Near", "Low",
    "High", "Thin", "Wide", "Deep", "Shallow", "Old", "New", "First", "Last", "Second",
    "Broken", "Whole", "Open", "Closed", "Little", "Great", "Private", "Public", "Secret", "Known",
    "Borrowed", "Kept", "Lost", "Found", "Gentle", "Sharp", "Wet", "Dry", "Long", "Brief",
    "Golden", "Ashen", "Ivory", "Scarlet", "Violet", "Azure", "Olive", "Rusted", "Frosted", "Smoked",
    "Paper", "Stone", "Glass", "Iron", "Silk", "Salt", "Honey", "Ink", "Ember", "Pearl",
    "Moonlit", "Sunlit", "Starlit", "Fogged", "Tide", "Wind", "Rain", "Snow", "Dust", "Spark",
]

RIGHT = [
    "Harbor", "Meadow", "Window", "Bridge", "Garden", "Orchard", "Chapel", "Kiln", "Well", "Gate",
    "Pier", "Dune", "Glacier", "Cove", "Grove", "Marsh", "Ridge", "Basin", "Aisle", "Attic",
    "Lantern", "Beacon", "Comet", "Orbit", "Choir", "Signal", "Mirror", "Pool", "Vein", "Bloom",
    "Wake", "Bell", "Cabin", "Tower", "Terrace", "Flats", "Nave", "Spine", "Breach", "Field",
    "Forge", "Hollow", "Tilt", "Storm", "Rain", "Dusk", "Dawn", "Hour", "Watch", "Room",
    "Path", "Shore", "Cliff", "Canal", "Market", "Yard", "Roof", "Step", "Arch", "Door",
    "River", "Lake", "Inlet", "Delta", "Cape", "Pass", "Trail", "Road", "Track", "Line",
    "Ember", "Halo", "Veil", "Crown", "Thread", "Knot", "Fold", "Sheet", "Page", "Mark",
]

LINES = [
    "The hour repeats until the color agrees.",
    "Nothing in the frame is in a hurry to finish.",
    "A small motion keeps the rest of the canvas honest.",
    "The dark around it is doing the real work.",
    "Light arrives late and leaves a forwarding address.",
    "The loop is shorter than the weather it remembers.",
    "One object keeps a promise the sky will not.",
    "It turns so the quiet can last.",
    "The edge of the picture is where the clock lives.",
    "A second thought of the same landscape.",
]


SIZE = 640
FRAMES = 16
DURATION_MS = 100
_XY: tuple[np.ndarray, np.ndarray] | None = None
_LIB: dict | None = None


def _xy() -> tuple[np.ndarray, np.ndarray]:
    global _XY
    if _XY is None:
        yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
        _XY = (xx, yy)
    return _XY


def _smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _rgb(hex_color: str) -> np.ndarray:
    value = hex_color.lstrip("#")
    return np.array([int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


def _mix(a: np.ndarray | float, b: np.ndarray | float, t: float | np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    t = np.asarray(t, dtype=np.float32)
    if t.ndim >= 2 and a.ndim == 1:
        t = t[..., None]
    return a * (1.0 - t) + b * t


def _blank() -> np.ndarray:
    return np.zeros((SIZE, SIZE, 4), dtype=np.float32)


def _over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


def _vertical_wash(top: np.ndarray, bottom: np.ndarray, power: float = 1.0) -> np.ndarray:
    _xx, yy = _xy()
    t = (yy / (SIZE - 1)) ** power
    dst = _blank()
    dst[..., :3] = _mix(top, bottom, t)
    dst[..., 3] = 1.0
    return dst


def _glow(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float) -> None:
    xx, yy = _xy()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.exp(-0.5 * (d / max(r, 1.0)) ** 2) * opacity
    layer = _blank()
    layer[..., :3] = color
    layer[..., 3] = a
    _over(dst, layer)


def _disc(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float = 1.0, soft: float = 2.0) -> None:
    xx, yy = _xy()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = _smoothstep(r + soft, r - soft, d) * opacity
    layer = _blank()
    layer[..., :3] = color
    layer[..., 3] = a
    _over(dst, layer)


def _ellipse(dst: np.ndarray, cx: float, cy: float, rx: float, ry: float, color: np.ndarray, opacity: float = 1.0, soft: float = 2.0) -> None:
    xx, yy = _xy()
    d = np.sqrt(((xx - cx) / max(rx, 1.0)) ** 2 + ((yy - cy) / max(ry, 1.0)) ** 2)
    a = _smoothstep(1.0 + soft / max(rx, ry), 1.0 - soft / max(rx, ry), d) * opacity
    layer = _blank()
    layer[..., :3] = color
    layer[..., 3] = a
    _over(dst, layer)


def _rect(dst: np.ndarray, x0: float, y0: float, x1: float, y1: float, color: np.ndarray, opacity: float = 1.0, radius: float = 0.0) -> None:
    xx, yy = _xy()
    layer = _blank()
    layer[..., :3] = color
    if radius <= 0:
        mask = (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)
        layer[..., 3] = mask.astype(np.float32) * opacity
    else:
        cx = np.clip(xx, x0 + radius, x1 - radius)
        cy = np.clip(yy, y0 + radius, y1 - radius)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        layer[..., 3] = _smoothstep(radius + 1.4, radius - 1.4, d) * opacity
    _over(dst, layer)


def _phase(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def _to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr * 255.0, 0, 255).astype(np.uint8), "RGBA")


def _lib():
    global _LIB
    if _LIB is None:
        _LIB = {
            "FRAMES": FRAMES,
            "blank": _blank,
            "disc": _disc,
            "ellipse": _ellipse,
            "glow": _glow,
            "grid": _xy,
            "mix": _mix,
            "over": _over,
            "phase": _phase,
            "rect": _rect,
            "rgb": _rgb,
            "smoothstep": _smoothstep,
            "to_image": _to_image,
            "vertical_wash": _vertical_wash,
        }
    return _LIB


def save_series_gif(frames: list[Image.Image], path: Path) -> None:
    from io import BytesIO

    path.parent.mkdir(parents=True, exist_ok=True)
    rgb_frames = [frame.convert("RGB") for frame in frames]
    quantized = [
        frame.quantize(colors=160, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        for frame in rgb_frames
    ]
    buffer = BytesIO()
    quantized[0].save(
        buffer,
        save_all=True,
        append_images=quantized[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=False,
        disposal=2,
        format="GIF",
    )
    path.write_bytes(buffer.getvalue())


def mix_seed(token_id: int, salt: int = 0) -> int:
    return (token_id * 0x9E3779B9 ^ SERIES_SEED ^ (salt * 0x85EBCA6B)) & 0xFFFFFFFF


def _pick(seq, rng: random.Random):
    return seq[rng.randrange(len(seq))]


def make_recipe(token_id: int, reserved_titles: set[str], salt: int = 0) -> dict:
    rng = random.Random(mix_seed(token_id, salt))
    family = _pick(FAMILIES, rng)
    palette = _pick(PALETTES, rng)
    motion = _pick(MOTIONS, rng)
    season = _pick(SEASONS, rng)
    weather = _pick(WEATHERS, rng)
    title = f"{_pick(LEFT, rng)} {_pick(RIGHT, rng)}"
    if title in reserved_titles:
        title = f"{title} {_pick(RIGHT, rng)}"
    description = f"{title} holds a {motion.lower()} in {palette[0].lower()}. { _pick(LINES, rng)}"
    layout = rng.random()
    density = 0.35 + rng.random() * 0.55
    scale = 0.82 + rng.random() * 0.4
    focal = rng.random()
    fingerprint = "|".join(
        [
            family,
            palette[0],
            motion,
            season,
            weather,
            f"{int(layout * 24)}",
            f"{int(density * 16)}",
            f"{int(scale * 16)}",
            f"{int(focal * 20)}",
        ]
    )
    return {
        "id": token_id,
        "family": family,
        "title": title,
        "description": description,
        "layout": layout,
        "density": density,
        "scale": scale,
        "focal": focal,
        "fingerprint": fingerprint,
        "attributes": {
            "Series": "Afterimages",
            "Palette": palette[0],
            "Motion": motion,
            "Season": season,
            "Medium": "APNG",
            "Family": family,
            "Weather": weather,
        },
        "colors": {
            "top": palette[1],
            "bottom": palette[2],
            "accent": palette[3],
            "highlight": palette[4],
            "ground": palette[5],
        },
    }


def build_generated_roster(count: int, reserved_titles: set[str]) -> list[dict]:
    roster: list[dict] = []
    seen_fp: set[str] = set()
    titles = set(reserved_titles)
    token_id = SIGNATURE_COUNT + 1
    while len(roster) < count:
        salt = 0
        recipe = make_recipe(token_id, titles, salt)
        while recipe["fingerprint"] in seen_fp or recipe["title"] in titles:
            salt += 1
            if salt > 80:
                recipe["title"] = f"{recipe['title']} {token_id}"
                recipe["fingerprint"] = f"{recipe['fingerprint']}|{token_id}"
                break
            recipe = make_recipe(token_id, titles, salt)
        seen_fp.add(recipe["fingerprint"])
        titles.add(recipe["title"])
        roster.append(recipe)
        token_id += 1
    return roster


def _weather(dst, weather: str, frame: int, accent, L) -> None:
    xx, yy = L["grid"]()
    blank = L["blank"]
    over = L["over"]
    if weather == "Clear":
        return
    layer = blank()
    layer[..., :3] = accent
    if weather == "Rain":
        streak = ((xx * 0.55 + yy + frame * 22) % 36) < 1.6
        layer[..., 3] = streak.astype(np.float32) * 0.2
    elif weather == "Snow":
        dots = ((xx * 12.8 + yy * 7.3 + frame * 9) % 51) < 1.15
        layer[..., 3] = dots.astype(np.float32) * 0.35
    elif weather == "Sparks":
        dots = ((xx * 9.1 + yy * 13.7 + frame * 14) % 63) < 0.9
        layer[..., 3] = dots.astype(np.float32) * 0.45
    elif weather == "Petals":
        blobs = ((xx * 5.4 + yy * 8.1 + frame * 11) % 47) < 2.2
        layer[..., 3] = blobs.astype(np.float32) * 0.22
    else:
        mist = L["smoothstep"](180, 520, yy) * (0.12 + 0.08 * math.sin(frame / 3))
        layer[..., 3] = mist.astype(np.float32)
    over(dst, layer)


def _motion_t(frame: int, motion: str, L) -> float:
    t = L["phase"](frame)
    speeds = {
        "Rise": 1.0,
        "Pulse": 2.0,
        "Fall": 1.15,
        "Sweep": 1.4,
        "Drift": 0.7,
        "Flash": 2.6,
        "Spin": 1.8,
        "Breath": 0.85,
        "Wave": 1.25,
        "Trail": 1.55,
    }
    return t * speeds.get(motion, 1.0)


def paint_recipe(recipe: dict, frame: int):
    L = _lib()
    rgb = L["rgb"]
    colors = recipe["colors"]
    top, bottom = rgb(colors["top"]), rgb(colors["bottom"])
    accent, highlight, ground = rgb(colors["accent"]), rgb(colors["highlight"]), rgb(colors["ground"])
    t = _motion_t(frame, recipe["attributes"]["Motion"], L)
    family = recipe["family"]
    painters = {
        "Waterline": _waterline,
        "Stormfield": _stormfield,
        "Grove": _grove,
        "Sanctum": _sanctum,
        "Voidlight": _voidlight,
        "Harbor": _harbor,
        "Emberland": _emberland,
        "Botanica": _botanica,
        "Mineral": _mineral,
        "Nightwork": _nightwork,
        "Paperweather": _paperweather,
        "Orbitwell": _orbitwell,
    }
    dst = painters[family](frame, t, recipe, top, bottom, accent, highlight, ground, L)
    _weather(dst, recipe["attributes"]["Weather"], frame, highlight, L)
    return dst


def _waterline(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 0.85)
    cx = 220 + recipe["layout"] * 200
    cy = 140 + 28 * math.sin(t) * recipe["scale"]
    L["glow"](dst, cx, cy, 120 * recipe["scale"], accent, 0.28)
    L["disc"](dst, cx, cy, 42 * recipe["scale"], highlight, 0.95, soft=3)
    xx, yy = L["grid"]()
    horizon = 390 + 10 * recipe["layout"] + 5 * np.sin(xx / 42 + t)
    water = L["blank"]()
    water[..., :3] = L["mix"](ground, bottom, (yy - 390) / 250)
    water[..., 3] = L["smoothstep"](horizon - 8, horizon + 6, yy)
    L["over"](dst, water)
    for i in range(10):
        L["ellipse"](dst, cx, 430 + i * 16 + 3 * math.sin(t + i), 70 + i * 14, 5, highlight, 0.08)
    L["glow"](dst, cx, 430, 80, highlight, 0.16 + 0.06 * math.sin(t))
    return dst


def _stormfield(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 1.1)
    flash = 0.15 + 0.55 * max(0.0, math.sin(t * 2) ** 8)
    L["glow"](dst, 200 + recipe["layout"] * 240, 160, 180, highlight, 0.12 + flash)
    for i in range(5):
        L["ellipse"](dst, 80 + i * 120 + 20 * math.sin(t + i), 140 + 18 * recipe["focal"], 90, 36, ground, 0.45)
    L["rect"](dst, 0, 470, 640, 640, ground, 0.92)
    if flash > 0.4:
        xx, yy = L["grid"]()
        bolt = np.abs(xx - (180 + recipe["layout"] * 280) - 12 * np.sin(yy / 18)) < 2.2
        bolt &= (yy > 90) & (yy < 470)
        layer = L["blank"]()
        layer[..., :3] = highlight
        layer[..., 3] = bolt.astype(np.float32) * 0.85
        L["over"](dst, layer)
    return dst


def _grove(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 0.9)
    L["rect"](dst, 0, 500, 640, 640, ground, 0.95)
    for i in range(6):
        x = 50 + i * 100 + 18 * recipe["layout"]
        L["rect"](dst, x, 280 - 40 * recipe["scale"], x + 18, 520, ground, 0.9)
        L["ellipse"](dst, x + 9, 270, 46 + 10 * math.sin(t + i), 70, accent, 0.55)
    for i in range(int(8 + recipe["density"] * 14)):
        x = (80 + i * 37 + 40 * math.sin(t + i)) % 640
        y = 200 + (i * 47 + frame * 9) % 280
        L["disc"](dst, x, y, 2.2, highlight, 0.5 + 0.3 * math.sin(t + i))
    return dst


def _sanctum(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom)
    L["rect"](dst, 90, 70, 550, 600, ground, 0.95, radius=16)
    pulse = 0.7 + 0.25 * math.sin(t)
    L["rect"](dst, 160, 140, 480, 420, accent, pulse, radius=10)
    L["glow"](dst, 320, 280, 140, highlight, 0.18 * pulse)
    L["rect"](dst, 300, 420, 340, 600, ground, 1.0)
    L["ellipse"](dst, 320, 430, 80 * recipe["scale"], 18, highlight, 0.25)
    L["disc"](dst, 320, 200 + 8 * math.sin(t), 16, highlight, 0.9)
    return dst


def _voidlight(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 1.2)
    L["glow"](dst, 320, 300, 220, accent, 0.12)
    xx, yy = L["grid"]()
    stars = ((xx * 17.3 + yy * 11.9 + recipe["id"] * 0.01) % 29) < 0.45
    layer = L["blank"]()
    layer[..., :3] = highlight
    layer[..., 3] = stars.astype(np.float32) * 0.55
    L["over"](dst, layer)
    x = 80 + (frame * 18 + recipe["layout"] * 400) % 700 - 40
    y = 80 + recipe["focal"] * 200 + 20 * math.sin(t)
    L["glow"](dst, x, y, 50, highlight, 0.4)
    L["ellipse"](dst, x - 40, y + 8, 48, 6, highlight, 0.35)
    L["disc"](dst, 320, 320, 28 * recipe["scale"], ground, 0.9)
    L["glow"](dst, 320, 320, 90, accent, 0.2 + 0.1 * math.sin(t))
    return dst


def _harbor(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 0.8)
    L["rect"](dst, 0, 430, 640, 640, ground, 0.9)
    for i in range(5):
        x = 40 + i * 120 + 10 * recipe["layout"]
        L["rect"](dst, x, 220 - 30 * (i % 3), x + 18, 430, ground, 0.85)
        L["rect"](dst, x - 30, 240, x + 80, 252, ground, 0.7)
        L["glow"](dst, x + 8, 230, 12, highlight, 0.35 + 0.25 * math.sin(t + i))
    xx, yy = L["grid"]()
    water = L["blank"]()
    water[..., :3] = L["mix"](accent, bottom, 0.5 + 0.2 * np.sin(xx / 30 + t))
    water[..., 3] = L["smoothstep"](430, 470, yy) * 0.55
    L["over"](dst, water)
    return dst


def _emberland(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 1.3)
    L["rect"](dst, 0, 480, 640, 640, ground, 0.95)
    L["glow"](dst, 320, 430, 160, accent, 0.35 + 0.15 * math.sin(t * 2))
    L["ellipse"](dst, 320, 470, 180, 40, accent, 0.5)
    for i in range(int(6 + recipe["density"] * 8)):
        x = 180 + i * 40 + 12 * math.sin(t + i)
        y = 400 - (frame * 10 + i * 23) % 180
        L["disc"](dst, x, y, 3, highlight, 0.55)
    L["rect"](dst, 250, 360, 390, 500, ground, 0.35, radius=8)
    return dst


def _botanica(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 0.7)
    L["rect"](dst, 0, 520, 640, 640, ground, 0.92)
    for i in range(5):
        x = 80 + i * 120 + 20 * recipe["layout"]
        sway = 10 * math.sin(t + i)
        L["rect"](dst, x, 300, x + 10, 530, ground, 0.85)
        L["disc"](dst, x + 5 + sway, 280, 36 * recipe["scale"], accent, 0.8)
        L["disc"](dst, x + 5 + sway, 280, 12, highlight, 0.9)
    L["glow"](dst, 480, 90, 140, highlight, 0.25)
    return dst


def _mineral(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 0.6)
    xx, yy = L["grid"]()
    crack = np.abs(yy - (220 + recipe["layout"] * 180) - 40 * np.sin(xx / 70 + t)) < (2.5 + recipe["density"] * 3)
    layer = L["blank"]()
    layer[..., :3] = accent
    layer[..., 3] = crack.astype(np.float32) * (0.5 + 0.3 * math.sin(t))
    L["over"](dst, layer)
    L["ellipse"](dst, 320, 420, 220, 90, ground, 0.45)
    L["glow"](dst, 320, 240, 130, highlight, 0.16)
    L["disc"](dst, 180 + recipe["focal"] * 280, 500, 18, highlight, 0.35)
    return dst


def _nightwork(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 1.0)
    for i, h in enumerate((220, 280, 190, 310, 240)):
        x0 = 40 + i * 120
        L["rect"](dst, x0, 640 - h, x0 + 90, 640, ground, 0.85)
        on = 0.2 + 0.7 * (0.5 + 0.5 * math.sin(t * 2 + i))
        L["rect"](dst, x0 + 18, 640 - h + 24, x0 + 40, 640 - h + 44, highlight, on)
    L["rect"](dst, 0, 560, 640, 640, ground, 0.5)
    L["glow"](dst, 80 + recipe["layout"] * 480, 180, 70, accent, 0.2)
    return dst


def _paperweather(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 0.8)
    for i in range(int(7 + recipe["density"] * 6)):
        x = 40 + (i * 73 + 30 * math.sin(t + i)) % 560
        y = 80 + (i * 51) % 360
        L["ellipse"](dst, x, y, 18, 26, accent, 0.7)
        L["rect"](dst, x - 2, y + 20, x + 2, y + 70, ground, 0.6)
        L["glow"](dst, x, y, 22, highlight, 0.25 + 0.15 * math.sin(t + i))
    L["rect"](dst, 0, 500, 640, 640, ground, 0.88)
    return dst


def _orbitwell(frame, t, recipe, top, bottom, accent, highlight, ground, L):
    dst = L["vertical_wash"](top, bottom, 1.15)
    L["disc"](dst, 320, 320, 70 * recipe["scale"], ground, 0.9)
    L["disc"](dst, 320, 320, 18, highlight, 0.95)
    r = 140 + 40 * recipe["layout"]
    x = 320 + r * math.cos(t)
    y = 320 + r * 0.55 * math.sin(t)
    L["glow"](dst, x, y, 28, accent, 0.55)
    L["disc"](dst, x, y, 8, highlight, 0.95)
    L["ellipse"](dst, 320, 320, r + 10, r * 0.55 + 8, accent, 0.12, soft=6)
    return dst


def render_generated_frames(recipe: dict) -> list[Image.Image]:
    L = _lib()
    return [L["to_image"](paint_recipe(recipe, frame)) for frame in range(L["FRAMES"])]


def paint_generated_job(recipe: dict) -> tuple[int, str]:
    token_id = int(recipe["id"])
    gif_path = GIF_DIR / f"{token_id}.gif"
    preview_path = PREVIEW_DIR / f"{token_id}.gif"
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    if gif_path.exists() and gif_path.stat().st_size > 0:
        if token_id in PREVIEW_IDS:
            PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
            if not preview_path.exists():
                preview_path.write_bytes(gif_path.read_bytes())
        return token_id, "exists"
    frames = render_generated_frames(recipe)
    save_series_gif(frames, gif_path)
    if token_id in PREVIEW_IDS:
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        if not preview_path.exists():
            preview_path.write_bytes(gif_path.read_bytes())
    return token_id, recipe["title"]
