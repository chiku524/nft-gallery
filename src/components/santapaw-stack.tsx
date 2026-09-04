"use client";

import { ApngImage } from "@/components/apng-image";
import {
  santapawSelectionToLayers,
  SANTAPAW_DURATION_MS,
  SANTAPAW_FRAMES,
  type SantaPawSelection,
} from "@/data/santapaw-traits";
import { cn } from "@/lib/utils";

export function SantaPawStack({
  selection,
  className,
  label = "Assembled Santa Paw",
}: {
  selection: SantaPawSelection;
  className?: string;
  label?: string;
}) {
  const layers = santapawSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#12203a] shadow-[0_24px_60px_rgba(18,32,58,0.45)]",
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
        {layers.length} layers · {SANTAPAW_FRAMES}f · {SANTAPAW_DURATION_MS}ms
      </p>
    </div>
  );
}
