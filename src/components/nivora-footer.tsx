import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { nivora } from "@/data/nivora";
import { nivoraPath } from "@/lib/nivora";
import { openSeaListings } from "@/lib/opensea";

export function NivoraFooter() {
  return (
    <footer className="mt-auto border-t border-[#c9a25a]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#1c1610)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{nivora.name}</p>
          <p className="text-sm text-muted-foreground">
            {nivora.supply.toLocaleString()} snow-globe PFPs · ${nivora.mintPriceUsd} · {nivora.chain.name} ·{" "}
            {openSeaListings(nivora.opensea).map((listing, index) => (
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
          <Link href={nivoraPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={nivoraPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={nivoraPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={nivoraPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(nivora.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={nivora.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
