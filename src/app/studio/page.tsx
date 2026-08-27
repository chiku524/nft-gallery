import type { Metadata } from "next";
import { StudioMixer } from "@/components/studio-mixer";

export const metadata: Metadata = {
  title: "Trait studio",
  description: "Mix background, base, hat, body, and accessory layers for Pugs On The Block.",
};

export default function StudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Generator</p>
      <h1 className="mt-2 font-heading text-4xl">Build a pug on the block.</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        This is the same layer stack the collection mints from. Shuffle for a random stoop pug, or
        click a trait tile and download the PNG.
      </p>
      <div className="mt-8">
        <StudioMixer />
      </div>
    </div>
  );
}
