export const LOOPKINS_BASE = "/loopkins";

export function loopkinsPath(path = ""): string {
  if (!path || path === "/") {
    return LOOPKINS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${LOOPKINS_BASE}${suffix}`;
}
