import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { collection } from "@/data/collection";
import { sampleMints } from "@/data/gallery";
import { combinationCount, traitCategories } from "@/data/traits";
import { potbPath } from "@/lib/potb";

export default function HomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <Image
          src="/brand/banner-pugs-on-the-block.png"
          alt="Three pugs peeking over a brownstone block"
          fill
          priority
          className="object-cover object-[center_35%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#2a1a12] via-[#2a1a12]/55 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {collection.supply.toLocaleString()} PFPs · {collection.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {collection.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{collection.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href={potbPath("/gallery")}>
                See sample mints
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={potbPath("/launch")}>Launch on OpenSea</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">The drop</p>
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">Peeking over every stoop on the chain.</h2>
            <p className="mt-4 text-muted-foreground">{collection.description}</p>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Supply", collection.supply.toLocaleString()],
                ["Possible combos", combinationCount().toLocaleString()],
                ["Mint", `${collection.mintPriceEth} ETH`],
                ["Chain ID", String(collection.chain.chainId)],
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
              <Link key={mint.id} href={potbPath("/gallery")} className="group overflow-hidden rounded-2xl border bg-card">
                <Image
                  src={mint.image}
                  alt={mint.name}
                  width={1024}
                  height={1024}
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
            <Card key={category.id} className="border-none bg-transparent shadow-none">
              <CardContent className="px-0">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{category.label}</p>
                <h3 className="mt-1 font-heading text-2xl">
                  {category.traits.length}
                  {category.noneLabel ? "+" : ""} looks
                </h3>
                <p className="mt-2 text-sm text-muted-foreground">{category.blurb}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="overflow-hidden rounded-[2rem] border bg-[#2f5d50] text-[#f4eadc]">
          <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-[#d9c7a2]">Marketplace</p>
              <h2 className="mt-2 font-heading text-4xl">Robinhood Chain is already live on OpenSea.</h2>
              <p className="mt-4 text-[#f4eadc]/80">
                List the collection where Stock Tokens, memecoins, and NFTs already trade — no extra
                marketplace app. This repo ships the trait art, OpenSea metadata shape, and an ERC-721
                ready for chain ID {collection.chain.chainId}.
              </p>
            </div>
            <div className="flex flex-col justify-end gap-3">
              <Button asChild size="lg" variant="secondary">
                <Link href={potbPath("/launch")}>Read the launch checklist</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#f4eadc]/30 bg-transparent text-[#f4eadc]">
                <Link href={potbPath("/traits")}>Browse every trait sheet</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
