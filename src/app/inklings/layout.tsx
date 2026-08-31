import type { Metadata } from "next";
import { InklingsFooter } from "@/components/inklings-footer";
import { InklingsHeader } from "@/components/inklings-header";
import { inklings } from "@/data/inklings";

export const metadata: Metadata = {
  title: {
    default: inklings.name,
    template: `%s · ${inklings.name}`,
  },
  description: inklings.description,
};

export default function InklingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <InklingsHeader />
      <div className="flex-1">{children}</div>
      <InklingsFooter />
    </>
  );
}
