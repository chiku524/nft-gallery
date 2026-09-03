import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { ApngImage } from "@/components/apng-image";
import { Button } from "@/components/ui/button";
import { shookums } from "@/data/shookums";

export const metadata: Metadata = {
  title: "OpenSea launch",
  description: "Upload flattened Halloween Shook'ums GIFs to an OpenSea Drop on Abstract.",
};

const steps = [
  {
    title: "Traits stay layered. The drop is flattened.",
    body: "OpenSea does not stack APNG layers for you. Studio is a live compositor. For a Drop you upload finished GIFs plus a CSV. Run the generator to bake each token onto the shared 12-frame clock, then gif_bake.py to make the marketplace loops.",
  },
  {
    title: "Create a Drop on Abstract",
    body: `In OpenSea Studio, create a Drop on ${shookums.chain.name} (chain ID ${shookums.chain.chainId}). Set supply to ${shookums.supply.toLocaleString()}, paste the project description, and upload the listing kit from public/brand.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: `Upload every file in generated/shookums/gifs (1.gif–${shookums.supply}.gif) and generated/shookums/SHOOKUMS-opensea-drop.csv. The CSV already uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). OpenSea plays GIF, not APNG. Preview the loops, then publish.`,
  },
  {
    title: "Or deploy the ERC-721 yourself",
    body: `contracts/Shookums.sol mints token IDs 1–${shookums.supply.toLocaleString()}. Pin generated/shookums/json and set the base URI. Import that contract on OpenSea instead of using a Drop if you want a custom mint. Gas is ETH.`,
  },
];

export default function ShookumsLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch on OpenSea, Abstract.</h1>
      <p className="mt-4 text-muted-foreground">
        Halloween Shook&apos;ums ships as layered APNG traits and as flattened GIF tokens. OpenSea wants
        the GIF bake of those loops. The APNG stack stays in this repo for the studio and any later
        restack.
      </p>
      <div className="mt-6">
        <Button asChild>
          <a href={shookums.opensea.collection} target="_blank" rel="noreferrer">
            View the live collection on OpenSea
          </a>
        </Button>
      </div>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", shookums.chain.name],
          ["Chain ID", String(shookums.chain.chainId)],
          ["Currency", shookums.chain.currency],
          ["Supply", shookums.supply.toLocaleString()],
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
          Collection name {shookums.name}. Symbol {shookums.symbol}. Category PFPs. The same copy lives in{" "}
          <code className="rounded bg-secondary px-1.5 py-0.5 text-xs">public/metadata/shookums-description.txt</code>.
        </p>
        <pre className="mt-5 overflow-x-auto whitespace-pre-wrap rounded-2xl bg-background p-4 text-sm leading-relaxed text-foreground">
          {shookums.story}
        </pre>
      </div>

      <div className="mt-8 rounded-[1.75rem] border bg-card p-6 sm:p-8">
        <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Listing kit</p>
        <h2 className="mt-2 font-heading text-2xl">Logo, featured, banner, collection GIF.</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          OpenSea wants a square logo, a 3:2 featured image, and a wide 4:1 banner — three different pictures,
          no type on the marketplace images. The site hero can reuse the taller banner.
        </p>
        <ul className="mt-6 grid gap-4 sm:grid-cols-2">
          {[
            ["Logo", "public/brand/logo-shookums.png", "512×512, 1:1", "/brand/logo-shookums.png"],
            ["Featured", "public/brand/featured-shookums.jpg", "1200×800, 3:2", "/brand/featured-shookums.jpg"],
            ["OpenSea banner", "public/brand/banner-shookums-opensea.jpg", "2800×700, 4:1", "/brand/banner-shookums-opensea.jpg"],
            ["Collection GIF", "public/brand/collection-shookums.gif", "1000×1000 loop", "/brand/collection-shookums.gif"],
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
          RPC {shookums.chain.rpcUrl}
          <br />
          Explorer {shookums.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton chain={shookums.chain} />
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
        <a className="underline" href={shookums.opensea.metadataGuide} target="_blank" rel="noreferrer">
          Preparing metadata for your drop
        </a>
        . Live collection:{" "}
        <a className="underline" href={shookums.opensea.collection} target="_blank" rel="noreferrer">
          opensea.io/collection/halloween-shookums
        </a>
        . OpenSea-compatible chains:{" "}
        <a className="underline" href={shookums.opensea.blog} target="_blank" rel="noreferrer">
          blockchains compatible with OpenSea
        </a>
        .
      </p>
    </div>
  );
}
