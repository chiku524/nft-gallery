"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { gallery, projects } from "@/data/projects";
import { cn } from "@/lib/utils";

export function GalleryChrome() {
  const pathname = usePathname();
  const onHub = pathname === "/";

  return (
    <div className="border-b border-white/10 bg-[#070816] text-[#f4f1ff]">
      <div className="mx-auto flex h-11 w-full max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
        <Link
          href="/"
          className={cn(
            "font-heading text-sm tracking-tight sm:text-base",
            onHub ? "text-white" : "text-[#f4f1ff]/80 hover:text-white",
          )}
        >
          {gallery.name}
        </Link>
        <nav className="flex min-w-0 items-center gap-1 overflow-x-auto text-xs sm:text-sm">
          <Link
            href="/studio"
            className={cn(
              "shrink-0 rounded-full px-2.5 py-1 transition-colors",
              pathname === "/studio" || pathname.startsWith("/studio/")
                ? "bg-[#49f2c2] text-[#070816]"
                : "text-[#f4f1ff]/70 hover:bg-white/10 hover:text-white",
            )}
          >
            Studio
          </Link>
          {projects.map((project) => {
            const active = pathname === project.href || pathname.startsWith(`${project.href}/`);
            return (
              <Link
                key={project.slug}
                href={project.href}
                className={cn(
                  "shrink-0 rounded-full px-2.5 py-1 transition-colors",
                  active
                    ? "bg-[#49f2c2] text-[#070816]"
                    : "text-[#f4f1ff]/70 hover:bg-white/10 hover:text-white",
                )}
              >
                {project.name}
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
