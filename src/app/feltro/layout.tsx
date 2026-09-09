import type { Metadata } from "next";
import { FeltroFooter } from "@/components/feltro-footer";
import { FeltroHeader } from "@/components/feltro-header";
import { feltro } from "@/data/feltro";

export const metadata: Metadata = {
  title: {
    default: feltro.name,
    template: `%s · ${feltro.name}`,
  },
  description: feltro.description,
};

export default function FeltroLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <FeltroHeader />
      <div className="flex-1">{children}</div>
      <FeltroFooter />
    </>
  );
}
