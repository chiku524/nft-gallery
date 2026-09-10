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
  const rootRef = useRef<HTMLDivElement>(null);
  const [api, setApi] = useState<CarouselApi>();
  const [current, setCurrent] = useState(startIndex);
  const active = drops[current] ?? drops[0];

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

    let locked = false;
    let accumulated = 0;
    let unlockTimer = 0;

    const onWheel = (event: WheelEvent) => {
      if (event.ctrlKey) return;
      if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;

      event.preventDefault();
      accumulated += event.deltaY;
      if (locked) return;

      const threshold = event.deltaMode === WheelEvent.DOM_DELTA_LINE
        ? WHEEL_LINE_THRESHOLD
        : event.deltaMode === WheelEvent.DOM_DELTA_PAGE
          ? 0.4
          : WHEEL_PIXEL_THRESHOLD;
      if (Math.abs(accumulated) < threshold) return;

      if (accumulated > 0) api.scrollNext();
      else api.scrollPrev();

      accumulated = 0;
      locked = true;
      window.clearTimeout(unlockTimer);
      unlockTimer = window.setTimeout(() => {
        locked = false;
      }, WHEEL_COOLDOWN_MS);
    };

    root.addEventListener("wheel", onWheel, { passive: false });
    return () => {
      root.removeEventListener("wheel", onWheel);
      window.clearTimeout(unlockTimer);
    };
  }, [api]);

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
        api?.scrollNext();
      } else if (event.key === "ArrowUp" || event.key === "PageUp") {
        event.preventDefault();
        api?.scrollPrev();
      }
    },
    [api],
  );

  return (
    <div ref={rootRef} className="w-full">
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
    </div>
  );
}
