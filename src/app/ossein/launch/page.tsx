import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { ApngImage } from "@/components/apng-image";
import { Button } from "@/components/ui/button";
import { ossein } from "@/data/ossein";
import { openSeaListings } from "@/lib/opensea";

export const metadata: Metadata = {
  title: "OpenSea launch",
  description: "Upload flattened Ossein GIFs to a free OpenSea Drop on Robinhood Chain.",
};

const steps = [
  {
    title: "Traits stay layered. The drop is flattened.",
    body: "OpenSea does not stack APNG layers for you. Studio is a live compositor. For a Drop you upload finished GIFs plus a CSV. Bake the full 10,000-token pack with python scripts/generate_ossein.py --all — gifs/, OSSN-opensea-drop.csv, and the kit README land in generated/ossein/.",
  },
  {
    title: "Create a Drop on Robinhood Chain",
    body: `In OpenSea Studio, create a Drop on ${ossein.chain.name} (chain ID ${ossein.chain.chainId}). Set supply to ${ossein.supply.toLocaleString()}, set mint to free, paste the project description, and upload the listing kit from public/brand.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: `Upload every file in generated/ossein/gifs (1.gif–${ossein.supply}.gif) and generated/ossein/OSSN-opensea-drop.csv. The CSV already uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). OpenSea plays GIF, not APNG. Preview the loops, then publish.`,
  },
  {
    title: "Or deploy the ERC-721 yourself",
    body: `contracts/Ossein.sol mints token IDs 1–${ossein.supply.toLocaleString()} at 0 ETH. Pin generated/ossein/json and set the base URI. Import that contract on OpenSea instead of using a Drop if you want a custom mint. Gas is ETH.`,
  },
];

export default function OsseinLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch on OpenSea, Robinhood Chain.</h1>
      <p className="mt-4 text-muted-foreground">
        Ossein ships as layered APNG traits and as flattened GIF tokens. OpenSea wants
        the GIF bake of those loops. The mint is free. The APNG stack stays in this repo for the
        studio and any later restack.
      </p>
      <div className="mt-6 flex flex-wrap gap-3">
        {openSeaListings(ossein.opensea).map((listing) => (
          <Button key={listing.href} asChild className="bg-[#5c769c] text-[#1c1814] hover:bg-[#5c769c]/90">
            <a href={listing.href} target="_blank" rel="noreferrer">
              OpenSea · {listing.label}
            </a>
          </Button>
        ))}
      </div>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", ossein.chain.name],
          ["Chain ID", String(ossein.chain.chainId)],
          ["Currency", ossein.chain.currency],
          ["Supply", ossein.supply.toLocaleString()],
          ["Mint", "Free"],
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
          Collection name {ossein.name}. Symbol {ossein.symbol}. Category PFPs. The same copy lives in{" "}
          <code className="rounded bg-secondary px-1.5 py-0.5 text-xs">public/metadata/ossein-description.txt</code>.
        </p>
        <pre className="mt-5 overflow-x-auto whitespace-pre-wrap rounded-2xl bg-background p-4 text-sm leading-relaxed text-foreground">
          {ossein.story}
        </pre>
      </div>

      <div className="mt-8 rounded-[1.75rem] border bg-card p-6 sm:p-8">
        <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Listing kit</p>
        <h2 className="mt-2 font-heading text-2xl">Logo, featured, banner, collection GIF.</h2>
        <ul className="mt-6 grid gap-4 sm:grid-cols-2">
          {[
            ["Logo", "public/brand/logo-ossein.png", "512×512, 1:1", "/brand/logo-ossein.png"],
            ["Featured", "public/brand/featured-ossein.jpg", "1200×800, 3:2", "/brand/featured-ossein.jpg"],
            ["OpenSea banner", "public/brand/banner-ossein-opensea.jpg", "2800×700, 4:1", "/brand/banner-ossein-opensea.jpg"],
            ["Collection GIF", "public/brand/collection-ossein.gif", "1000×1000 loop", "/brand/collection-ossein.gif"],
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
          RPC {ossein.chain.rpcUrl}
          <br />
          Explorer {ossein.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton chain={ossein.chain} />
        </div>
      </div>

      <ol className="mt-10 space-y-6">
        {steps.map((step, index) => (
          <li key={step.title} className="grid grid-cols-[auto_1fr] gap-4">
            <span className="flex size-8 items-center justify-center rounded-full bg-[#5c769c] text-sm text-[#1c1814]">
              {index + 1}
            </span>
            <div>
              <h2 className="font-heading text-2xl">{step.title}</h2>
              <p className="mt-1 text-muted-foreground">{step.body}</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}
