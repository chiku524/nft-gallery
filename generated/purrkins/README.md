# Purrkins OpenSea pack

10,000 flattened chibi-cat loops at 512×512, 12 frames, 80ms.

Upload every file in `gifs/` (1.gif–10000.gif) plus `PURRKINS-opensea-drop.csv` or `opensea-metadata.csv` to an OpenSea Drop on HyperEVM (chain ID 999).
OpenSea Drops play GIF, not APNG, and cap a Drop upload at 10 GB / 10,000 files.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Studio trait layers stay in `public/purrkins-traits/` and are not the upload pack.
