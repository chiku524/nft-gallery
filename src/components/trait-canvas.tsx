"use client";

import { useEffect, useRef, useState } from "react";
import { findTrait, traitSrc, type Selection, type Trait } from "@/data/traits";

type Layer = {
  src: string;
  x: number;
  y: number;
  scale: number;
};

function loadImage(src: string) {
  return new Promise<HTMLImageElement>((resolve, reject) => {
    const image = new Image();
    image.crossOrigin = "anonymous";
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error(`Failed to load ${src}`));
    image.src = src;
  });
}

export function selectionToLayers(selection: Selection): Layer[] {
  const layers: Layer[] = [];
  const background = findTrait("background", selection.background);
  const block = findTrait("block", selection.block);
  const base = findTrait("base", selection.base);
  const body = findTrait("body", selection.body);
  const hat = findTrait("hat", selection.hat);
  const accessory = findTrait("accessory", selection.accessory);

  const push = (trait?: Trait | null) => {
    if (!trait?.image) return;
    layers.push({
      src: traitSrc(trait.image),
      x: trait.overlay?.x ?? 0,
      y: trait.overlay?.y ?? 0,
      scale: trait.overlay?.scale ?? 1,
    });
  };

  // Original gallery stack: scene, ledge, pug, clothes, hat, toy.
  push(background);
  push(block);
  push(base);
  push(body);
  push(hat);
  push(accessory);
  return layers;
}

export function TraitCanvas({
  selection,
  size = 720,
  className,
}: {
  selection: Selection;
  size?: number;
  className?: string;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let cancelled = false;
    setStatus("loading");

    async function draw() {
      const layers = selectionToLayers(selection);
      try {
        const images = await Promise.all(layers.map((layer) => loadImage(layer.src)));
        if (cancelled || !ctx || !canvas) return;
        ctx.clearRect(0, 0, size, size);
        images.forEach((image, index) => {
          const layer = layers[index];
          const width = size * layer.scale;
          const height = size * layer.scale;
          ctx.drawImage(image, size * layer.x, size * layer.y, width, height);
        });
        setStatus("ready");
      } catch {
        if (!cancelled) setStatus("error");
      }
    }

    void draw();
    return () => {
      cancelled = true;
    };
  }, [selection, size]);

  function download() {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const anchor = document.createElement("a");
    anchor.href = canvas.toDataURL("image/png");
    anchor.download = "pugs-on-the-block.png";
    anchor.click();
  }

  return (
    <div className={className}>
      <canvas
        ref={canvasRef}
        width={size}
        height={size}
        className="aspect-square w-full rounded-[1.75rem] bg-[#1a1410] shadow-[0_24px_60px_rgba(40,22,12,0.28)]"
        aria-label="Assembled pug preview"
      />
      <div className="mt-3 flex items-center justify-between text-sm text-muted-foreground">
        <span>
          {status === "loading" && "Stacking traits…"}
          {status === "ready" && "Layered PFP preview"}
          {status === "error" && "Could not load a trait image."}
        </span>
        <button
          type="button"
          onClick={download}
          disabled={status !== "ready"}
          className="font-medium text-primary underline-offset-4 hover:underline disabled:opacity-40"
        >
          Download PNG
        </button>
      </div>
    </div>
  );
}
