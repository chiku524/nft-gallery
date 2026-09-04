import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { strangers } from "@/data/strangers";
import { strangersPath } from "@/lib/strangers";

export function StrangersFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{strangers.name}</p>
          <p className="text-sm text-muted-foreground">
            {strangers.supply} open editions · {strangers.chain.name} ·{" "}
            <OpenSeaLink href={strangers.opensea.collection} className="hover:underline">
              OpenSea
            </OpenSeaLink>
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href={strangersPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={strangersPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          <OpenSeaLink href={strangers.opensea.collection} className="hover:underline" />
          <a href={strangers.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
