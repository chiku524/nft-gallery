import type { Metadata } from "next";
import { HoodkinsStudio } from "@/components/hoodkins-studio";
import { hoodkins } from "@/data/hoodkins";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live chibi-raccoon trait stack for Hoodkins.",
};

export default function HoodkinsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered raccoon mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {hoodkins.name} plays every trait as its own looping APNG. The preview is a live stack —
        pads, pelts, and gear keep moving instead of baking to a still.
      </p>
      <div className="mt-10">
        <HoodkinsStudio />
      </div>
    </div>
  );
}
