# Boogie Squad OpenSea pack

16 flattened jelly-cel dance loops at 512×512, 12 frames, 90ms.

Upload every file in `gifs/` (1.gif–16.gif) plus `BOOG-opensea-drop.csv` or `opensea-metadata.csv` to an OpenSea Drop on Robinhood Chain.
OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Full metadata for all 10,000 lives in `json/` after `generate_boogiesquad.py`. Bake every GIF with `python3 scripts/generate_boogiesquad.py --all`.
