import type { Metadata } from "next";
import { VinylonStudio } from "@/components/vinylon-studio";
import { vinylon } from "@/data/vinylon";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live balloon-animal trait stack for Vinylon.",
};

export default function VinylonStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Booth mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {vinylon.name} plays every trait as its own looping APNG. The preview is a live stack —
        a party booth, latex, a twist, knots, a valve, gleam, and confetti.
      </p>
      <div className="mt-10">
        <VinylonStudio />
      </div>
    </div>
  );
}
