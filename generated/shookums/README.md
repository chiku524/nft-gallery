# Halloween Shook'ums OpenSea pack

5,555 flattened Halloween Shook'ums loops at 512×512, 12 frames, 90ms.

Listing kit (OpenSea collection page):
- Name: Halloween Shook'ums · Symbol: SHOOK · Category: PFPs · Chain: Abstract (2741)
- Description: `public/metadata/shookums-description.txt`
- Logo: `public/brand/logo-shookums.png` (512×512)
- Featured: `public/brand/featured-shookums.jpg` (1200×800)
- Banner: `public/brand/banner-shookums-opensea.jpg` (2800×700)
- Collection GIF: `public/brand/collection-shookums.gif` (1000×1000)

Drop upload: every file in `gifs/` (1.gif–5555.gif) plus `SHOOKUMS-opensea-drop.csv` or `opensea-metadata.csv`.
OpenSea Drops play GIF, not APNG, and cap a Drop upload at 10 GB / 10,000 files.
The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].
Studio trait layers stay in `public/shookums-traits/` and are not the upload pack.
