"use client";

import { ApngImage } from "@/components/apng-image";
import {
  purrkinSelectionToLayers,
  PURRKIN_DURATION_MS,
  PURRKIN_FRAMES,
  type PurrkinSelection,
} from "@/data/purrkin-traits";
import { cn } from "@/lib/utils";

export function PurrkinStack({
  selection,
  className,
  label = "Assembled Purrkin",
}: {
  selection: PurrkinSelection;
  className?: string;
  label?: string;
}) {
  const layers = purrkinSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#0d221e] shadow-[0_24px_60px_rgba(13,34,30,0.45)]",
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
        {layers.length} layers · {PURRKIN_FRAMES}f · {PURRKIN_DURATION_MS}ms
      </p>
    </div>
  );
}
