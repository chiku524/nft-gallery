import type { Metadata } from "next";
import { BoogieSquadStudio } from "@/components/boogiesquad-studio";
import { boogiesquad } from "@/data/boogiesquad";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live jelly-cel dance trait stack for Boogie Squad.",
};

export default function BoogieSquadStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Boogie mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {boogiesquad.name} plays every trait as its own looping APNG. The preview is a live stack —
        stages pulse, lights flash, the dancer steps, faces blink, fits and props ride the same groove.
      </p>
      <div className="mt-10">
        <BoogieSquadStudio />
      </div>
    </div>
  );
}
