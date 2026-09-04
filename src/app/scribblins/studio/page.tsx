import type { Metadata } from "next";
import { ScribblinsStudio } from "@/components/scribblins-studio";
import { scribblins } from "@/data/scribblins";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live doodle-critter trait stack for Scribblins.",
};

export default function ScribblinsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Scribblins mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {scribblins.name} plays every trait as its own looping APNG. The preview is a live stack —
        fields stay still, eyes blink, the doodle hovers, hats sit on the same crown.
      </p>
      <div className="mt-10">
        <ScribblinsStudio />
      </div>
    </div>
  );
}
