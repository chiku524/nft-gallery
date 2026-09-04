export const GALLERIA_BASE = "/galleria";

export function galleriaPath(path = ""): string {
  if (!path || path === "/") {
    return GALLERIA_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${GALLERIA_BASE}${suffix}`;
}
