import type { Metadata } from "next";
import { NivoraFooter } from "@/components/nivora-footer";
import { NivoraHeader } from "@/components/nivora-header";
import { nivora } from "@/data/nivora";

export const metadata: Metadata = {
  title: {
    default: nivora.name,
    template: `%s · ${nivora.name}`,
  },
  description: nivora.description,
};

export default function NivoraLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <NivoraHeader />
      <div className="flex-1">{children}</div>
      <NivoraFooter />
    </>
  );
}
