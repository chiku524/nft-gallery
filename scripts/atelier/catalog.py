"""Load every independent painter. Adding a work is dropping a file in works/."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Callable

from PIL import Image

from atelier.surface import WorkSpec

WorksDir = Path(__file__).resolve().parent / "works"


def load_works() -> list[tuple[WorkSpec, Callable[[int], Image.Image]]]:
    loaded: list[tuple[WorkSpec, Callable[[int], Image.Image]]] = []
    for path in sorted(WorksDir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        module = importlib.import_module(f"atelier.works.{path.stem}")
        spec = getattr(module, "WORK", None)
        painter = getattr(module, "paint", None)
        if not isinstance(spec, WorkSpec) or not callable(painter):
            raise SystemExit(f"{path.name} must export WORK: WorkSpec and paint(frame) -> Image")
        loaded.append((spec, painter))
    loaded.sort(key=lambda item: item[0].id)
    ids = [spec.id for spec, _ in loaded]
    if ids != list(range(1, len(ids) + 1)):
        raise SystemExit(f"Work ids must be 1..N with no gaps. Got {ids}")
    return loaded
