export const FLTR_BASE = "/feltro";

export function feltroPath(path = ""): string {
  if (!path || path === "/") {
    return FLTR_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${FLTR_BASE}${suffix}`;
}
