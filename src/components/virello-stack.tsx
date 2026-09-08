"use client";

import { ApngImage } from "@/components/apng-image";
import {
  virelloSelectionToLayers,
  VIRELLO_DURATION_MS,
  VIRELLO_FRAMES,
  type VirelloSelection,
} from "@/data/virello-traits";
import { cn } from "@/lib/utils";

export function VirelloStack({
  selection,
  className,
  label = "Assembled Virello toy",
}: {
  selection: VirelloSelection;
  className?: string;
  label?: string;
}) {
  const layers = virelloSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#f3ead4] shadow-[0_24px_60px_rgba(196,60,44,0.18)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#2a1f18]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f3ead4]/90">
        {layers.length} plates · {VIRELLO_FRAMES}f · {VIRELLO_DURATION_MS}ms
      </p>
    </div>
  );
}
