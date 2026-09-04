export const groovy = {
  name: "Groovy Nation",
  symbol: "GROOVY",
  tagline: "Chrome notes. Sunset stages. One shared beat.",
  description:
    "Groovy Nation is an 8,888-piece collection of looping musical-note PFP GIFs. Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — then flattened onto one 12-frame GIF. Airbrushed chrome. Sunset fill. Notes that dance.",
  story:
    "Welcome to Groovy Nation.\n\nAn 8,888-piece collection of looping musical-note PFP GIFs on Robinhood Chain. Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — then flattened onto one 12-frame GIF. Chrome note-heads. Stems that dance. Lava-lamp stages.\n\nFour notes only: quarter, eighth, whole, and beamed. The drawing stays airbrushed — soft discs, sunset fill, no ink outline. Shades sit on the head. Chains hang on the stem. Riffs float beside the beat. One shared clock.\n\nMinting on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/groovy-nation/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type GroovyCollection = typeof groovy;
