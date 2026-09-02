import type { Metadata } from "next";
import { HoodkinsFooter } from "@/components/hoodkins-footer";
import { HoodkinsHeader } from "@/components/hoodkins-header";
import { hoodkins } from "@/data/hoodkins";

export const metadata: Metadata = {
  title: {
    default: hoodkins.name,
    template: `%s · ${hoodkins.name}`,
  },
  description: hoodkins.description,
};

export default function HoodkinsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <HoodkinsHeader />
      <div className="flex-1">{children}</div>
      <HoodkinsFooter />
    </>
  );
}
