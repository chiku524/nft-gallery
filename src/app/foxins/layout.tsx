import type { Metadata } from "next";
import { FoxinsFooter } from "@/components/foxins-footer";
import { FoxinsHeader } from "@/components/foxins-header";
import { foxins } from "@/data/foxins";

export const metadata: Metadata = {
  title: {
    default: foxins.name,
    template: `%s · ${foxins.name}`,
  },
  description: foxins.description,
};

export default function FoxinsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <FoxinsHeader />
      <div className="flex-1">{children}</div>
      <FoxinsFooter />
    </>
  );
}
