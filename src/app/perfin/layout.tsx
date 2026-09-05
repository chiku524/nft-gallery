import type { Metadata } from "next";
import { PerfinFooter } from "@/components/perfin-footer";
import { PerfinHeader } from "@/components/perfin-header";
import { perfin } from "@/data/perfin";

export const metadata: Metadata = {
  title: {
    default: perfin.name,
    template: `%s · ${perfin.name}`,
  },
  description: perfin.description,
};

export default function PerfinLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <PerfinHeader />
      <div className="flex-1">{children}</div>
      <PerfinFooter />
    </>
  );
}
