import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { partyPandas } from "@/data/party-pandas";
import { partyPandasPath } from "@/lib/party-pandas";

export function PartyPandasFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{partyPandas.name}</p>
          <p className="text-sm text-muted-foreground">
            {partyPandas.supply.toLocaleString()} party panda PFPs · {partyPandas.chain.name} ·{" "}
            <OpenSeaLink href={partyPandas.opensea.collection} className="hover:underline">
              OpenSea
            </OpenSeaLink>
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href={partyPandasPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={partyPandasPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={partyPandasPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={partyPandasPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          <OpenSeaLink href={partyPandas.opensea.collection} className="hover:underline" />
          <a href={partyPandas.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
