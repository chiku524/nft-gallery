"use client";

import { ApngImage } from "@/components/apng-image";
import {
  ceraSelectionToLayers,
  CERA_DURATION_MS,
  CERA_FRAMES,
  type CeraSelection,
} from "@/data/cera-traits";
import { cn } from "@/lib/utils";

export function CeraStack({
  selection,
  className,
  label = "Assembled Cera lava lamp",
}: {
  selection: CeraSelection;
  className?: string;
  label?: string;
}) {
  const layers = ceraSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#16121c] shadow-[0_24px_60px_rgba(217,70,166,0.22)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#16121c]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f4eef2]/90">
        {layers.length} plates · {CERA_FRAMES}f · {CERA_DURATION_MS}ms
      </p>
    </div>
  );
}
