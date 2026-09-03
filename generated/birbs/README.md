# BirbNation OpenSea pack

2,222 flattened BirbNation loops at 512×512, 12 frames, 90ms.

Listing kit (OpenSea collection page):
- Name: BirbNation · Symbol: BIRB · Category: PFPs · Chain: Robinhood (4663)
- Description: `public/metadata/birbs-description.txt`
- Logo: `public/brand/logo-birbs.png` (512×512)
- Featured: `public/brand/featured-birbs.jpg` (1200×800)
- Banner: `public/brand/banner-birbs-opensea.jpg` (2800×700)
- Collection GIF: `public/brand/collection-birbs.gif` (1000×1000)

Drop upload: every file in `gifs/` (1.gif–2222.gif) plus `BIRBS-opensea-drop.csv` or `opensea-metadata.csv`.
OpenSea Drops play GIF, not APNG, and cap a Drop upload at 10 GB / 10,000 files.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Studio trait layers stay in `public/birbs-traits/` and are not the upload pack.
