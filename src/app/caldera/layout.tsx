import type { Metadata } from "next";
import { CalderaFooter } from "@/components/caldera-footer";
import { CalderaHeader } from "@/components/caldera-header";
import { caldera } from "@/data/caldera";

export const metadata: Metadata = {
  title: {
    default: caldera.name,
    template: `%s · ${caldera.name}`,
  },
  description: caldera.description,
};

export default function CalderaLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <CalderaHeader />
      <div className="flex-1">{children}</div>
      <CalderaFooter />
    </>
  );
}
