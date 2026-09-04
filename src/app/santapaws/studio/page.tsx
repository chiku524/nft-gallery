import type { Metadata } from "next";
import { SantaPawsStudio } from "@/components/santapaws-studio";
import { santapaws } from "@/data/santapaws";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live chibi-cat trait stack for Santa Paws.",
};

export default function SantaPawsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered giving-cat mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {santapaws.name} plays every trait as its own looping APNG. The preview is a live stack —
        yards stay put, eyes blink, hats sit on the same crown, cocoa sways in the same paws.
      </p>
      <div className="mt-10">
        <SantaPawsStudio />
      </div>
    </div>
  );
}
