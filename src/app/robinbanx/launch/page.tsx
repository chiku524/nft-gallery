import type { Metadata } from "next";
import { AddChainButton } from "@/components/add-chain-button";
import { robinBanx } from "@/data/robinbanx";

export const metadata: Metadata = {
  title: "Launch briefing",
  description: "Deployment and marketplace checklist for the Robin Banx free mint on Base.",
};

const steps = [
  {
    code: "01 / BAKE",
    title: "Flatten every case file",
    body: "Export each approved transparent plate stack as one 512×512 static PNG. Keep token IDs, filenames, metadata records, and the generated gallery catalog in the same sequential order.",
  },
  {
    code: "02 / PIN",
    title: "Publish immutable evidence",
    body: "Pin the complete image and JSON directories. Confirm every JSON image URI resolves, uses the Robin Banx name, and includes the final trait attributes before setting the contract base URI.",
  },
  {
    code: "03 / DEPLOY",
    title: "Deploy and verify on Base",
    body: `Deploy contracts/RobinBanx.sol on Base (chain ID ${robinBanx.chain.chainId}), verify the source, set the pinned base URI, test a free mint, then open public minting. Mint price is zero; users still pay ETH gas.`,
  },
  {
    code: "04 / LIST",
    title: "Create the marketplace record",
    body: "Only after deployment, import the verified contract into OpenSea and add the resulting live collection URL to the site. No marketplace link is published before that record exists.",
  },
];

export default function RobinBanxLaunchPage() {
  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-12 sm:px-6">
      <div className="border-b border-[#c7bda7]/20 pb-10">
        <p className="font-mono text-xs uppercase tracking-[0.24em] text-[#e24932]">Operational briefing / pre-launch</p>
        <h1 className="mt-3 text-5xl font-black uppercase leading-none sm:text-7xl">Release protocol</h1>
        <p className="mt-5 max-w-2xl text-[#aeb1a7]">
          Robin Banx is planned as a free mint on Base. There is no live OpenSea collection URL yet; marketplace
          links remain intentionally absent until the verified contract is imported.
        </p>
      </div>

      <dl className="mt-10 grid gap-px border border-[#c7bda7]/20 bg-[#c7bda7]/20 sm:grid-cols-2 lg:grid-cols-4">
        {[
          ["Network", robinBanx.chain.name],
          ["Chain ID", String(robinBanx.chain.chainId)],
          ["Supply", robinBanx.supply.toLocaleString()],
          ["Mint", "0 ETH + gas"],
        ].map(([label, value]) => (
          <div key={label} className="bg-[#121412] p-5">
            <dt className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#7d8577]">{label}</dt>
            <dd className="mt-2 text-xl font-black uppercase">{value}</dd>
          </div>
        ))}
      </dl>

      <section className="mt-12 grid gap-8 border border-[#667357] bg-[#141715] p-6 md:grid-cols-[1fr_auto] md:items-center sm:p-8">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#e24932]">Wallet network record</p>
          <h2 className="mt-2 text-2xl font-black uppercase">Base mainnet / ETH gas</h2>
          <p className="mt-2 break-all text-sm text-[#92988c]">
            RPC {robinBanx.chain.rpcUrl}<br />Explorer {robinBanx.chain.explorer}
          </p>
        </div>
        <AddChainButton chain={robinBanx.chain} />
      </section>

      <ol className="mt-14 space-y-4">
        {steps.map((step) => (
          <li key={step.code} className="grid gap-5 border-l-4 border-[#667357] bg-[#111312] p-6 sm:grid-cols-[8rem_1fr] sm:p-8">
            <span className="font-mono text-xs font-black uppercase tracking-[0.16em] text-[#e24932]">{step.code}</span>
            <div>
              <h2 className="text-2xl font-black uppercase">{step.title}</h2>
              <p className="mt-2 leading-relaxed text-[#a2a79c]">{step.body}</p>
            </div>
          </li>
        ))}
      </ol>

      <section className="mt-12 border-2 border-[#e24932] p-6 sm:p-8">
        <p className="font-mono text-xs font-black uppercase tracking-[0.2em] text-[#e24932]">Marketplace status</p>
        <h2 className="mt-2 text-3xl font-black uppercase">{robinBanx.marketplace.status}</h2>
        <p className="mt-3 text-[#aeb1a7]">
          Follow OpenSea&apos;s{" "}
          <a href={robinBanx.marketplace.metadataGuide} target="_blank" rel="noreferrer" className="underline decoration-[#e24932] underline-offset-4">
            metadata preparation guide
          </a>
          , then add a real collection URL only after launch.
        </p>
      </section>
    </div>
  );
}
