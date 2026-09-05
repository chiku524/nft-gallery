import type { Metadata } from "next";
import { OpalineStudio } from "@/components/opaline-studio";
import { opaline } from "@/data/opaline";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live smoked-glass trait stack for Opaline.",
};

export default function OpalineStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Opaline mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {opaline.name} plays every trait as its own looping APNG. The preview is a live stack —
        ateliers breathe, film shifts, the crystal bust stays seated.
      </p>
      <div className="mt-10">
        <OpalineStudio />
      </div>
    </div>
  );
}
