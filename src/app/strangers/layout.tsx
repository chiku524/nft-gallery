import type { Metadata } from "next";
import { StrangersFooter } from "@/components/strangers-footer";
import { StrangersHeader } from "@/components/strangers-header";
import { strangers } from "@/data/strangers";

export const metadata: Metadata = {
  title: {
    default: strangers.name,
    template: `%s · ${strangers.name}`,
  },
  description: strangers.description,
};

export default function StrangersLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <StrangersHeader />
      <div className="flex-1">{children}</div>
      <StrangersFooter />
    </>
  );
}
