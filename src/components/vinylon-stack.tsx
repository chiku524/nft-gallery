"use client";

import { ApngImage } from "@/components/apng-image";
import {
  vinylonSelectionToLayers,
  VNYL_DURATION_MS,
  VNYL_FRAMES,
  type VinylonSelection,
} from "@/data/vinylon-traits";
import { cn } from "@/lib/utils";

export function VinylonStack({
  selection,
  className,
  label = "Assembled Vinylon twist",
}: {
  selection: VinylonSelection;
  className?: string;
  label?: string;
}) {
  const layers = vinylonSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1a1420] shadow-[0_24px_60px_rgba(26,18,8,0.35)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      {layers.map((src, index) => (
        <ApngImage key={`${src}-${index}`} src={src} alt="" className="absolute inset-0 size-full object-cover" />
      ))}
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1a1420]/80 px-2.5 py-1 text-[11px] tracking-wide text-white/90">
        {layers.length} plates · {VNYL_FRAMES}f · {VNYL_DURATION_MS}ms
      </p>
    </div>
  );
}
