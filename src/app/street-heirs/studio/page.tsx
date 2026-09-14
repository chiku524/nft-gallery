import type { Metadata } from "next";
import { StreetHeirsStudio } from "@/components/street-heirs-studio";

export const metadata: Metadata = {
  title: "Studio",
  description: "Compose a compatible Street Heirs portrait from 70 weighted artwork plates.",
};

export default function StreetHeirsStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-[#496A9A]">Portrait studio</p>
      <h1 className="mt-2 font-heading text-4xl sm:text-5xl">Tune the signal.</h1>
      <p className="mt-4 max-w-2xl text-[#202A3D]/70">
        Select every plate or use weighted shuffle. Incompatible combinations are held back, and signals automatically move behind or in front of the character.
      </p>
      <div className="mt-10"><StreetHeirsStudio /></div>
    </div>
  );
}
