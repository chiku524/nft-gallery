export const cera = {
  name: "Cera",
  symbol: "CERA",
  tagline: "Paraffin in glass. A nightstand. The wax is the loop.",
  description:
    "Cera is a 10,000-piece collection of looping lava-lamp PFP GIFs. Each lamp is stacked from seven plates — sill, socket, flask, serum, melt, coil, and lid — then flattened onto one 12-frame GIF. Paraffin in a glass flask on a nightstand. The wax is the loop.",
  story:
    "Cera.\n\nA 10,000-piece collection of looping lava-lamp PFP GIFs on Robinhood Chain. Each lamp is stacked from seven plates — sill, socket, flask, serum, melt, coil, and lid — then flattened onto one 12-frame GIF. Eight sockets: rocket, saucer, cone, cube, mushroom, chrome, walnut, and ceramic. The glass holds oil. The wax is the loop.\n\nA paraffin lamp on a nightstand, not a matchbook. Not a tin toy. Not a snow globe. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The flask stays seated on one envelope. The melt is the wax. One shared clock.\n\nMinting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 10000,
  mintPriceUsd: "0.25",
  mintPriceEth: "0.0001",
  frames: 12,
  frameDurationMs: 180,
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
    collection: "https://opensea.io/collection/cera/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/cera/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/cera/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type CeraCollection = typeof cera;
