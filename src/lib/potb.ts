export const POTB_BASE = "/pugs-on-the-block";

export function potbPath(path = ""): string {
  if (!path || path === "/") {
    return POTB_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${POTB_BASE}${suffix}`;
}
