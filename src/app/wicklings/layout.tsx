import type { Metadata } from "next";
import { WicklingsFooter } from "@/components/wicklings-footer";
import { WicklingsHeader } from "@/components/wicklings-header";
import { wicklings } from "@/data/wicklings";

export const metadata: Metadata = {
  title: {
    default: wicklings.name,
    template: `%s · ${wicklings.name}`,
  },
  description: wicklings.description,
};

export default function WicklingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <WicklingsHeader />
      <div className="flex-1">{children}</div>
      <WicklingsFooter />
    </>
  );
}
