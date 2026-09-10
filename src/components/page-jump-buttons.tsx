"use client";

import { useEffect, useState } from "react";
import { ChevronsDown, ChevronsUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { setWallEngaged } from "@/lib/wall-lock";

const EDGE = 12;

export function PageJumpButtons() {
  const [atTop, setAtTop] = useState(true);
  const [atBottom, setAtBottom] = useState(false);

  useEffect(() => {
    const update = () => {
      const y = window.scrollY;
      const max = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
      setAtTop(y <= EDGE);
      setAtBottom(y >= max - EDGE);
    };

    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => {
      window.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, []);

  return (
    <div
      role="group"
      aria-label="Page position"
      className="fixed top-24 right-4 z-40 flex flex-col gap-2 sm:top-28"
    >
      <Button
        type="button"
        variant="outline"
        size="lg"
        disabled={atTop}
        aria-label="Scroll to top of page"
        title="Scroll to top of page"
        onClick={() => {
          setWallEngaged(false);
          requestAnimationFrame(() => {
            window.scrollTo({ top: 0, behavior: "smooth" });
          });
        }}
        className="border-white/20 bg-background/90 shadow-[0_8px_24px_rgba(0,0,0,0.35)] backdrop-blur-md"
      >
        <ChevronsUp data-icon="inline-start" />
        Top of page
      </Button>
      <Button
        type="button"
        variant="outline"
        size="lg"
        disabled={atBottom}
        aria-label="Scroll to bottom of page"
        title="Scroll to bottom of page"
        onClick={() => {
          setWallEngaged(false);
          requestAnimationFrame(() => {
            window.scrollTo({
              top: document.documentElement.scrollHeight,
              behavior: "smooth",
            });
          });
        }}
        className="border-white/20 bg-background/90 shadow-[0_8px_24px_rgba(0,0,0,0.35)] backdrop-blur-md"
      >
        <ChevronsDown data-icon="inline-start" />
        Bottom of page
      </Button>
    </div>
  );
}
