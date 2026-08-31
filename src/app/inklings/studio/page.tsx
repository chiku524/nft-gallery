import type { Metadata } from "next";
import { InklingsStudio } from "@/components/inklings-studio";
import { inklings } from "@/data/inklings";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live ink-wash trait stack for Inklings.",
};

export default function InklingsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered ink-wash mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {inklings.name} plays every trait as its own looping wash. The preview is a live stack — paper,
        blooms, squids, and marks keep moving instead of baking to a still.
      </p>
      <div className="mt-10">
        <InklingsStudio />
      </div>
    </div>
  );
}
