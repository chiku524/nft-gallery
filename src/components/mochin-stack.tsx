"use client";

import { ApngImage } from "@/components/apng-image";
import {
  mochinSelectionToLayers,
  MOCHIN_DURATION_MS,
  MOCHIN_FRAMES,
  type MochinSelection,
} from "@/data/mochin-traits";
import { cn } from "@/lib/utils";

export function MochinStack({
  selection,
  className,
  label = "Assembled Mochin",
}: {
  selection: MochinSelection;
  className?: string;
  label?: string;
}) {
  const layers = mochinSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1a1410] shadow-[0_24px_60px_rgba(26,20,16,0.45)]",
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
        {layers.length} layers · {MOCHIN_FRAMES}f · {MOCHIN_DURATION_MS}ms
      </p>
    </div>
  );
}
