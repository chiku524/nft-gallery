# Robin Banx

**Robin Banx** (`RBX`) is a 10,000-piece collection of static PNG PFPs planned for Base (chain ID `8453`). The mint is free; collectors pay only ETH gas. The collection route is `/robinbanx`.

## Visual system

Robin Banx uses an angular noir security-dossier collage language:

- masked human crooks, never mascots or oval bodies
- hard crop lines and offset paper geometry
- halftone shadows and photocopy texture
- evidence stamps, file numbers, and redactions
- multichain-themed accessories treated as seized objects
- a restrained coal, paper, evidence-red, and institutional-green palette

The final token is a 512×512 static PNG. Transparent trait PNGs are stacked in a fixed catalog order and flattened once; there is no animation clock.

## Site routes

- `/robinbanx` — collection case file
- `/robinbanx/gallery` — generated sample lineup and attributes
- `/robinbanx/studio` — interactive transparent-PNG assembly desk
- `/robinbanx/traits` — complete evidence/trait index
- `/robinbanx/launch` — Base deployment and marketplace checklist

The site expects generated catalogs at:

- `src/data/robinbanx-traits.ts`
- `src/data/robinbanx-gallery.ts`

Those catalogs are the source of truth for plate order, default and random selections, trait image paths, gallery samples, and sample attributes.

## Contract

`contracts/RobinBanx.sol` is an OpenZeppelin `ERC721Enumerable` and `Ownable` contract:

- name `Robin Banx`, symbol `RBX`
- hard cap of 10,000 tokens
- sequential token IDs beginning at `1`
- public payable mint with a zero price
- maximum 10 tokens per transaction
- owner-controlled mint state and base metadata URI
- metadata URI shape `{baseURI}{tokenId}.json`

Deployment sequence:

1. Export and inspect all 10,000 flattened PNGs and JSON records.
2. Pin image and metadata directories to durable storage.
3. Deploy to Base with the pinned metadata base URI.
4. Verify the contract source and test metadata plus a free mint.
5. Open minting only after the full set resolves correctly.

## Marketplace status

There is no live OpenSea collection URL yet. The site intentionally omits marketplace links until the verified Base contract has been imported and a real collection record exists. Do not substitute a guessed collection slug.

## Pre-launch checks

- Confirm every image and metadata record resolves by token ID.
- Confirm metadata names, descriptions, and trait labels match the generated catalogs.
- Confirm the owner address and Base network before deployment.
- Test quantities `1`, `10`, `0`, and `11`, plus sold-out behavior.
- Verify that any nonzero `msg.value` is rejected by the free mint.
- Record the deployed address, verification URL, and real marketplace URL after launch.
