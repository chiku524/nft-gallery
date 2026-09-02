export const PURRKINS_BASE = "/purrkins";

export function purrkinsPath(path = ""): string {
  if (!path || path === "/") {
    return PURRKINS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${PURRKINS_BASE}${suffix}`;
}
