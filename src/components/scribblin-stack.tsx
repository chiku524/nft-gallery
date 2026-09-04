"use client";

import { ApngImage } from "@/components/apng-image";
import {
  scribblinSelectionToLayers,
  SCRIBBLIN_DURATION_MS,
  SCRIBBLIN_FRAMES,
  type ScribblinSelection,
} from "@/data/scribblin-traits";
import { cn } from "@/lib/utils";

export function ScribblinStack({
  selection,
  className,
  label = "Assembled Scribblin",
}: {
  selection: ScribblinSelection;
  className?: string;
  label?: string;
}) {
  const layers = scribblinSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#f4e8d2] shadow-[0_24px_60px_rgba(36,28,24,0.22)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#3a342c]/70 px-2.5 py-1 text-[11px] tracking-wide text-[#fff6e8]/90">
        {layers.length} layers · {SCRIBBLIN_FRAMES}f · {SCRIBBLIN_DURATION_MS}ms
      </p>
    </div>
  );
}
