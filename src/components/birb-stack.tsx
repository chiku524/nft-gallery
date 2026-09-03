"use client";

import { ApngImage } from "@/components/apng-image";
import {
  birbSelectionToLayers,
  BIRB_DURATION_MS,
  BIRB_FRAMES,
  type BirbSelection,
} from "@/data/birb-traits";
import { cn } from "@/lib/utils";

export function BirbStack({
  selection,
  className,
  label = "Assembled Birb",
}: {
  selection: BirbSelection;
  className?: string;
  label?: string;
}) {
  const layers = birbSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#f7f4ef] shadow-[0_24px_60px_rgba(74,52,40,0.22)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#4a3428]/70 px-2.5 py-1 text-[11px] tracking-wide text-[#fff8ef]/90">
        {layers.length} layers · {BIRB_FRAMES}f · {BIRB_DURATION_MS}ms
      </p>
    </div>
  );
}
