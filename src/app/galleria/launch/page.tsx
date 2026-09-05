import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { ApngImage } from "@/components/apng-image";
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
    body: `In OpenSea Studio, create a collection on ${galleria.chain.name} (chain ID ${galleria.chain.chainId}) and add 500 open-edition items — one per artwork. Do not set unique 1:1 supply. Paste the collection description, upload the listing kit from public/brand, and set mint to ${galleria.mintPriceEth} ETH.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: "Upload every file in generated/galleria/gifs (1.gif–500.gif) and generated/galleria/GOI-opensea-drop.csv. The CSV uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). GIF is the media OpenSea will play.",
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

      <div className="mt-10 rounded-[1.75rem] border bg-card p-6 sm:p-8">
        <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Project description</p>
        <h2 className="mt-2 font-heading text-2xl">Paste this into OpenSea.</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Collection name {galleria.name}. Symbol {galleria.symbol}. Category Art. The same copy lives in{" "}
          <code className="rounded bg-secondary px-1.5 py-0.5 text-xs">public/metadata/galleria-description.txt</code>.
        </p>
        <pre className="mt-5 overflow-x-auto whitespace-pre-wrap rounded-2xl bg-background p-4 text-sm leading-relaxed text-foreground">
          {galleria.story}
        </pre>
      </div>

      <div className="mt-8 rounded-[1.75rem] border bg-card p-6 sm:p-8">
        <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Listing kit</p>
        <h2 className="mt-2 font-heading text-2xl">Logo, featured, banner, collection GIF.</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          OpenSea wants a square logo, a 3:2 featured image, and a wide 4:1 banner — three different pictures,
          no type on the marketplace images. The site hero can keep the titled banner.
        </p>
        <ul className="mt-6 grid gap-4 sm:grid-cols-2">
          {[
            ["Logo", "public/brand/logo-galleria.png", "512×512, 1:1", "/brand/logo-galleria.png"],
            ["Featured", "public/brand/featured-galleria.jpg", "1200×800, 3:2", "/brand/featured-galleria.jpg"],
            ["OpenSea banner", "public/brand/banner-galleria-opensea.jpg", "2800×700, 4:1", "/brand/banner-galleria-opensea.jpg"],
            ["Collection GIF", "public/brand/collection-galleria.gif", "1000×1000 loop", "/brand/collection-galleria.gif"],
          ].map(([label, path, size, src]) => (
            <li key={label} className="overflow-hidden rounded-2xl border bg-background">
              <ApngImage src={src} alt={`${label} preview`} className="aspect-[3/2] w-full object-cover" />
              <div className="space-y-1 p-3">
                <p className="font-medium">{label}</p>
                <p className="text-xs text-muted-foreground">{size}</p>
                <p className="break-all text-xs text-muted-foreground">{path}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>

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
        . Kit notes:{" "}
        <code className="rounded bg-secondary px-1.5 py-0.5 text-xs">generated/galleria/README.md</code>
        . Ink network docs:{" "}
        <a className="underline" href={galleria.chain.docs} target="_blank" rel="noreferrer">
          docs.inkonchain.com
        </a>
        .
      </p>
    </div>
  );
}
