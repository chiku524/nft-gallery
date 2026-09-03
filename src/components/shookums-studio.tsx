"use client";

import { useMemo, useState } from "react";
import { ApngImage } from "@/components/apng-image";
import { ShookumStack } from "@/components/shookum-stack";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  defaultShookumSelection,
  findShookumTrait,
  shookumCategoryById,
  shookumTraitCategories,
  shookumTraitSrc,
  randomShookumSelection,
  type ShookumSelection,
  type ShookumTraitCategory,
} from "@/data/shookum-traits";
import { cn } from "@/lib/utils";

export function ShookumsStudio() {
  const [selection, setSelection] = useState<ShookumSelection>({ ...defaultShookumSelection });

  const recipe = useMemo(
    () =>
      shookumTraitCategories.map((category) => {
        const trait = findShookumTrait(category.id, selection[category.id]);
        return {
          label: category.label,
          value: trait?.name ?? (category.noneLabel ?? "None"),
        };
      }),
    [selection],
  );

  function setTrait(categoryId: ShookumTraitCategory["id"], traitId: string) {
    setSelection((current) => ({ ...current, [categoryId]: traitId }));
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
      <div>
        <ShookumStack selection={selection} />
        <ul className="mt-4 grid grid-cols-2 gap-2 text-sm sm:grid-cols-3">
          {recipe.map((row) => (
            <li key={row.label} className="rounded-xl border bg-card px-3 py-2">
              <p className="text-[11px] uppercase tracking-wider text-muted-foreground">{row.label}</p>
              <p className="font-medium">{row.value}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="min-w-0 rounded-[1.75rem] border bg-card p-4 sm:p-5">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Layer mixer</p>
            <h2 className="font-heading text-2xl">Stack a haunt</h2>
          </div>
          <div className="flex gap-2">
            <Button type="button" variant="secondary" onClick={() => setSelection(randomShookumSelection())}>
              Random
            </Button>
            <Button type="button" variant="outline" onClick={() => setSelection({ ...defaultShookumSelection })}>
              Reset
            </Button>
          </div>
        </div>

        <Tabs defaultValue="night">
          <TabsList variant="line" className="mb-4 w-full flex-wrap justify-start">
            {shookumTraitCategories.map((category) => (
              <TabsTrigger key={category.id} value={category.id}>
                {category.label}
              </TabsTrigger>
            ))}
          </TabsList>
          {shookumTraitCategories.map((category) => (
            <TabsContent key={category.id} value={category.id}>
              <p className="mb-3 text-sm text-muted-foreground">{category.blurb}</p>
              <ScrollArea className="h-[28rem]">
                <div className="grid grid-cols-2 gap-3 pr-2 sm:grid-cols-3">
                  {category.noneLabel ? (
                    <TraitPick
                      name={category.noneLabel}
                      selected={selection[category.id] === "none"}
                      onSelect={() => setTrait(category.id, "none")}
                    />
                  ) : null}
                  {category.traits.map((trait) => (
                    <TraitPick
                      key={trait.id}
                      name={trait.name}
                      src={shookumTraitSrc(trait.image)}
                      selected={selection[category.id] === trait.id}
                      onSelect={() => setTrait(category.id, trait.id)}
                    />
                  ))}
                </div>
              </ScrollArea>
              <p className="mt-3 text-xs text-muted-foreground">
                {shookumCategoryById(category.id).traits.length}
                {category.noneLabel ? " + none" : ""} loops in this layer.
              </p>
            </TabsContent>
          ))}
        </Tabs>
      </div>
    </div>
  );
}

function TraitPick({
  name,
  src,
  selected,
  onSelect,
}: {
  name: string;
  src?: string;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        "overflow-hidden rounded-2xl border text-left transition",
        selected ? "border-primary ring-2 ring-primary/40" : "hover:border-foreground/20",
      )}
    >
      <div className="relative aspect-square bg-[repeating-conic-gradient(#f4ebe0_0%_25%,#e8c4d0_0%_50%)] bg-[length:16px_16px]">
        {src ? (
          <ApngImage src={src} alt="" className="absolute inset-0 size-full object-cover" />
        ) : (
          <div className="absolute inset-0 grid place-items-center text-xs text-muted-foreground">empty</div>
        )}
      </div>
      <div className="flex items-center justify-between gap-2 px-2.5 py-2">
        <span className="text-sm font-medium">{name}</span>
        {selected ? <Badge variant="secondary">on</Badge> : null}
      </div>
    </button>
  );
}
