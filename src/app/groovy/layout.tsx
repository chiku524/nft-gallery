import type { Metadata } from "next";
import { GroovyFooter } from "@/components/groovy-footer";
import { GroovyHeader } from "@/components/groovy-header";
import { groovy } from "@/data/groovy";

export const metadata: Metadata = {
  title: {
    default: groovy.name,
    template: `%s · ${groovy.name}`,
  },
  description: groovy.description,
};

export default function GroovyLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <GroovyHeader />
      <div className="flex-1">{children}</div>
      <GroovyFooter />
    </>
  );
}
