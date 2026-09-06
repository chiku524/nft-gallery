import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { umbraSamples } from "@/data/umbra-gallery";
import { umbraCombinationCount, umbraTraitCategories } from "@/data/umbra-traits";
import { umbra } from "@/data/umbra";
import { umbraPath } from "@/lib/umbra";
import { openSeaListings } from "@/lib/opensea";

export default function UmbraHomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <ApngImage
          src="/brand/banner-umbra.png"
          alt="Five Umbra shadow puppets lined up"
          className="absolute inset-0 size-full object-cover object-[center_40%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#1a1208] via-[#1a1208]/45 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {umbra.supply.toLocaleString()} PFP GIFs · free mint · {umbra.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {umbra.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{umbra.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg" className="bg-[#e8a04a] text-[#1a1208] hover:bg-[#e8a04a]/90">
              <Link href={umbraPath("/studio")}>
                Open the lamp studio
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={umbraPath("/gallery")}>See sample loops</Link>
            </Button>
            {openSeaListings(umbra.opensea).map((listing) => (
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
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">Eight casts. One lamp.</h2>
            <div className="mt-4 space-y-4 text-muted-foreground">
              {umbra.story.split("\n\n").map((paragraph) => (
                <p key={paragraph.slice(0, 40)}>{paragraph}</p>
              ))}
            </div>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Supply", umbra.supply.toLocaleString()],
                ["Possible combos", umbraCombinationCount().toLocaleString()],
                ["Loop", `${umbra.frames} × ${umbra.frameDurationMs}ms`],
                ["Mint", "Free"],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border bg-card p-4">
                  <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-heading text-2xl">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:col-span-7 sm:grid-cols-4">
            {umbraSamples.slice(0, 8).map((mint) => (
              <Link
                key={mint.id}
                href={umbraPath("/gallery")}
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
          {umbraTraitCategories.map((category) => (
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
        <div className="overflow-hidden rounded-[2rem] border bg-[#1a1208] text-[#f3e6c8]">
          <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-[#e8a04a]">How the stack works</p>
              <h2 className="mt-2 font-heading text-4xl">Studio stacks the lamp. The drop flattens it.</h2>
              <p className="mt-4 text-[#f3e6c8]/75">
                Each trait is its own looping APNG. The studio stacks those files so cloth, ember,
                cast, hinge, cutwork, leaf, and soot keep the same seated clock. The hide stays
                locked. Hinges swing the dance. Minted tokens composite the same 12 frames into one
                GIF OpenSea can list on Robinhood Chain.
              </p>
            </div>
            <div className="flex flex-col justify-end gap-3">
              <Button asChild size="lg" variant="secondary">
                <Link href={umbraPath("/traits")}>Browse every Umbra plate</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#e8a04a]/40 bg-transparent text-[#f3e6c8]">
                <Link href={umbraPath("/launch")}>Launch checklist</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
