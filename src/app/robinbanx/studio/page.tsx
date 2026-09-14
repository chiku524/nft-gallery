import type { Metadata } from "next";
import { RobinBanxStudio } from "@/components/robinbanx-studio";

export const metadata: Metadata = {
  title: "Assembly desk",
  description: "Build a Robin Banx portrait from static transparent PNG plates.",
};

export default function RobinBanxStudioPage() {
  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6">
      <p className="font-mono text-xs uppercase tracking-[0.24em] text-[#e24932]">Composite lab / authorized access</p>
      <h1 className="mt-3 text-5xl font-black uppercase leading-none sm:text-7xl">Assembly desk</h1>
      <p className="mt-5 max-w-2xl text-[#aeb1a7]">
        Select transparent PNG plates to assemble a live dossier portrait. The studio shows the working stack;
        collection tokens are exported as single static PNG files.
      </p>
      <div className="mt-12">
        <RobinBanxStudio />
      </div>
    </div>
  );
}
