import type { Metadata } from "next";
import { CalderaStudio } from "@/components/caldera-studio";
import { caldera } from "@/data/caldera";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live hotel-matchbook trait stack for Caldera.",
};

export default function CalderaStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Match mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {caldera.name} plays every trait as its own looping APNG. The preview is a live stack —
        a cardboard book on a cafe cloth, a printed inn, a flame that flickers.
      </p>
      <div className="mt-10">
        <CalderaStudio />
      </div>
    </div>
  );
}
