import type { Metadata } from "next";
import Image from "next/image";
import { sampleMints } from "@/data/gallery";

export const metadata: Metadata = {
  title: "Gallery",
  description: "Eight finished Pugs On The Block sample mints.",
};

export default function GalleryPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Sample stoop</p>
      <h1 className="mt-2 font-heading text-4xl">Finished pugs</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Eight fully dressed previews with traits already composited. Token metadata for each lives
        in <code className="rounded bg-secondary px-1.5 py-0.5 text-sm">public/metadata</code>.
      </p>

      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {sampleMints.map((mint) => (
          <article key={mint.id} className="overflow-hidden rounded-[1.6rem] border bg-card">
            <Image
              src={mint.image}
              alt={mint.name}
              width={1024}
              height={1024}
              className="aspect-square w-full object-cover"
            />
            <div className="space-y-3 p-4">
              <h2 className="font-heading text-xl">{mint.name}</h2>
              <ul className="space-y-1 text-sm text-muted-foreground">
                {mint.attributes.map((attribute) => (
                  <li key={attribute.trait_type} className="flex justify-between gap-3">
                    <span>{attribute.trait_type}</span>
                    <span className="text-foreground">{attribute.value}</span>
                  </li>
                ))}
              </ul>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
