"use client";

import { ApngImage } from "@/components/apng-image";
import {
  wicklingSelectionToLayers,
  WICKLING_DURATION_MS,
  WICKLING_FRAMES,
  type WicklingSelection,
} from "@/data/wickling-traits";
import { cn } from "@/lib/utils";

export function WicklingStack({
  selection,
  className,
  label = "Assembled Wickling",
}: {
  selection: WicklingSelection;
  className?: string;
  label?: string;
}) {
  const layers = wicklingSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#0b1024] shadow-[0_24px_60px_rgba(11,16,36,0.45)]",
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
        {layers.length} layers · {WICKLING_FRAMES}f · {WICKLING_DURATION_MS}ms
      </p>
    </div>
  );
}
