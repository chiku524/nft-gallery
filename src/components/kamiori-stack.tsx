"use client";

import { ApngImage } from "@/components/apng-image";
import {
  kamioriSelectionToLayers,
  KAMIORI_DURATION_MS,
  KAMIORI_FRAMES,
  type KamioriSelection,
} from "@/data/kamiori-traits";
import { cn } from "@/lib/utils";

export function KamioriStack({
  selection,
  className,
  label = "Assembled Kamiori sheet",
}: {
  selection: KamioriSelection;
  className?: string;
  label?: string;
}) {
  const layers = kamioriSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1a1814] shadow-[0_24px_60px_rgba(26,24,20,0.35)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      {layers.map((src, index) => (
        <ApngImage
          key={`${src}-${index}`}
          src={src}
          alt=""
          className="absolute inset-0 size-full object-cover"
        />
      ))}
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1a1814]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f6f0e4]/90">
        {layers.length} plates · {KAMIORI_FRAMES}f · {KAMIORI_DURATION_MS}ms
      </p>
    </div>
  );
}
