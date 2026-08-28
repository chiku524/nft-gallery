"use client";

import { useMemo, useState } from "react";
import Image from "next/image";
import { Dices } from "lucide-react";
import { TraitCanvas } from "@/components/trait-canvas";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  defaultSelection,
  randomSelection,
  traitCategories,
  type Selection,
  type TraitCategory,
} from "@/data/traits";
import { cn } from "@/lib/utils";

function optionsFor(category: TraitCategory) {
  const extras = category.noneLabel
    ? [{ id: "none", name: category.noneLabel, rarity: 28, image: undefined }]
    : [];
  return [...extras, ...category.traits];
}

export function StudioMixer() {
  const [selection, setSelection] = useState<Selection>({ ...defaultSelection });
  const [active, setActive] = useState<TraitCategory["id"]>("hat");

  const category = useMemo(
    () => traitCategories.find((item) => item.id === active)!,
    [active],
  );
  const options = optionsFor(category);

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
      <TraitCanvas selection={selection} />

      <div className="flex min-w-0 flex-col gap-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="font-heading text-2xl">Trait mixer</p>
            <p className="text-sm text-muted-foreground">
              Stack a background, pug, ledge, hat, clothes, and a ledge toy. Clothes wrap
              the neck behind the paws; hats tuck behind the ears.
            </p>
          </div>
          <Button type="button" variant="outline" onClick={() => setSelection(randomSelection())}>
            <Dices data-icon="inline-start" />
            Shuffle
          </Button>
        </div>

        <div className="flex flex-wrap gap-2">
          {traitCategories.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => setActive(item.id)}
              className={cn(
                "rounded-full border px-3 py-1.5 text-sm transition-colors",
                active === item.id
                  ? "border-foreground bg-foreground text-background"
                  : "border-border bg-card text-muted-foreground hover:text-foreground",
              )}
            >
              {item.label}
            </button>
          ))}
        </div>

        <p className="text-sm text-muted-foreground">{category.blurb}</p>

        <ScrollArea className="h-[28rem] rounded-2xl border bg-card p-3">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {options.map((trait) => {
              const selected = selection[category.id] === trait.id;
              return (
                <button
                  key={trait.id}
                  type="button"
                  onClick={() =>
                    setSelection((current) => ({ ...current, [category.id]: trait.id }))
                  }
                  className={cn(
                    "overflow-hidden rounded-2xl border text-left transition",
                    selected
                      ? "border-foreground ring-2 ring-foreground/20"
                      : "border-border hover:border-foreground/40",
                  )}
                >
                  <div className="relative aspect-square bg-[repeating-conic-gradient(#efe4d4_0%_25%,#f7f0e6_0%_50%)] bg-[length:16px_16px]">
                    {trait.image ? (
                      <Image
                        src={trait.image}
                        alt=""
                        fill
                        sizes="160px"
                        unoptimized
                        className={
                          category.id === "block"
                            ? "object-cover object-bottom"
                            : "object-contain"
                        }
                      />
                    ) : (
                      <div className="flex size-full items-center justify-center text-xs text-muted-foreground">
                        None
                      </div>
                    )}
                  </div>
                  <div className="flex items-center justify-between gap-2 px-2 py-2">
                    <span className="truncate text-sm font-medium">{trait.name}</span>
                    {trait.id !== "none" ? (
                      <Badge variant="secondary" className="shrink-0 text-[10px]">
                        {trait.rarity}%
                      </Badge>
                    ) : null}
                  </div>
                </button>
              );
            })}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}
