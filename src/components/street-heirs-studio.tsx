"use client";

import Image from "next/image";
import { useMemo, useState } from "react";
import { StreetHeirsStack } from "@/components/street-heirs-stack";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  defaultStreetHeirsSelection,
  isStreetHeirsSelectionCompatible,
  streetHeirsTraitCategories,
  streetHeirsTraitSrc,
  type StreetHeirsCategoryId,
  type StreetHeirsSelection,
  type StreetHeirsTrait,
} from "@/data/street-heirs-traits";
import { cn } from "@/lib/utils";

function weightedTrait(traits: StreetHeirsTrait[]) {
  const total = traits.reduce((sum, trait) => sum + trait.weight, 0);
  let cursor = Math.random() * total;
  for (const trait of traits) {
    cursor -= trait.weight;
    if (cursor < 0) return trait;
  }
  return traits[traits.length - 1];
}

function randomCompatibleSelection(): StreetHeirsSelection {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const next = { ...defaultStreetHeirsSelection };
    for (const category of streetHeirsTraitCategories) {
      next[category.id] = weightedTrait(category.traits).id;
    }
    if (isStreetHeirsSelectionCompatible(next)) return next;
  }
  return { ...defaultStreetHeirsSelection };
}

export function StreetHeirsStudio() {
  const [selection, setSelection] = useState<StreetHeirsSelection>({ ...defaultStreetHeirsSelection });
  const [notice, setNotice] = useState<string | null>(null);
  const recipe = useMemo(
    () =>
      streetHeirsTraitCategories.map((category) => ({
        label: category.label,
        value: category.traits.find((trait) => trait.id === selection[category.id])?.name ?? selection[category.id],
      })),
    [selection],
  );

  function selectTrait(categoryId: StreetHeirsCategoryId, traitId: string) {
    const next = { ...selection, [categoryId]: traitId };
    if (!isStreetHeirsSelectionCompatible(next)) {
      setNotice("That plate conflicts with the current recipe. Change the related look first.");
      return;
    }
    setSelection(next);
    setNotice(null);
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1.02fr)_minmax(0,0.98fr)]">
      <div>
        <StreetHeirsStack selection={selection} />
        <h2 className="mt-5 font-heading text-2xl text-[#202A3D]">Current recipe</h2>
        <ul className="mt-3 grid grid-cols-2 gap-2 text-sm sm:grid-cols-4">
          {recipe.map((row) => (
            <li key={row.label} className="rounded-xl border border-[#202A3D]/15 bg-white/55 px-3 py-2">
              <p className="text-[10px] uppercase tracking-[0.16em] text-[#496A9A]">{row.label}</p>
              <p className="font-medium text-[#202A3D]">{row.value}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="min-w-0 rounded-[2rem] border border-[#202A3D]/15 bg-white/60 p-4 sm:p-5">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-[#496A9A]">Plate editor</p>
            <h2 className="font-heading text-2xl text-[#202A3D]">Build an heir</h2>
          </div>
          <div className="flex gap-2">
            <Button
              type="button"
              className="bg-[#D3B36C] text-[#202A3D] hover:bg-[#D3B36C]/85"
              onClick={() => { setSelection(randomCompatibleSelection()); setNotice(null); }}
            >
              Weighted shuffle
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => { setSelection({ ...defaultStreetHeirsSelection }); setNotice(null); }}
            >
              Reset
            </Button>
          </div>
        </div>
        <p className="mb-3 min-h-5 text-sm text-[#496A9A]" role="status" aria-live="polite">{notice}</p>

        <Tabs defaultValue={streetHeirsTraitCategories[0].id}>
          <TabsList variant="line" className="mb-4 h-auto w-full flex-wrap justify-start">
            {streetHeirsTraitCategories.map((category) => (
              <TabsTrigger key={category.id} value={category.id}>{category.label}</TabsTrigger>
            ))}
          </TabsList>
          {streetHeirsTraitCategories.map((category) => (
            <TabsContent key={category.id} value={category.id}>
              <ScrollArea className="h-[31rem]">
                <div className="grid grid-cols-2 gap-3 pr-2 sm:grid-cols-3">
                  {category.traits.map((trait) => {
                    const candidate = { ...selection, [category.id]: trait.id };
                    const compatible = isStreetHeirsSelectionCompatible(candidate);
                    return (
                      <button
                        key={trait.id}
                        type="button"
                        onClick={() => selectTrait(category.id, trait.id)}
                        aria-pressed={selection[category.id] === trait.id}
                        aria-describedby={!compatible ? `${category.id}-${trait.id}-conflict` : undefined}
                        className={cn(
                          "overflow-hidden rounded-2xl border bg-[#F4EFE5] text-left transition",
                          selection[category.id] === trait.id
                            ? "border-[#D3B36C] ring-2 ring-[#D3B36C]/45"
                            : "border-[#202A3D]/15 hover:border-[#496A9A]",
                          !compatible && "opacity-45",
                        )}
                      >
                        <div className="relative aspect-square bg-[#202A3D]">
                          <Image
                            src={streetHeirsTraitSrc(trait.image)}
                            alt=""
                            fill
                            sizes="(max-width: 640px) 45vw, 170px"
                            unoptimized
                            className="object-cover"
                          />
                        </div>
                        <div className="p-2.5">
                          <span className="text-sm font-medium text-[#202A3D]">{trait.name}</span>
                          <div className="mt-1 flex items-center justify-between gap-2">
                            <span className="text-xs text-[#496A9A]">Weight {trait.weight}</span>
                            {selection[category.id] === trait.id ? <Badge variant="secondary">On</Badge> : null}
                          </div>
                          {!compatible ? <span id={`${category.id}-${trait.id}-conflict`} className="text-[10px] text-[#202A3D]/65">Conflicts</span> : null}
                        </div>
                      </button>
                    );
                  })}
                </div>
              </ScrollArea>
            </TabsContent>
          ))}
        </Tabs>
      </div>
    </div>
  );
}
