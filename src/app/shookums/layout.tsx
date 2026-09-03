import type { Metadata } from "next";
import { ShookumsFooter } from "@/components/shookums-footer";
import { ShookumsHeader } from "@/components/shookums-header";
import { shookums } from "@/data/shookums";

export const metadata: Metadata = {
  title: {
    default: shookums.name,
    template: `%s · ${shookums.name}`,
  },
  description: shookums.description,
};

export default function ShookumsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ShookumsHeader />
      <div className="flex-1">{children}</div>
      <ShookumsFooter />
    </>
  );
}
