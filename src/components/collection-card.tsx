import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { GalleryProject } from "@/data/projects";

export function CollectionCard({ drop }: { drop: GalleryProject }) {
  const galleryHref = `${drop.href}/gallery`;
  const thumbs = drop.previews.slice(0, drop.kind === "1of1" ? 6 : 8);

  return (
    <article className="overflow-hidden rounded-[2rem] border bg-card">
      <Link href={drop.href} className="group relative block h-56 sm:h-80">
        <ApngImage
          src={drop.cover}
          alt={`${drop.name} banner`}
          className="absolute inset-0 size-full object-cover object-[center_35%] transition duration-500 group-hover:scale-[1.03]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#070816] via-[#070816]/45 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 p-6 sm:p-8">
          <Badge className="mb-3 bg-background/90 text-foreground">{drop.status}</Badge>
          <h3 className="font-heading text-3xl text-white sm:text-5xl">{drop.name}</h3>
          <p className="mt-2 max-w-xl text-white/80">{drop.tagline}</p>
        </div>
      </Link>

      <div className="grid gap-8 p-6 sm:p-8 lg:grid-cols-12">
        <div className="lg:col-span-5">
          <p className="text-muted-foreground">{drop.description}</p>
          <dl className="mt-6 grid grid-cols-2 gap-3">
            {[
              ["Supply", drop.kind === "1of1" ? `${drop.supply} × 1/1` : drop.supply.toLocaleString()],
              ["Chain", drop.chain],
              ["Chain ID", String(drop.chainId)],
            ].map(([label, value]) => (
              <div key={label} className="rounded-2xl border bg-background/60 p-3">
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">{label}</dt>
                <dd className="mt-1 font-heading text-xl">{value}</dd>
              </div>
            ))}
          </dl>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href={drop.href}>
                Enter the drop
                <ArrowRight data-icon="inline-end" />
              </Link>
            </Button>
            {drop.studioHref ? (
              <Button asChild size="lg" variant="secondary">
                <Link href={drop.studioHref}>Open the studio</Link>
              </Button>
            ) : (
              <Button asChild size="lg" variant="secondary">
                <Link href={galleryHref}>See the 1:1s</Link>
              </Button>
            )}
            {drop.openseaListings.map((listing) => (
              <Button key={listing.href} asChild size="lg" variant="outline">
                <a href={listing.href} target="_blank" rel="noreferrer">
                  {drop.openseaListings.length > 1 ? `OpenSea · ${listing.label}` : "View on OpenSea"}
                </a>
              </Button>
            ))}
          </div>
        </div>
        <div
          className={
            drop.kind === "1of1"
              ? "grid grid-cols-2 gap-3 sm:grid-cols-3 lg:col-span-7"
              : "grid grid-cols-2 gap-3 sm:grid-cols-4 lg:col-span-7"
          }
        >
          {thumbs.map((image, index) => (
            <Link key={`${drop.slug}-${image}`} href={galleryHref} className="overflow-hidden rounded-2xl border bg-background">
              <ApngImage
                src={image}
                alt={`${drop.name} preview ${index + 1}`}
                width={640}
                height={640}
                className="aspect-square w-full object-cover"
              />
            </Link>
          ))}
        </div>
      </div>
    </article>
  );
}
