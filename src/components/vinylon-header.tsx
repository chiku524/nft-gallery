"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { ApngImage } from "@/components/apng-image";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { vinylon } from "@/data/vinylon";
import { vinylonPath } from "@/lib/vinylon";
import { openSeaListings } from "@/lib/opensea";
import { cn } from "@/lib/utils";

const links: { href: string; label: string; external?: boolean }[] = [
  { href: vinylonPath(), label: "Drop" },
  { href: vinylonPath("/traits"), label: "Traits" },
  { href: vinylonPath("/gallery"), label: "Gallery" },
  { href: vinylonPath("/launch"), label: "Launch" },
  ...openSeaListings(vinylon.opensea).map((listing) => ({
    href: listing.href,
    label: `OpenSea · ${listing.label}`,
    external: true,
  })),
];

export function VinylonHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-[#ec4848]/20 bg-[color-mix(in_oklch,var(--background)_78%,#f6d2c8)]/92 backdrop-blur-md">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href={vinylonPath()} className="flex items-center gap-3">
          <ApngImage
            src="/brand/logo-vinylon.png"
            alt=""
            width={40}
            height={40}
            className="size-10 rounded-[0.7rem] border border-[#ec4848]/40 object-cover"
          />
          <div className="leading-tight">
            <p className="font-heading text-lg tracking-tight">{vinylon.name}</p>
            <p className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
              Balloon Animal PFPs
            </p>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map((link) => {
            const className = cn(
              "rounded-full px-3 py-1.5 text-sm transition-colors",
              !link.external && pathname === link.href
                ? "bg-[#ec4848] text-[#1a1420]"
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
          <Button asChild size="sm" className="hidden bg-[#ec4848] text-[#1a1420] hover:bg-[#ec4848]/90 sm:inline-flex">
            <Link href={vinylonPath("/studio")}>Studio</Link>
          </Button>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="md:hidden" aria-label="Open menu">
                <Menu />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-72">
              <SheetHeader>
                <SheetTitle>{vinylon.name}</SheetTitle>
              </SheetHeader>
              <div className="mt-6 flex flex-col gap-2 px-4">
                {links.map((link) =>
                  link.external ? (
                    <a key={link.href} href={link.href} target="_blank" rel="noreferrer" className="rounded-xl px-3 py-2 text-base hover:bg-secondary">
                      {link.label}
                    </a>
                  ) : (
                    <Link key={link.href} href={link.href} className="rounded-xl px-3 py-2 text-base hover:bg-secondary">
                      {link.label}
                    </Link>
                  ),
                )}
                <Link href={vinylonPath("/studio")} className="rounded-xl px-3 py-2 text-base hover:bg-secondary">
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
