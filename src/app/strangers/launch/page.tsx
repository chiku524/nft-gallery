import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { Button } from "@/components/ui/button";
import { strangers } from "@/data/strangers";

export const metadata: Metadata = {
  title: "Open edition launch",
  description: `Upload ${strangers.supply} Strangers GIFs as open editions on ${strangers.chain.name}.`,
};

const steps = [
  {
    title: "Each file is a finished painting.",
    body: "Strangers is not a trait stack. Each of the 24 works is painted by its own engine. The site shows APNG loops. OpenSea does not play APNG, so the pack is a GIF bake of every work.",
  },
  {
    title: `Create an Open Edition collection on ${strangers.chain.name}`,
    body: `In OpenSea Studio, create a collection on ${strangers.chain.name} (chain ID ${strangers.chain.chainId}) and add 24 open-edition items — one per artwork. Do not set unique 1:1 supply. Paste the collection description from public/metadata/strangers-description.txt. Upload logo-strangers.png, featured-strangers.jpg, banner-strangers-opensea.jpg, and collection-strangers.gif from public/brand. Mint price is ${strangers.mintPriceEth} ETH.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: "Upload every file in generated/strangers/gifs (1.gif–24.gif) and generated/strangers/opensea-metadata.csv. The CSV uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). GIF is the media OpenSea will play.",
  },
];

export default function StrangersLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch open editions on {strangers.chain.name}.</h1>
      <p className="mt-4 text-muted-foreground">
        Strangers ships as {strangers.supply} unique looping paintings. Each artwork is an open edition.
        The composition is 1:1. The mint is not.
      </p>
      <div className="mt-6">
        <Button asChild>
          <a href={strangers.opensea.collection} target="_blank" rel="noreferrer">
            OpenSea
          </a>
        </Button>
      </div>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", strangers.chain.name],
          ["Chain ID", String(strangers.chain.chainId)],
          ["Currency", strangers.chain.currency],
          ["Works", `${strangers.supply} × ${strangers.edition}`],
          ["Mint", `${strangers.mintPriceEth} ETH`],
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
          RPC {strangers.chain.rpcUrl}
          <br />
          Explorer {strangers.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton chain={strangers.chain} />
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
        <a className="underline" href={strangers.opensea.metadataGuide} target="_blank" rel="noreferrer">
          Preparing metadata for your drop
        </a>
        . Base network docs:{" "}
        <a className="underline" href={strangers.chain.docs} target="_blank" rel="noreferrer">
          docs.base.org
        </a>
        .
      </p>
    </div>
  );
}
