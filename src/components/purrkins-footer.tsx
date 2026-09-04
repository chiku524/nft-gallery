import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { purrkins } from "@/data/purrkins";
import { purrkinsPath } from "@/lib/purrkins";
import { openSeaListings } from "@/lib/opensea";

export function PurrkinsFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{purrkins.name}</p>
          <p className="text-sm text-muted-foreground">
            {purrkins.supply.toLocaleString()} chibi cat PFPs · {purrkins.chain.name} ·{" "}
            {openSeaListings(purrkins.opensea).map((listing, index) => (
              <span key={listing.href}>
                {index > 0 ? " · " : null}
                <OpenSeaLink href={listing.href} className="hover:underline">
                  OpenSea · {listing.label}
                </OpenSeaLink>
              </span>
            ))}
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href={purrkinsPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={purrkinsPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={purrkinsPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={purrkinsPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(purrkins.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={purrkins.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
