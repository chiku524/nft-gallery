export const OSSN_BASE = "/ossein";

export function osseinPath(path = ""): string {
  if (!path || path === "/") {
    return OSSN_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${OSSN_BASE}${suffix}`;
}
