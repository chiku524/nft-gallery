import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { ApngImage } from "@/components/apng-image";
import { inklings } from "@/data/inklings";

export const metadata: Metadata = {
  title: "OpenSea launch",
  description: "Upload flattened Inklings GIFs to an OpenSea Drop on Ink.",
};

const steps = [
  {
    title: "Traits stay layered. The drop is flattened.",
    body: "OpenSea does not stack APNG layers for you. Studio is a live compositor. For a Drop you upload finished GIFs plus a CSV. Run the generator to bake each token onto the shared 16-frame clock, then gif_bake.py to make the marketplace loops.",
  },
  {
    title: "Create a Drop on Ink",
    body: `In OpenSea Studio, create a Drop on ${inklings.chain.name} (chain ID ${inklings.chain.chainId}). Set supply to ${inklings.supply.toLocaleString()}, paste the project description, upload the listing kit from public/brand, and keep the mint price at ${inklings.mintPriceEth} ETH or whatever you choose.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: "Upload every file in generated/inklings/gifs (1.gif–5555.gif) and generated/inklings/INKLINGS-opensea-drop.csv. The CSV already uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). OpenSea plays GIF, not APNG. Preview the loops, then publish.",
  },
  {
    title: "Or deploy the ERC-721 yourself",
    body: `contracts/Inklings.sol mints token IDs 1–${inklings.supply.toLocaleString()}. Pin generated/inklings/json and set the base URI. Import that contract on OpenSea instead of using a Drop if you want a custom mint.`,
  },
];

export default function InklingsLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch on OpenSea, Ink.</h1>
      <p className="mt-4 text-muted-foreground">
        Inklings ships as layered ink-wash APNG traits and as flattened GIF tokens. OpenSea wants the
        GIF bake of those loops. The APNG stack stays in this repo for the studio and any later restack.
      </p>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", inklings.chain.name],
          ["Chain ID", String(inklings.chain.chainId)],
          ["Currency", inklings.chain.currency],
          ["Supply", inklings.supply.toLocaleString()],
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
          Collection name {inklings.name}. Symbol {inklings.symbol}. Category PFPs. The same copy lives in{" "}
          <code className="rounded bg-secondary px-1.5 py-0.5 text-xs">public/metadata/inklings-description.txt</code>.
        </p>
        <pre className="mt-5 overflow-x-auto whitespace-pre-wrap rounded-2xl bg-background p-4 text-sm leading-relaxed text-foreground">
          {inklings.story}
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
            ["Logo", "public/brand/logo-inklings.png", "512×512, 1:1", "/brand/logo-inklings.png"],
            ["Featured", "public/brand/featured-inklings.jpg", "1200×800, 3:2", "/brand/featured-inklings.jpg"],
            ["OpenSea banner", "public/brand/banner-inklings-opensea.jpg", "2800×700, 4:1", "/brand/banner-inklings-opensea.jpg"],
            ["Collection GIF", "public/brand/collection-inklings.gif", "1000×1000 loop", "/brand/collection-inklings.gif"],
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
          RPC {inklings.chain.rpcUrl}
          <br />
          Explorer {inklings.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton chain={inklings.chain} />
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
        <a className="underline" href={inklings.opensea.metadataGuide} target="_blank" rel="noreferrer">
          Preparing metadata for your drop
        </a>
        . OpenSea on Ink:{" "}
        <a className="underline" href={inklings.opensea.blog} target="_blank" rel="noreferrer">
          supported chains
        </a>
        .
      </p>
    </div>
  );
}
