import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, Fingerprint, ScanLine } from "lucide-react";
import { Button } from "@/components/ui/button";
import { robinBanxSamples } from "@/data/robinbanx-gallery";
import { robinBanxTraitCategories } from "@/data/robinbanx-traits";
import { robinBanx } from "@/data/robinbanx";
import { robinBanxPath } from "@/lib/robinbanx";

export default function RobinBanxHomePage() {
  const lead = robinBanxSamples[0];
  const combinationCount = robinBanxTraitCategories.reduce(
    (product, category) => product * category.traits.length,
    1,
  );

  return (
    <div className="overflow-hidden">
      <section className="relative border-b border-[#c7bda7]/20">
        <div className="absolute inset-0 bg-[radial-gradient(#3f443d_0.8px,transparent_0.8px)] bg-[length:7px_7px] opacity-30" />
        <div className="relative mx-auto grid min-h-[680px] w-full max-w-7xl items-center gap-10 px-4 py-16 sm:px-6 lg:grid-cols-[1.05fr_0.95fr]">
          <div className="relative z-10">
            <div className="mb-8 flex items-center gap-3 font-mono text-xs uppercase tracking-[0.2em] text-[#9fa596]">
              <ScanLine className="size-4 text-[#e24932]" aria-hidden="true" />
              File RBX–8453 / Access cleared
            </div>
            <h1 className="max-w-3xl text-6xl font-black uppercase leading-[0.82] tracking-[-0.07em] sm:text-8xl lg:text-[7rem]">
              Robin
              <span className="block text-[#e24932]">Banx</span>
            </h1>
            <p className="mt-7 max-w-xl border-l-4 border-[#667357] pl-5 text-lg leading-relaxed text-[#b8b9af]">
              {robinBanx.tagline} Static PNG portraits built as angular security-dossier collages.
            </p>
            <div className="mt-9 flex flex-wrap gap-3">
              <Button asChild size="lg" className="rounded-none bg-[#e24932] font-mono uppercase text-[#090a0a] hover:bg-[#f15a43]">
                <Link href={robinBanxPath("/studio")}>Open assembly desk <ArrowUpRight /></Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="rounded-none border-[#c7bda7]/35 bg-transparent font-mono uppercase text-[#eee8da] hover:bg-[#eee8da] hover:text-[#090a0a]">
                <Link href={robinBanxPath("/gallery")}>View the lineup</Link>
              </Button>
            </div>
            <dl className="mt-12 grid max-w-xl grid-cols-2 gap-px border border-[#c7bda7]/20 bg-[#c7bda7]/20 sm:grid-cols-4">
              {[
                ["Supply", robinBanx.supply.toLocaleString()],
                ["Mint", "Free"],
                ["Network", robinBanx.chain.name],
                ["Format", "PNG"],
              ].map(([label, value]) => (
                <div key={label} className="bg-[#101211] p-4">
                  <dt className="font-mono text-[10px] uppercase tracking-widest text-[#7f857a]">{label}</dt>
                  <dd className="mt-1 text-xl font-black uppercase">{value}</dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="relative mx-auto w-full max-w-xl lg:rotate-2">
            <div className="absolute -inset-4 border border-[#667357]/50" />
            <div className="relative aspect-square overflow-hidden bg-[#171918] shadow-[18px_18px_0_#667357]">
              {lead ? (
                <Image src={lead.image} alt={lead.name} fill priority sizes="(min-width: 1024px) 45vw, 90vw" className="object-cover" unoptimized />
              ) : (
                <div className="absolute inset-0 grid place-items-center bg-[linear-gradient(135deg,#1c201d_25%,#111311_25%,#111311_50%,#1c201d_50%,#1c201d_75%,#111311_75%)] bg-[length:28px_28px]">
                  <Fingerprint className="size-32 text-[#667357]" aria-hidden="true" />
                </div>
              )}
            </div>
            <span className="absolute -right-3 top-8 rotate-6 border-4 border-[#e24932] px-4 py-2 font-mono text-lg font-black uppercase tracking-[0.2em] text-[#e24932]">
              Person of interest
            </span>
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-7xl px-4 py-20 sm:px-6">
        <div className="grid gap-12 lg:grid-cols-[0.8fr_1.2fr]">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.24em] text-[#e24932]">Case summary</p>
            <h2 className="mt-3 text-4xl font-black uppercase leading-none sm:text-5xl">Identity redacted. Trail intact.</h2>
          </div>
          <div className="space-y-5 text-lg leading-relaxed text-[#aeb1a7]">
            {robinBanx.story.split("\n\n").map((paragraph) => <p key={paragraph.slice(0, 40)}>{paragraph}</p>)}
          </div>
        </div>
      </section>

      <section className="border-y border-[#c7bda7]/20 bg-[#131614]">
        <div className="mx-auto w-full max-w-7xl px-4 py-16 sm:px-6">
          <div className="flex flex-wrap items-end justify-between gap-6">
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.24em] text-[#e24932]">Evidence index</p>
              <h2 className="mt-2 text-4xl font-black uppercase">The portrait plates</h2>
            </div>
            <p className="font-mono text-sm text-[#8f9688]">{combinationCount.toLocaleString()} possible files</p>
          </div>
          <div className="mt-10 grid gap-px border border-[#c7bda7]/20 bg-[#c7bda7]/20 sm:grid-cols-2 lg:grid-cols-4">
            {robinBanxTraitCategories.map((category, index) => (
              <article key={category.id} className="relative min-h-56 bg-[#0d0f0e] p-6">
                <span className="font-mono text-xs text-[#667357]">EX-{String(index + 1).padStart(2, "0")}</span>
                <h3 className="mt-8 text-2xl font-black uppercase">{category.label}</h3>
                <p className="mt-2 text-sm text-[#92988c]">
                  {category.optional ? "Optional overlay with an explicit clear record." : "Required plate in every assembled case file."}
                </p>
                <p className="absolute bottom-5 right-5 font-mono text-xs uppercase text-[#e24932]">
                  {category.traits.length} entries
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-7xl px-4 py-20 sm:px-6">
        <div className="grid gap-8 border-2 border-[#667357] bg-[#e7e0d1] p-8 text-[#121412] shadow-[10px_10px_0_#667357] md:grid-cols-[1fr_auto] md:items-end md:p-12">
          <div>
            <p className="font-mono text-xs font-bold uppercase tracking-[0.24em] text-[#b93827]">Distribution notice</p>
            <h2 className="mt-3 max-w-3xl text-4xl font-black uppercase leading-none">Free mint. Ten per transaction. Gas remains evidence.</h2>
          </div>
          <Button asChild size="lg" className="rounded-none bg-[#121412] font-mono uppercase text-[#eee8da]">
            <Link href={robinBanxPath("/launch")}>Read launch briefing</Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
