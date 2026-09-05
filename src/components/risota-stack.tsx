"use client";

import { ApngImage } from "@/components/apng-image";
import {
  risotaSelectionToLayers,
  RISOTA_DURATION_MS,
  RISOTA_FRAMES,
  type RisotaSelection,
} from "@/data/risota-traits";
import { cn } from "@/lib/utils";

export function RisotaStack({
  selection,
  className,
  label = "Assembled Risota print",
}: {
  selection: RisotaSelection;
  className?: string;
  label?: string;
}) {
  const layers = risotaSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#f4ead4] shadow-[0_24px_60px_rgba(42,24,32,0.28)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#2a1820]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f4ead4]/90">
        {layers.length} plates · {RISOTA_FRAMES}f · {RISOTA_DURATION_MS}ms
      </p>
    </div>
  );
}
