import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { noxelle } from "@/data/noxelle";
import { noxellePath } from "@/lib/noxelle";
import { openSeaListings } from "@/lib/opensea";

export function NoxelleFooter() {
  return (
    <footer className="mt-auto border-t border-[#e14bff]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#1a0e28)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{noxelle.name}</p>
          <p className="text-sm text-muted-foreground">
            {noxelle.supply.toLocaleString()} neon-tube PFPs · ${noxelle.mintPriceUsd} · {noxelle.chain.name} ·{" "}
            {openSeaListings(noxelle.opensea).map((listing, index) => (
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
          <Link href={noxellePath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={noxellePath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={noxellePath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={noxellePath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(noxelle.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={noxelle.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
