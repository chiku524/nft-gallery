"use client";

import { ApngImage } from "@/components/apng-image";
import {
  boogieSelectionToLayers,
  BOOGIE_DURATION_MS,
  BOOGIE_FRAMES,
  type BoogieSelection,
} from "@/data/boogie-traits";
import { cn } from "@/lib/utils";

export function BoogieStack({
  selection,
  className,
  label = "Assembled Boogie Squad dancer",
}: {
  selection: BoogieSelection;
  className?: string;
  label?: string;
}) {
  const layers = boogieSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#14081f] shadow-[0_24px_60px_rgba(255,80,180,0.22)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      {layers.map((src, index) => (
        <ApngImage key={`${src}-${index}`} src={src} alt="" className="absolute inset-0 size-full object-cover" />
      ))}
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#14081f]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#fff4e8]/90">
        {layers.length} layers · {BOOGIE_FRAMES}f · {BOOGIE_DURATION_MS}ms
      </p>
    </div>
  );
}
