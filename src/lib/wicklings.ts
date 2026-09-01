export const WICKLINGS_BASE = "/wicklings";

export function wicklingsPath(path = ""): string {
  if (!path || path === "/") {
    return WICKLINGS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${WICKLINGS_BASE}${suffix}`;
}
