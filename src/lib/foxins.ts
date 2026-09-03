export const FOXINS_BASE = "/foxins";

export function foxinsPath(path = ""): string {
  if (!path || path === "/") {
    return FOXINS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${FOXINS_BASE}${suffix}`;
}
