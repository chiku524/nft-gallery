# Starting a new collection

The drawing generator is reset. The next drop does not inherit Scribblins, Foxins, or any other living painter.

## Start here

1. Lock name, ticker, subject, chain, supply, and mint price with the user.
2. Copy `scripts/build_drop.template.py` to `scripts/build_<slug>.py`.
3. Import `paint_kit` for clock and file I/O only.
4. Invent a new look: silhouette, materials, palette, layer language, and motion.

## Do not copy

- Last drop's painter, palette, or character skeleton
- Doodle charcoal / sticker-cutout / oval-egg body language
- Trait names Field, Body, Mug, Hat, Wrap, Charm

For a salon of unrelated 1:1 open editions, do not write one painter with scene variants. Add a new file under `scripts/atelier/works/` that exports `WORK` and `paint(frame)`. The orchestrator is `scripts/build_galleria.py`.

## House pipeline (keep)

- 512×512, 12 frames, 90ms unless the art direction asks otherwise
- APNG traits for Studio, flattened 12-frame GIF + CSV for OpenSea
- Ignore `/generated/<slug>/{images,gifs,json}/` in `.gitignore`
- Keep sample GIFs small enough to push; leave the full bake on disk
