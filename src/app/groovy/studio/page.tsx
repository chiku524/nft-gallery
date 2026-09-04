import type { Metadata } from "next";
import { GroovyStudio } from "@/components/groovy-studio";
import { groovy } from "@/data/groovy";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live cartoon-note trait stack for Groovy Nation.",
};

export default function GroovyStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered Groovy mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {groovy.name} plays every trait as its own looping APNG. The preview is a live stack —
        venues glow, notes bounce, toppers sit on the same cartoon head.
      </p>
      <div className="mt-10">
        <GroovyStudio />
      </div>
    </div>
  );
}
