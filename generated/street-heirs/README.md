# Street Heirs static generation pack

Deterministic 512×512 clean-cartoon portraits for Robinhood Chain (`4663`). This export contains 5,555 of the 5,555 token supply.

## Collection

- Symbol: `HEIRS`
- Supply: `5,555`
- Mint: `0.005 ETH`
- Roster seed: `46635555`
- Art version: `street-heirs-v1`
- Layers: Atmosphere, Complexion, Tailoring, Coiffure, Visage, Cadence, Adornment, Signal
- Compatibility exclusions: `5`

## Contents

- `images/`: flattened PNG art
- `json/`: token metadata with exact rendered pixel hashes
- `HEIRS-opensea-drop.csv`: OpenSea Studio import
- `stats.json`: realized trait distribution and uniqueness totals
- `provenance.json`: roster digest and per-token pixel hashes

## Reproduce

```bash
python3 scripts/build_street_heirs.py
python3 scripts/generate_street_heirs.py --count 16 --force
python3 scripts/generate_street_heirs.py --all --workers 6
```
