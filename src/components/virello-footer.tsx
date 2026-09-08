import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { virello } from "@/data/virello";
import { virelloPath } from "@/lib/virello";
import { openSeaListings } from "@/lib/opensea";

export function VirelloFooter() {
  return (
    <footer className="mt-auto border-t border-[#c43c2c]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f3ead4)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{virello.name}</p>
          <p className="text-sm text-muted-foreground">
            {virello.supply.toLocaleString()} wind-up tin PFPs · ${virello.mintPriceUsd} · {virello.chain.name} ·{" "}
            {openSeaListings(virello.opensea).map((listing, index) => (
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
          <Link href={virelloPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={virelloPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={virelloPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={virelloPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(virello.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={virello.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
