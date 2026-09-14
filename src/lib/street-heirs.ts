export const STREET_HEIRS_BASE = "/street-heirs";

export function streetHeirsPath(path = ""): string {
  if (!path || path === "/") {
    return STREET_HEIRS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${STREET_HEIRS_BASE}${suffix}`;
}
