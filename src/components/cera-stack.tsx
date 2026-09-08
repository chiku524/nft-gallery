"use client";

import { ApngImage } from "@/components/apng-image";
import {
  ceraFlaskMaskSrc,
  ceraSelectionToLayers,
  CERA_DURATION_MS,
  CERA_FRAMES,
  type CeraSelection,
} from "@/data/cera-traits";
import { cn } from "@/lib/utils";

const LIQUID_LAYERS = new Set(["serum", "melt", "coil"]);

export function CeraStack({
  selection,
  className,
  label = "Assembled Cera lava lamp",
}: {
  selection: CeraSelection;
  className?: string;
  label?: string;
}) {
  const layers = ceraSelectionToLayers(selection);
  const flaskMask = ceraFlaskMaskSrc(selection.flask);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[1.75rem] bg-[#16121c] shadow-[0_24px_60px_rgba(217,70,166,0.22)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      {layers.map((layer, index) => {
        const image = (
          <ApngImage
            src={layer.src}
            alt=""
            className="absolute inset-0 size-full object-cover"
          />
        );
        if (!LIQUID_LAYERS.has(layer.id)) {
          return (
            <div key={`${layer.src}-${index}`} className="absolute inset-0 size-full">
              {image}
            </div>
          );
        }
        return (
          <div
            key={`${layer.src}-${index}`}
            className="absolute inset-0 size-full"
            style={{
              maskImage: `url(${flaskMask})`,
              WebkitMaskImage: `url(${flaskMask})`,
              maskSize: "100% 100%",
              WebkitMaskSize: "100% 100%",
              maskRepeat: "no-repeat",
              WebkitMaskRepeat: "no-repeat",
            }}
          >
            {image}
          </div>
        );
      })}
      <p className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#16121c]/80 px-2.5 py-1 text-[11px] tracking-wide text-[#f4eef2]/90">
        {layers.length} plates · {CERA_FRAMES}f · {CERA_DURATION_MS}ms
      </p>
    </div>
  );
}
