export const NOXELLE_BASE = "/noxelle";

export function noxellePath(path = ""): string {
  if (!path || path === "/") {
    return NOXELLE_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${NOXELLE_BASE}${suffix}`;
}
