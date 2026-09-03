import type { Metadata } from "next";
import { BirbsFooter } from "@/components/birbs-footer";
import { BirbsHeader } from "@/components/birbs-header";
import { birbs } from "@/data/birbs";

export const metadata: Metadata = {
  title: {
    default: birbs.name,
    template: `%s · ${birbs.name}`,
  },
  description: birbs.description,
};

export default function BirbsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <BirbsHeader />
      <div className="flex-1">{children}</div>
      <BirbsFooter />
    </>
  );
}
