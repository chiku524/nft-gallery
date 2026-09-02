import type { Metadata } from "next";
import { PurrkinsFooter } from "@/components/purrkins-footer";
import { PurrkinsHeader } from "@/components/purrkins-header";
import { purrkins } from "@/data/purrkins";

export const metadata: Metadata = {
  title: {
    default: purrkins.name,
    template: `%s · ${purrkins.name}`,
  },
  description: purrkins.description,
};

export default function PurrkinsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <PurrkinsHeader />
      <div className="flex-1">{children}</div>
      <PurrkinsFooter />
    </>
  );
}
