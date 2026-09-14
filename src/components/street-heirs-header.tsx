"use client";

import Image from "next/image";
import Link from "next/link";
import { Menu } from "lucide-react";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { streetHeirs } from "@/data/street-heirs";
import { streetHeirsPath } from "@/lib/street-heirs";
import { cn } from "@/lib/utils";

const links = [
  { href: streetHeirsPath(), label: "Story" },
  { href: streetHeirsPath("/gallery"), label: "Gallery" },
  { href: streetHeirsPath("/traits"), label: "Traits" },
  { href: streetHeirsPath("/launch"), label: "Launch" },
];

export function StreetHeirsHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-[#202A3D]/15 bg-[#F4EFE5]/95 text-[#202A3D] backdrop-blur-md">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href={streetHeirsPath()} className="flex items-center gap-3" aria-label="Street Heirs home">
          <Image
            src="/brand/logo-street-heirs.png"
            alt=""
            width={40}
            height={40}
            className="size-10 rounded-full border border-[#D3B36C] object-cover"
          />
          <div className="leading-tight">
            <p className="font-heading text-lg">{streetHeirs.name}</p>
            <p className="text-[10px] uppercase tracking-[0.2em] text-[#496A9A]">Editorial portraits</p>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex" aria-label="Street Heirs navigation">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              aria-current={pathname === link.href ? "page" : undefined}
              className={cn(
                "rounded-full px-3 py-1.5 text-sm transition-colors",
                pathname === link.href
                  ? "bg-[#202A3D] text-[#F4EFE5]"
                  : "text-[#202A3D]/70 hover:bg-[#B6C3A3]/35 hover:text-[#202A3D]",
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <Button asChild size="sm" className="hidden bg-[#D3B36C] text-[#202A3D] hover:bg-[#D3B36C]/85 sm:inline-flex">
            <Link href={streetHeirsPath("/studio")}>Studio</Link>
          </Button>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="border-[#202A3D]/30 md:hidden" aria-label="Open menu">
                <Menu />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-72 bg-[#F4EFE5] text-[#202A3D]">
              <SheetHeader><SheetTitle>{streetHeirs.name}</SheetTitle></SheetHeader>
              <nav className="mt-6 flex flex-col gap-2 px-4" aria-label="Mobile Street Heirs navigation">
                {[...links, { href: streetHeirsPath("/studio"), label: "Studio" }].map((link) => (
                  <Link key={link.href} href={link.href} className="rounded-xl px-3 py-2 hover:bg-[#B6C3A3]/35">
                    {link.label}
                  </Link>
                ))}
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
