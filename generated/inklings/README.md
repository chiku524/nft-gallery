# Inklings OpenSea pack

16 flattened ink-wash loops at 512×512, 16 frames, 90ms.

Upload every file in `gifs/` (1.gif–5555.gif) plus `INKLINGS-opensea-drop.csv` or `opensea-metadata.csv` to an OpenSea Drop on Ink (chain ID 57073).
OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Studio trait layers stay in `public/inklings-traits/` and are not the upload pack.
