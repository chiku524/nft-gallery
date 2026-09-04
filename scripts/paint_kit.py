"""Style-neutral house clock and I/O for a new collection painter.

This is the reset starting point. It has no characters, palettes, skeletons,
or layer names. Import this — not the last drop's `build_*.py` — when a new
collection needs APNG/GIF helpers.

Clock defaults match recent OpenSea packs. A new drop may change them if the
art direction asks for it.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 512
FRAMES = 12
DURATION_MS = 90


def write_bytes_retry(path: Path, data: bytes, attempts: int = 10) -> None:
    import time

    last_error: OSError | None = None
    for attempt in range(attempts):
        try:
            path.write_bytes(data)
            return
        except OSError as error:
            last_error = error
            time.sleep(0.15 * (attempt + 1))
    if last_error is not None:
        raise last_error


def save_image(image: Image.Image, path: Path, **kwargs) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fmt = kwargs.pop("format", None) or path.suffix.lstrip(".").upper()
    if fmt == "JPG":
        fmt = "JPEG"
    buffer = BytesIO()
    image.save(buffer, format=fmt, **kwargs)
    write_bytes_retry(path, buffer.getvalue())


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
        buffer := BytesIO(),
        save_all=True,
        append_images=stamped[1:],
        duration=[DURATION_MS] * len(stamped),
        loop=0,
        format="PNG",
        disposal=1,
        blend=0,
        compress_level=6,
    )
    write_bytes_retry(path, buffer.getvalue())


def rounded_portrait(portrait: Image.Image, size: int, radius: int = 56) -> Image.Image:
    face = portrait.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    face.putalpha(Image.composite(face.split()[-1], Image.new("L", (size, size), 0), mask))
    return face


def place_portrait(
    canvas: Image.Image, portrait: Image.Image, x: int, y: int, size: int, radius: int = 56
) -> None:
    face = rounded_portrait(portrait, size, radius)
    shadow = Image.new("RGBA", (size + 24, size + 24), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(28, 18, 40, 80))
    canvas.alpha_composite(shadow, (x - 8, y - 6))
    canvas.alpha_composite(face, (x, y))
