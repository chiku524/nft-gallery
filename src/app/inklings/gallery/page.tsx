import type { Metadata } from "next";
import { ApngImage } from "@/components/apng-image";
import { inklingSamples } from "@/data/inkling-gallery";
import { inklings } from "@/data/inklings";

export const metadata: Metadata = {
  title: "Gallery",
  description: "Signature Inklings stacked from ink-wash PFP layers.",
};

const extraPreviews = [9, 10, 11, 12, 13, 14, 15, 16];

export default function InklingsGalleryPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Sample loops</p>
      <h1 className="mt-2 font-heading text-4xl">Flattened PFP GIFs</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Tokens 1–8 are the signature looks. Each file is one looping GIF: every trait layer composited
        on the same {inklings.frames}-frame clock. The rest of the {inklings.supply.toLocaleString()} lives
        in <code className="rounded bg-secondary px-1.5 py-0.5 text-sm">generated/inklings/gifs</code> after
        you run the generator.
      </p>

      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {inklingSamples.map((mint) => (
          <article key={mint.id} className="overflow-hidden rounded-[1.6rem] border bg-card">
            <ApngImage
              src={mint.image}
              alt={mint.name}
              width={640}
              height={640}
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

      <h2 className="mt-16 font-heading text-3xl">More from the shuffle</h2>
      <p className="mt-2 max-w-2xl text-muted-foreground">
        Eight more baked loops. Open them as files and they keep playing — these are GIFs, not stills.
      </p>
      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {extraPreviews.map((id) => (
          <article key={id} className="overflow-hidden rounded-2xl border bg-card">
            <ApngImage
              src={`/inklings-preview/${id}.gif`}
              alt={`Inkling #${id}`}
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
