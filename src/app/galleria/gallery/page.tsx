import type { Metadata } from "next";
import Link from "next/link";
import { galleria, galleriaWorks } from "@/data/galleria";
import { galleriaPath } from "@/lib/galleria";

export const metadata: Metadata = {
  title: "Gallery",
  description: `${galleria.supply} open-edition Galleria On Ink looping paintings.`,
};

const PAGE_SIZE = 24;

export default async function GalleriaGalleryPage({
  searchParams,
}: {
  searchParams: Promise<{ page?: string }>;
}) {
  const params = await searchParams;
  const totalPages = Math.max(1, Math.ceil(galleriaWorks.length / PAGE_SIZE));
  const requested = Number(params.page) || 1;
  const page = Math.min(totalPages, Math.max(1, requested));
  const start = (page - 1) * PAGE_SIZE;
  const visible = galleriaWorks.slice(start, start + PAGE_SIZE);

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Salon</p>
      <h1 className="mt-2 font-heading text-4xl">{galleria.supply} open editions</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Each file is a finished loop — {galleria.canvas}×{galleria.canvas}, {galleria.frames} frames,{" "}
        {galleria.frameDurationMs}ms — painted by its own engine. Neighboring works do not share a
        medium. The mint is an open edition on {galleria.chain.name}. Stills on this wall; open a work
        to play the loop.
      </p>

      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {visible.map((work) => (
          <Link
            key={work.id}
            href={galleriaPath(`/${work.id}`)}
            className="group overflow-hidden rounded-[1.6rem] border bg-card"
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`/galleria/thumbs/${work.id}.jpg`}
              alt={work.title}
              width={320}
              height={320}
              className="aspect-square w-full object-cover transition duration-300 group-hover:scale-[1.03]"
            />
            <div className="space-y-2 p-4">
              <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">
                #{work.id} · {galleria.edition}
              </p>
              <h2 className="font-heading text-xl">{work.title}</h2>
              <p className="text-sm text-muted-foreground">{work.description}</p>
            </div>
          </Link>
        ))}
      </div>

      <nav className="mt-10 flex flex-wrap items-center justify-between gap-4 text-sm">
        {page > 1 ? (
          <Link href={galleriaPath(page === 2 ? "/gallery" : `/gallery?page=${page - 1}`)} className="underline">
            Previous
          </Link>
        ) : (
          <span />
        )}
        <p className="text-muted-foreground">
          Page {page} of {totalPages}
        </p>
        {page < totalPages ? (
          <Link href={galleriaPath(`/gallery?page=${page + 1}`)} className="underline">
            Next
          </Link>
        ) : (
          <span />
        )}
      </nav>
    </div>
  );
}
