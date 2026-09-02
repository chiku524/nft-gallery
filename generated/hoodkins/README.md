# Hoodkins OpenSea pack

16 flattened chibi-raccoon loops at 512×512, 12 frames, 80ms.

Upload every file in `gifs/` (1.gif–16.gif) plus `HOODKINS-opensea-drop.csv` or `opensea-metadata.csv` to an OpenSea Drop on Robinhood Chain (chain ID 4663).
OpenSea Drops play GIF, not APNG, and cap a Drop upload at 10 GB / 10,000 files.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Studio trait layers stay in `public/hoodkins-traits/` and are not the upload pack.
