import type { Metadata } from "next";
import { OsseinStudio } from "@/components/ossein-studio";
import { ossein } from "@/data/ossein";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live anatomical-chart trait stack for Ossein.",
};

export default function OsseinStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Plate mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {ossein.name} plays every trait as its own looping APNG. The preview is a live stack —
        a ruled sheet, a specimen, joints, leaders, stain, and chalk.
      </p>
      <div className="mt-10">
        <OsseinStudio />
      </div>
    </div>
  );
}
