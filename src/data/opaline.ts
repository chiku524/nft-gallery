export const opaline = {
  name: "Opaline",
  symbol: "OPAL",
  tagline: "Eight glass beasts. Iridescent film. One seated face.",
  description:
    "Opaline is a 10,000-piece collection of looping smoked-glass PFP GIFs. Each portrait is stacked from six layers — atelier, cast, sheen, regard, crest, and clasp — then flattened onto one 12-frame GIF. Eight crystal beasts. Dichroic film. Editorial light.",
  story:
    "Opaline.\n\nA 10,000-piece collection of looping smoked-glass PFP GIFs on Base. Each portrait is stacked from six layers — atelier, cast, sheen, regard, crest, and clasp — then flattened onto one 12-frame GIF. Eight beasts share one seated face: stag, serpent, moth, beetle, ram, ibis, wyrm, and mantis. Light walks the facets. Film shifts hue. Inclusions dim.\n\nCrystal creatures. Seven films, including bare glass. No charcoal outline. No sticker cutout. The beast stays seated. One shared clock.\n\nMinting on Base (chain ID 8453). Gas is ETH.",
  supply: 10000,
  mintPriceEth: "0.005",
  frames: 12,
  frameDurationMs: 90,
  canvas: 512,
  chain: {
    name: "Base",
    chainId: 8453,
    chainIdHex: "0x2105",
    currency: "ETH",
    rpcUrl: "https://mainnet.base.org",
    explorer: "https://basescan.org",
    docs: "https://docs.base.org",
  },
  opensea: {
    chainSlug: "base",
    collection: "https://opensea.io/collection/opaline/overview",
    listings: [{ label: "Base", href: "https://opensea.io/collection/opaline/overview" }],
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/opaline/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type OpalineCollection = typeof opaline;
