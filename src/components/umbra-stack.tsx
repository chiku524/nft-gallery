"use client";

import { ApngImage } from "@/components/apng-image";
import {
  umbraSelectionToLayers,
  UMBRA_DURATION_MS,
  UMBRA_FRAMES,
  type UmbraSelection,
} from "@/data/umbra-traits";
import { cn } from "@/lib/utils";

export function UmbraStack({
  selection,
  className,
  label = "Assembled Umbra shade",
}: {
  selection: UmbraSelection;
  className?: string;
  label?: string;
}) {
  const layers = umbraSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1a1208] shadow-[0_24px_60px_rgba(26,18,8,0.35)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1a1208]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f3e6c8]/90">
        {layers.length} plates · {UMBRA_FRAMES}f · {UMBRA_DURATION_MS}ms
      </p>
    </div>
  );
}
