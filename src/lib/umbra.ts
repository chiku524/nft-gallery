export const UMBRA_BASE = "/umbra";

export function umbraPath(path = ""): string {
  if (!path || path === "/") {
    return UMBRA_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${UMBRA_BASE}${suffix}`;
}
