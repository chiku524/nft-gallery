export const nivora = {
  name: "Nivora",
  symbol: "NIVO",
  tagline: "A dome of liquor. A turned plinth. Glitter is the loop.",
  description:
    "Nivora is a 10,000-piece collection of looping snow-globe PFP GIFs. Each souvenir is stacked from seven plates — plinth, bath, vista, flurry, lens, collar, and plaque — then flattened onto one 12-frame GIF. A dome of liquor on a lathe-turned base. Glitter is the loop.",
  story:
    "Nivora.\n\nA 10,000-piece collection of looping snow-globe PFP GIFs on Robinhood Chain. Each souvenir is stacked from seven plates — plinth, bath, vista, flurry, lens, collar, and plaque — then flattened onto one 12-frame GIF. Eight vistas: cabin, pine, lighthouse, deer, chapel, tram, bridge, and moon. Glycerin holds the flake. A collar seats the dome.\n\nA sphere on a turned plinth, not a dancer. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The globe stays seated on one envelope. The weather is the flurry. One shared clock.\n\nMinting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    collection: "https://opensea.io/collection/nivora/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/nivora/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/nivora/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type NivoraCollection = typeof nivora;
