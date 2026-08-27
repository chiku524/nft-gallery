import type { Metadata } from "next";
import Image from "next/image";
import { sampleMints } from "@/data/gallery";

export const metadata: Metadata = {
  title: "Gallery",
  description: "Hand-dressed samples and a slice of the 10,000 shuffled Pugs On The Block drop.",
};

const shuffledPreviews = [1, 2, 3, 4, 5, 6, 7, 8, 112, 1362, 2612, 3862, 5112, 6362, 7612, 8862];

export default function GalleryPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Sample stoop</p>
      <h1 className="mt-2 font-heading text-4xl">Finished pugs</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Eight hand-composited looks, plus the full 10,000 shuffled drop in{" "}
        <code className="rounded bg-secondary px-1.5 py-0.5 text-sm">generated/images</code>.
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

      <h2 className="mt-16 font-heading text-3xl">From the 10,000</h2>
      <p className="mt-2 max-w-2xl text-muted-foreground">
        A slice of the rarity-weighted shuffle. Upload all 10,000 JPEGs and{" "}
        <code className="rounded bg-secondary px-1.5 py-0.5 text-sm">generated/opensea-metadata.csv</code>{" "}
        to an OpenSea Drop.
      </p>
      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-8">
        {shuffledPreviews.map((id) => (
          <article key={id} className="overflow-hidden rounded-2xl border bg-card">
            <Image
              src={`/generated-preview/${id}.jpg`}
              alt={`Pugs On The Block #${id}`}
              width={1024}
              height={1024}
              className="aspect-square w-full object-cover"
            />
            <p className="px-2 py-1.5 text-xs text-muted-foreground">#{id}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
