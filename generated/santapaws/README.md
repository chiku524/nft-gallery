# Santa Paws OpenSea pack

16 flattened chibi-cat loops at 512×512, 12 frames, 90ms.

Upload every file in `gifs/` (1.gif–16.gif) plus `SANTAPAWS-opensea-drop.csv` or `opensea-metadata.csv` to an OpenSea Drop on Base.
OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Full metadata for all 7,777 lives in `json/` after `generate_santapaws.py`. Bake every GIF with `python3 scripts/generate_santapaws.py --all`.
