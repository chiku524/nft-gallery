"use client";

import { ApngImage } from "@/components/apng-image";
import {
  nivoraSelectionToLayers,
  NIVORA_DURATION_MS,
  NIVORA_FRAMES,
  type NivoraSelection,
} from "@/data/nivora-traits";
import { cn } from "@/lib/utils";

export function NivoraStack({
  selection,
  className,
  label = "Assembled Nivora globe",
}: {
  selection: NivoraSelection;
  className?: string;
  label?: string;
}) {
  const layers = nivoraSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1c1610] shadow-[0_24px_60px_rgba(28,22,16,0.45)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#1c1610]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#e8eef2]/90">
        {layers.length} plates · {NIVORA_FRAMES}f · {NIVORA_DURATION_MS}ms
      </p>
    </div>
  );
}
