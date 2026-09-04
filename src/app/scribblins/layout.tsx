import type { Metadata } from "next";
import { ScribblinsFooter } from "@/components/scribblins-footer";
import { ScribblinsHeader } from "@/components/scribblins-header";
import { scribblins } from "@/data/scribblins";

export const metadata: Metadata = {
  title: {
    default: scribblins.name,
    template: `%s · ${scribblins.name}`,
  },
  description: scribblins.description,
};

export default function ScribblinsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ScribblinsHeader />
      <div className="flex-1">{children}</div>
      <ScribblinsFooter />
    </>
  );
}
