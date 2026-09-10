import { CollectionCarousel } from "@/components/collection-carousel";
import { GalleryFooter } from "@/components/gallery-footer";
import { PageJumpButtons } from "@/components/page-jump-buttons";
import { gallery, projects } from "@/data/projects";

export default function GalleryHomePage() {
  return (
    <>
      <div className="flex-1">
        <section className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6 sm:py-12">
          <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">House of collections</p>
          <h1 className="mt-3 max-w-3xl font-heading text-4xl leading-[1.05] sm:text-6xl">
            {gallery.name}
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-muted-foreground">{gallery.tagline}</p>
        </section>

        <CollectionCarousel drops={projects} />
      </div>
      <GalleryFooter />
      <PageJumpButtons />
    </>
  );
}
