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
remain dominant at avatar size.

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

The prototype contains 70 transparent 512×512 trait plates and 16 curated signatures.
Weights in `public/street-heirs-traits/manifest.json` express relative selection
probability; they are not final rarity percentages.

## Compatibility

The manifest records exclusions for combinations with known collisions, including
bulky head coverings with studio headphones, the visor with headphones, and the heavy
hoodie with a curb chain. The painter validates every signature before rendering.

## Deterministic build

The art version and seed are:

```text
prototype-4
street-heirs/clean-cartoon/v4
```

Generate the prototype from the repository root:

```bash
npm run generate:street-heirs
```

Outputs:

- `public/street-heirs-traits/` — trait plates and manifest
- `public/street-heirs-preview/1.png` through `16.png` — flattened portraits
- `public/street-heirs-preview/contact-sheet.jpg` — review sheet
- `public/metadata/street-heirs.json` — lightweight collection metadata
- `public/metadata/street-heirs-description.txt` — marketplace description draft
- `src/data/street-heirs-traits.ts` — generated TypeScript trait catalog

## Approval checklist

- Portraits remain readable when displayed as small avatars.
- The 16 signatures have distinct silhouettes and no duplicate pixel hashes.
- Hairstyles, skin tones, face structures, and styling feel varied without reducing
  identity to stereotypes.
- Graphic signals complement the portraits instead of obscuring defining features.
- Clothing, hair, eyewear, jewelry, and foreground marks do not collide.
- The set feels original and does not replicate Jubilee's Hood or an existing painter
  in this repository.
- The taxonomy has enough compatible combinations to support a later 5,555-token bake.
