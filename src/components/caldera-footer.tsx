import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { caldera } from "@/data/caldera";
import { calderaPath } from "@/lib/caldera";
import { openSeaListings } from "@/lib/opensea";

export function CalderaFooter() {
  return (
    <footer className="mt-auto border-t border-[#e85d04]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f4efe6)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{caldera.name}</p>
          <p className="text-sm text-muted-foreground">
            {caldera.supply.toLocaleString()} hotel matchbook PFPs · ${caldera.mintPriceUsd} · {caldera.chain.name} ·{" "}
            {openSeaListings(caldera.opensea).map((listing, index) => (
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
          <Link href={calderaPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={calderaPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={calderaPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={calderaPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(caldera.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={caldera.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
