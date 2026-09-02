import type { Metadata } from "next";
import Link from "next/link";
import { ApngImage } from "@/components/apng-image";
import { afterimageWorks, afterimages } from "@/data/afterimages";
import { afterimagesPath } from "@/lib/afterimages";

export const metadata: Metadata = {
  title: "Gallery",
  description: `${afterimages.supply.toLocaleString()} one-of-one Afterimages looping paintings.`,
};

const extraPreviews = [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66];

export default function AfterimagesGalleryPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Viewing room</p>
      <h1 className="mt-2 font-heading text-4xl">{afterimages.supply.toLocaleString()} 1:1 loops</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Tokens 1–{afterimageWorks.length} are the signature paintings. Each file is a finished loop —{" "}
        {afterimages.canvas}×{afterimages.canvas}, {afterimages.frames} frames, {afterimages.frameDurationMs}
        ms. The rest of the {afterimages.supply.toLocaleString()} lives in{" "}
        <code className="rounded bg-secondary px-1.5 py-0.5 text-sm">generated/afterimages/gifs</code> for
        the OpenSea Drop on {afterimages.chain.name}.
      </p>

      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {afterimageWorks.map((work) => (
          <Link
            key={work.id}
            href={afterimagesPath(`/${work.id}`)}
            className="group overflow-hidden rounded-[1.6rem] border bg-card"
          >
            <ApngImage
              src={work.image}
              alt={work.title}
              width={640}
              height={640}
              className="aspect-square w-full object-cover transition duration-300 group-hover:scale-[1.03]"
            />
            <div className="space-y-2 p-4">
              <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">
                #{work.id} · {afterimages.edition}
              </p>
              <h2 className="font-heading text-xl">{work.title}</h2>
              <p className="text-sm text-muted-foreground">{work.description}</p>
            </div>
          </Link>
        ))}
      </div>

      <h2 className="mt-16 font-heading text-3xl">More from the series</h2>
      <p className="mt-2 max-w-2xl text-muted-foreground">
        Sixteen loops from tokens 51–66. The OpenSea pack is every file from 1.gif through{" "}
        {afterimages.supply}.gif.
      </p>
      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {extraPreviews.map((id) => (
          <article key={id} className="overflow-hidden rounded-2xl border bg-card">
            <ApngImage
              src={`/afterimages-preview/${id}.gif`}
              alt={`Afterimage #${id}`}
              width={640}
              height={640}
              className="aspect-square w-full object-cover"
            />
            <p className="px-2 py-1.5 text-xs text-muted-foreground">#{id}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
