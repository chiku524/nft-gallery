export const opaline = {
  name: "Opaline",
  symbol: "OPAL",
  tagline: "Eight glass reef fish. Iridescent film. One shared clock.",
  description:
    "Opaline is a 5,555-piece collection of looping smoked-glass PFP GIFs. Each portrait is stacked from seven layers — atelier, vapor, cast, sheen, regard, crest, and clasp — then flattened onto one 12-frame GIF. Eight crystal reef fish. Dichroic film. Editorial light.",
  story:
    "Opaline.\n\nA 5,555-piece collection of looping smoked-glass PFP GIFs on Base. Each portrait is stacked from seven layers — atelier, vapor, cast, sheen, regard, crest, and clasp — then flattened onto one 12-frame GIF. Eight saltwater fish, each its own glass: parrotfish, blue marlin, queen angelfish, lionfish, triggerfish, seahorse, green moray, and manta. Vapor hangs in the room. Light walks the facets. Film shifts hue. Inclusions dim.\n\nCrystal reef fish. Seven films, including bare glass. No charcoal outline. No sticker cutout. The fish stays seated. One shared clock.\n\nMinting on Base (chain ID 8453). Gas is ETH.",
  supply: 5555,
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
