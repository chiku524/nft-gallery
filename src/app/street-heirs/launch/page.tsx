import type { Metadata } from "next";
import Image from "next/image";
import { AddChainButton } from "@/components/add-chain-button";
import { streetHeirs } from "@/data/street-heirs";

export const metadata: Metadata = {
  title: "Launch status",
  description: "Street Heirs pre-launch status and verified Robinhood Chain connection details.",
};

export default function StreetHeirsLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-12 sm:px-6">
      <p className="text-xs uppercase tracking-[0.22em] text-[#496A9A]">Pre-launch status</p>
      <h1 className="mt-2 max-w-3xl font-heading text-4xl sm:text-5xl">The art is baked. The contract is not live.</h1>
      <p className="mt-4 max-w-2xl text-[#202A3D]/70">
        All {streetHeirs.supply.toLocaleString()} static PNGs and their metadata have been completed. The contract address, creator wallet, launch date, and OpenSea URL are still unset. Minting is not live.
      </p>

      <div className="mt-10 grid gap-6 md:grid-cols-[1.15fr_0.85fr]">
        <div className="rounded-[2rem] bg-[#202A3D] p-6 text-[#F4EFE5] sm:p-8">
          <p className="text-xs uppercase tracking-[0.2em] text-[#D3B36C]">Verified network</p>
          <h2 className="mt-2 font-heading text-3xl">{streetHeirs.chain.name}</h2>
          <dl className="mt-6 space-y-3 text-sm">
            {[
              ["Chain ID", `${streetHeirs.chain.chainId} (${streetHeirs.chain.chainIdHex})`],
              ["Currency", streetHeirs.chain.currency],
              ["RPC", streetHeirs.chain.rpcUrl],
              ["Explorer", streetHeirs.chain.explorer],
            ].map(([label, value]) => (
              <div key={label} className="border-t border-[#F4EFE5]/15 pt-3">
                <dt className="text-[#F4EFE5]/55">{label}</dt>
                <dd className="mt-1 break-all">{value}</dd>
              </div>
            ))}
          </dl>
          <div className="mt-6 [&_button]:bg-[#D3B36C] [&_button]:text-[#202A3D]">
            <AddChainButton chain={streetHeirs.chain} />
          </div>
          <a href={streetHeirs.chain.docs} target="_blank" rel="noreferrer" className="mt-4 inline-block text-sm text-[#D3B36C] underline">
            Robinhood Chain connection docs
          </a>
        </div>
        <Image
          src="/brand/featured-street-heirs.jpg"
          alt="Featured Street Heirs collection artwork"
          width={1200}
          height={800}
          priority
          sizes="(max-width: 768px) 100vw, 36vw"
          className="h-full min-h-72 rounded-[2rem] object-cover"
        />
      </div>

      <section className="mt-10 rounded-[2rem] border border-[#202A3D]/15 bg-white/55 p-6 sm:p-8">
        <p className="text-xs uppercase tracking-[0.2em] text-[#496A9A]">Release gate</p>
        <h2 className="mt-2 font-heading text-3xl">What remains</h2>
        <ol className="mt-6 grid gap-4 sm:grid-cols-3">
          {[
            ["01", "Deploy and verify the collection contract on Robinhood Chain."],
            ["02", "Publish the marketplace collection and confirm its official URL."],
            ["03", "Connect the mint surface only after contract and sale details are verified."],
          ].map(([number, copy]) => (
            <li key={number} className="rounded-2xl border border-[#202A3D]/10 p-4">
              <span className="font-heading text-2xl text-[#D3B36C]">{number}</span>
              <p className="mt-3 text-sm text-[#202A3D]/70">{copy}</p>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
