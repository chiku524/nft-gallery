# Mochins OpenSea pack

16 flattened soft-3D mochi loops at 512×512, 16 frames, 100ms.

Upload every file in `gifs/` (1.gif–16.gif) plus `MOCHINS-opensea-drop.csv` or `opensea-metadata.csv` to an OpenSea Drop on Shape (chain ID 360).
OpenSea Drops play GIF, not APNG, and cap a Drop upload at 10 GB / 10,000 files.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Studio trait layers stay in `public/mochins-traits/` and are not the upload pack.
