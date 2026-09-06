import type { Metadata } from "next";
import { UmbraStudio } from "@/components/umbra-studio";
import { umbra } from "@/data/umbra";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live shadow-puppet trait stack for Umbra.",
};

export default function UmbraStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Lamp mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {umbra.name} plays every trait as its own looping APNG. The preview is a live stack —
        a woven screen, an oil lamp, a seated hide, hinges that swing the dance.
      </p>
      <div className="mt-10">
        <UmbraStudio />
      </div>
    </div>
  );
}
