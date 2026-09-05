import type { Metadata } from "next";
import { RisotaFooter } from "@/components/risota-footer";
import { RisotaHeader } from "@/components/risota-header";
import { risota } from "@/data/risota";

export const metadata: Metadata = {
  title: {
    default: risota.name,
    template: `%s · ${risota.name}`,
  },
  description: risota.description,
};

export default function RisotaLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <RisotaHeader />
      <div className="flex-1">{children}</div>
      <RisotaFooter />
    </>
  );
}
