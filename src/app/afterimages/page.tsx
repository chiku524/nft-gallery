import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { afterimageWorks, afterimages } from "@/data/afterimages";
import { afterimagesPath } from "@/lib/afterimages";

export default function AfterimagesHomePage() {
  return (
    <div>
      <section className="relative h-[420px] overflow-hidden border-b border-border sm:h-[520px]">
        <ApngImage
          src="/brand/banner-afterimages.png"
          alt="Three Afterimages paintings across a warm wall"
          className="absolute inset-0 size-full object-cover object-[center_40%]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#140e0a] via-[#140e0a]/55 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-6xl px-4 pb-10 sm:px-6">
          <Badge className="mb-3 bg-background/90 text-foreground">
            {afterimages.supply} one-of-ones · {afterimages.chain.name}
          </Badge>
          <h1 className="max-w-3xl font-heading text-4xl leading-[1.05] text-white sm:text-6xl">
            {afterimages.name}
          </h1>
          <p className="mt-3 max-w-xl text-base text-white/85 sm:text-lg">{afterimages.tagline}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href={afterimagesPath("/gallery")}>
                Enter the viewing room
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={afterimagesPath("/launch")}>OpenSea drop notes</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">The drop</p>
            <h2 className="mt-2 font-heading text-3xl sm:text-4xl">
              {afterimages.supply} finished APNGs. No trait stack.
            </h2>
            <p className="mt-4 text-muted-foreground">{afterimages.description}</p>
            <dl className="mt-8 grid grid-cols-2 gap-4">
              {[
                ["Supply", String(afterimages.supply)],
                ["Edition", afterimages.edition],
                ["Mint", `${afterimages.mintPriceEth} ETH`],
                ["Loop", `${afterimages.frames} × ${afterimages.frameDurationMs}ms`],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border bg-card p-4">
                  <dt className="text-xs uppercase tracking-wider text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-heading text-2xl">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:col-span-7 sm:grid-cols-3">
            {afterimageWorks.slice(0, 9).map((work) => (
              <Link
                key={work.id}
                href={afterimagesPath(`/${work.id}`)}
                className="group overflow-hidden rounded-2xl border bg-card"
              >
                <ApngImage
                  src={work.image}
                  alt={work.title}
                  width={640}
                  height={640}
                  className="aspect-square w-full object-cover transition duration-300 group-hover:scale-[1.04]"
                />
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-border bg-card/60">
        <div className="mx-auto grid w-full max-w-6xl gap-6 px-4 py-14 sm:px-6 md:grid-cols-3">
          {[
            ["Finished paintings", "Each token is one complete APNG. OpenSea lists the file you see — nothing is assembled at mint."],
            ["One of one", `${afterimages.supply} titles, ${afterimages.supply} clocks. No shuffle, no leftover combinations, no studio mixer.`],
            ["Drop-ready", `The pack is 1.gif–${afterimages.supply}.gif plus a Studio CSV. Upload it as an OpenSea Drop on Robinhood Chain.`],
          ].map(([title, body]) => (
            <div key={title}>
              <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">1:1</p>
              <h3 className="mt-1 font-heading text-2xl">{title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="overflow-hidden rounded-[2rem] border bg-[#1a120e] text-[#ffe8c8]">
          <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-[#f0c878]">Why APNG</p>
              <h2 className="mt-2 font-heading text-4xl">The loop is the painting.</h2>
              <p className="mt-4 text-[#ffe8c8]/75">
                A still would be a poster. Afterimages keeps the motion inside the file — 16 frames,
                100ms, looping — so the marketplace preview is the artwork.
              </p>
            </div>
            <div className="flex flex-col justify-end gap-3">
              <Button asChild size="lg" variant="secondary">
                <Link href={afterimagesPath("/gallery")}>Walk the wall</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#ffe8c8]/25 bg-transparent text-[#ffe8c8]">
                <Link href={afterimagesPath("/launch")}>Launch checklist</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
