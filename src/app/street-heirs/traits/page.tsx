import type { Metadata } from "next";
import Image from "next/image";
import { Badge } from "@/components/ui/badge";
import { streetHeirsTraitCategories, streetHeirsTraitSrc } from "@/data/street-heirs-traits";

export const metadata: Metadata = {
  title: "Traits",
  description: "All 70 Street Heirs artwork plates, grouped by category.",
};

export default function StreetHeirsTraitsPage() {
  const total = streetHeirsTraitCategories.reduce((sum, category) => sum + category.traits.length, 0);
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-[#496A9A]">Plate library</p>
      <h1 className="mt-2 font-heading text-4xl sm:text-5xl">{total} illustrated plates.</h1>
      <p className="mt-4 max-w-2xl text-[#202A3D]/70">
        Eight required categories build every portrait. Signal placement is encoded in the generated data, so the Studio automatically moves those plates behind the character or into the foreground.
      </p>
      <div className="mt-12 space-y-16">
        {streetHeirsTraitCategories.map((category) => (
          <section key={category.id} id={category.id}>
            <div className="mb-5 flex items-end justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-[0.18em] text-[#496A9A]">{category.id}</p>
                <h2 className="font-heading text-3xl">{category.label}</h2>
              </div>
              <Badge className="bg-[#202A3D] text-[#F4EFE5]">{category.traits.length} plates</Badge>
            </div>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
              {category.traits.map((trait) => (
                <article key={trait.id} className="overflow-hidden rounded-2xl border border-[#202A3D]/15 bg-white/55">
                  <div className="relative aspect-square bg-[#202A3D]">
                    <Image
                      src={streetHeirsTraitSrc(trait.image)}
                      alt={`${trait.name} ${category.label} plate`}
                      fill
                      sizes="(max-width: 640px) 50vw, (max-width: 1024px) 25vw, 20vw"
                      unoptimized
                      className="object-cover"
                    />
                  </div>
                  <div className="p-3">
                    <h3 className="font-medium">{trait.name}</h3>
                    <div className="mt-1 flex flex-wrap gap-1.5 text-[11px] text-[#496A9A]">
                      <span>Weight {trait.weight}</span>
                      {trait.placement ? <span>· {trait.placement === "behind-character" ? "Behind character" : "Foreground"}</span> : null}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
