# Loopkins OpenSea pack

10,000 flattened APNGs at 256×256, 12 frames, 80ms.

Upload every file in `images/` (1.png–10000.png) plus `opensea-metadata.csv` to an OpenSea Drop.
The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
OpenSea Drops accept up to 10,000 PNG files and 5GB total. These files are sized for that cap.
Studio trait layers stay in `public/traits/` and are not the upload pack.
