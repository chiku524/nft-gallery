import type { Metadata } from "next";
import { OpalineFooter } from "@/components/opaline-footer";
import { OpalineHeader } from "@/components/opaline-header";
import { opaline } from "@/data/opaline";

export const metadata: Metadata = {
  title: {
    default: opaline.name,
    template: `%s · ${opaline.name}`,
  },
  description: opaline.description,
};

export default function OpalineLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <OpalineHeader />
      <div className="flex-1">{children}</div>
      <OpalineFooter />
    </>
  );
}
