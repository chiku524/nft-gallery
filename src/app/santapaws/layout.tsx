import type { Metadata } from "next";
import { SantaPawsFooter } from "@/components/santapaws-footer";
import { SantaPawsHeader } from "@/components/santapaws-header";
import { santapaws } from "@/data/santapaws";

export const metadata: Metadata = {
  title: {
    default: santapaws.name,
    template: `%s · ${santapaws.name}`,
  },
  description: santapaws.description,
};

export default function SantaPawsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SantaPawsHeader />
      <div className="flex-1">{children}</div>
      <SantaPawsFooter />
    </>
  );
}
