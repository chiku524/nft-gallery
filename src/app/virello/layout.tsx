import type { Metadata } from "next";
import { VirelloFooter } from "@/components/virello-footer";
import { VirelloHeader } from "@/components/virello-header";
import { virello } from "@/data/virello";

export const metadata: Metadata = {
  title: {
    default: virello.name,
    template: `%s · ${virello.name}`,
  },
  description: virello.description,
};

export default function VirelloLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <VirelloHeader />
      <div className="flex-1">{children}</div>
      <VirelloFooter />
    </>
  );
}
