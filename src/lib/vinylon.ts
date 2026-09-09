export const VNYL_BASE = "/vinylon";

export function vinylonPath(path = ""): string {
  if (!path || path === "/") {
    return VNYL_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${VNYL_BASE}${suffix}`;
}
