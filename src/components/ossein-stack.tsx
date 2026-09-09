"use client";

import { ApngImage } from "@/components/apng-image";
import {
  osseinSelectionToLayers,
  OSSN_DURATION_MS,
  OSSN_FRAMES,
  type OsseinSelection,
} from "@/data/ossein-traits";
import { cn } from "@/lib/utils";

export function OsseinStack({
  selection,
  className,
  label = "Assembled Ossein chart",
}: {
  selection: OsseinSelection;
  className?: string;
  label?: string;
}) {
  const layers = osseinSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1c1814] shadow-[0_24px_60px_rgba(26,18,8,0.35)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      {layers.map((src, index) => (
        <ApngImage key={`${src}-${index}`} src={src} alt="" className="absolute inset-0 size-full object-cover" />
      ))}
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1c1814]/80 px-2.5 py-1 text-[11px] tracking-wide text-white/90">
        {layers.length} plates · {OSSN_FRAMES}f · {OSSN_DURATION_MS}ms
      </p>
    </div>
  );
}
