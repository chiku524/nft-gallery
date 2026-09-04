import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { galleria, galleriaWorks, getGalleriaWork } from "@/data/galleria";
import { galleriaPath } from "@/lib/galleria";

export function generateStaticParams() {
  return galleriaWorks.map((work) => ({ id: String(work.id) }));
}

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params;
  const work = getGalleriaWork(Number(id));
  if (!work) {
    return { title: "Artwork" };
  }
  return {
    title: work.title,
    description: work.description,
  };
}

export default async function GalleriaWorkPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const work = getGalleriaWork(Number(id));
  if (!work) {
    notFound();
  }

  const featuredCount = galleriaWorks.length;
  const prev = getGalleriaWork(work.id === 1 ? featuredCount : work.id - 1);
  const next = getGalleriaWork(work.id === featuredCount ? 1 : work.id + 1);

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <Link href={galleriaPath("/gallery")} className="text-sm text-muted-foreground hover:text-foreground">
        ← Back to the salon
      </Link>

      <div className="mt-6 grid gap-10 lg:grid-cols-12">
        <div className="overflow-hidden rounded-[2rem] border bg-card lg:col-span-7">
          <ApngImage
            src={work.image}
            alt={work.title}
            width={512}
            height={512}
            className="aspect-square w-full object-cover"
          />
        </div>
        <div className="lg:col-span-5">
          <Badge variant="secondary">
            Work #{work.id} · {galleria.edition}
          </Badge>
          <h1 className="mt-4 font-heading text-4xl">{work.title}</h1>
          <p className="mt-4 text-muted-foreground">{work.description}</p>
          <dl className="mt-8 space-y-2">
            {work.attributes.map((attribute) => (
              <div key={attribute.trait_type} className="flex justify-between gap-4 rounded-2xl border bg-card px-4 py-3">
                <dt className="text-sm text-muted-foreground">{attribute.trait_type}</dt>
                <dd className="text-sm font-medium">{attribute.value}</dd>
              </div>
            ))}
          </dl>
          <p className="mt-6 text-sm text-muted-foreground">
            File <code className="rounded bg-secondary px-1.5 py-0.5">{work.id}.png</code> ·{" "}
            {galleria.canvas}×{galleria.canvas} APNG · {galleria.frames} frames · {galleria.mintPriceEth} ETH
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            {prev ? (
              <Button asChild variant="secondary">
                <Link href={galleriaPath(`/${prev.id}`)}>
                  <ArrowLeft data-icon="inline-start" />
                  {prev.title}
                </Link>
              </Button>
            ) : null}
            {next ? (
              <Button asChild>
                <Link href={galleriaPath(`/${next.id}`)}>
                  {next.title}
                  <ArrowRight data-icon="inline-end" />
                </Link>
              </Button>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}
