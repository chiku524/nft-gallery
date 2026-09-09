import type { Metadata } from "next";
import { VinylonFooter } from "@/components/vinylon-footer";
import { VinylonHeader } from "@/components/vinylon-header";
import { vinylon } from "@/data/vinylon";

export const metadata: Metadata = {
  title: {
    default: vinylon.name,
    template: `%s · ${vinylon.name}`,
  },
  description: vinylon.description,
};

export default function VinylonLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <VinylonHeader />
      <div className="flex-1">{children}</div>
      <VinylonFooter />
    </>
  );
}
