export const OPALINE_BASE = "/opaline";

export function opalinePath(path = ""): string {
  if (!path || path === "/") {
    return OPALINE_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${OPALINE_BASE}${suffix}`;
}
