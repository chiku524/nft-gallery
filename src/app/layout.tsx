import type { Metadata } from "next";
import { Fraunces, Nunito_Sans } from "next/font/google";
import { TooltipProvider } from "@/components/ui/tooltip";
import { GalleryChrome } from "@/components/gallery-chrome";
import { gallery } from "@/data/projects";
import "./globals.css";

const display = Fraunces({
  variable: "--font-display",
  subsets: ["latin"],
});

const sans = Nunito_Sans({
  variable: "--font-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: gallery.name,
    template: `%s · ${gallery.name}`,
  },
  description: gallery.description,
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${sans.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <TooltipProvider>
          <div className="flex min-h-full flex-1 flex-col">
            <GalleryChrome />
            {children}
          </div>
        </TooltipProvider>
      </body>
    </html>
  );
}
