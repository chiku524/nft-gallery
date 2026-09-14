# Robin Banx static generation pack

Deterministic 512×512 PNG dossier collages for Base (`8453`). This export contains 10,000 of the 10,000 token supply.

## Collection

- Symbol: `RBX`
- Supply: `10,000`
- Mint: `Free`
- Seed: `845320260914`
- Layers: Safehouse, Alias, Getup, Disguise, Headpiece, Instrument, Chain Trail, Evidence Mark
- Compatibility exclusions: `7`

## Contents

- `images/`: flattened PNG art
- `json/`: token metadata with exact rendered pixel hashes
- `RBX-opensea-drop.csv`: OpenSea Studio import
- `stats.json`: realized trait distribution and uniqueness totals
- `provenance.json`: seed, roster digest, and per-token pixel hashes

## Reproduce

```bash
python scripts/build_robinbanx.py
python scripts/generate_robinbanx.py --count 16 --force
python scripts/generate_robinbanx.py --all --workers 6
```
