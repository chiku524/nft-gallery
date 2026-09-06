import type { Metadata } from "next";
import { KamioriStudio } from "@/components/kamiori-studio";
import { kamiori } from "@/data/kamiori";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live origami trait stack for Kamiori.",
};

export default function KamioriStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Kamiori mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {kamiori.name} plays every trait as its own looping APNG. The preview is a live stack —
        deckle washi, a seated fold, crease scores, a draft that lifts one corner.
      </p>
      <div className="mt-10">
        <KamioriStudio />
      </div>
    </div>
  );
}
