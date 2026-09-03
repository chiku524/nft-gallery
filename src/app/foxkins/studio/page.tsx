import type { Metadata } from "next";
import { FoxkinsStudio } from "@/components/foxkins-studio";
import { foxkins } from "@/data/foxkins";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live bold-graphic fox trait stack for Foxkins.",
};

export default function FoxkinsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Foxkins mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {foxkins.name} plays every trait as its own looping APNG. The preview is a live stack —
        fields stay still, eyes blink, the sticker hovers, hats sit between the same ears.
      </p>
      <div className="mt-10">
        <FoxkinsStudio />
      </div>
    </div>
  );
}
