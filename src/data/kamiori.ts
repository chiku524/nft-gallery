export const kamiori = {
  name: "Kamiori",
  symbol: "KMIO",
  tagline: "Polygonal facets. Valley scores. A corner that lifts.",
  description:
    "Kamiori is an 8,888-piece collection of looping origami PFP GIFs. Each sheet is stacked from seven plates — pulp, fleck, fold, score, facet, seal, and draft — then flattened onto one 12-frame GIF. Polygonal facets. Valley and mountain scores. A corner that lifts.",
  story:
    "Kamiori.\n\nAn 8,888-piece collection of looping origami PFP GIFs on Robinhood Chain. Each sheet is stacked from seven plates — pulp, fleck, fold, score, facet, seal, and draft — then flattened onto one 12-frame GIF. Eight folds, each its own washi dye: crane, frog, beetle, boat, hare, fan, kite, and lotus. A crease diagram sits on the paper. A draft lifts one corner.\n\nDeckle washi. Angular facets. No engraved bust. No perforated stamp. No charcoal outline. No sticker cutout. The fold stays seated. One shared clock.\n\nMinting free on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 8888,
  mintPriceEth: "0",
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
    collection: "https://opensea.io/collection/kamiori/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/kamiori/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/kamiori/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type KamioriCollection = typeof kamiori;
