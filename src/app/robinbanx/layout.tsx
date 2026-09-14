import type { Metadata } from "next";
import { RobinBanxFooter } from "@/components/robinbanx-footer";
import { RobinBanxHeader } from "@/components/robinbanx-header";
import { robinBanx } from "@/data/robinbanx";

export const metadata: Metadata = {
  title: {
    default: robinBanx.name,
    template: `%s / ${robinBanx.name}`,
  },
  description: robinBanx.description,
};

export default function RobinBanxLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-[#0d0f0e] text-[#eee8da]">
      <RobinBanxHeader />
      <main className="flex-1">{children}</main>
      <RobinBanxFooter />
    </div>
  );
}
