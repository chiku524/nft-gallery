import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { umbra } from "@/data/umbra";
import { umbraPath } from "@/lib/umbra";
import { openSeaListings } from "@/lib/opensea";

export function UmbraFooter() {
  return (
    <footer className="mt-auto border-t border-[#e8a04a]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f3e6c8)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{umbra.name}</p>
          <p className="text-sm text-muted-foreground">
            {umbra.supply.toLocaleString()} shadow-puppet PFPs · free mint · {umbra.chain.name} ·{" "}
            {openSeaListings(umbra.opensea).map((listing, index) => (
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
          <Link href={umbraPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={umbraPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={umbraPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={umbraPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(umbra.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={umbra.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
