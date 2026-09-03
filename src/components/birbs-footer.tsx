import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { birbs } from "@/data/birbs";
import { birbsPath } from "@/lib/birbs";

export function BirbsFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{birbs.name}</p>
          <p className="text-sm text-muted-foreground">
            {birbs.supply.toLocaleString()} round robin PFPs · {birbs.chain.name} ·{" "}
            <OpenSeaLink href={birbs.opensea.collection} className="hover:underline">
              OpenSea
            </OpenSeaLink>
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href={birbsPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={birbsPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={birbsPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={birbsPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          <OpenSeaLink href={birbs.opensea.collection} className="hover:underline" />
          <a href={birbs.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
