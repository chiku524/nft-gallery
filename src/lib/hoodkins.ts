export const HOODKINS_BASE = "/hoodkins";

export function hoodkinsPath(path = ""): string {
  if (!path || path === "/") {
    return HOODKINS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${HOODKINS_BASE}${suffix}`;
}
