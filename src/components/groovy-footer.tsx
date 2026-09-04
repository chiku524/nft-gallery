import Link from "next/link";
import { OpenSeaLink } from "@/components/opensea-link";
import { groovy } from "@/data/groovy";
import { groovyPath } from "@/lib/groovy";

export function GroovyFooter() {
  return (
    <footer className="mt-auto border-t border-[#f25aa0]/20 bg-[color-mix(in_oklch,var(--secondary)_40%,#1a0610)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{groovy.name}</p>
          <p className="text-sm text-muted-foreground">
            {groovy.supply.toLocaleString()} musical note PFPs · {groovy.chain.name} ·{" "}
            <OpenSeaLink href={groovy.opensea.collection} className="hover:underline">
              OpenSea
            </OpenSeaLink>
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          <Link href="/" className="hover:underline">
            NFT Gallery
          </Link>
          <Link href={groovyPath("/studio")} className="hover:underline">
            Studio
          </Link>
          <Link href={groovyPath("/traits")} className="hover:underline">
            Traits
          </Link>
          <Link href={groovyPath("/gallery")} className="hover:underline">
            Gallery
          </Link>
          <Link href={groovyPath("/launch")} className="hover:underline">
            Launch notes
          </Link>
          <OpenSeaLink href={groovy.opensea.collection} className="hover:underline" />
          <a href={groovy.chain.docs} className="hover:underline" target="_blank" rel="noreferrer">
            Chain docs
          </a>
        </div>
      </div>
    </footer>
  );
}
