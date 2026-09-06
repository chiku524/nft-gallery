import type { Metadata } from "next";
import { KamioriFooter } from "@/components/kamiori-footer";
import { KamioriHeader } from "@/components/kamiori-header";
import { kamiori } from "@/data/kamiori";

export const metadata: Metadata = {
  title: {
    default: kamiori.name,
    template: `%s · ${kamiori.name}`,
  },
  description: kamiori.description,
};

export default function KamioriLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <KamioriHeader />
      <div className="flex-1">{children}</div>
      <KamioriFooter />
    </>
  );
}
