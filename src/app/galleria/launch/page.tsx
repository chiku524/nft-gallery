import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { Button } from "@/components/ui/button";
import { galleria } from "@/data/galleria";

export const metadata: Metadata = {
  title: "Open edition launch",
  description: `Upload ${galleria.supply} Galleria On Ink GIFs as open editions on ${galleria.chain.name}.`,
};

const steps = [
  {
    title: "Each file is a finished painting.",
    body: "Galleria On Ink is not a trait stack. Each of the 500 works is painted by its own engine. The salon grid uses stills so 500 loops do not lock the page. Open the work to play the APNG. OpenSea does not play APNG, so the pack is a GIF bake of every work.",
  },
  {
    title: `Create an Open Edition collection on ${galleria.chain.name}`,
    body: `In OpenSea Studio, create a collection on ${galleria.chain.name} (chain ID ${galleria.chain.chainId}) and add 500 open-edition items — one per artwork. Do not set unique 1:1 supply. Paste the collection description from public/metadata/galleria-description.txt. Upload logo-galleria.png, featured-galleria.jpg, banner-galleria-opensea.jpg, and collection-galleria.gif from public/brand. Mint price is ${galleria.mintPriceEth} ETH.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: "Upload every file in generated/galleria/gifs (1.gif–500.gif) and generated/galleria/opensea-metadata.csv. The CSV uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). GIF is the media OpenSea will play.",
  },
];

export default function GalleriaLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch open editions on {galleria.chain.name}.</h1>
      <p className="mt-4 text-muted-foreground">
        Galleria On Ink ships as {galleria.supply} unique looping paintings. Each artwork is an open edition.
        The composition is 1:1. The mint is not.
      </p>
      <div className="mt-6">
        <Button asChild>
          <a href={galleria.opensea.collection} target="_blank" rel="noreferrer">
            OpenSea
          </a>
        </Button>
      </div>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", galleria.chain.name],
          ["Chain ID", String(galleria.chain.chainId)],
          ["Currency", galleria.chain.currency],
          ["Works", `${galleria.supply} × ${galleria.edition}`],
          ["Mint", `${galleria.mintPriceEth} ETH`],
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
          RPC {galleria.chain.rpcUrl}
          <br />
          Explorer {galleria.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton chain={galleria.chain} />
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
        <a className="underline" href={galleria.opensea.metadataGuide} target="_blank" rel="noreferrer">
          Preparing metadata for your drop
        </a>
        . Ink network docs:{" "}
        <a className="underline" href={galleria.chain.docs} target="_blank" rel="noreferrer">
          docs.inkonchain.com
        </a>
        .
      </p>
    </div>
  );
}
