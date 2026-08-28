import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { GalleryFooter } from "@/components/gallery-footer";
import { sampleMints } from "@/data/gallery";
import { gallery, projects } from "@/data/projects";
import { potbPath } from "@/lib/potb";

export default function GalleryHomePage() {
  const potb = projects[0];

  return (
    <>
      <div className="flex-1">
        <section className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6 sm:py-16">
          <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">House of collections</p>
          <h1 className="mt-3 max-w-3xl font-heading text-4xl leading-[1.05] sm:text-6xl">
            {gallery.name}
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-muted-foreground">{gallery.description}</p>
        </section>

        <section className="mx-auto w-full max-w-6xl px-4 pb-16 sm:px-6">
          <div className="mb-6 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">On the wall</p>
              <h2 className="mt-1 font-heading text-3xl">Collections</h2>
            </div>
            <p className="hidden text-sm text-muted-foreground sm:block">
              {projects.length} live · more drops later
            </p>
          </div>

          <article className="overflow-hidden rounded-[2rem] border bg-card">
            <Link href={potb.href} className="group relative block h-56 sm:h-80">
              <Image
                src={potb.cover}
                alt={`${potb.name} banner`}
                fill
                priority
                className="object-cover object-[center_35%] transition duration-500 group-hover:scale-[1.03]"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#1c1410] via-[#1c1410]/45 to-transparent" />
              <div className="absolute inset-x-0 bottom-0 p-6 sm:p-8">
                <Badge className="mb-3 bg-background/90 text-foreground">{potb.status}</Badge>
                <h3 className="font-heading text-3xl text-white sm:text-5xl">{potb.name}</h3>
                <p className="mt-2 max-w-xl text-white/80">{potb.tagline}</p>
              </div>
            </Link>

            <div className="grid gap-8 p-6 sm:p-8 lg:grid-cols-12">
              <div className="lg:col-span-5">
                <p className="text-muted-foreground">{potb.description}</p>
                <dl className="mt-6 grid grid-cols-2 gap-3">
                  {[
                    ["Supply", potb.supply.toLocaleString()],
                    ["Chain", potb.chain],
                    ["Mint", `${potb.mintPriceEth} ETH`],
                    ["Chain ID", String(potb.chainId)],
                  ].map(([label, value]) => (
                    <div key={label} className="rounded-2xl border bg-background/60 p-3">
                      <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">{label}</dt>
                      <dd className="mt-1 font-heading text-xl">{value}</dd>
                    </div>
                  ))}
                </dl>
                <div className="mt-6 flex flex-wrap gap-3">
                  <Button asChild size="lg">
                    <Link href={potb.href}>
                      Enter the drop
                      <ArrowRight data-icon="inline-end" />
                    </Link>
                  </Button>
                  <Button asChild size="lg" variant="secondary">
                    <Link href={potbPath("/studio")}>Open the studio</Link>
                  </Button>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:col-span-7">
                {sampleMints.slice(0, 8).map((mint) => (
                  <Link
                    key={mint.id}
                    href={potbPath("/gallery")}
                    className="overflow-hidden rounded-2xl border bg-background"
                  >
                    <Image
                      src={mint.image}
                      alt={mint.name}
                      width={512}
                      height={512}
                      className="aspect-square w-full object-cover"
                    />
                  </Link>
                ))}
              </div>
            </div>
          </article>

          <div className="mt-6 rounded-[1.6rem] border border-dashed bg-card/40 px-6 py-10 text-center">
            <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Coming up</p>
            <h3 className="mt-2 font-heading text-2xl">The next drop is not on the wall yet.</h3>
            <p className="mx-auto mt-2 max-w-md text-sm text-muted-foreground">
              New collections land here as their own sub-projects — same gallery door, separate
              studio and mint path.
            </p>
          </div>
        </section>
      </div>
      <GalleryFooter />
    </>
  );
}
