export const partyPandas = {
  name: "Party Pandas",
  symbol: "PAND",
  tagline: "Looping party-panda PFP GIFs that never sit still.",
  description:
    "Party Pandas is a 4,444-piece collection of looping party-panda PFP GIFs on Base. Each panda is stacked from six layers — venue, glow, panda, mood, fit, and extra — then flattened onto one 12-frame GIF. Classic black-and-white markings, crisp outlines, fluffy fur. Clubs pulse. Hats bounce. Confetti never lands.",
  story:
    "Party Pandas never sit still.\n\nA 4,444-piece collection of looping party-panda PFP GIFs on Base. Each panda is stacked from six layers — venue, glow, panda, mood, fit, and extra — then flattened onto one 12-frame GIF. Clubs pulse. Eyes blink. Hats bounce. Confetti never lands.\n\nCartoon pandas with classic black-and-white markings, crisp outlines, and fluffy fur. Soft edges. One shared clock.\n\nMinting on Base (chain ID 8453). Gas is ETH.",
  supply: 4444,
  mintPriceEth: "0.004",
  frames: 12,
  frameDurationMs: 80,
  canvas: 512,
  chain: {
    name: "Base",
    chainId: 8453,
    chainIdHex: "0x2105",
    currency: "ETH",
    rpcUrl: "https://mainnet.base.org",
    explorer: "https://basescan.org",
    docs: "https://docs.base.org/docs",
  },
  opensea: {
    chainSlug: "base",
    collection: "https://opensea.io/collection/party-pandas/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/party-pandas/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type PartyPandasCollection = typeof partyPandas;
