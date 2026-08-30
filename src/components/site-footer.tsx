import Link from "next/link";
import { collection } from "@/data/collection";
import { loopkinsPath } from "@/lib/loopkins";

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{collection.name}</p>
          <p className="text-sm text-muted-foreground">
            {collection.supply.toLocaleString()} loops · {collection.chain.name} · OpenSea
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href="/studio" className="hover:underline">
            Studio
          </Link>
          <Link href={loopkinsPath("/traits")} className="hover:underline">
            Trait loops
          </Link>
          <Link href={loopkinsPath("/gallery")} className="hover:underline">
            Sample mints
          </Link>
          <Link href={loopkinsPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          <a href={collection.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
