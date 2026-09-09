"use client";

import { ApngImage } from "@/components/apng-image";
import {
  feltroSelectionToLayers,
  FLTR_DURATION_MS,
  FLTR_FRAMES,
  type FeltroSelection,
} from "@/data/feltro-traits";
import { cn } from "@/lib/utils";

export function FeltroStack({
  selection,
  className,
  label = "Assembled Feltro suit",
}: {
  selection: FeltroSelection;
  className?: string;
  label?: string;
}) {
  const layers = feltroSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#241816] shadow-[0_24px_60px_rgba(26,18,8,0.35)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      {layers.map((src, index) => (
        <ApngImage key={`${src}-${index}`} src={src} alt="" className="absolute inset-0 size-full object-cover" />
      ))}
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#241816]/80 px-2.5 py-1 text-[11px] tracking-wide text-white/90">
        {layers.length} plates · {FLTR_FRAMES}f · {FLTR_DURATION_MS}ms
      </p>
    </div>
  );
}
