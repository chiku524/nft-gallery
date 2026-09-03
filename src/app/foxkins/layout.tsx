import type { Metadata } from "next";
import { FoxkinsFooter } from "@/components/foxkins-footer";
import { FoxkinsHeader } from "@/components/foxkins-header";
import { foxkins } from "@/data/foxkins";

export const metadata: Metadata = {
  title: {
    default: foxkins.name,
    template: `%s · ${foxkins.name}`,
  },
  description: foxkins.description,
};

export default function FoxkinsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <FoxkinsHeader />
      <div className="flex-1">{children}</div>
      <FoxkinsFooter />
    </>
  );
}
