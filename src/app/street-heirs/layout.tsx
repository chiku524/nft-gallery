import type { Metadata } from "next";
import { StreetHeirsFooter } from "@/components/street-heirs-footer";
import { StreetHeirsHeader } from "@/components/street-heirs-header";
import { streetHeirs } from "@/data/street-heirs";

export const metadata: Metadata = {
  title: {
    default: streetHeirs.name,
    template: `%s · ${streetHeirs.name}`,
  },
  description: streetHeirs.description,
};

export default function StreetHeirsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-[#F4EFE5] text-[#202A3D]">
      <StreetHeirsHeader />
      <main className="flex-1">{children}</main>
      <StreetHeirsFooter />
    </div>
  );
}
