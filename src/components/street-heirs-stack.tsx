import Image from "next/image";
import {
  streetHeirsSelectionToLayers,
  type StreetHeirsSelection,
} from "@/data/street-heirs-traits";
import { cn } from "@/lib/utils";

export function StreetHeirsStack({
  selection,
  className,
  label = "Assembled Street Heirs portrait",
}: {
  selection: StreetHeirsSelection;
  className?: string;
  label?: string;
}) {
  const layers = streetHeirsSelectionToLayers(selection);

  return (
    <div
      className={cn(
        "relative aspect-square overflow-hidden rounded-[2rem] border border-[#D3B36C]/50 bg-[#202A3D] shadow-[0_24px_70px_rgba(32,42,61,0.2)]",
        className,
      )}
      role="img"
      aria-label={label}
    >
      {layers.map((src, index) => (
        <Image
          key={`${src}-${index}`}
          src={src}
          alt=""
          fill
          sizes="(max-width: 1024px) 100vw, 52vw"
          unoptimized
          className="absolute inset-0 object-cover"
        />
      ))}
      <span className="pointer-events-none absolute bottom-3 left-3 rounded-full bg-[#F4EFE5]/90 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.14em] text-[#202A3D]">
        {layers.length} plates · live stack
      </span>
    </div>
  );
}
