import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { ApngImage } from "@/components/apng-image";
import { Button } from "@/components/ui/button";
import { noxelle } from "@/data/noxelle";
import { openSeaListings } from "@/lib/opensea";

export const metadata: Metadata = {
  title: "OpenSea launch",
  description: "Upload flattened Noxelle GIFs to a $0.25 OpenSea Drop on Robinhood Chain.",
};

const steps = [
  {
    title: "Traits stay layered. The drop is flattened.",
    body: "OpenSea does not stack APNG layers for you. Studio is a live compositor. For a Drop you upload finished GIFs plus a CSV. Bake the full 10,000-token pack with python3 scripts/generate_noxelle.py --all — gifs/, NOXELLE-opensea-drop.csv, and the kit README land in generated/noxelle/.",
  },
  {
    title: "Create a Drop on Robinhood Chain",
    body: `In OpenSea Studio, create a Drop on ${noxelle.chain.name} (chain ID ${noxelle.chain.chainId}). Set supply to ${noxelle.supply.toLocaleString()}, set mint to $${noxelle.mintPriceUsd}, paste the project description, and upload the listing kit from public/brand.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: `Upload every file in generated/noxelle/gifs (1.gif–${noxelle.supply}.gif) and generated/noxelle/NOXELLE-opensea-drop.csv. The CSV already uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). OpenSea plays GIF, not APNG. Preview the loops, then publish.`,
  },
  {
    title: "Or deploy the ERC-721 yourself",
    body: `contracts/Noxelle.sol mints token IDs 1–${noxelle.supply.toLocaleString()} at ${noxelle.mintPriceEth} ETH (about $${noxelle.mintPriceUsd}; owner can retune the wei amount). Pin generated/noxelle/json and set the base URI. Import that contract on OpenSea instead of using a Drop if you want a custom mint. Gas is ETH.`,
  },
];

export default function NoxelleLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch on OpenSea, Robinhood Chain.</h1>
      <p className="mt-4 text-muted-foreground">
        Noxelle ships as layered APNG traits and as flattened GIF tokens. OpenSea wants
        the GIF bake of those loops. The mint is ${noxelle.mintPriceUsd}. The APNG stack stays in this repo for the
        studio and any later restack.
      </p>
      <div className="mt-6 flex flex-wrap gap-3">
        {openSeaListings(noxelle.opensea).map((listing) => (
          <Button key={listing.href} asChild className="bg-[#e14bff] text-[#12081c] hover:bg-[#e14bff]/90">
            <a href={listing.href} target="_blank" rel="noreferrer">
              OpenSea · {listing.label}
            </a>
          </Button>
        ))}
      </div>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", noxelle.chain.name],
          ["Chain ID", String(noxelle.chain.chainId)],
          ["Currency", noxelle.chain.currency],
          ["Supply", noxelle.supply.toLocaleString()],
          ["Mint", `$${noxelle.mintPriceUsd}`],
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
          Collection name {noxelle.name}. Symbol {noxelle.symbol}. Category PFPs. The same copy lives in{" "}
          <code className="rounded bg-secondary px-1.5 py-0.5 text-xs">public/metadata/noxelle-description.txt</code>.
        </p>
        <pre className="mt-5 overflow-x-auto whitespace-pre-wrap rounded-2xl bg-background p-4 text-sm leading-relaxed text-foreground">
          {noxelle.story}
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
            ["Logo", "public/brand/logo-noxelle.png", "512×512, 1:1", "/brand/logo-noxelle.png"],
            ["Featured", "public/brand/featured-noxelle.jpg", "1200×800, 3:2", "/brand/featured-noxelle.jpg"],
            ["OpenSea banner", "public/brand/banner-noxelle-opensea.jpg", "2800×700, 4:1", "/brand/banner-noxelle-opensea.jpg"],
            ["Collection GIF", "public/brand/collection-noxelle.gif", "1000×1000 loop", "/brand/collection-noxelle.gif"],
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
          RPC {noxelle.chain.rpcUrl}
          <br />
          Explorer {noxelle.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton chain={noxelle.chain} />
        </div>
      </div>

      <ol className="mt-10 space-y-6">
        {steps.map((step, index) => (
          <li key={step.title} className="grid grid-cols-[auto_1fr] gap-4">
            <span className="flex size-8 items-center justify-center rounded-full bg-[#e14bff] text-sm text-[#12081c]">
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
        <a className="underline" href={noxelle.opensea.metadataGuide} target="_blank" rel="noreferrer">
          Preparing metadata for your drop
        </a>
        . Live collections:{" "}
        {openSeaListings(noxelle.opensea).map((listing, index) => (
          <span key={listing.href}>
            {index > 0 ? " · " : null}
            <a className="underline" href={listing.href} target="_blank" rel="noreferrer">
              {listing.label}
            </a>
          </span>
        ))}
        . OpenSea on Robinhood Chain:{" "}
        <a className="underline" href={noxelle.opensea.blog} target="_blank" rel="noreferrer">
          Robinhood Chain is live on OpenSea
        </a>
        .
      </p>
    </div>
  );
}
