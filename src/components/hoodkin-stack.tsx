"use client";

import { ApngImage } from "@/components/apng-image";
import {
  hoodkinSelectionToLayers,
  HOODKIN_DURATION_MS,
  HOODKIN_FRAMES,
  type HoodkinSelection,
} from "@/data/hoodkin-traits";
import { cn } from "@/lib/utils";

export function HoodkinStack({
  selection,
  className,
  label = "Assembled Hoodkin",
}: {
  selection: HoodkinSelection;
  className?: string;
  label?: string;
}) {
  const layers = hoodkinSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#081610] shadow-[0_24px_60px_rgba(8,22,16,0.45)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-black/45 px-2.5 py-1 text-[11px] tracking-wide text-white/80">
        {layers.length} layers · {HOODKIN_FRAMES}f · {HOODKIN_DURATION_MS}ms
      </p>
    </div>
  );
}
