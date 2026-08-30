import type { Metadata } from "next";
import { AfterimagesFooter } from "@/components/afterimages-footer";
import { AfterimagesHeader } from "@/components/afterimages-header";
import { afterimages } from "@/data/afterimages";

export const metadata: Metadata = {
  title: {
    default: afterimages.name,
    template: `%s · ${afterimages.name}`,
  },
  description: afterimages.description,
};

export default function AfterimagesLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <AfterimagesHeader />
      <div className="flex-1">{children}</div>
      <AfterimagesFooter />
    </>
  );
}
