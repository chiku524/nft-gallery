import type { Metadata } from "next";
import { BirbsStudio } from "@/components/birbs-studio";
import { birbs } from "@/data/birbs";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live round-borb robin trait stack for BirbNation.",
};

export default function BirbsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered BirbNation mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {birbs.name} plays every trait as its own looping APNG. The preview is a live stack —
        fields stay still, eyes blink, wings twitch, accents bob.
      </p>
      <div className="mt-10">
        <BirbsStudio />
      </div>
    </div>
  );
}
