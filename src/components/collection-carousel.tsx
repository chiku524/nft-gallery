"use client";

import { useCallback, useEffect, useRef, useState, type KeyboardEvent } from "react";
import { CollectionCard } from "@/components/collection-card";
import { ApngImage } from "@/components/apng-image";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  type CarouselApi,
} from "@/components/ui/carousel";
import type { GalleryProject } from "@/data/projects";
import { isWallEngaged, lockPageScroll, setWallEngaged, snapElementToTop } from "@/lib/wall-lock";
import { cn } from "@/lib/utils";

const WHEEL_PIXEL_THRESHOLD = 48;
const WHEEL_LINE_THRESHOLD = 1;
const WHEEL_COOLDOWN_MS = 420;

function newestIndex(drops: readonly GalleryProject[]) {
  const index = drops.findIndex((drop) => drop.status === "new on the wall");
  return index >= 0 ? index : 0;
}

export function CollectionCarousel({ drops }: { drops: readonly GalleryProject[] }) {
  const startIndex = newestIndex(drops);
  const rootRef = useRef<HTMLElement>(null);
  const [api, setApi] = useState<CarouselApi>();
  const [current, setCurrent] = useState(startIndex);
  const active = drops[current] ?? drops[0];

  const alignAndLock = useCallback(() => {
    const wall = rootRef.current;
    if (!wall) return false;
    const aligned = snapElementToTop(wall);
    lockPageScroll();
    return aligned;
  }, []);

  useEffect(() => {
    if (!api) return;

    const sync = () => setCurrent(api.selectedScrollSnap());
    sync();
    api.on("select", sync);
    api.on("reInit", sync);

    return () => {
      api.off("select", sync);
      api.off("reInit", sync);
    };
  }, [api]);

  useEffect(() => {
    const root = rootRef.current;
    if (!api || !root) return;

    let cooling = false;
    let accumulated = 0;
    let coolTimer = 0;

    const advance = (deltaY: number, deltaMode: number) => {
      accumulated += deltaY;
      if (cooling) return;

      const threshold = deltaMode === WheelEvent.DOM_DELTA_LINE
        ? WHEEL_LINE_THRESHOLD
        : deltaMode === WheelEvent.DOM_DELTA_PAGE
          ? 0.4
          : WHEEL_PIXEL_THRESHOLD;
      if (Math.abs(accumulated) < threshold) return;

      if (accumulated > 0) api.scrollNext();
      else api.scrollPrev();

      accumulated = 0;
      cooling = true;
      window.clearTimeout(coolTimer);
      coolTimer = window.setTimeout(() => {
        cooling = false;
      }, WHEEL_COOLDOWN_MS);
    };

    const onWallWheel = (event: WheelEvent) => {
      if (event.ctrlKey) return;
      if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;

      event.preventDefault();
      event.stopPropagation();
      if (!alignAndLock()) {
        accumulated = 0;
        cooling = true;
        window.clearTimeout(coolTimer);
        coolTimer = window.setTimeout(() => {
          cooling = false;
        }, WHEEL_COOLDOWN_MS);
        return;
      }
      advance(event.deltaY, event.deltaMode);
    };

    const onWindowWheel = (event: WheelEvent) => {
      if (!isWallEngaged()) return;
      if (event.ctrlKey) return;
      if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;

      event.preventDefault();
      alignAndLock();
      advance(event.deltaY, event.deltaMode);
    };

    const onWallClick = (event: Event) => {
      const target = event.target;
      if (!(target instanceof Element)) return;
      if (
        target.closest('[data-slot="carousel-previous"]') ||
        target.closest('[data-slot="carousel-next"]') ||
        target.closest('[role="tab"]')
      ) {
        alignAndLock();
      }
    };

    root.addEventListener("wheel", onWallWheel, { passive: false });
    window.addEventListener("wheel", onWindowWheel, { passive: false });
    root.addEventListener("click", onWallClick);
    return () => {
      root.removeEventListener("wheel", onWallWheel);
      window.removeEventListener("wheel", onWindowWheel);
      root.removeEventListener("click", onWallClick);
      window.clearTimeout(coolTimer);
      setWallEngaged(false);
    };
  }, [alignAndLock, api]);

  const scrollTo = useCallback(
    (index: number) => {
      api?.scrollTo(index);
    },
    [api],
  );

  const onKeyDown = useCallback(
    (event: KeyboardEvent<HTMLDivElement>) => {
      if (event.key === "ArrowDown" || event.key === "PageDown") {
        event.preventDefault();
        alignAndLock();
        api?.scrollNext();
      } else if (event.key === "ArrowUp" || event.key === "PageUp") {
        event.preventDefault();
        alignAndLock();
        api?.scrollPrev();
      }
    },
    [alignAndLock, api],
  );

  return (
    <section ref={rootRef} id="on-the-wall" className="w-full pb-16">
      <div className="mx-auto mb-6 flex w-full max-w-6xl items-end justify-between gap-4 px-4 sm:px-6">
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">On the wall</p>
          <h2 className="mt-1 font-heading text-3xl">Collections</h2>
        </div>
        <p className="hidden text-sm text-muted-foreground sm:block">
          {drops.length} live · scroll, swipe, or use the arrows
        </p>
      </div>
      <Carousel
        setApi={setApi}
        opts={{ align: "start", loop: true, startIndex }}
        className="w-full"
        aria-label="Collections on the wall"
        tabIndex={0}
        onKeyDown={onKeyDown}
      >
        <div className="relative">
          <CarouselContent className="-ml-0">
            {drops.map((drop) => (
              <CarouselItem key={drop.slug} className="basis-full pl-0">
                <div className="w-full px-4 sm:px-6 lg:px-10">
                  <CollectionCard drop={drop} />
                </div>
              </CarouselItem>
            ))}
          </CarouselContent>

          <CarouselPrevious
            size="icon-lg"
            className="left-2 z-10 size-10 border-white/20 bg-background/80 backdrop-blur-sm sm:left-4"
          />
          <CarouselNext
            size="icon-lg"
            className="right-2 z-10 size-10 border-white/20 bg-background/80 backdrop-blur-sm sm:right-4"
          />
        </div>

        <div className="mx-auto mt-6 flex w-full max-w-6xl flex-col items-center gap-4 px-4 sm:px-6">
          <p className="text-sm text-muted-foreground">
            <span className="font-heading text-foreground">{active?.name}</span>
            {" · "}
            {current + 1} of {drops.length}
          </p>

          <div
            role="tablist"
            aria-label="Jump to a collection"
            className="flex max-w-full flex-wrap justify-center gap-2"
          >
            {drops.map((drop, index) => {
              const selected = index === current;
              return (
                <button
                  key={drop.slug}
                  type="button"
                  role="tab"
                  aria-selected={selected}
                  aria-label={`Show ${drop.name}`}
                  title={drop.name}
                  onClick={() => scrollTo(index)}
                  className={cn(
                    "relative size-10 overflow-hidden rounded-[0.85rem] border shadow-[0_6px_14px_rgba(0,0,0,0.35)] outline-none transition duration-300 focus-visible:ring-2 focus-visible:ring-[#49f2c2]/60 sm:size-11",
                    selected
                      ? "scale-110 border-[#49f2c2] ring-2 ring-[#49f2c2]/50"
                      : "border-white/20 hover:scale-105 hover:border-white/55",
                  )}
                >
                  <ApngImage
                    src={drop.thumb}
                    alt=""
                    width={88}
                    height={88}
                    className="size-full object-cover"
                  />
                </button>
              );
            })}
          </div>
        </div>
      </Carousel>
    </section>
  );
}
