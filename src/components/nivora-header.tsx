"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { nivora } from "@/data/nivora";
import { nivoraPath } from "@/lib/nivora";
import { openSeaListings } from "@/lib/opensea";
import { cn } from "@/lib/utils";

const links: { href: string; label: string; external?: boolean }[] = [
  { href: nivoraPath(), label: "Drop" },
  { href: nivoraPath("/traits"), label: "Traits" },
  { href: nivoraPath("/gallery"), label: "Gallery" },
  { href: nivoraPath("/launch"), label: "Launch" },
  ...openSeaListings(nivora.opensea).map((listing) => ({
    href: listing.href,
    label: `OpenSea · ${listing.label}`,
    external: true,
  })),
];

export function NivoraHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-[#c9a25a]/20 bg-[color-mix(in_oklch,var(--background)_78%,#1c1610)]/92 backdrop-blur-md">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href={nivoraPath()} className="flex items-center gap-3">
          <ApngImage
            src="/brand/logo-nivora.png"
            alt=""
            width={40}
            height={40}
            className="size-10 rounded-[0.7rem] border border-[#c9a25a]/40 object-cover"
          />
          <div className="leading-tight">
            <p className="font-heading text-lg tracking-tight">{nivora.name}</p>
            <p className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
              Snow-globe PFPs
            </p>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map((link) => {
            const className = cn(
              "rounded-full px-3 py-1.5 text-sm transition-colors",
              !link.external && pathname === link.href
                ? "bg-[#c9a25a] text-[#1c1610]"
                : "text-muted-foreground hover:bg-secondary hover:text-foreground",
            );
            return link.external ? (
              <a key={link.href} href={link.href} target="_blank" rel="noreferrer" className={className}>
                {link.label}
              </a>
            ) : (
              <Link key={link.href} href={link.href} className={className}>
                {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <Button asChild size="sm" className="hidden bg-[#c9a25a] text-[#1c1610] hover:bg-[#c9a25a]/90 sm:inline-flex">
            <Link href={nivoraPath("/studio")}>Studio</Link>
          </Button>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="md:hidden" aria-label="Open menu">
                <Menu />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-72">
              <SheetHeader>
                <SheetTitle>{nivora.name}</SheetTitle>
              </SheetHeader>
              <div className="mt-6 flex flex-col gap-2 px-4">
                {links.map((link) =>
                  link.external ? (
                    <a
                      key={link.href}
                      href={link.href}
                      target="_blank"
                      rel="noreferrer"
                      className="rounded-xl px-3 py-2 text-base hover:bg-secondary"
                    >
                      {link.label}
                    </a>
                  ) : (
                    <Link key={link.href} href={link.href} className="rounded-xl px-3 py-2 text-base hover:bg-secondary">
                      {link.label}
                    </Link>
                  ),
                )}
                <Link href={nivoraPath("/studio")} className="rounded-xl px-3 py-2 text-base hover:bg-secondary">
                  Studio
                </Link>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
