# Santa Paws

Looping **chibi-cat PFP GIFs** — kawaii bust-crop cats, thick outlines, flat cel fills, a Christmas / giving wardrobe. A **7,777-piece** collection built to mint on **Base** (chain ID `8453`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/santapaws`.

The look is a Purrkins sibling: same locked head, twitching ears, and shared bob, dressed for cozy winter. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame, 90ms clock (same clock as Foxins), then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/santapaws-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/santapaws-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/santapaws-description.txt`
- Trait studio at `/santapaws/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/SantaPaws.sol` — ERC-721 named Santa Paws with a 7,777 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_santapaws.py
python3 scripts/generate_santapaws.py        # full 7,777 metadata + 16 preview GIFs
python3 scripts/generate_santapaws.py --all  # full 7,777 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --santapaws --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/santapaws/`.

`generate_santapaws.py` always writes deterministic metadata (JSON + CSV + stats) for all 7,777 tokens from seed `84537777`. Default GIF bake is a 16-token preview so the pipeline is cheap to re-run. Pass `--all` when you need the marketplace pack.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Yard
2. Glow
3. Pelt
4. Mug
5. Hat
6. Gear

Seven pelt bodies share one Purrkins-style chibi skeleton. Hats and gear never edit the pelt file — they composite on the same crown, collar, and paws. Eyes blink. Ears twitch. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature giver — snowy night, soft halo, white fluff, cheerful mug, Santa hat, scarf.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/santapaws/gifs` plus `generated/santapaws/SANTAPAWS-opensea-drop.csv`.
