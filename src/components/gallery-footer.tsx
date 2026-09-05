import { OpenSeaLink } from "@/components/opensea-link";
import { gallery, projects } from "@/data/projects";

export function GalleryFooter() {
  return (
    <footer className="mt-auto border-t border-border bg-[color-mix(in_oklch,var(--secondary)_55%,var(--background))]">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <p className="font-heading text-lg">{gallery.name}</p>
          <p className="text-sm text-muted-foreground">{gallery.tagline}</p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
          {projects.flatMap((project) =>
            project.openseaListings.map((listing) => (
              <OpenSeaLink key={`${project.slug}-${listing.href}`} href={listing.href} className="hover:underline">
                {project.openseaListings.length > 1
                  ? `${project.name} on ${listing.label}`
                  : `${project.name} on OpenSea`}
              </OpenSeaLink>
            )),
          )}
        </div>
      </div>
    </footer>
  );
}
