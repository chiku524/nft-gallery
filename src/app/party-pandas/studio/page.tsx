import type { Metadata } from "next";
import { PartyPandasStudio } from "@/components/party-pandas-studio";
import { partyPandas } from "@/data/party-pandas";

export const metadata: Metadata = {
  title: "Studio",
  description: "Live party-panda trait stack for Party Pandas.",
};

export default function PartyPandasStudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">Layered party mixer</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        {partyPandas.name} plays every trait as its own looping APNG. The preview is a live stack —
        venues, pandas, and extras keep moving instead of baking to a still.
      </p>
      <div className="mt-10">
        <PartyPandasStudio />
      </div>
    </div>
  );
}
