"use client";

import { ApngImage } from "@/components/apng-image";
import {
  opalineSelectionToLayers,
  OPALINE_DURATION_MS,
  OPALINE_FRAMES,
  type OpalineSelection,
} from "@/data/opaline-traits";
import { cn } from "@/lib/utils";

export function OpalineStack({
  selection,
  className,
  label = "Assembled Opaline portrait",
}: {
  selection: OpalineSelection;
  className?: string;
  label?: string;
}) {
  const layers = opalineSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#0c0d12] shadow-[0_24px_60px_rgba(12,13,18,0.55)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#0c0d12]/75 px-2.5 py-1 text-[11px] tracking-wide text-[#c6c2b8]/90">
        {layers.length} layers · {OPALINE_FRAMES}f · {OPALINE_DURATION_MS}ms
      </p>
    </div>
  );
}
