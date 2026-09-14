import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { streetHeirsSamples } from "@/data/street-heirs-gallery";
import { streetHeirs } from "@/data/street-heirs";
import { streetHeirsPath } from "@/lib/street-heirs";

const routes = [
  ["Studio", "Compose a compatible eight-plate portrait.", "/studio"],
  ["Gallery", "Meet 16 signature heirs from the completed bake.", "/gallery"],
  ["Traits", "Browse all 70 illustrated plates and signal positions.", "/traits"],
  ["Launch", "Review network details and pre-launch readiness.", "/launch"],
] as const;

export default function StreetHeirsHomePage() {
  return (
    <div>
      <section className="relative min-h-[520px] overflow-hidden border-b border-[#202A3D]/15">
        <Image
          src="/brand/banner-street-heirs.png"
          alt="A lineup of illustrated Street Heirs portraits"
          fill
          priority
          sizes="100vw"
          className="object-cover object-center"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-[#202A3D]/95 via-[#202A3D]/65 to-transparent" />
        <div className="relative mx-auto flex min-h-[520px] w-full max-w-6xl items-end px-4 py-12 sm:px-6">
          <div className="max-w-2xl text-[#F4EFE5]">
            <p className="text-xs font-medium uppercase tracking-[0.24em] text-[#D3B36C]">Pre-launch collection · {streetHeirs.symbol}</p>
            <h1 className="mt-3 font-heading text-5xl leading-none sm:text-7xl">{streetHeirs.name}</h1>
            <p className="mt-4 max-w-xl text-lg text-[#F4EFE5]/85">{streetHeirs.tagline}</p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Button asChild size="lg" className="bg-[#D3B36C] text-[#202A3D] hover:bg-[#D3B36C]/85">
                <Link href={streetHeirsPath("/studio")}>Open Studio <ArrowRight data-icon="inline-end" /></Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-[#F4EFE5]/40 bg-transparent text-[#F4EFE5] hover:bg-[#F4EFE5]/10">
                <Link href={streetHeirsPath("/gallery")}>View the gallery</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-[1fr_1.15fr]">
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-[#496A9A]">The collection</p>
          <h2 className="mt-2 font-heading text-4xl">Portraits of inheritance in motion.</h2>
          <div className="mt-5 space-y-4 text-[#202A3D]/70">
            {streetHeirs.story.split("\n\n").map((paragraph) => <p key={paragraph.slice(0, 42)}>{paragraph}</p>)}
          </div>
        </div>
        <div>
          <dl className="grid grid-cols-2 gap-3">
            {[
              ["Supply", streetHeirs.supply.toLocaleString()],
              ["Mint price", `${streetHeirs.mintPriceEth} ETH`],
              ["Network", streetHeirs.chain.name],
              ["Artwork", streetHeirs.format],
            ].map(([label, value]) => (
              <div key={label} className="rounded-2xl border border-[#202A3D]/15 bg-white/50 p-5">
                <dt className="text-xs uppercase tracking-[0.16em] text-[#496A9A]">{label}</dt>
                <dd className="mt-1 font-heading text-2xl">{value}</dd>
              </div>
            ))}
          </dl>
          <div className="mt-4 grid grid-cols-4 gap-2">
            {streetHeirsSamples.slice(0, 4).map((sample) => (
              <Image key={sample.id} src={sample.image} alt={sample.name} width={512} height={512} unoptimized className="aspect-square rounded-xl object-cover" />
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-[#202A3D]/15 bg-[#B6C3A3]/25">
        <div className="mx-auto grid w-full max-w-6xl gap-4 px-4 py-14 sm:grid-cols-2 sm:px-6 lg:grid-cols-4">
          {routes.map(([title, body, href]) => (
            <Link key={title} href={streetHeirsPath(href)} className="group rounded-2xl border border-[#202A3D]/15 bg-[#F4EFE5] p-5 transition hover:-translate-y-1 hover:border-[#D3B36C]">
              <h2 className="font-heading text-2xl">{title}</h2>
              <p className="mt-2 text-sm text-[#202A3D]/65">{body}</p>
              <span className="mt-6 inline-flex text-sm font-medium text-[#496A9A] group-hover:text-[#202A3D]">Explore →</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
