export const groovy = {
  name: "Groovy Nation",
  symbol: "GROOVY",
  tagline: "Round noteheads. Stick limbs. One shared beat.",
  description:
    "Groovy Nation is an 8,888-piece collection of looping musical-note PFP GIFs. Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — then flattened onto one 12-frame GIF. Clip-art note mascots: round heads, black stems, dancing stick limbs.",
  story:
    "Welcome to Groovy Nation.\n\nAn 8,888-piece collection of looping musical-note PFP GIFs on Robinhood Chain. Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — then flattened onto one 12-frame GIF. The notehead is the face. A black stem goes up. Flags and beams sit at the top. Stick arms and legs dance on the beat.\n\nFour notes only: quarter, eighth, whole, and beamed. Bold outline, flat fill, cartoon notation. Shades sit on the head. Chains hang on the chin. Riffs float beside the beat. One shared clock.\n\nMinting on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    collection: "https://opensea.io/collection/groovy-nation/overview",
    listings: [
      { label: "Robinhood Chain", href: "https://opensea.io/collection/groovy-nation/overview" },
      { label: "Ink", href: "https://opensea.io/collection/groovies-on-ink" },
    ],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/groovy-nation/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type GroovyCollection = typeof groovy;
