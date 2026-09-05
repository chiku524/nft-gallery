import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { opalineSamples } from "@/data/opaline-gallery";
import { opalineCombinationCount, opalineTraitCategories } from "@/data/opaline-traits";
import { opaline } from "@/data/opaline";
import { opalinePath } from "@/lib/opaline";
import { openSeaListings } from "@/lib/opensea";

export default function OpalineHomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <ApngImage
          src="/brand/banner-opaline.png"
          alt="Five Opaline glass busts lined up as portraits"
          className="absolute inset-0 size-full object-cover object-[center_40%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#0c0d12] via-[#0c0d12]/50 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {opaline.supply.toLocaleString()} PFP GIFs · {opaline.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {opaline.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{opaline.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg" className="bg-[#c6c2b8] text-[#121318] hover:bg-[#c6c2b8]/90">
              <Link href={opalinePath("/studio")}>
                Open the layer studio
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={opalinePath("/gallery")}>See sample loops</Link>
            </Button>
            {openSeaListings(opaline.opensea).map((listing) => (
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
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">Faceted glass. Seated light.</h2>
            <div className="mt-4 space-y-4 text-muted-foreground">
              {opaline.story.split("\n\n").map((paragraph) => (
                <p key={paragraph.slice(0, 40)}>{paragraph}</p>
              ))}
            </div>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Supply", opaline.supply.toLocaleString()],
                ["Possible combos", opalineCombinationCount().toLocaleString()],
                ["Loop", `${opaline.frames} × ${opaline.frameDurationMs}ms`],
                ["Mint", `${opaline.mintPriceEth} ${opaline.chain.currency}`],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border bg-card p-4">
                  <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-heading text-2xl">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:col-span-7 sm:grid-cols-4">
            {opalineSamples.slice(0, 8).map((mint) => (
              <Link
                key={mint.id}
                href={opalinePath("/gallery")}
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
        <div className="mx-auto grid w-full max-w-6xl gap-6 px-4 py-14 sm:px-6 sm:grid-cols-2 lg:grid-cols-3">
          {opalineTraitCategories.map((category) => (
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
        <div className="overflow-hidden rounded-[2rem] border bg-[#0c0d12] text-[#e8e4dc]">
          <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-[#c6c2b8]">How the stack works</p>
              <h2 className="mt-2 font-heading text-4xl">Studio plays layers. The drop flattens them.</h2>
              <p className="mt-4 text-[#e8e4dc]/75">
                Each trait is its own looping APNG. The studio stacks those files so ateliers, casts,
                sheens, regards, crests, and clasps keep the same seated clock. The bust stays locked.
                Minted tokens composite the same 12 frames into one GIF OpenSea can list on Base.
              </p>
            </div>
            <div className="flex flex-col justify-end gap-3">
              <Button asChild size="lg" variant="secondary">
                <Link href={opalinePath("/traits")}>Browse every Opaline layer</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#c6c2b8]/25 bg-transparent text-[#e8e4dc]">
                <Link href={opalinePath("/launch")}>Launch checklist</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
