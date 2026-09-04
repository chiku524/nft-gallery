# Groovy Nation

Looping **musical-note PFP GIFs** — clip-art note mascots with round heads, black stems, and dancing stick limbs. An **8,888-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/groovy`.

The look is cartoon notation on a shared 12-frame clock: the notehead is the face, a black stem goes up, flags and beams sit at the top. Not doodle ink. Not sticker cutouts. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF with 192 colors, no dither, and a palette sampled from every frame so flat fills stay clean.

## What’s in the drop

- Trait art at `public/groovy-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/groovy-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/groovy-description.txt`
- Trait studio at `/groovy/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/GroovyNation.sol` — ERC-721 named Groovy Nation with an 8,888 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_groovy.py
python3 scripts/generate_groovy.py        # 16 samples
python3 scripts/generate_groovy.py --all  # full 8,888 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --groovy --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/groovy/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Venue
2. Note
3. Expression
4. Topper
5. Cable
6. Riff

Four note bodies share one bounce. Toppers, cables, and riffs never edit the note file — they composite on the same head and stem. Notes bounce. Riffs pulse. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.
