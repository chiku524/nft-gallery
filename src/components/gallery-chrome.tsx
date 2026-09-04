"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ApngImage } from "@/components/apng-image";
import { gallery, projects, type GalleryProject } from "@/data/projects";
import { cn } from "@/lib/utils";

function CollectionFrame({
  project,
  active,
}: {
  project: GalleryProject;
  active: boolean;
}) {
  const hang = project.slug.length % 3 === 0 ? "-translate-y-0.5" : project.slug.length % 3 === 1 ? "translate-y-0.5" : "";
  const frameRef = useRef<HTMLAnchorElement>(null);

  useEffect(() => {
    if (!active) return;
    frameRef.current?.scrollIntoView({ inline: "center", block: "nearest", behavior: "smooth" });
  }, [active]);

  return (
    <Link
      ref={frameRef}
      href={project.href}
      aria-current={active ? "page" : undefined}
      title={`${project.name} · ${project.chain}`}
      className={cn(
        "group relative flex shrink-0 flex-col items-center gap-1 outline-none",
        hang,
      )}
    >
      <span
        className={cn(
          "relative block size-10 overflow-hidden rounded-[0.85rem] border shadow-[0_6px_14px_rgba(0,0,0,0.35)] transition duration-300 sm:size-11",
          active
            ? "scale-110 border-[#49f2c2] ring-2 ring-[#49f2c2]/50"
            : "border-white/20 group-hover:border-white/55 group-hover:scale-105 group-focus-visible:border-[#49f2c2]",
        )}
      >
        <ApngImage
          src={project.thumb}
          alt=""
          width={88}
          height={88}
          className="size-full object-cover"
        />
        {project.status === "new on the wall" ? (
          <span className="absolute right-0.5 top-0.5 size-1.5 rounded-full bg-[#49f2c2] shadow-[0_0_8px_#49f2c2]" />
        ) : null}
      </span>
      <span
        className={cn(
          "max-w-[4.6rem] truncate text-[10px] leading-none tracking-wide sm:max-w-[5.4rem]",
          active ? "font-medium text-white" : "text-[#f4f1ff]/45 group-hover:text-[#f4f1ff]/85",
        )}
      >
        {project.name}
      </span>
    </Link>
  );
}

export function GalleryChrome() {
  const pathname = usePathname();
  const onHub = pathname === "/";

  return (
    <div className="border-b border-white/10 bg-[#070816] text-[#f4f1ff]">
      <div className="mx-auto flex w-full max-w-6xl items-center gap-4 px-4 py-2.5 sm:px-6">
        <Link
          href="/"
          aria-current={onHub ? "page" : undefined}
          className={cn(
            "flex shrink-0 flex-col justify-center rounded-lg px-1 py-0.5 leading-tight outline-none focus-visible:ring-2 focus-visible:ring-[#49f2c2]/60",
            onHub ? "text-white" : "text-[#f4f1ff]/80 hover:text-white",
          )}
        >
          <span className="font-heading text-sm tracking-tight sm:text-base">{gallery.name}</span>
          <span className="text-[10px] uppercase tracking-[0.18em] text-[#f4f1ff]/40">On the wall</span>
        </Link>

        <div className="hidden h-10 w-px shrink-0 bg-white/10 sm:block" aria-hidden="true" />

        <nav aria-label="Collections on the wall" className="relative min-w-0 flex-1">
          <div className="pointer-events-none absolute inset-y-0 left-0 z-10 w-6 bg-gradient-to-r from-[#070816] to-transparent" />
          <div className="pointer-events-none absolute inset-y-0 right-0 z-10 w-6 bg-gradient-to-l from-[#070816] to-transparent" />
          <div className="flex items-end gap-3 overflow-x-auto px-4 py-0.5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            {projects.map((project) => (
              <CollectionFrame
                key={project.slug}
                project={project}
                active={pathname === project.href || pathname.startsWith(`${project.href}/`)}
              />
            ))}
          </div>
        </nav>
      </div>
    </div>
  );
}
