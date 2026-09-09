import type { Metadata } from "next";
import { FeltroStudio } from "@/components/feltro-studio";
import { feltro } from "@/data/feltro";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live foam-mascot trait stack for Feltro.",
};

export default function FeltroStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Court mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {feltro.name} plays every trait as its own looping APNG. The preview is a live stack —
        a gym floor, a foam suit, nap, mesh, a seam, a crest, and fuzz.
      </p>
      <div className="mt-10">
        <FeltroStudio />
      </div>
    </div>
  );
}
