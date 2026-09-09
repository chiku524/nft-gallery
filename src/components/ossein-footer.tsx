import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { ossein } from "@/data/ossein";
import { osseinPath } from "@/lib/ossein";
import { openSeaListings } from "@/lib/opensea";

export function OsseinFooter() {
  return (
    <footer className="mt-auto border-t border-[#5c769c]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#efe6d2)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{ossein.name}</p>
          <p className="text-sm text-muted-foreground">
            {ossein.supply.toLocaleString()} anatomical-chart PFPs · free mint · {ossein.chain.name} ·{" "}
            {openSeaListings(ossein.opensea).map((listing, index) => (
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
          <Link href={osseinPath("/studio")} className="hover:underline">Studio</Link>
          <Link href={osseinPath("/traits")} className="hover:underline">Traits</Link>
          <Link href={osseinPath("/gallery")} className="hover:underline">Gallery</Link>
          <Link href={osseinPath("/launch")} className="hover:underline">Launch notes</Link>
          {openSeaListings(ossein.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={ossein.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
