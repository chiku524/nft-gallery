import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { hoodkinSamples } from "@/data/hoodkin-gallery";
import { hoodkinCombinationCount, hoodkinTraitCategories } from "@/data/hoodkin-traits";
import { hoodkins } from "@/data/hoodkins";
import { hoodkinsPath } from "@/lib/hoodkins";

export default function HoodkinsHomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <ApngImage
          src="/brand/banner-hoodkins.png"
          alt="Five Hoodkins lined up on ledger and night desks"
          className="absolute inset-0 size-full object-cover object-[center_40%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#081610] via-[#081610]/55 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {hoodkins.supply.toLocaleString()} PFP GIFs · {hoodkins.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {hoodkins.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{hoodkins.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href={hoodkinsPath("/studio")}>
                Open the layer studio
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={hoodkinsPath("/gallery")}>See sample loops</Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/30 bg-transparent text-white hover:bg-white/10">
              <a href={hoodkins.opensea.collection} target="_blank" rel="noreferrer">
                View on OpenSea
              </a>
            </Button>
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">The drop</p>
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">Chibi raccoons, looping like Loopkins.</h2>
            <div className="mt-4 space-y-4 text-muted-foreground">
              {hoodkins.story.split("\n\n").map((paragraph) => (
                <p key={paragraph.slice(0, 40)}>{paragraph}</p>
              ))}
            </div>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Supply", hoodkins.supply.toLocaleString()],
                ["Possible combos", hoodkinCombinationCount().toLocaleString()],
                ["Loop", `${hoodkins.frames} × ${hoodkins.frameDurationMs}ms`],
                ["Mint", `${hoodkins.mintPriceEth} ${hoodkins.chain.currency}`],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border bg-card p-4">
                  <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-heading text-2xl">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:col-span-7 sm:grid-cols-4">
            {hoodkinSamples.slice(0, 8).map((mint) => (
              <Link
                key={mint.id}
                href={hoodkinsPath("/gallery")}
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
        <div className="mx-auto grid w-full max-w-6xl gap-6 px-4 py-14 sm:px-6 md:grid-cols-3">
          {hoodkinTraitCategories.map((category) => (
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
        <div className="overflow-hidden rounded-[2rem] border bg-[#081610] text-[#f4f1ff]">
          <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-[#49f2c2]">How the stack works</p>
              <h2 className="mt-2 font-heading text-4xl">Studio plays layers. The drop flattens them.</h2>
              <p className="mt-4 text-[#f4f1ff]/75">
                Each trait is its own looping APNG. The studio stacks those files so pads, pelts, and
                gear keep moving. Minted tokens composite the same 12 frames into one GIF OpenSea can
                list on Robinhood Chain.
              </p>
            </div>
            <div className="flex flex-col justify-end gap-3">
              <Button asChild size="lg" variant="secondary">
                <Link href={hoodkinsPath("/traits")}>Browse every raccoon layer</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#f4f1ff]/25 bg-transparent text-[#f4f1ff]">
                <Link href={hoodkinsPath("/launch")}>Launch checklist</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
