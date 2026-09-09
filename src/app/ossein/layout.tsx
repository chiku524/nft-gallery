import type { Metadata } from "next";
import { OsseinFooter } from "@/components/ossein-footer";
import { OsseinHeader } from "@/components/ossein-header";
import { ossein } from "@/data/ossein";

export const metadata: Metadata = {
  title: {
    default: ossein.name,
    template: `%s · ${ossein.name}`,
  },
  description: ossein.description,
};

export default function OsseinLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <OsseinHeader />
      <div className="flex-1">{children}</div>
      <OsseinFooter />
    </>
  );
}
