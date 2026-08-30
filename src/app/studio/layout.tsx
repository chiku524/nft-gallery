import type { Metadata } from "next";
import Link from "next/link";
import { GalleryFooter } from "@/components/gallery-footer";
import { gallery } from "@/data/projects";

export const metadata: Metadata = {
  title: {
    default: "Studio",
    template: `%s · ${gallery.name}`,
  },
  description: gallery.description,
};

export default function StudioLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <header className="sticky top-0 z-40 border-b border-border/80 bg-[color-mix(in_oklch,var(--background)_88%,white)]/90 backdrop-blur-md">
        <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4 sm:px-6">
          <Link href="/" className="font-heading text-lg tracking-tight">
            {gallery.name}
          </Link>
          <p className="text-sm text-muted-foreground">Trait studio</p>
        </div>
      </header>
      <div className="flex-1">{children}</div>
      <GalleryFooter />
    </>
  );
}
