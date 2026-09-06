import type { Metadata } from "next";
import { UmbraFooter } from "@/components/umbra-footer";
import { UmbraHeader } from "@/components/umbra-header";
import { umbra } from "@/data/umbra";

export const metadata: Metadata = {
  title: {
    default: umbra.name,
    template: `%s · ${umbra.name}`,
  },
  description: umbra.description,
};

export default function UmbraLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <UmbraHeader />
      <div className="flex-1">{children}</div>
      <UmbraFooter />
    </>
  );
}
