"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { robinBanx } from "@/data/robinbanx";
import { robinBanxPath } from "@/lib/robinbanx";
import { cn } from "@/lib/utils";

const links = [
  { href: robinBanxPath(), label: "Case file" },
  { href: robinBanxPath("/traits"), label: "Evidence" },
  { href: robinBanxPath("/gallery"), label: "Lineup" },
  { href: robinBanxPath("/studio"), label: "Assembly" },
  { href: robinBanxPath("/launch"), label: "Briefing" },
];

export function RobinBanxHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-[#c7bda7]/20 bg-[#0b0c0c]/95 text-[#eee8da] backdrop-blur-md">
      <div className="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6">
        <Link href={robinBanxPath()} className="flex items-center gap-3" aria-label="Robin Banx home">
          <span
            aria-hidden="true"
            className="grid size-10 -rotate-2 place-items-center border-2 border-[#e24932] bg-[#151817] font-mono text-sm font-black text-[#eee8da] shadow-[4px_4px_0_#667357]"
          >
            RBX
          </span>
          <span>
            <span className="block font-mono text-base font-black uppercase tracking-[0.08em]">{robinBanx.name}</span>
            <span className="block text-[10px] uppercase tracking-[0.24em] text-[#a8ad9f]">Restricted archive</span>
          </span>
        </Link>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Robin Banx">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "border border-transparent px-3 py-2 font-mono text-xs uppercase tracking-wider transition",
                pathname === link.href
                  ? "border-[#e24932] bg-[#e24932] text-[#0b0c0c]"
                  : "text-[#a8ad9f] hover:border-[#c7bda7]/30 hover:text-[#eee8da]",
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <Sheet>
          <SheetTrigger asChild>
            <Button
              variant="outline"
              size="icon"
              className="border-[#c7bda7]/30 bg-transparent text-[#eee8da] lg:hidden"
              aria-label="Open navigation"
            >
              <Menu />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="border-[#c7bda7]/20 bg-[#101211] text-[#eee8da]">
            <SheetHeader>
              <SheetTitle className="font-mono uppercase text-[#eee8da]">{robinBanx.name}</SheetTitle>
            </SheetHeader>
            <nav className="mt-6 flex flex-col gap-2 px-4" aria-label="Robin Banx mobile">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="border-l-2 border-[#e24932] px-3 py-2 font-mono text-sm uppercase tracking-wider hover:bg-[#1b1e1c]"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
