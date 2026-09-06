import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { kamiori } from "@/data/kamiori";
import { kamioriPath } from "@/lib/kamiori";
import { openSeaListings } from "@/lib/opensea";

export function KamioriFooter() {
  return (
    <footer className="mt-auto border-t border-[#c4452d]/15 bg-[color-mix(in_oklch,var(--secondary)_40%,#f6f0e4)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{kamiori.name}</p>
          <p className="text-sm text-muted-foreground">
            {kamiori.supply.toLocaleString()} origami PFPs · free mint · {kamiori.chain.name} ·{" "}
            {openSeaListings(kamiori.opensea).map((listing, index) => (
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
          <Link href={kamioriPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={kamioriPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={kamioriPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={kamioriPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          {openSeaListings(kamiori.opensea).map((listing) => (
            <OpenSeaLink key={listing.href} href={listing.href} className="hover:underline">
              OpenSea · {listing.label}
            </OpenSeaLink>
          ))}
          <a href={kamiori.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
