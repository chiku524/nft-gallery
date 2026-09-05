import type { Metadata } from "next";
import { PerfinStudio } from "@/components/perfin-studio";
import { perfin } from "@/data/perfin";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live engraved-stamp trait stack for Perfin.",
};

export default function PerfinStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Perfin mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {perfin.name} plays every trait as its own looping APNG. The preview is a live stack —
        wove paper, security guilloche, a seated bust, a cancel that walks the face.
      </p>
      <div className="mt-10">
        <PerfinStudio />
      </div>
    </div>
  );
}
