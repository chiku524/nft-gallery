import type { Metadata } from "next";
import Image from "next/image";
import { robinBanxTraitCategories, robinBanxTraitSrc } from "@/data/robinbanx-traits";
import { robinBanx } from "@/data/robinbanx";

export const metadata: Metadata = {
  title: "Evidence index",
  description: "The static transparent PNG trait plates used in Robin Banx portraits.",
};

export default function RobinBanxTraitsPage() {
  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6">
      <p className="font-mono text-xs uppercase tracking-[0.24em] text-[#e24932]">Property room / indexed exhibits</p>
      <h1 className="mt-3 text-5xl font-black uppercase leading-none sm:text-7xl">Evidence index</h1>
      <p className="mt-5 max-w-3xl text-[#aeb1a7]">
        Every exhibit is a transparent static PNG registered to a {robinBanx.canvas}×{robinBanx.canvas} canvas.
        Stack order is fixed by the catalog so silhouettes, masks, shadows, stamps, and seized accessories remain aligned.
      </p>

      <div className="mt-14 space-y-20">
        {robinBanxTraitCategories.map((category, categoryIndex) => (
          <section key={category.id} id={category.id} aria-labelledby={`${category.id}-heading`}>
            <div className="mb-6 grid gap-3 border-l-4 border-[#e24932] pl-5 md:grid-cols-[1fr_auto] md:items-end">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#778071]">
                  Exhibit series {String(categoryIndex + 1).padStart(2, "0")}
                </p>
                <h2 id={`${category.id}-heading`} className="mt-1 text-3xl font-black uppercase">{category.label}</h2>
                <p className="mt-2 max-w-2xl text-sm text-[#969c90]">
                  {category.optional
                    ? "Optional evidence plate; the catalog includes a clear record when this layer is absent."
                    : "Required foundation plate present in every composite."}
                </p>
              </div>
              <p className="font-mono text-xs uppercase text-[#e24932]">
                {category.traits.length} records
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
              {category.traits.map((trait) => (
                <article key={trait.id} className="border border-[#c7bda7]/20 bg-[#141715]">
                  <div className="relative aspect-square bg-[linear-gradient(135deg,#222622_25%,#111311_25%,#111311_50%,#222622_50%,#222622_75%,#111311_75%)] bg-[length:18px_18px]">
                    {trait.image ? (
                      <Image
                        src={robinBanxTraitSrc(trait.image)}
                        alt=""
                        fill
                        sizes="(min-width: 1024px) 20vw, (min-width: 640px) 33vw, 50vw"
                        className="object-cover"
                        unoptimized
                      />
                    ) : null}
                  </div>
                  <div className="border-t border-[#c7bda7]/20 p-3">
                    <h3 className="text-sm font-bold uppercase text-[#eee8da]">{trait.name}</h3>
                    <div className="mt-2 flex justify-between gap-2 font-mono text-[10px] uppercase text-[#778071]">
                      <span>{trait.id}.png</span>
                      <span>{trait.rarity}%</span>
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
