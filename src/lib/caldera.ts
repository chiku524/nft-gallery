export const CALDERA_BASE = "/caldera";

export function calderaPath(path = ""): string {
  if (!path || path === "/") {
    return CALDERA_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${CALDERA_BASE}${suffix}`;
}
