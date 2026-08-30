import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { collection } from "@/data/collection";
import { sampleMints } from "@/data/gallery";
import { combinationCount, traitCategories } from "@/data/traits";
import { loopkinsPath } from "@/lib/loopkins";

export default function LoopkinsHomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <ApngImage
          src="/brand/banner-loopkins.png"
          alt="Three Loopkins against drifting night skies"
          className="absolute inset-0 size-full object-cover object-[center_40%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#070816] via-[#070816]/55 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {collection.supply.toLocaleString()} APNG PFPs · {collection.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {collection.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{collection.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href="/studio">
                Open the layer studio
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={loopkinsPath("/gallery")}>See sample loops</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">The drop</p>
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">Six APNG layers. One shared clock.</h2>
            <p className="mt-4 text-muted-foreground">{collection.description}</p>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Supply", collection.supply.toLocaleString()],
                ["Possible combos", combinationCount().toLocaleString()],
                ["Mint", `${collection.mintPriceEth} ETH`],
                ["Loop", `${collection.frames} × ${collection.frameDurationMs}ms`],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border bg-card p-4">
                  <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-heading text-2xl">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:col-span-7 sm:grid-cols-4">
            {sampleMints.slice(0, 8).map((mint) => (
              <Link
                key={mint.id}
                href={loopkinsPath("/gallery")}
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
          {traitCategories.map((category) => (
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
        <div className="overflow-hidden rounded-[2rem] border bg-[#12162c] text-[#f4f1ff]">
          <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-[#49f2c2]">How the stack works</p>
              <h2 className="mt-2 font-heading text-4xl">Studio plays layers. The drop flattens them.</h2>
              <p className="mt-4 text-[#f4f1ff]/75">
                Each trait is its own APNG. The studio stacks those files so skies, faces, and charms
                keep looping. Minted tokens composite the same 12 frames into one APNG OpenSea can list.
              </p>
            </div>
            <div className="flex flex-col justify-end gap-3">
              <Button asChild size="lg" variant="secondary">
                <Link href={loopkinsPath("/traits")}>Browse every APNG layer</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#f4f1ff]/25 bg-transparent text-[#f4f1ff]">
                <Link href={loopkinsPath("/launch")}>Launch checklist</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
