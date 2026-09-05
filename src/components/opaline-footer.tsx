import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { opaline } from "@/data/opaline";
import { opalinePath } from "@/lib/opaline";
import { openSeaListings } from "@/lib/opensea";

export function OpalineFooter() {
  return (
    <footer className="mt-auto border-t border-white/10 bg-[color-mix(in_oklch,var(--secondary)_40%,#0c0d12)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{opaline.name}</p>
          <p className="text-sm text-muted-foreground">
            {opaline.supply.toLocaleString()} smoked-glass PFPs · {opaline.chain.name} ·{" "}
            {openSeaListings(opaline.opensea).map((listing, index) => (
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
          <Link href={opalinePath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={opalinePath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={opalinePath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={opalinePath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(opaline.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={opaline.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
