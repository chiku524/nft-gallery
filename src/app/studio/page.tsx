import type { Metadata } from "next";
import { StudioMixer } from "@/components/studio-mixer";
import { collection } from "@/data/collection";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live APNG trait stack for Loopkins.",
};

export default function StudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered APNG mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {collection.name} plays every trait as its own APNG. The preview is a live stack — skies,
        auras, faces, and charms keep looping instead of baking to a still.
      </p>
      <div className="mt-10">
        <StudioMixer />
      </div>
    </div>
  );
}
