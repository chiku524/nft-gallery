import type { Metadata } from "next";
import { VirelloStudio } from "@/components/virello-studio";
import { virello } from "@/data/virello";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live wind-up tin-toy trait stack for Virello.",
};

export default function VirelloStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Toy mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {virello.name} plays every trait as its own looping APNG. The preview is a live stack —
        a stamped chassis on a toy-shop bench, litho enamel, a winding key that turns.
      </p>
      <div className="mt-10">
        <VirelloStudio />
      </div>
    </div>
  );
}
