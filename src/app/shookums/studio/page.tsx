import type { Metadata } from "next";
import { ShookumsStudio } from "@/components/shookums-studio";
import { shookums } from "@/data/shookums";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live sheet-ghost trait stack for Halloween Shook'ums.",
};

export default function ShookumsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Shook&apos;ums mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {shookums.name} plays every trait as its own looping APNG. The preview is a live stack —
        nights stay still, eyes blink, the sheet hovers, hats sit on the same crown.
      </p>
      <div className="mt-10">
        <ShookumsStudio />
      </div>
    </div>
  );
}
