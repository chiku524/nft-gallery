import type { Metadata } from "next";
import { PurrkinsStudio } from "@/components/purrkins-studio";
import { purrkins } from "@/data/purrkins";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live chibi-cat trait stack for Purrkins.",
};

export default function PurrkinsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered cat mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {purrkins.name} plays every trait as its own looping APNG. The preview is a live stack —
        pads, pelts, and gear keep moving instead of baking to a still.
      </p>
      <div className="mt-10">
        <PurrkinsStudio />
      </div>
    </div>
  );
}
