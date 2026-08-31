export const INKLINGS_BASE = "/inklings";

export function inklingsPath(path = ""): string {
  if (!path || path === "/") {
    return INKLINGS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${INKLINGS_BASE}${suffix}`;
}
