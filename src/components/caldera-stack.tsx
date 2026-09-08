"use client";

import { ApngImage } from "@/components/apng-image";
import {
  calderaSelectionToLayers,
  CALDERA_DURATION_MS,
  CALDERA_FRAMES,
  type CalderaSelection,
} from "@/data/caldera-traits";
import { cn } from "@/lib/utils";

export function CalderaStack({
  selection,
  className,
  label = "Assembled Caldera matchbook",
}: {
  selection: CalderaSelection;
  className?: string;
  label?: string;
}) {
  const layers = calderaSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#f4efe6] shadow-[0_24px_60px_rgba(232,93,4,0.18)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1c1612]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f4efe6]/90">
        {layers.length} plates · {CALDERA_FRAMES}f · {CALDERA_DURATION_MS}ms
      </p>
    </div>
  );
}
