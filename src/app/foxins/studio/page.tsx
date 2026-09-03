import type { Metadata } from "next";
import { FoxinsStudio } from "@/components/foxins-studio";
import { foxins } from "@/data/foxins";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live bold-graphic fox trait stack for Foxins.",
};

export default function FoxinsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Foxins mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {foxins.name} plays every trait as its own looping APNG. The preview is a live stack —
        fields stay still, eyes blink, the sticker hovers, hats sit between the same ears.
      </p>
      <div className="mt-10">
        <FoxinsStudio />
      </div>
    </div>
  );
}
