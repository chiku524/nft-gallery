export const boogiesquad = {
  name: "Boogie Squad",
  symbol: "BOOG",
  tagline: "Mixed dancers. One groove. The floor never sits still.",
  description:
    "Boogie Squad is a 10,000-piece collection of looping jelly-cel dance PFP GIFs on Robinhood Chain. Each dancer is stacked from six layers — stage, lights, cast, face, fit, and prop — then flattened onto one 12-frame GIF. Cats, frogs, blobs, birds, robots, and more. A side-step. A groove. One shared clock.",
  story:
    "Boogie Squad.\n\nA 10,000-piece collection of looping jelly-cel dance PFP GIFs on Robinhood Chain. Each Boogie is stacked from six layers — stage, lights, cast, face, fit, and prop — then flattened onto one 12-frame GIF. Mixed cartoon dancers: cats, frogs, blobs, birds, little robots, bunnies, and pigs. Species is a trait. The floor is a trait. The groove is the loop.\n\nSoft vinyl fills. Cream outlines. Sausage limbs. Visible feet that step. Not a sticker fox. Not a bust-crop cat. Not a musical note. Not a risograph plate. One shared 12-frame, 90ms clock.\n\nMinting on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 10000,
  mintPriceEth: "0.005",
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
    collection: "https://opensea.io/collection/boogie-squad/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/boogie-squad/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/boogie-squad/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type BoogieSquadCollection = typeof boogiesquad;
