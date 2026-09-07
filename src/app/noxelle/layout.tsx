import type { Metadata } from "next";
import { NoxelleFooter } from "@/components/noxelle-footer";
import { NoxelleHeader } from "@/components/noxelle-header";
import { noxelle } from "@/data/noxelle";

export const metadata: Metadata = {
  title: {
    default: noxelle.name,
    template: `%s · ${noxelle.name}`,
  },
  description: noxelle.description,
};

export default function NoxelleLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <NoxelleHeader />
      <div className="flex-1">{children}</div>
      <NoxelleFooter />
    </>
  );
}
