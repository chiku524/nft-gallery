"use client";

import { ApngImage } from "@/components/apng-image";
import { selectionToLayers, TRAIT_DURATION_MS, TRAIT_FRAMES, type Selection } from "@/data/traits";
import { cn } from "@/lib/utils";

export function ApngStack({
  selection,
  className,
  label = "Assembled Loopkin",
}: {
  selection: Selection;
  className?: string;
  label?: string;
}) {
  const layers = selectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#070816] shadow-[0_24px_60px_rgba(8,10,28,0.45)]",
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
        {layers.length} APNG layers · {TRAIT_FRAMES}f · {TRAIT_DURATION_MS}ms
      </p>
    </div>
  );
}
