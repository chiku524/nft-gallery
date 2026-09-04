import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { Button } from "@/components/ui/button";
import { afterimages } from "@/data/afterimages";

export const metadata: Metadata = {
  title: "OpenSea launch",
  description: `Upload ${afterimages.supply.toLocaleString()} Afterimages GIFs to an OpenSea Drop on ${afterimages.chain.name}.`,
};

const steps = [
  {
    title: "These files are already finished.",
    body: "Afterimages is not a trait stack. Tokens 1–50 are signature APNGs on the site. OpenSea does not play APNG, so the Drop pack is a GIF bake of every loop, 1 through 3,333.",
  },
  {
    title: `Create a Drop on ${afterimages.chain.name}`,
    body: `In OpenSea Studio, create a Drop on ${afterimages.chain.name} (chain ID ${afterimages.chain.chainId}). Set supply to ${afterimages.supply.toLocaleString()}, edition style to unique 1:1s. Paste the collection description from public/metadata/afterimages-description.txt. Upload logo-afterimages.png, featured-afterimages.jpg, banner-afterimages-opensea.jpg, and collection-afterimages.gif from public/brand.`,
  },
  {
    title: "Bulk-upload GIFs + CSV",
    body: `Upload every file in generated/afterimages/gifs (1.gif–${afterimages.supply}.gif) and generated/afterimages/opensea-metadata.csv. The CSV already uses OpenSea’s required headers (tokenID, name, description, file_name, attributes[Trait]). GIF is the media OpenSea will play. Preview the loops, then publish.`,
  },
  {
    title: "Or deploy the ERC-721 yourself",
    body: `contracts/Afterimages.sol mints token IDs 1–${afterimages.supply.toLocaleString()} on ${afterimages.chain.name}. Pin generated/afterimages/json and set the base URI. Import that contract on OpenSea instead of using a Drop if you want a custom mint.`,
  },
];

export default function AfterimagesLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Marketplace</p>
      <h1 className="mt-2 font-heading text-4xl">Launch on OpenSea, {afterimages.chain.name}.</h1>
      <p className="mt-4 text-muted-foreground">
        Afterimages ships as {afterimages.supply.toLocaleString()} unique looping paintings. The site shows
        the signature fifty as APNG; the Drop pack is a GIF bake of the full {afterimages.supply.toLocaleString()}.
      </p>
      <div className="mt-6">
        <Button asChild>
          <a href={afterimages.opensea.collection} target="_blank" rel="noreferrer">
            OpenSea
          </a>
        </Button>
      </div>

      <dl className="mt-8 grid gap-3 sm:grid-cols-2">
        {[
          ["Network", afterimages.chain.name],
          ["Chain ID", String(afterimages.chain.chainId)],
          ["Currency", afterimages.chain.currency],
          ["Supply", `${afterimages.supply.toLocaleString()} × ${afterimages.edition}`],
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
          RPC {afterimages.chain.rpcUrl}
          <br />
          Explorer {afterimages.chain.explorer}
        </p>
        <div className="mt-4">
          <AddChainButton chain={afterimages.chain} />
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
        <a className="underline" href={afterimages.opensea.metadataGuide} target="_blank" rel="noreferrer">
          Preparing metadata for your drop
        </a>
        . Live collection:{" "}
        <a className="underline" href={afterimages.opensea.collection} target="_blank" rel="noreferrer">
          opensea.io/collection/afterimages-on-ink
        </a>
        . Ink network docs:{" "}
        <a className="underline" href={afterimages.chain.docs} target="_blank" rel="noreferrer">
          docs.inkonchain.com
        </a>
        .
      </p>
    </div>
  );
}
