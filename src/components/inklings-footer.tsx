import Link from "next/link";
import { inklings } from "@/data/inklings";
import { inklingsPath } from "@/lib/inklings";

export function InklingsFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{inklings.name}</p>
          <p className="text-sm text-muted-foreground">
            {inklings.supply.toLocaleString()} ink-wash PFPs · {inklings.chain.name} · OpenSea
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href={inklingsPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={inklingsPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={inklingsPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={inklingsPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          <a href={inklings.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
