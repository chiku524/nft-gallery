import type { Metadata } from "next";
import { CeraFooter } from "@/components/cera-footer";
import { CeraHeader } from "@/components/cera-header";
import { cera } from "@/data/cera";

export const metadata: Metadata = {
  title: {
    default: cera.name,
    template: `%s · ${cera.name}`,
  },
  description: cera.description,
};

export default function CeraLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <CeraHeader />
      <div className="flex-1">{children}</div>
      <CeraFooter />
    </>
  );
}
