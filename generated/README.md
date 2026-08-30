# Generated collection (10,000)

OpenSea **does not** generate NFTs from trait layers. A Drop lets you bulk-upload up to **10,000** finished images and a CSV of string traits.

This folder is that pack.

## Files

| Path | What it is |
| --- | --- |
| `images/1.jpg` … `images/10000.jpg` | Unique PFPs (1024×1024 JPEG). Tokens 1–8 are the signature stoop looks. |
| `opensea-metadata.csv` | OpenSea Studio Drop metadata (tokenID, name, description, image, traits) |
| `json/1.json` … | ERC-721 metadata if you self-host a base URI |
| `stats.json` | Trait counts after the shuffle |
| `provenance.json` | SHA-256 of each image plus a concatenated collection hash |
| `metadata.jsonl` | One JSON object per token |

Regenerate with:

```bash
python3 scripts/build_traits.py
python3 scripts/generate_collection.py
```

## Upload to OpenSea Studio

1. Create a Drop on **Robinhood Chain** (chain ID 4663).
2. Set supply to 10,000.
3. In Media & Metadata, upload all JPEGs from `images/` and `opensea-metadata.csv`.
4. Preview traits, then publish / reveal per OpenSea’s drop flow.

Keep filenames as `{tokenID}.jpg` so they match the CSV `image` column.
