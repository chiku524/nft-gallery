import { cn } from "@/lib/utils";

/**
 * APNG must skip next/image optimization — the optimizer flattens animation
 * to the first frame. A plain img keeps every loop intact.
 */
export function ApngImage({
  src,
  alt,
  className,
  width,
  height,
}: {
  src: string;
  alt: string;
  className?: string;
  width?: number;
  height?: number;
}) {
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img src={src} alt={alt} width={width} height={height} className={cn(className)} draggable={false} />
  );
}
