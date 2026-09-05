"use client";

import { ApngImage } from "@/components/apng-image";
import {
  perfinSelectionToLayers,
  PERFIN_DURATION_MS,
  PERFIN_FRAMES,
  type PerfinSelection,
} from "@/data/perfin-traits";
import { cn } from "@/lib/utils";

export function PerfinStack({
  selection,
  className,
  label = "Assembled Perfin frank",
}: {
  selection: PerfinSelection;
  className?: string;
  label?: string;
}) {
  const layers = perfinSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1b365d] shadow-[0_24px_60px_rgba(27,54,93,0.35)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1b365d]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f3ede0]/90">
        {layers.length} plates · {PERFIN_FRAMES}f · {PERFIN_DURATION_MS}ms
      </p>
    </div>
  );
}
