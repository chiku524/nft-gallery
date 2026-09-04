"use client";

import { ApngImage } from "@/components/apng-image";
import {
  groovySelectionToLayers,
  GROOVY_DURATION_MS,
  GROOVY_FRAMES,
  type GroovySelection,
} from "@/data/groovy-traits";
import { cn } from "@/lib/utils";

export function GroovyStack({
  selection,
  className,
  label = "Assembled Groovy Nation citizen",
}: {
  selection: GroovySelection;
  className?: string;
  label?: string;
}) {
  const layers = groovySelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#1a0610] shadow-[0_24px_60px_rgba(242,90,160,0.28)]",
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
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#2a0818]/75 px-2.5 py-1 text-[11px] tracking-wide text-[#ffe8a8]/90">
        {layers.length} layers · {GROOVY_FRAMES}f · {GROOVY_DURATION_MS}ms
      </p>
    </div>
  );
}
