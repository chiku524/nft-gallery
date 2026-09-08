import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { cera } from "@/data/cera";
import { ceraPath } from "@/lib/cera";
import { openSeaListings } from "@/lib/opensea";

export function CeraFooter() {
  return (
    <footer className="mt-auto border-t border-[#d946a6]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#16121c)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{cera.name}</p>
          <p className="text-sm text-muted-foreground">
            {cera.supply.toLocaleString()} lava lamp PFPs · ${cera.mintPriceUsd} · {cera.chain.name} ·{" "}
            {openSeaListings(cera.opensea).map((listing, index) => (
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
          <Link href={ceraPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={ceraPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={ceraPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={ceraPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(cera.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={cera.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
