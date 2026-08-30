# Loopkins drop files

Each token is a flattened APNG. Traits themselves stay layered in `public/traits/`.

```bash
python3 scripts/generate_collection.py        # 16 samples
python3 scripts/generate_collection.py --all  # full 3,333
```

Upload `images/*.png` plus `opensea-metadata.csv` to an OpenSea Drop.
