"use client";

import { ApngImage } from "@/components/apng-image";
import {
  shookumSelectionToLayers,
  SHOOKUM_DURATION_MS,
  SHOOKUM_FRAMES,
  type ShookumSelection,
} from "@/data/shookum-traits";
import { cn } from "@/lib/utils";

export function ShookumStack({
  selection,
  className,
  label = "Assembled Shook'um",
}: {
  selection: ShookumSelection;
  className?: string;
  label?: string;
}) {
  const layers = shookumSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#f4ebe0] shadow-[0_24px_60px_rgba(28,24,48,0.28)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1c1830]/70 px-2.5 py-1 text-[11px] tracking-wide text-[#fff8ef]/90">
        {layers.length} layers · {SHOOKUM_FRAMES}f · {SHOOKUM_DURATION_MS}ms
      </p>
    </div>
  );
}
