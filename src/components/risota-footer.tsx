import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { risota } from "@/data/risota";
import { risotaPath } from "@/lib/risota";
import { openSeaListings } from "@/lib/opensea";

export function RisotaFooter() {
  return (
    <footer className="mt-auto border-t border-[#ff48b0]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f4ead4)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{risota.name}</p>
          <p className="text-sm text-muted-foreground">
            {risota.supply.toLocaleString()} risograph PFPs · {risota.chain.name} ·{" "}
            {openSeaListings(risota.opensea).map((listing, index) => (
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
          <Link href={risotaPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={risotaPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={risotaPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={risotaPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(risota.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={risota.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
