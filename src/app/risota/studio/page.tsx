import type { Metadata } from "next";
import { RisotaStudio } from "@/components/risota-studio";
import { risota } from "@/data/risota";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live risograph trait stack for Risota.",
};

export default function RisotaStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Risota mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {risota.name} plays every trait as its own looping APNG. The preview is a live stack —
        paper tooth, halftone drift, a second plate that misses the register, the dancer stays seated.
      </p>
      <div className="mt-10">
        <RisotaStudio />
      </div>
    </div>
  );
}
