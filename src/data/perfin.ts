export const perfin = {
  name: "Perfin",
  symbol: "PRFN",
  tagline: "Intaglio hatch. Perforated edges. A cancel that walks.",
  description:
    "Perfin is an 8,888-piece collection of looping engraved postage-stamp PFP GIFs. Each frank is stacked from seven plates — wove, guilloche, bust, surcharge, aspect, device, and cancel — then flattened onto one 12-frame GIF. Intaglio hatch. Perforated edges. A cancellation that walks.",
  story:
    "Perfin.\n\nAn 8,888-piece collection of looping engraved postage-stamp PFP GIFs on Robinhood Chain. Each frank is stacked from seven plates — wove, guilloche, bust, surcharge, aspect, device, and cancel — then flattened onto one 12-frame GIF. Eight busts, each its own stamp ink: pilot, keeper, clerk, captain, botanist, mapper, signal, and warden. Guilloche turns behind the vignette. A cancellation walks the face.\n\nIntaglio lines on wove paper. Perforated rectangle. No charcoal outline. No sticker cutout. No dancing blot. The bust stays seated. One shared clock.\n\nMinting free on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    collection: "https://opensea.io/collection/perfin/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/perfin/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/perfin/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type PerfinCollection = typeof perfin;
