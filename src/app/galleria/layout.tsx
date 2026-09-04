import type { Metadata } from "next";
import { GalleriaFooter } from "@/components/galleria-footer";
import { GalleriaHeader } from "@/components/galleria-header";
import { galleria } from "@/data/galleria";

export const metadata: Metadata = {
  title: {
    default: galleria.name,
    template: `%s · ${galleria.name}`,
  },
  description: galleria.description,
};

export default function GalleriaLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <GalleriaHeader />
      <div className="flex-1">{children}</div>
      <GalleriaFooter />
    </>
  );
}
