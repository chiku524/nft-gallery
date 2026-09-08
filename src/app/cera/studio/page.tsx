import type { Metadata } from "next";
import { CeraStudio } from "@/components/cera-studio";
import { cera } from "@/data/cera";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live lava-lamp trait stack for Cera.",
};

export default function CeraStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Lamp mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {cera.name} plays every trait as its own looping APNG. The preview is a live stack —
        a glass flask on a nightstand, paraffin that rises, a coil that glows.
      </p>
      <div className="mt-10">
        <CeraStudio />
      </div>
    </div>
  );
}
