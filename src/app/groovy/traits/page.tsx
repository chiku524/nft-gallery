import type { Metadata } from "next";
import { ApngImage } from "@/components/apng-image";
import { Badge } from "@/components/ui/badge";
import { GROOVY_DURATION_MS, GROOVY_FRAMES, groovyTraitCategories } from "@/data/groovy-traits";
import { groovy } from "@/data/groovy";

export const metadata: Metadata = {
  title: "Trait loops",
  description: "Every cartoon-note trait layer in the Groovy Nation stack.",
};

export default function GroovyTraitsPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Layer library</p>
      <h1 className="mt-2 font-heading text-4xl">Trait loops</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Each file is an APNG on a {groovy.canvas}×{groovy.canvas} canvas: {GROOVY_FRAMES} frames,{" "}
        {GROOVY_DURATION_MS}ms, looping. Studio stacks venue → note → expression → topper → cable → riff.
        Notes bounce. Toppers sit on one head. The stem stays put.
      </p>

      <div className="mt-10 space-y-14">
        {groovyTraitCategories.map((category) => (
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
                  <div className="relative aspect-square bg-[repeating-conic-gradient(#2a0818_0%_25%,#4a1230_0%_50%)] bg-[length:16px_16px]">
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
