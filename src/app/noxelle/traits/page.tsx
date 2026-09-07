import type { Metadata } from "next";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { NOXELLE_DURATION_MS, NOXELLE_FRAMES, noxelleTraitCategories } from "@/data/noxelle-traits";
import { noxelle } from "@/data/noxelle";

export const metadata: Metadata = {
  title: "Trait loops",
  description: "Every neon-tube trait layer in the Noxelle stack.",
};

export default function NoxelleTraitsPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Layer library</p>
      <h1 className="mt-2 font-heading text-4xl">Trait loops</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Each file is an APNG on a {noxelle.canvas}×{noxelle.canvas} canvas: {NOXELLE_FRAMES} frames,{" "}
        {NOXELLE_DURATION_MS}ms, looping. Studio stacks wall → spill → gas → bend → clip → badge →
        mote. The glass stays put. The dance is the bend.
      </p>

      <div className="mt-10 space-y-14">
        {noxelleTraitCategories.map((category) => (
          <section key={category.id} id={category.id}>
            <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
              <div>
                <h2 className="font-heading text-3xl">{category.label}</h2>
                <p className="text-sm text-muted-foreground">{category.blurb}</p>
              </div>
              <Badge variant="secondary">
                {category.traits.length}
                {category.noneLabel ? " + none" : ""} loops
              </Badge>
            </div>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
              {category.traits.map((trait) => (
                <article key={trait.id} className="overflow-hidden rounded-2xl border bg-card">
                  <div className="relative aspect-square bg-[repeating-conic-gradient(#1a0e28_0%_25%,#12081c_0%_50%)] bg-[length:16px_16px]">
                    {trait.image ? (
                      <ApngImage
                        src={trait.image}
                        alt={trait.name}
                        className="absolute inset-0 size-full object-cover"
                      />
                    ) : null}
                  </div>
                  <div className="flex items-center justify-between gap-2 px-3 py-3">
                    <div>
                      <h3 className="font-medium">{trait.name}</h3>
                      <p className="text-xs text-muted-foreground">{trait.id}.png</p>
                    </div>
                    <span className="text-sm tabular-nums text-muted-foreground">{trait.rarity}%</span>
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
