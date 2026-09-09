import type { Metadata } from "next";
import { BoogieSquadFooter } from "@/components/boogiesquad-footer";
import { BoogieSquadHeader } from "@/components/boogiesquad-header";
import { boogiesquad } from "@/data/boogiesquad";

export const metadata: Metadata = {
  title: {
    default: boogiesquad.name,
    template: `%s · ${boogiesquad.name}`,
  },
  description: boogiesquad.description,
};

export default function BoogieSquadLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <BoogieSquadHeader />
      <div className="flex-1">{children}</div>
      <BoogieSquadFooter />
    </>
  );
}
