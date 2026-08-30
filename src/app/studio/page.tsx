import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Studio",
  description: "Empty trait studio for the next NFT Gallery collection.",
};

export default function StudioPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Studio</p>
      <h1 className="mt-2 font-heading text-4xl">No collection loaded.</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        This mixer is empty on purpose. When you have the next drop, trait layers and
        the stack preview land here.
      </p>

      <div className="mt-10 grid gap-8 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
        <div className="aspect-square w-full rounded-[1.75rem] border border-dashed bg-[repeating-conic-gradient(#efe4d4_0%_25%,#f7f0e6_0%_50%)] bg-[length:18px_18px] shadow-[0_24px_60px_rgba(40,22,12,0.12)]" />

        <div className="flex min-w-0 flex-col justify-center gap-3 rounded-[1.75rem] border bg-card p-6">
          <p className="font-heading text-2xl">Waiting on a new idea.</p>
          <p className="text-sm text-muted-foreground">
            Pugs On The Block is no longer in this studio. Start the next collection
            from a blank stack.
          </p>
        </div>
      </div>
    </div>
  );
}
