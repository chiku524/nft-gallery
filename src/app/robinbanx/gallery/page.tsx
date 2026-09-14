import type { Metadata } from "next";
import Image from "next/image";
import { robinBanxSamples } from "@/data/robinbanx-gallery";
import { robinBanx } from "@/data/robinbanx";

export const metadata: Metadata = {
  title: "Suspect lineup",
  description: "Sample static PNG portraits from the Robin Banx case files.",
};

export default function RobinBanxGalleryPage() {
  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6">
      <div className="grid gap-6 border-b border-[#c7bda7]/20 pb-10 md:grid-cols-[1fr_auto] md:items-end">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.24em] text-[#e24932]">Visual identification / samples</p>
          <h1 className="mt-3 text-5xl font-black uppercase leading-none sm:text-7xl">Suspect lineup</h1>
          <p className="mt-5 max-w-2xl text-[#aeb1a7]">
            Planned sample files from a {robinBanx.supply.toLocaleString()}-portrait collection. Each token is a
            flattened {robinBanx.canvas}×{robinBanx.canvas} static PNG; the attributes record every plate in the composite.
          </p>
        </div>
        <div className="-rotate-2 border-2 border-[#e24932] px-4 py-2 font-mono text-sm font-black uppercase tracking-[0.16em] text-[#e24932]">
          Unreleased material
        </div>
      </div>

      {robinBanxSamples.length ? (
        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {robinBanxSamples.map((sample, index) => (
            <article key={sample.id} className="group border border-[#c7bda7]/20 bg-[#141715] p-2">
              <div className="relative aspect-square overflow-hidden bg-[#1c201d]">
                <Image
                  src={sample.image}
                  alt={sample.name}
                  fill
                  sizes="(min-width: 1280px) 25vw, (min-width: 640px) 50vw, 100vw"
                  className="object-cover transition duration-300 group-hover:scale-[1.025]"
                  unoptimized
                />
                <span className="absolute left-3 top-3 bg-[#e24932] px-2 py-1 font-mono text-[10px] font-black text-[#0b0c0c]">
                  RBX-{String(sample.id).padStart(5, "0")}
                </span>
              </div>
              <div className="p-3">
                <div className="flex items-center justify-between gap-3">
                  <h2 className="text-lg font-black uppercase">{sample.name}</h2>
                  <span className="font-mono text-xs text-[#788071]">#{index + 1}</span>
                </div>
                <dl className="mt-4 space-y-1.5 border-t border-[#c7bda7]/15 pt-3 text-xs">
                  {sample.attributes.map((attribute) => (
                    <div key={attribute.trait_type} className="flex justify-between gap-3">
                      <dt className="font-mono uppercase text-[#757c70]">{attribute.trait_type}</dt>
                      <dd className="text-right text-[#c8c6ba]">{attribute.value}</dd>
                    </div>
                  ))}
                </dl>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <div className="mt-12 border border-dashed border-[#c7bda7]/30 px-6 py-20 text-center">
          <p className="font-mono text-sm uppercase tracking-[0.2em] text-[#92988c]">Lineup catalog pending generation</p>
        </div>
      )}
    </div>
  );
}
