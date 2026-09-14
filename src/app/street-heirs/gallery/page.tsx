import type { Metadata } from "next";
import Image from "next/image";
import { streetHeirsSamples } from "@/data/street-heirs-gallery";

export const metadata: Metadata = {
  title: "Gallery",
  description: "Sixteen signature Street Heirs portraits and their complete trait recipes.",
};

export default function StreetHeirsGalleryPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-[#496A9A]">Signature selection</p>
      <h1 className="mt-2 font-heading text-4xl sm:text-5xl">Sixteen heirs, fully baked.</h1>
      <p className="mt-4 max-w-2xl text-[#202A3D]/70">
        Approved portraits from the completed static PNG collection. Every card records the eight plates behind its look.
      </p>
      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {streetHeirsSamples.map((sample) => (
          <article key={sample.id} className="overflow-hidden rounded-[1.6rem] border border-[#202A3D]/15 bg-white/55">
            <Image
              src={sample.image}
              alt={sample.name}
              width={512}
              height={512}
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
              unoptimized
              className="aspect-square w-full object-cover"
            />
            <div className="p-4">
              <h2 className="font-heading text-xl">{sample.name}</h2>
              <dl className="mt-3 space-y-1.5 text-xs">
                {sample.attributes.map((attribute) => (
                  <div key={attribute.trait_type} className="flex justify-between gap-3 border-t border-[#202A3D]/10 pt-1.5">
                    <dt className="text-[#496A9A]">{attribute.trait_type}</dt>
                    <dd className="text-right font-medium">{attribute.value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
