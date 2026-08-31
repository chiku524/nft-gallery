import type { Metadata } from "next";
import Link from "next/link";
import { ApngImage } from "@/components/apng-image";
import { afterimageWorks, afterimages } from "@/data/afterimages";
import { afterimagesPath } from "@/lib/afterimages";

export const metadata: Metadata = {
  title: "Gallery",
  description: `${afterimages.supply} one-of-one Afterimages APNG paintings.`,
};

export default function AfterimagesGalleryPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Viewing room</p>
      <h1 className="mt-2 font-heading text-4xl">{afterimages.supply} 1:1 loops</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Every file is a finished APNG — {afterimages.canvas}×{afterimages.canvas}, {afterimages.frames}{" "}
        frames, {afterimages.frameDurationMs}ms. Open one and it keeps playing. These are the tokens
        the OpenSea Drop uploads.
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
    </div>
  );
}
