import Link from "next/link";
import { streetHeirs } from "@/data/street-heirs";
import { streetHeirsPath } from "@/lib/street-heirs";

export function StreetHeirsFooter() {
  return (
    <footer className="mt-auto border-t border-[#202A3D]/15 bg-[#202A3D] text-[#F4EFE5]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-5 px-4 py-8 sm:flex-row sm:items-end sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-xl">{streetHeirs.name}</p>
          <p className="mt-1 text-sm text-[#F4EFE5]/65">
            {streetHeirs.supply.toLocaleString()} static portraits · {streetHeirs.chain.name} · Pre-launch
          </p>
        </div>
        <nav className="flex flex-wrap gap-x-5 gap-y-2 text-sm" aria-label="Street Heirs footer">
          <Link href="/" className="hover:text-[#D3B36C]">NFT Gallery</Link>
          <Link href={streetHeirsPath("/studio")} className="hover:text-[#D3B36C]">Studio</Link>
          <Link href={streetHeirsPath("/gallery")} className="hover:text-[#D3B36C]">Gallery</Link>
          <Link href={streetHeirsPath("/traits")} className="hover:text-[#D3B36C]">Traits</Link>
          <Link href={streetHeirsPath("/launch")} className="hover:text-[#D3B36C]">Launch</Link>
          <a href={streetHeirs.chain.docs} target="_blank" rel="noreferrer" className="hover:text-[#D3B36C]">
            Chain docs
          </a>
        </nav>
      </div>
    </footer>
  );
}
