import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { risotaSamples } from "@/data/risota-gallery";
import { risotaCombinationCount, risotaTraitCategories } from "@/data/risota-traits";
import { risota } from "@/data/risota";
import { risotaPath } from "@/lib/risota";
import { openSeaListings } from "@/lib/opensea";

export default function RisotaHomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <ApngImage
          src="/brand/banner-risota.png"
          alt="Five Risota risograph dancers lined up as portraits"
          className="absolute inset-0 size-full object-cover object-[center_40%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#2a1820] via-[#2a1820]/45 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {risota.supply.toLocaleString()} PFP GIFs · {risota.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {risota.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{risota.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg" className="bg-[#ff48b0] text-[#2a1820] hover:bg-[#ff48b0]/90">
              <Link href={risotaPath("/studio")}>
                Open the plate studio
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={risotaPath("/gallery")}>See sample loops</Link>
            </Button>
            {openSeaListings(risota.opensea).map((listing) => (
              <Button
                key={listing.href}
                asChild
                size="lg"
                variant="outline"
                className="border-white/30 bg-transparent text-white hover:bg-white/10"
              >
                <a href={listing.href} target="_blank" rel="noreferrer">
                  OpenSea · {listing.label}
                </a>
              </Button>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">The drop</p>
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">Eight dancers. Spot ink.</h2>
            <div className="mt-4 space-y-4 text-muted-foreground">
              {risota.story.split("\n\n").map((paragraph) => (
                <p key={paragraph.slice(0, 40)}>{paragraph}</p>
              ))}
            </div>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Supply", risota.supply.toLocaleString()],
                ["Possible combos", risotaCombinationCount().toLocaleString()],
                ["Loop", `${risota.frames} × ${risota.frameDurationMs}ms`],
                ["Mint", `${risota.mintPriceEth} ${risota.chain.currency}`],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border bg-card p-4">
                  <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-heading text-2xl">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:col-span-7 sm:grid-cols-4">
            {risotaSamples.slice(0, 8).map((mint) => (
              <Link
                key={mint.id}
                href={risotaPath("/gallery")}
                className="group overflow-hidden rounded-2xl border bg-card"
              >
                <ApngImage
                  src={mint.image}
                  alt={mint.name}
                  width={512}
                  height={512}
                  className="aspect-square w-full object-cover transition duration-300 group-hover:scale-[1.04]"
                />
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-border bg-card/60">
        <div className="mx-auto grid w-full max-w-6xl gap-6 px-4 py-14 sm:px-6 sm:grid-cols-2 lg:grid-cols-4">
          {risotaTraitCategories.map((category) => (
            <Card key={category.id} className="border-none bg-transparent shadow-none ring-0">
              <CardContent className="px-0">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{category.label}</p>
                <h3 className="mt-1 font-heading text-2xl">
                  {category.traits.length}
                  {category.noneLabel ? "+" : ""} loops
                </h3>
                <p className="mt-2 text-sm text-muted-foreground">{category.blurb}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="overflow-hidden rounded-[2rem] border bg-[#2a1820] text-[#f4ead4]">
          <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-[#ff48b0]">How the stack works</p>
              <h2 className="mt-2 font-heading text-4xl">Studio plays plates. The drop flattens them.</h2>
              <p className="mt-4 text-[#f4ead4]/75">
                Each trait is its own looping APNG. The studio stacks those files so stock, screen,
                figure, pass, knockout, slug, and mark keep the same seated clock. The dancer stays
                locked. Pass plates slide. Minted tokens composite the same 12 frames into one GIF
                OpenSea can list on Robinhood Chain.
              </p>
            </div>
            <div className="flex flex-col justify-end gap-3">
              <Button asChild size="lg" variant="secondary">
                <Link href={risotaPath("/traits")}>Browse every Risota plate</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#ff48b0]/30 bg-transparent text-[#f4ead4]">
                <Link href={risotaPath("/launch")}>Launch checklist</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
