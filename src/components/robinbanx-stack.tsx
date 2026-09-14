"use client";

import Image from "next/image";
import {
  robinBanxSelectionToLayers,
  type RobinBanxSelection,
} from "@/data/robinbanx-traits";
import { cn } from "@/lib/utils";

export function RobinBanxStack({
  selection,
  className,
  label = "Assembled Robin Banx masked portrait",
}: {
  selection: RobinBanxSelection;
  className?: string;
  label?: string;
}) {
  const layers = robinBanxSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden bg-[#171918] shadow-[14px_14px_0_#59634c,24px_24px_0_rgba(0,0,0,0.32)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      <div className="absolute inset-0 bg-[radial-gradient(#5d6258_0.7px,transparent_0.8px)] bg-[length:5px_5px] opacity-30" />
      {layers.map((src, index) => (
        <Image
          key={`${src}-${index}`}
          src={src}
          alt=""
          fill
          sizes="(min-width: 1024px) 52vw, 100vw"
          className="object-cover"
          unoptimized
        />
      ))}
      <span className="pointer-events-none absolute right-3 top-3 -rotate-3 border-2 border-[#e24932] px-2 py-1 font-mono text-[10px] font-black uppercase tracking-[0.18em] text-[#e24932]">
        Evidence / {layers.length} plates
      </span>
    </div>
  );
}
