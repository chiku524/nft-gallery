export const streetHeirs = {
  name: "Street Heirs",
  symbol: "HEIRS",
  tagline: "The city leaves signals. The next generation wears them forward.",
  description:
    "Street Heirs is a 5,555-piece collection of static editorial cartoon portraits on Robinhood Chain. Each heir combines eight hand-built plates into a crisp 512×512 PNG.",
  story:
    "Street Heirs is a portrait of inheritance in motion: the style, sound, confidence, and visual language passed through a city without ever standing still.\n\nEach character is assembled from eight illustrated plates. Tailoring and adornment carry personal detail; atmosphere and signal place each heir inside a wider broadcast. Some signals sit behind the character, while others cut across the foreground.\n\nThe full 5,555-piece art bake is complete. Contract deployment and marketplace publishing remain ahead, so the collection is presented here as a pre-launch archive and working studio.",
  supply: 5555,
  mintPriceEth: "0.005",
  format: "Static PNG",
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
  marketplace: {
    status: "pre-launch",
    collection: "",
    listings: [],
  },
  release: {
    contractAddress: null,
    creatorWallet: null,
    launchDate: null,
    openSeaUrl: null,
  },
} as const;

export type StreetHeirsCollection = typeof streetHeirs;
