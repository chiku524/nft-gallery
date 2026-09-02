import type { Metadata } from "next";
import { MochinsStudio } from "@/components/mochins-studio";
import { mochins } from "@/data/mochins";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live soft-3D mochi trait stack for Mochins.",
};

export default function MochinsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered mochi mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {mochins.name} plays every trait as its own looping APNG. The preview is a live stack —
        stages, dough, and steam keep moving instead of baking to a still.
      </p>
      <div className="mt-10">
        <MochinsStudio />
      </div>
    </div>
  );
}
