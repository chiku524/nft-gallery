export const risota = {
  name: "Risota",
  symbol: "RISO",
  tagline: "Spot ink. Fat dancers. Plates that miss the register.",
  description:
    "Risota is an 8,888-piece collection of looping risograph PFP GIFs. Each print is stacked from seven plates — stock, screen, figure, pass, knockout, slug, and mark — then flattened onto one 12-frame GIF. Dancing characters as overlapping ink. Misregister on the beat.",
  story:
    "Risota.\n\nAn 8,888-piece collection of looping risograph PFP GIFs on Robinhood Chain. Each print is stacked from seven plates — stock, screen, figure, pass, knockout, slug, and mark — then flattened onto one 12-frame GIF. Eight dancers, each its own spot ink: kick, twirl, pop, sway, hop, glide, stomp, and reach. A second plate slides out of register. Halftone hangs on the sheet. Faces knock through as a dark drum.\n\nSoy ink on uncoated paper. Fat blots, not outlines. No sticker edge. No egg body. The dancer stays seated on one envelope. One shared clock.\n\nMinting on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 8888,
  mintPriceEth: "0.003",
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
    collection: "https://opensea.io/collection/risota/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/risota/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/risota/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type RisotaCollection = typeof risota;
