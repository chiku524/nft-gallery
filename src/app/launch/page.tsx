import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { collection } from "@/data/collection";

export const metadata: Metadata = {
  title: "OpenSea launch",
  description: "Upload the 10,000 generated pugs to an OpenSea Drop on Robinhood Chain.",
};

const steps = [
  {
    title: "OpenSea does not generate from trait layers",
    body: "Studio will not build PFPs from hats, bases, and backgrounds. You upload finished images. This repo already shuffled 10,000 unique combos into generated/images plus an OpenSea CSV.",
  },
  {
    title: "Create a Drop on Robinhood Chain",
    body: `In OpenSea Studio, create a Drop on ${collection.chain.name} (chain ID ${collection.chain.chainId}). Set supply to ${collection.supply.toLocaleString()}, add the logo and banner from public/brand, and keep the mint price at ${collection.mintPriceEth} ETH or whatever you choose.`,
  },
  {
    title: "Bulk-upload media + CSV",
    body: "OpenSea Drops accept up to 10,000 JPG files (5 GB total) and a metadata CSV of string traits. Upload every file in generated/images (1.jpg–10000.jpg) and generated/opensea-metadata.csv. Preview and edit names if needed, then publish.",
  },
  {
    title: "Or deploy the ERC-721 yourself",
    body: `contracts/PugsOnTheBlock.sol mints token IDs 1–${collection.supply.toLocaleString()}. Pin generated/json (or a metadata server) and set the base URI. Import that contract on OpenSea instead of using a Drop if you want a custom mint.`,
  },
];

export default function LaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch on OpenSea, Robinhood Chain.</h1>
      <p className="mt-4 text-muted-foreground">
        OpenSea supports Robinhood Chain, but it does not include a trait-layer generator. The
        supported path for a 10,000-piece PFP set is an OpenSea Drop: finished images plus a CSV.
        This repo already produced both.
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
        Drop upload notes:{" "}
        <a
          className="underline"
          href="https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop"
          target="_blank"
          rel="noreferrer"
        >
          Preparing metadata for your drop
        </a>
        . OpenSea on Robinhood Chain:{" "}
        <a className="underline" href={collection.opensea.blog} target="_blank" rel="noreferrer">
          announcement
        </a>
        .
      </p>
    </div>
  );
}
