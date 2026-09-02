import type { Metadata } from "next";
import { MochinsFooter } from "@/components/mochins-footer";
import { MochinsHeader } from "@/components/mochins-header";
import { mochins } from "@/data/mochins";

export const metadata: Metadata = {
  title: {
    default: mochins.name,
    template: `%s · ${mochins.name}`,
  },
  description: mochins.description,
};

export default function MochinsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <MochinsHeader />
      <div className="flex-1">{children}</div>
      <MochinsFooter />
    </>
  );
}
