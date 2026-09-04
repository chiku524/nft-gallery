export type OpenSeaListing = {
  label: string;
  href: string;
};

export function openSeaListings(
  opensea: { collection: string; listings?: readonly OpenSeaListing[] },
  fallbackLabel = "OpenSea",
): readonly OpenSeaListing[] {
  return opensea.listings ?? [{ label: fallbackLabel, href: opensea.collection }];
}
