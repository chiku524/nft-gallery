"use client";

import Image from "next/image";
import { useMemo, useState } from "react";
import { RobinBanxStack } from "@/components/robinbanx-stack";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  defaultRobinBanxSelection,
  isRobinBanxSelectionCompatible,
  robinBanxTraitCategories,
  robinBanxTraitSrc,
  type RobinBanxSelection,
  type RobinBanxTraitCategory,
} from "@/data/robinbanx-traits";
import { cn } from "@/lib/utils";

export function RobinBanxStudio() {
  const [selection, setSelection] = useState<RobinBanxSelection>({ ...defaultRobinBanxSelection });
  const recipe = useMemo(
    () =>
      robinBanxTraitCategories.map((category) => {
        const trait = category.traits.find((item) => item.id === selection[category.id]);
        return {
          label: category.label,
          value: trait?.name ?? "Unfiled",
        };
      }),
    [selection],
  );

  function setTrait(categoryId: RobinBanxTraitCategory["id"], traitId: string) {
    setSelection((current) => ({ ...current, [categoryId]: traitId }));
  }

  function randomSelection(): RobinBanxSelection {
    for (let attempt = 0; attempt < 100; attempt += 1) {
      const candidate = Object.fromEntries(
        robinBanxTraitCategories.map((category) => {
          const total = category.traits.reduce((sum, trait) => sum + trait.rarity, 0);
          let roll = Math.random() * total;
          const selected =
            category.traits.find((trait) => {
              roll -= trait.rarity;
              return roll <= 0;
            }) ?? category.traits[0];
          return [category.id, selected.id];
        }),
      ) as RobinBanxSelection;
      if (isRobinBanxSelectionCompatible(candidate)) return candidate;
    }
    return { ...defaultRobinBanxSelection };
  }

  return (
    <div className="grid gap-10 lg:grid-cols-[minmax(0,1fr)_minmax(0,0.95fr)]">
      <div>
        <RobinBanxStack selection={selection} />
        <ul className="mt-7 grid grid-cols-2 gap-px border border-[#c7bda7]/20 bg-[#c7bda7]/20 text-sm sm:grid-cols-3">
          {recipe.map((row, index) => (
            <li key={row.label} className="bg-[#111312] p-3">
              <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#80877a]">
                Exhibit {String(index + 1).padStart(2, "0")} / {row.label}
              </p>
              <p className="mt-1 text-[#eee8da]">{row.value}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="min-w-0 border border-[#c7bda7]/20 bg-[#111312] p-4 sm:p-6">
        <div className="mb-5 flex flex-wrap items-end justify-between gap-3 border-b border-[#c7bda7]/20 pb-5">
          <div>
            <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-[#e24932]">Composite desk</p>
            <h2 className="mt-1 text-2xl font-black uppercase text-[#eee8da]">Build a suspect</h2>
          </div>
          <div className="flex gap-2">
            <Button type="button" onClick={() => setSelection(randomSelection())} className="rounded-none bg-[#e24932] text-[#090a0a] hover:bg-[#f15a43]">
              Shuffle file
            </Button>
            <Button type="button" variant="outline" onClick={() => setSelection({ ...defaultRobinBanxSelection })} className="rounded-none border-[#c7bda7]/30 text-[#eee8da]">
              Reset
            </Button>
          </div>
        </div>

        <Tabs defaultValue="safehouse">
          <TabsList variant="line" className="mb-4 h-auto w-full flex-wrap justify-start rounded-none">
            {robinBanxTraitCategories.map((category) => (
              <TabsTrigger key={category.id} value={category.id} className="font-mono text-xs uppercase">
                {category.label}
              </TabsTrigger>
            ))}
          </TabsList>
          {robinBanxTraitCategories.map((category) => (
            <TabsContent key={category.id} value={category.id}>
              <p className="mb-4 text-sm text-[#92988c]">
                Review every registered {category.label.toLowerCase()} plate before adding it to the file.
              </p>
              <ScrollArea className="h-[29rem]">
                <div className="grid grid-cols-2 gap-3 pr-3 sm:grid-cols-3">
                  {category.traits.map((trait) => (
                    <TraitPick
                      key={trait.id}
                      name={trait.name}
                      src={robinBanxTraitSrc(trait.image)}
                      selected={selection[category.id] === trait.id}
                      onSelect={() => setTrait(category.id, trait.id)}
                    />
                  ))}
                </div>
              </ScrollArea>
              <p className="mt-3 font-mono text-[10px] uppercase tracking-wider text-[#80877a]">
                {category.traits.length} plates logged
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
      aria-pressed={selected}
      className={cn(
        "overflow-hidden border bg-[#181b19] text-left transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#e24932]",
        selected ? "border-[#e24932] shadow-[4px_4px_0_#e24932]" : "border-[#c7bda7]/20 hover:border-[#c7bda7]/60",
      )}
    >
      <div className="relative aspect-square bg-[linear-gradient(135deg,#222622_25%,#121412_25%,#121412_50%,#222622_50%,#222622_75%,#121412_75%)] bg-[length:16px_16px]">
        {src ? (
          <Image src={src} alt="" fill sizes="160px" className="object-cover" unoptimized />
        ) : (
          <span className="absolute inset-0 grid place-items-center font-mono text-xs uppercase text-[#80877a]">clear</span>
        )}
      </div>
      <div className="flex min-h-12 items-center justify-between gap-2 border-t border-[#c7bda7]/20 px-2.5 py-2">
        <span className="text-sm text-[#eee8da]">{name}</span>
        {selected ? <Badge className="rounded-none bg-[#e24932] text-[#090a0a]">filed</Badge> : null}
      </div>
    </button>
  );
}
