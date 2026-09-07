import type { Metadata } from "next";
import { NoxelleStudio } from "@/components/noxelle-studio";
import { noxelle } from "@/data/noxelle";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live neon-tube trait stack for Noxelle.",
};

export default function NoxelleStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Tube mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {noxelle.name} plays every trait as its own looping APNG. The preview is a live stack —
        a club wall, a noble-gas bloom, a seated bend of glass.
      </p>
      <div className="mt-10">
        <NoxelleStudio />
      </div>
    </div>
  );
}
