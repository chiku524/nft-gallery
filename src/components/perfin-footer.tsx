import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { perfin } from "@/data/perfin";
import { perfinPath } from "@/lib/perfin";
import { openSeaListings } from "@/lib/opensea";

export function PerfinFooter() {
  return (
    <footer className="mt-auto border-t border-[#9b2d36]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f3ede0)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{perfin.name}</p>
          <p className="text-sm text-muted-foreground">
            {perfin.supply.toLocaleString()} engraved stamp PFPs · free mint · {perfin.chain.name} ·{" "}
            {openSeaListings(perfin.opensea).map((listing, index) => (
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
          <Link href={perfinPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={perfinPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={perfinPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={perfinPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(perfin.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={perfin.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
