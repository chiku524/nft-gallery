import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { collection } from "@/data/collection";

export const metadata: Metadata = {
  title: "OpenSea launch",
  description: "How to list Pugs On The Block on OpenSea on Robinhood Chain.",
};

const steps = [
  {
    title: "Pin the art and metadata",
    body: "Upload public/traits, public/gallery, and public/metadata to IPFS (or any OpenSea-compatible URI). Point each token’s image field at the finished PNG.",
  },
  {
    title: "Deploy the ERC-721 on Robinhood Chain",
    body: `Use contracts/PugsOnTheBlock.sol. Network: ${collection.chain.name}, chain ID ${collection.chain.chainId}, RPC ${collection.chain.rpcUrl}. Gas token is ETH.`,
  },
  {
    title: "Verify on Blockscout",
    body: `Confirm the contract at ${collection.chain.explorer.replace("https://", "")}, then set the base URI to your metadata folder.`,
  },
  {
    title: "Submit the collection on OpenSea",
    body: "OpenSea already supports Robinhood Chain. Import the contract, add the banner and logo from public/brand, and publish. No separate marketplace app.",
  },
];

export default function LaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch on OpenSea, Robinhood Chain.</h1>
      <p className="mt-4 text-muted-foreground">
        Robinhood Chain is an Ethereum Layer 2 (Arbitrum tech) that went public on July 1, 2026.
        OpenSea added the chain on July 11 — NFTs, Stock Tokens, and memecoins trade in the same
        interface. This collection is built as ordinary ERC-721s for that network.
      </p>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", collection.chain.name],
          ["Chain ID", String(collection.chain.chainId)],
          ["Currency", collection.chain.currency],
          ["Supply", collection.supply.toLocaleString()],
        ].map(([label, value]) => (
          <div key={label} className="rounded-2xl border bg-card p-4">
            <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
            <dd className="mt-1 font-medium break-all">{value}</dd>
          </div>
        ))}
      </dl>

      <div className="mt-8 rounded-2xl border bg-card p-5">
        <p className="font-heading text-xl">Wallet setup</p>
        <p className="mt-2 text-sm text-muted-foreground">
          RPC {collection.chain.rpcUrl}
          <br />
          Explorer {collection.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton />
        </div>
      </div>

      <ol className="mt-10 space-y-6">
        {steps.map((step, index) => (
          <li key={step.title} className="grid grid-cols-[auto_1fr] gap-4">
            <span className="flex size-8 items-center justify-center rounded-full bg-foreground text-sm text-background">
              {index + 1}
            </span>
            <div>
              <h2 className="font-heading text-2xl">{step.title}</h2>
              <p className="mt-1 text-muted-foreground">{step.body}</p>
            </div>
          </li>
        ))}
      </ol>

      <p className="mt-10 text-sm text-muted-foreground">
        OpenSea overview:{" "}
        <a className="underline" href={collection.opensea.blog} target="_blank" rel="noreferrer">
          Robinhood Chain is live on OpenSea
        </a>
        . Chain docs:{" "}
        <a className="underline" href={collection.chain.docs} target="_blank" rel="noreferrer">
          Connecting to Robinhood Chain
        </a>
        .
      </p>
    </div>
  );
}
