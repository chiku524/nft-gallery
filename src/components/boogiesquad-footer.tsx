import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { boogiesquad } from "@/data/boogiesquad";
import { boogiesquadPath } from "@/lib/boogiesquad";
import { openSeaListings } from "@/lib/opensea";

export function BoogieSquadFooter() {
  return (
    <footer className="mt-auto border-t border-[#ff50b4]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#14081f)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{boogiesquad.name}</p>
          <p className="text-sm text-muted-foreground">
            {boogiesquad.supply.toLocaleString()} dance PFPs · {boogiesquad.chain.name} ·{" "}
            {openSeaListings(boogiesquad.opensea).map((listing, index) => (
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
          <Link href={boogiesquadPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={boogiesquadPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={boogiesquadPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={boogiesquadPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(boogiesquad.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={boogiesquad.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
