import Link from "next/link";
import { collection } from "@/data/collection";
import { potbPath } from "@/lib/potb";

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{collection.name}</p>
          <p className="text-sm text-muted-foreground">
            {collection.supply.toLocaleString()} pugs · {collection.chain.name} · OpenSea
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href={potbPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={potbPath("/traits")} className="hover:underline">
            Trait sheets
          </Link>
          <Link href={potbPath("/gallery")} className="hover:underline">
            Sample mints
          </Link>
          <Link href={potbPath("/launch")} className="hover:underline">
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
