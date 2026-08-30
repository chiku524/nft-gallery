import type { Metadata } from "next";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { collection } from "@/data/collection";

export const metadata: Metadata = {
  title: {
    default: collection.name,
    template: `%s · ${collection.name}`,
  },
  description: collection.description,
};

export default function LoopkinsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SiteHeader />
      <div className="flex-1">{children}</div>
      <SiteFooter />
    </>
  );
}
