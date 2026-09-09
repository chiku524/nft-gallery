import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { vinylon } from "@/data/vinylon";
import { vinylonPath } from "@/lib/vinylon";
import { openSeaListings } from "@/lib/opensea";

export function VinylonFooter() {
  return (
    <footer className="mt-auto border-t border-[#ec4848]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f6d2c8)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{vinylon.name}</p>
          <p className="text-sm text-muted-foreground">
            {vinylon.supply.toLocaleString()} balloon-animal PFPs · free mint · {vinylon.chain.name} ·{" "}
            {openSeaListings(vinylon.opensea).map((listing, index) => (
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
          <Link href="/" className="hover:underline">NFT Gallery</Link>
          <Link href={vinylonPath("/studio")} className="hover:underline">Studio</Link>
          <Link href={vinylonPath("/traits")} className="hover:underline">Traits</Link>
          <Link href={vinylonPath("/gallery")} className="hover:underline">Gallery</Link>
          <Link href={vinylonPath("/launch")} className="hover:underline">Launch notes</Link>
          {openSeaListings(vinylon.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={vinylon.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
