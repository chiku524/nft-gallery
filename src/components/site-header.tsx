"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { collection } from "@/data/collection";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { potbPath } from "@/lib/potb";
import { cn } from "@/lib/utils";

const links = [
  { href: potbPath(), label: "Drop" },
  { href: potbPath("/traits"), label: "Traits" },
  { href: potbPath("/gallery"), label: "Gallery" },
  { href: potbPath("/launch"), label: "OpenSea" },
];

export function SiteHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-border/80 bg-[color-mix(in_oklch,var(--background)_88%,white)]/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href={potbPath()} className="flex items-center gap-3">
          <Image
            src="/brand/logo-pugs-on-the-block.png"
            alt=""
            width={40}
            height={40}
            className="size-10 rounded-full border border-border object-cover"
          />
          <div className="leading-tight">
            <p className="font-heading text-lg tracking-tight">{collection.name}</p>
            <p className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
              Robinhood Chain
            </p>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "rounded-full px-3 py-1.5 text-sm transition-colors",
                pathname === link.href
                  ? "bg-foreground text-background"
                  : "text-muted-foreground hover:bg-secondary hover:text-foreground",
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <Button asChild size="sm" className="hidden sm:inline-flex">
            <Link href={potbPath("/gallery")}>Sample mints</Link>
          </Button>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="md:hidden" aria-label="Open menu">
                <Menu />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-72">
              <SheetHeader>
                <SheetTitle>{collection.name}</SheetTitle>
              </SheetHeader>
              <div className="mt-6 flex flex-col gap-2 px-4">
                {links.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="rounded-xl px-3 py-2 text-base hover:bg-secondary"
                  >
                    {link.label}
                  </Link>
                ))}
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
