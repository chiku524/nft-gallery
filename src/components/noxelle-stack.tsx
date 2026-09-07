"use client";

import { ApngImage } from "@/components/apng-image";
import {
  noxelleSelectionToLayers,
  NOXELLE_DURATION_MS,
  NOXELLE_FRAMES,
  type NoxelleSelection,
} from "@/data/noxelle-traits";
import { cn } from "@/lib/utils";

export function NoxelleStack({
  selection,
  className,
  label = "Assembled Noxelle sign",
}: {
  selection: NoxelleSelection;
  className?: string;
  label?: string;
}) {
  const layers = noxelleSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#12081c] shadow-[0_24px_60px_rgba(18,8,28,0.45)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#12081c]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f4e8ff]/90">
        {layers.length} plates · {NOXELLE_FRAMES}f · {NOXELLE_DURATION_MS}ms
      </p>
    </div>
  );
}
