export const noxelle = {
  name: "Noxelle",
  symbol: "NOXL",
  tagline: "Bent glass. Noble gas. A dancer that is the tube.",
  description:
    "Noxelle is a 10,000-piece collection of looping neon-tube PFP GIFs. Each sign is stacked from seven plates — wall, spill, gas, bend, clip, badge, and mote — then flattened onto one 12-frame GIF. Bent glass. Noble gas. A dancer that is the tube.",
  story:
    "Noxelle.\n\nA 10,000-piece collection of looping neon-tube PFP GIFs on Robinhood Chain. Each sign is stacked from seven plates — wall, spill, gas, bend, clip, badge, and mote — then flattened onto one 12-frame GIF. Eight bends: sway, kick, wave, hop, point, dip, spin, and split. Argon, neon, krypton, mercury. Clips hold the glass. Spill stains the club wall.\n\nBent tubing, not a filled body. No sticker edge. No egg. Not a shadow puppet. Not a musical note. The dancer stays seated on one envelope. The dance is the bend. One shared clock.\n\nMinting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 10000,
  mintPriceUsd: "0.25",
  mintPriceEth: "0.0001",
  frames: 12,
  frameDurationMs: 90,
  canvas: 512,
  chain: {
    name: "Robinhood Chain",
    chainId: 4663,
    chainIdHex: "0x1237",
    currency: "ETH",
    rpcUrl: "https://rpc.mainnet.chain.robinhood.com",
    explorer: "https://robinhoodchain.blockscout.com",
    docs: "https://docs.robinhood.com/chain/connecting/",
  },
  opensea: {
    chainSlug: "robinhood",
    collection: "https://opensea.io/collection/noxelle/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/noxelle/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/noxelle/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type NoxelleCollection = typeof noxelle;
