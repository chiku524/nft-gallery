import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { feltro } from "@/data/feltro";
import { feltroPath } from "@/lib/feltro";
import { openSeaListings } from "@/lib/opensea";

export function FeltroFooter() {
  return (
    <footer className="mt-auto border-t border-[#ec5c30]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f4d8c4)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{feltro.name}</p>
          <p className="text-sm text-muted-foreground">
            {feltro.supply.toLocaleString()} foam-mascot PFPs · free mint · {feltro.chain.name} ·{" "}
            {openSeaListings(feltro.opensea).map((listing, index) => (
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
          <Link href={feltroPath("/studio")} className="hover:underline">Studio</Link>
          <Link href={feltroPath("/traits")} className="hover:underline">Traits</Link>
          <Link href={feltroPath("/gallery")} className="hover:underline">Gallery</Link>
          <Link href={feltroPath("/launch")} className="hover:underline">Launch notes</Link>
          {openSeaListings(feltro.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={feltro.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
