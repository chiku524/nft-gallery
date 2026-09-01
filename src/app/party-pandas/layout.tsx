import type { Metadata } from "next";
import { PartyPandasFooter } from "@/components/party-pandas-footer";
import { PartyPandasHeader } from "@/components/party-pandas-header";
import { partyPandas } from "@/data/party-pandas";

export const metadata: Metadata = {
  title: {
    default: partyPandas.name,
    template: `%s · ${partyPandas.name}`,
  },
  description: partyPandas.description,
};

export default function PartyPandasLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <PartyPandasHeader />
      <div className="flex-1">{children}</div>
      <PartyPandasFooter />
    </>
  );
}
