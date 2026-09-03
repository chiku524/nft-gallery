"use client";

import { ApngImage } from "@/components/apng-image";
import {
  foxkinSelectionToLayers,
  FOXKIN_DURATION_MS,
  FOXKIN_FRAMES,
  type FoxkinSelection,
} from "@/data/foxkin-traits";
import { cn } from "@/lib/utils";

export function FoxkinStack({
  selection,
  className,
  label = "Assembled Foxkin",
}: {
  selection: FoxkinSelection;
  className?: string;
  label?: string;
}) {
  const layers = foxkinSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#f3d6c4] shadow-[0_24px_60px_rgba(20,16,14,0.22)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#3a2a22]/70 px-2.5 py-1 text-[11px] tracking-wide text-[#fff8ef]/90">
        {layers.length} layers · {FOXKIN_FRAMES}f · {FOXKIN_DURATION_MS}ms
      </p>
    </div>
  );
}
