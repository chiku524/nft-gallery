# Street Heirs

Street Heirs is an original static editorial-vector PFP collection about personal style,
neighborhood craft, and the graphic language of the city.

## Locked brief

- Name: Street Heirs
- Ticker: HEIRS
- Subject: human streetwear portraits with surreal graphic overlays
- Chain: Robinhood Chain
- Planned supply: 5,555
- Planned mint price: 0.005 ETH
- Current phase: 16-image art prototype

The prototype is not a mint-ready drop. Full roster generation, provenance, marketplace
CSV files, site routes, brand campaign assets, and a mint contract begin only after the
visual system is approved.

## Drawing language

Portraits use clean cartoon shapes, midnight-blue contours, flat face planes, expressive
eyes and mouths, and controlled asymmetry. Authentic details come from varied face
structures, skin tones, protective hairstyles, contemporary cuts, tailoring, eyewear,
jewelry, and studio accessories. Graphic signals add crop marks, offset arcs, halftone
fields, type bars, prisms, waveform marks, and translucent color exposures. Repeated
details are intentionally sparse so the face, hairstyle, and clothing silhouette
remain dominant at avatar size. Backgrounds use muted solid fields with one restrained
motif—such as a disc, rule, panel, or arc—to keep the overall set simple and elegant.
Jewelry uses outlined, evenly spaced links and pearls with small controlled highlights
so necklaces remain readable instead of merging into a single decorative band.

The system is intentionally separate from previous collection painters. It does not
reuse their skeletons, palettes, materials, motion, or trait-layer names.

## Trait taxonomy

The stack is composited in this order:

1. `atmosphere` — architectural color grounds and large framing geometry
2. `tailoring` — outerwear, knitwear, sportswear, and workwear behind the portrait
3. `complexion` — skin tone, neck, ears, face structure, highlight plane, and nose
4. `coiffure` — hairstyles and integrated head coverings
5. `visage` — eyes, brows, liner, eyewear, and visor treatments
6. `cadence` — mouth, facial hair, and tooth details
7. `adornment` — jewelry and audio accessories
8. `signal` — foreground graphic marks

Signal placement varies by intent. Halftone, crop, pixel, and corner accents remain in
front. Halos, type bars, orbit lines, prism slices, waveforms, and translucent exposure
panels are composited directly behind the character.

The production kit contains 70 transparent 512×512 trait plates and 16 curated
signatures used as the opening tokens in the full roster.
Weights in `public/street-heirs-traits/manifest.json` express relative selection
probability; they are not final rarity percentages.

## Compatibility

The manifest records exclusions for combinations with known collisions, including
bulky head coverings with studio headphones, the visor with headphones, and the heavy
hoodie with a curb chain. The painter validates every signature before rendering.

## Deterministic build

The production art version and painter seed are:

```text
street-heirs-v1
street-heirs/production/v1
```

Generate the public trait kit, site catalogs, and a 16-token sample pack:

```bash
npm run generate:street-heirs
```

Bake the complete 5,555-token roster:

```bash
python3 scripts/build_street_heirs.py
python3 scripts/generate_street_heirs.py --all --workers 6
```

The production roster seed is `46635555`. The completed bake contains 5,555 unique
trait fingerprints and 5,555 unique rendered pixel hashes. Any art-layer change
requires a new art version and a complete provenance rebuild.

Outputs:

- `public/street-heirs-traits/` — trait plates and manifest
- `public/street-heirs-preview/1.png` through `16.png` — flattened portraits
- `public/street-heirs-preview/contact-sheet.jpg` — review sheet
- `public/brand/` — logo, collection tile, featured card, and marketplace banners
- `public/metadata/street-heirs.json` — collection metadata
- `public/metadata/street-heirs-description.txt` — marketplace description draft
- `src/data/street-heirs-traits.ts` — generated TypeScript trait catalog
- `src/data/street-heirs-gallery.ts` — generated signature gallery catalog
- `generated/street-heirs/images/` — full flattened PNG roster
- `generated/street-heirs/json/` — token metadata and exact pixel hashes
- `generated/street-heirs/HEIRS-opensea-drop.csv` — marketplace import sheet
- `generated/street-heirs/stats.json` — realized distributions and uniqueness totals
- `generated/street-heirs/provenance.json` — roster digest and per-token hashes

Bulk PNG and JSON directories are gitignored. They must be pinned to permanent storage
before a contract base URI or marketplace import is finalized.

## Website

The integrated collection experience is available at:

- `/street-heirs` — collection story and release facts
- `/street-heirs/gallery` — 16 signature portraits and recipes
- `/street-heirs/studio` — weighted, compatibility-aware live compositor
- `/street-heirs/traits` — all 70 plates and signal-placement labels
- `/street-heirs/launch` — verified Robinhood Chain details and release readiness

The website intentionally remains pre-launch. It does not display a contract address,
mint action, or OpenSea collection link until those resources exist and are verified.

## Approval checklist

- Portraits remain readable when displayed as small avatars.
- The 16 signatures have distinct silhouettes and no duplicate pixel hashes.
- Hairstyles, skin tones, face structures, and styling feel varied without reducing
  identity to stereotypes.
- Graphic signals complement the portraits instead of obscuring defining features.
- Clothing, hair, eyewear, jewelry, and foreground marks do not collide.
- The set feels original and does not replicate Jubilee's Hood or an existing painter
  in this repository.
- Full-roster stats report exactly 5,555 unique combinations and pixel hashes.
