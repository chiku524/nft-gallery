import type { Metadata } from "next";
import { WicklingsStudio } from "@/components/wicklings-studio";
import { wicklings } from "@/data/wicklings";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live paper-lantern trait stack for Wicklings.",
};

export default function WicklingsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered lantern mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {wicklings.name} plays every trait as its own looping APNG. The preview is a live stack —
        nights, paper vessels, and drifting moths keep moving instead of baking to a still.
      </p>
      <div className="mt-10">
        <WicklingsStudio />
      </div>
    </div>
  );
}
