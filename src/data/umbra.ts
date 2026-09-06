export const umbra = {
  name: "Umbra",
  symbol: "UMBR",
  tagline: "Leather silhouettes. Brass brads. A lamp that dances with the limbs.",
  description:
    "Umbra is an 8,888-piece collection of looping shadow-puppet PFP GIFs. Each shade is stacked from seven plates — cloth, ember, cast, hinge, cutwork, leaf, and soot — then flattened onto one 12-frame GIF. Leather silhouettes. Brass brads. A lamp that dances with the limbs.",
  story:
    "Umbra.\n\nAn 8,888-piece collection of looping shadow-puppet PFP GIFs on Robinhood Chain. Each shade is stacked from seven plates — cloth, ember, cast, hinge, cutwork, leaf, and soot — then flattened onto one 12-frame GIF. Eight dancing casts: clown, knight, bride, ogre, sage, harper, bird, and demon. Hinges swing the step. Cutwork lets the lamp through. Gold leaf rides the hide.\n\nLeather on a woven screen. Not risograph blots. Not origami facets. Not an engraved bust. The cast stays seated in one envelope. The dance is in the joints. One shared clock.\n\nMinting free on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    collection: "https://opensea.io/collection/umbra/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/umbra/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/umbra/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type UmbraCollection = typeof umbra;
