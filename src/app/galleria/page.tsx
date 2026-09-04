import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { galleria, galleriaWorks } from "@/data/galleria";
import { galleriaPath } from "@/lib/galleria";

export default function GalleriaHomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <ApngImage
          src="/brand/banner-galleria.png"
          alt="Five Galleria On Ink paintings across a dark salon wall"
          className="absolute inset-0 size-full object-cover object-[center_40%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#0c0c0e] via-[#0c0c0e]/55 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {galleria.supply} open editions · {galleria.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {galleria.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{galleria.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href={galleriaPath("/gallery")}>
                Enter the salon
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <a href={galleria.opensea.collection} target="_blank" rel="noreferrer">
                View on OpenSea
              </a>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/30 bg-transparent text-white hover:bg-white/10">
              <Link href={galleriaPath("/launch")}>Open edition notes</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">The salon</p>
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">
              {galleria.supply} finished paintings. No house style.
            </h2>
            <p className="mt-4 text-muted-foreground">{galleria.description}</p>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Works", String(galleria.supply)],
                ["Edition", galleria.edition],
                ["Price", `${galleria.mintPriceEth} ETH`],
                ["Loop", `${galleria.frames} × ${galleria.frameDurationMs}ms`],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border bg-card p-4">
                  <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-heading text-2xl">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:col-span-7 sm:grid-cols-3">
            {galleriaWorks.slice(0, 9).map((work) => (
              <Link
                key={work.id}
                href={galleriaPath(`/${work.id}`)}
                className="group overflow-hidden rounded-2xl border bg-card"
              >
                <ApngImage
                  src={work.image}
                  alt={work.title}
                  width={512}
                  height={512}
                  className="aspect-square w-full object-cover transition duration-300 group-hover:scale-[1.04]"
                />
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
