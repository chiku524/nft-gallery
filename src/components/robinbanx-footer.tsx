import Link from "next/link";
import { robinBanx } from "@/data/robinbanx";
import { robinBanxPath } from "@/lib/robinbanx";

export function RobinBanxFooter() {
  return (
    <footer className="mt-auto border-t border-[#c7bda7]/20 bg-[#090a0a] text-[#eee8da]">
      <div className="mx-auto grid w-full max-w-7xl gap-6 px-4 py-8 sm:px-6 md:grid-cols-[1fr_auto] md:items-end">
        <div>
          <p className="font-mono font-black uppercase tracking-[0.12em]">{robinBanx.name} / {robinBanx.symbol}</p>
          <p className="mt-2 max-w-xl text-sm text-[#92988c]">
            {robinBanx.supply.toLocaleString()} static PNG dossiers · {robinBanx.chain.name} · free mint,
            collector pays ETH gas. Marketplace file pending launch.
          </p>
        </div>
        <nav className="flex flex-wrap gap-x-5 gap-y-2 font-mono text-xs uppercase tracking-wider" aria-label="Footer">
          <Link href="/" className="hover:text-[#e24932]">NFT Gallery</Link>
          <Link href={robinBanxPath("/studio")} className="hover:text-[#e24932]">Assembly</Link>
          <Link href={robinBanxPath("/traits")} className="hover:text-[#e24932]">Evidence</Link>
          <Link href={robinBanxPath("/launch")} className="hover:text-[#e24932]">Briefing</Link>
          <a href={robinBanx.chain.docs} target="_blank" rel="noreferrer" className="hover:text-[#e24932]">
            Base docs
          </a>
        </nav>
      </div>
    </footer>
  );
}
